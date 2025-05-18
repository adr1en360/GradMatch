import json
import os
from pathlib import Path
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.template.loader import render_to_string
from langchain.chains import load_chain 
from .models import *
from django.shortcuts import render

BASE_DIR = Path(__file__).resolve().parent
FLOW_PATH = BASE_DIR / "langflows/AI_flow.json"

class RecomendationView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Get user inputs from POST request
            user_data = json.loads(request.body)
            program = user_data.get("program")
            gpa = user_data.get("gpa")
            gre = user_data.get("gre")
            research = user_data.get("research")
            
            user_data = UserData.objects.create(
            program=program,
            gpa=gpa,
            gre=gre,
            research=research
            )

            with open(FLOW_PATH, "r") as file:
                flow_data = json.load(file)

            chain = load_chain(flow_data)

            inputs = {
                "program": program,
                "gpa": gpa,
                "gre": gre,
                "research": research,
            }
            result = chain.run(inputs)
            
            # Render the response
            html_content = f"""
            <div class="bg-white p-4 rounded-md shadow border border-green-300">
                <h3 class="font-bold mb-2">Recommendations:</h3>
                <div>{result}</div>
            </div>
            """
            return HttpResponse(html_content)

        except Exception as e:
            return HttpResponse(f"<div class='text-red-600'>Error: {str(e)}</div>", status=500)