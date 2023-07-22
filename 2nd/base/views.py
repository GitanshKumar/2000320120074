from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests, json, time
from datetime import datetime, timedelta


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

def isValidDepartureTime(data):
    try:
        hours = data["departureTime"]["Hours"]
        minutes = data["departureTime"]["Minutes"]
        seconds = data["departureTime"]["Seconds"]
        
        current_time = datetime.now()
        
        departure_time = current_time.replace(hour=hours, minute=minutes, second=seconds)
        
        max_allowed_time = current_time + timedelta(hours=12)
        
        min_allowed_time = current_time + timedelta(minutes=30)
        
        if departure_time >= current_time and departure_time <= max_allowed_time and departure_time > min_allowed_time:
            return True
        else:
            return False
    
    except (KeyError, json.JSONDecodeError):
        return False

def getTrainsData(request):
    url = "http://20.244.56.144/train/trains"
    header = {
        "authorization": "Bearer " + auth()
    }
    result = requests.get(url, headers=header)
    if result.status_code == 200:
        filteredData = filter(isValidDepartureTime, result.json())
        return render(request, 'base/trains.html', {"trains": list(filteredData)})

def getTrainData(request, pk):
    url = "http://20.244.56.144/train/trains/" + pk
    header = {
        "authorization": "Bearer " + auth()
    }
    result = requests.get(url, headers=header)
    if result.status_code == 200:
        return render(request, 'base/train.html', {"train": result.json()})