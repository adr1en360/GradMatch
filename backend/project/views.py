import json
import os
from pathlib import Path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from langchain.chains import load_chain
from langchain.chains.base import Chain
from .models import *

BASE_DIR = Path(__file__).resolve().parent
FLOW_PATH = BASE_DIR / "langflows/AI_flow.json"

class LangflowExecuteView(View):
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

            # Return the result as JSON
            return JsonResponse({"result": result})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)