import json
import os
from pathlib import Path
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.shortcuts import render
# Importing Langchain components
from langchain.chains import SequentialChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from .models import UserData

BASE_DIR = Path(__file__).resolve().parent
FLOW_PATH = BASE_DIR / "langflows/AI_flow.json"

def home(request):
    return render(request, "form.html")

@method_decorator(csrf_exempt, name='dispatch')
class RecomendationView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Extract form data
            program = request.POST.get("program")
            gpa = request.POST.get("gpa")
            gre = request.POST.get("gre")
            experience = request.POST.get("experience")

            # Save data to the UserData model
            UserData.objects.create(
                program=program,
                gpa=gpa,
                gre=gre,
                experience=experience
            )

            # Load the Langflow JSON
            with open(FLOW_PATH, "r") as file:
                flow_data = json.load(file)

            # Check the structure of the flow data
            if "nodes" not in flow_data:
                raise ValueError("Invalid flow structure. 'nodes' key is missing.")

            # Process the nodes
            # Assuming the flow has a prompt template node and an LLM node
            prompt_template = flow_data["nodes"][0].get("template")
            llm_node = flow_data["nodes"][1].get("llm")

            # Create the prompt template
            prompt = PromptTemplate(template=prompt_template, input_variables=["program", "gpa", "gre", "experience"])

            # Initialize the LLM (assuming OpenAI for now; adjust based on your flow)
            llm = OpenAI()

            # Construct the chain
            chain = SequentialChain(chains=[prompt, llm], input_variables=["program", "gpa", "gre", "experience"])

            # Execute the flow
            inputs = {
                "program": program,
                "gpa": gpa,
                "gre": gre,
                "experience": experience,
            }
            result = chain.run(inputs)

            # Render the response
            recommendations = json.loads(result) if isinstance(result, str) else result
            html_content = render_to_string("results.html", {"universities": recommendations})

            return HttpResponse(html_content)

        except Exception as e:
            return HttpResponse(f"<div class='text-red-600'>Error: {str(e)}</div>", status=500)