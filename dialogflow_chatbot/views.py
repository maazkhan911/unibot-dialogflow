import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
import google.auth.transport.requests
from google.oauth2 import service_account


def index(request):
    return render(request, 'index.html')


def chatbot(request):
    if request.method == 'GET':
        return render(request, 'chatbot.html')

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            creds = service_account.Credentials.from_service_account_file(
                r"C:\Users\HomePC\Desktop\Dialogflow\Second Bot\agent-for-admission.json", 
                scopes=['https://www.googleapis.com/auth/cloud-platform']
            )
            request_auth = google.auth.transport.requests.Request()
            creds.refresh(request_auth)

            access_token = creds.token


            project_id = "agent-for-admission-vkbg"  
            session_id = "mysessionid123"
            language_code = "en"

            url = f"https://dialogflow.googleapis.com/v2/projects/{project_id}/agent/sessions/{session_id}:detectIntent"

            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            payload = {
                "queryInput": {
                    "text": {
                        "text": user_message,
                        "languageCode": language_code
                    }
                }
            }

            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                result = response.json()
                reply = result['queryResult']['fulfillmentText']
                return JsonResponse({'reply': reply})
            else:
                return JsonResponse({'reply': 'Error from Dialogflow (status code {})'.format(response.status_code)})

        except Exception as e:
            return JsonResponse({'reply': f'Error: {str(e)}'})

    return JsonResponse({'reply': 'Invalid request method'}) 