import json
import os
import logging
from pathlib import Path
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import UserData
import requests

logger = logging.getLogger(__name__)

@require_http_methods(["GET"])
def application_form(request):
    return render(request, 'form.html')

@require_http_methods(["POST"])
def get_recommendations(request):
    try:
        logger.debug("Form Data: %s", request.POST)
        
        gre = request.POST.get('gre')
        program = request.POST.get('program')
        gpa = request.POST.get('gpa')
        research = request.POST.get('research')

        # Format input message
        input_message = f"""
        Program: {program}
        GPA: {gpa}
        GRE Score: {gre}
        Research Experience: {research}
        """

        url = "http://127.0.0.1:7860/api/v1/run/49f4fc8b-9d52-4ade-9261-7cdb390228ec"
        
        payload = {
            "input_value": input_message,
            "output_type": "text",  # Changed from "chat" to "text"
            "input_type": "text"
        }

        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            logger.debug(f"API Response Status: {response.status_code}")
            logger.debug(f"API Response: {response.text}")
            
            # Save to database
            UserData.objects.create(
                gre=gre,
                program=program,
                gpa=gpa,
                experience=research
            )
            
            # Parse the nested response structure
            ai_response = response.json()
            
            # Navigate through the response structure to get the text
            text_output = (
                ai_response.get('outputs', [])[0]
                .get('outputs', [])[0]
                .get('messages', [])[0]
                .get('message', '')
            )
            
            logger.debug("Extracted text: %s", text_output)
            
            # Create a single university entry from text response
            universities = [{
                'name': f'Recommendations for {program}',
                'chance': 'Analysis',
                'reason': text_output,
                'readiness': '100',
                'suggestions': 'Based on AI analysis',
                'color': 'green-500'
            }]
            
            # Return the results template with context
            return render(request, 'results.html', {
                'universities': universities,
                'raw_response': text_output  # Add raw response for debugging
            })
            
        except (requests.exceptions.RequestException, KeyError, IndexError) as e:
            logger.error(f"Error processing response: {str(e)}")
            return HttpResponse(
                '<div class="text-red-500">Error processing AI response. Please try again.</div>',
                status=500
            )
            
    except Exception as e:
        logger.error("Error in get_recommendations: %s", str(e))
        return HttpResponse(str(e), status=500)