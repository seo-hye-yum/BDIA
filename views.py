from django.shortcuts import render
from openai import OpenAI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import requests
import json


class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def execute(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'text/event-stream'
        }

        result = ''
        with requests.post(self._host + '/testapp/v1/chat-completions/HCX-002',
                           headers=headers, json=completion_request, stream=True) as r:
            response_text=r.text
            lines = response_text.strip().split('\n\n')

            for line in lines:
                if line.find('event:result') != -1:
                    line_dict = json.loads(line.split('data:', 1)[1])
                    result = line_dict['message']['content']
        
        return result


def clova(prompt):
    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiYwbOU8C6YbcVmMu3aJBaodX7gTyBaZmWgeFzK8ME0TiBBScSihuooHY1VICSYTy41KRhvHpkO2xXMM0RS3rZfP5hFsgieIrZLxlZ0LqDJF0mIPlICVH57TEqW76hGsd7hUL9bWJQACwCh1CwY9WhCtZdi2PqJjDgMcqGaQYxRFkdbivvQTLZkM1Tvzq7VuKHpOJB5RJghiuXJacpnfx6Bo0=',
        api_key_primary_val='HolL48sNDJV2GluXorHDVnS36TEx5OmJ7K9um5pP',
        request_id='b50adfab61354b31a9a4469f563fe7e1'
    )

    preset_text = [{"role":"user","content":prompt}]
    request_data = {
        'messages': preset_text,
        'topP': 0.8,
        'topK': 0,
        'maxTokens': 256,
        'temperature': 0.5,
        'repeatPenalty': 5.0,
        'stopBefore': [],
        'includeAiFilters': True
    }

    return completion_executor.execute(request_data)


client = OpenAI(api_key="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")
# Create your views here.




#chatGPT에게 채팅 요청 API
def chatGPT(prompt):
    completion = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}])
    print(completion)
    result = completion.choices[0].message.content
    return result

#chatGPT에게 그림 요청 API
def imageGPT(prompt):
    response = client.images.generate(prompt=prompt,
    n=1,
    size="256x256")
    result =response['data'][0]['url']
    return result

def index(request):
    return render(request, 'gpt/index.html')

# def chat(request):
#     #post로 받은 question
#     prompt = request.POST.get('question')


#     #type가 text면 chatGPT에게 채팅 요청 , type가 image면 imageGPT에게 채팅 요청
#     result = chatGPT(prompt)

#     context = {
#         'question': prompt,
#         'result': result
#     }

#     return render(request, 'gpt/result.html', context) 

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        user_message = request.POST.get('question')
        result = clova(user_message)
        response_data = {
            'result': result
        }
        return JsonResponse(response_data)


