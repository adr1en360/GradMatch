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
        LANGFLOW_API_URL = "http://127.0.0.1:7860/api/v1/execute" 
        try:
            # Extract form data
            program = request.POST.get("program")
            gpa = request.POST.get("gpa")
            gre = request.POST.get("gre")
            experience = request.POST.get("experience")

            # Prepare payload for Langflow
            payload = {
                "program": program,
                "gpa": gpa,
                "gre": gre,
                "research": experience
            }

            # Send request to Langflow
            try:
                response = requests.post(LANGFLOW_API_URL, json=payload, timeout=10)
                response.raise_for_status()  # Raises HTTPError for bad responses
                recommendations = response.json()
                return HttpResponse(f"<div>{recommendations}</div>")

            except requests.exceptions.RequestException as e:
                # Show Langflow error directly in the response
                return HttpResponse(f"<div class='text-red-600'>Langflow Error: {str(e)}</div>", status=500)

        except Exception as e:
            return HttpResponse(f"<div class='text-red-600'>General Error: {str(e)}</div>", status=500)