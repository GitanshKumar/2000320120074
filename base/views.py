from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests, json

# Create your views here.

def home(request):
    return render(request, "base/home.html")

def auth():
    url = "http://20.244.56.144/train/auth"
    payload = {
        "companyName": "Train Central",
        "clientID": "bc7cf8a9-b124-4cbb-a97f-2a8e65923a0b",
        "clientSecret": "OMWJPKLdPagMDpbV",
        "ownerName": "Gitansh",
        "ownerEmail": "gitanshkumar5@gmail.com",
        "rollNo": "2000320120074"
    }
    result = requests.post(url,  data=json.dumps(payload))
    return result.json()["access_token"]

def getTrainsData(request):
    url = "http://20.244.56.144/train/trains"
    header = {
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTAwMDU4MDQsImNvbXBhbnlOYW1lIjoiVHJhaW4gQ2VudHJhbCIsImNsaWVudElEIjoiYmM3Y2Y4YTktYjEyNC00Y2JiLWE5N2YtMmE4ZTY1OTIzYTBiIiwib3duZXJOYW1lIjoiIiwib3duZXJFbWFpbCI6IiIsInJvbGxObyI6IjIwMDAzMjAxMjAwNzQifQ.iNKuEcemB6KPB7Di7UBxfxh3-J_AeOyaJHFQH-p2DZs"
    }
    result = requests.get(url, headers=header)
    if result.status_code == 200:
        if "message" in result.json():
            header = {
                "authorization": "Bearer " + auth()
            }
            result = requests.get(url, headers=header)
            if result.status_code == 200:
                price_sorted = sorted(result.json(), key=lambda x: min(x['price'].values()))
                return render(request, 'base/trains.html', {"trains": price_sorted})
        
        price_sorted = sorted(result.json(), key=lambda x: min(x['price'].values()))
        return render(request, 'base/trains.html', {"trains": price_sorted})

def getTrainData(request, pk):
    url = "http://20.244.56.144/train/trains/" + pk
    header = {
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTAwMDU4MDQsImNvbXBhbnlOYW1lIjoiVHJhaW4gQ2VudHJhbCIsImNsaWVudElEIjoiYmM3Y2Y4YTktYjEyNC00Y2JiLWE5N2YtMmE4ZTY1OTIzYTBiIiwib3duZXJOYW1lIjoiIiwib3duZXJFbWFpbCI6IiIsInJvbGxObyI6IjIwMDAzMjAxMjAwNzQifQ.iNKuEcemB6KPB7Di7UBxfxh3-J_AeOyaJHFQH-p2DZs"
    }
    result = requests.get(url, headers=header)
    if result.status_code == 200:
        if "message" in result.json():
            header = {
                "authorization": "Bearer " + auth()
            }
            result = requests.get(url, headers=header)
            if result.status_code == 200:
                return render(request, 'base/train.html', {"train": result.json()})
        
        return render(request, 'base/train.html', {"train": result.json()})