import logging
import requests
import json
from pathlib import Path
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import UserData

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')

@require_http_methods(["GET"])
def auth(request):
    return render(request, 'auth.html')

@require_http_methods(["GET"])
def dashboard(request):
    context = {
        'recent_activities': [
            {
                'type': 'statement',
                'title': 'Personal Statement Draft 1',
                'date': '2 days ago'
            },
            {
                'type': 'application',
                'title': 'Stanford Application Updated',
                'date': '1 week ago'
            }
        ],
        'upcoming_deadlines': [
            {
                'school': 'Stanford University',
                'program': 'Computer Science PhD',
                'deadline': 'July 30, 2025'
            }
        ]
    }
    return render(request, 'dashboard.html', context)

@require_http_methods(["GET"])
def application_form(request):
    return render(request, 'form.html')

@require_http_methods(["GET"])
def statement_editor(request):
    return render(request, 'statement_editor.html')

@require_http_methods(["GET"])
def checklist(request):
    schools = [
        {
            'name': 'Stanford University',
            'program': 'Computer Science PhD',
            'deadline': 'July 30, 2025',
            'progress': 75
        }
    ]
    return render(request, 'checklist.html', {'schools': schools})

@require_http_methods(["GET"])
def checklist_detail(request):
    school_id = request.GET.get('school')
    return render(request, 'checklist_detail.html', {
        'school': {'name': 'Stanford University', 'program': 'Computer Science PhD'}
    })

@require_http_methods(["GET"])
def forum(request):
    topics = [
        {
            'title': 'Tips for CS PhD Applications',
            'author': 'Mark Zukerberg',
            'posted': '2 hours ago',
            'replies': 15
        }
    ]
    return render(request, 'forum.html', {'topics': topics})


def parse_university_text(response_json):
    try:
        # Extract the text content from the response
        text_content = response_json['outputs'][0]['outputs'][0]['results']['text']['text']
        
        universities = []
        current_uni = {}
        
        for line in text_content.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('#UNIVERSITY'):
                if current_uni:
                    universities.append(current_uni)
                current_uni = {}
            elif line.startswith('NAME:'):
                current_uni['name'] = line.replace('NAME:', '').strip()
            elif line.startswith('CHANCE:'):
                current_uni['chance'] = line.replace('CHANCE:', '').strip()
            elif line.startswith('REASON:'):
                current_uni['reason'] = line.replace('REASON:', '').strip()
            elif line.startswith('READINESS:'):
                current_uni['readiness'] = line.replace('READINESS:', '').strip().rstrip('%')
            elif line.startswith('SUGGESTIONS:'):
                current_uni['suggestions'] = line.replace('SUGGESTIONS:', '').strip()
        
        if current_uni:
            universities.append(current_uni)
            
        return universities
    except Exception as e:
        logger.error(f"Error parsing response: {e}")
        return []

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
            "input_value": "input_message",
            "output_type": "text", 
            "input_type": "text"
        }
        logger.debug("Payload: %s", payload)
        
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
            
            # Parse the response
            response_json = response.json()
            universities = parse_university_text(response_json)
            
            if not universities:
                logger.error("No universities found in response")
                return HttpResponse(
                    '<div class="text-red-500">Invalid response format from AI service</div>',
                    status=500
                )
            
            # Add color coding for chance levels
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
                
        except requests.exceptions.RequestException as e:
            logger.error("API request failed: %s", str(e))
            return HttpResponse(
                '<div class="text-red-500">Failed to connect to AI service</div>',
                status=500
            )
        except json.JSONDecodeError as e:
            logger.error("Error parsing JSON response: %s", str(e))
            return HttpResponse(
                '<div class="text-red-500">Invalid response from AI service</div>',
                status=500
            )
            
    except Exception as e:
        logger.error("Unexpected error: %s", str(e))
        return HttpResponse(
            '<div class="text-red-500">An unexpected error occurred</div>',
            status=500
        )