from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
import requests, random

# Create your views here.
def HomeView(request):
    return render(request, 'home.html')

class SearchView(View):
    def get(self, request):
        query = request.GET.get('query', '').strip()
        if len(query) > 0:
            data = {
                "query": f"{query}",
                "messages": [
                    {
                        "id": "HIuGdU3",
                        "content": f"{query}",
                        "role": "user"
                    }
                ],
                "index": None
            }
            headers = {
                'x-requested-with': 'com.blackbox.blackboxapp',
                'content-type': 'application/json',
                'host': 'www.blackbox.ai',
            }
            response = requests.post("https://www.blackbox.ai/api/check", json=data, headers=headers)
            results = response.json()
            if '\'results\': []' in str(results):
                results = {
                    'results': {
                        'organic': []
                    }
                }
            for result in results['results']['organic']:
                result['rating'] = random.randint(1, 5)
                result['ratingCount'] = random.randint(1, 100)
        else:
            results = {
                'results': {
                    'organic': []
                }
            }
        return JsonResponse(
            results, safe=False, status=200, json_dumps_params={'ensure_ascii': False}, content_type='application/json'
        )