import json
import os
import logging
import requests
from pathlib import Path

from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import UserData

logger = logging.getLogger(__name__)

@require_http_methods(["GET"])
def index(request):
    return render(request, 'index.html')

@require_http_methods(["GET"])
def auth(request):
    return render(request, 'auth.html')

@require_http_methods(["GET"])
def statement_editor(request):
    # TODO: Add logic to fetch saved drafts
    return render(request, 'statement_editor.html', {
        'drafts': [],  # Placeholder for saved drafts
    })

@require_http_methods(["GET"])
def checklist(request):
    # TODO: Add logic to fetch user's schools
    schools = [
        {
            'name': 'Stanford University',
            'program': 'Computer Science PhD',
            'deadline': 'Dec 15, 2023',
            'progress': 75,
        },
        # Add more example schools
    ]
    return render(request, 'checklist.html', {
        'schools': schools
    })

@require_http_methods(["GET"])
def checklist_detail(request):
    school_id = request.GET.get('school')
    # TODO: Add logic to fetch specific school details
    items = [
        {
            'task': 'Submit Application Form',
            'deadline': 'Dec 1, 2023',
            'completed': False,
        },
        # Add more checklist items
    ]
    return render(request, 'checklist_detail.html', {
        'school': {'name': 'Stanford University', 'program': 'Computer Science PhD'},
        'items': items
    })

@require_http_methods(["GET"])
def forum(request):
    # TODO: Add logic to fetch forum topics
    topics = [
        {
            'title': 'Tips for CS PhD Applications',
            'author': 'Jane Doe',
            'posted': '2 hours ago',
            'replies': 15,
        },
        # Add more topics
    ]
    return render(request, 'forum.html', {
        'topics': topics
    })

@require_http_methods(["GET"])
def application_form(request):
    return render(request, 'form.html')


def parse_university_text(text):
    universities = []
    current_uni = {}
    
    for line in text.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('#UNIVERSITY'):
            if current_uni:
                universities.append(current_uni)
            current_uni = {}
            continue
            
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()
            
            if key == 'name':
                current_uni['name'] = value
            elif key == 'chance':
                current_uni['chance'] = value
            elif key == 'reason':
                current_uni['reason'] = value
            elif key == 'readiness':
                current_uni['readiness'] = value.rstrip('%')
            elif key == 'suggestions':
                current_uni['suggestions'] = value
                
    if current_uni:
        universities.append(current_uni)
        
    return universities

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
            "output_type": "text", 
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
            
            # Extract the message text and parse JSON
            text_output = (
                ai_response.get('outputs', [])[0]
                .get('outputs', [])[0]
                .get('messages', [])[0]
                .get('message', '')
            )
            
            try:
                # Parse the text response
                universities = parse_university_text(text_output)
                
                if not universities:
                    logger.error("No universities found in response")
                    return HttpResponse(
                        '<div class="text-red-500">Invalid response format from AI service</div>',
                        status=500
                    )
                
                # Add color coding
                for uni in universities:
                    uni['color'] = {
                        'High': 'green-500',
                        'Med': 'yellow-500',
                        'Low': 'red-500'
                    }.get(uni['chance'], 'gray-500')
                
                logger.debug("Processed universities: %s", universities)
                
                return render(request, 'results.html', {
                    'universities': universities,
                    'program': program,
                    'debug': settings.DEBUG
                })
                
            except Exception as e:
                logger.error("Error processing response: %s", str(e))
                return HttpResponse(
                    '<div class="text-red-500">Error processing response</div>',
                    status=500
                )
                
        except requests.exceptions.RequestException as e:
            logger.error("API request failed: %s", str(e))
            return HttpResponse(
                '<div class="text-red-500">Failed to connect to AI service</div>',
                status=500
            )
            
    except Exception as e:
        logger.error("Unexpected error: %s", str(e))
        return HttpResponse(
            '<div class="text-red-500">An unexpected error occurred</div>',
            status=500
        )