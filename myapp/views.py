import sys

from django.shortcuts import render
from geopy.geocoders import Nominatim
import time
from pprint import pprint
from twilio.rest import Client
from django.conf import settings

to=''

def get_location_by_address(address):
    """This function returns a location as raw from an address
    will repeat until success"""
    app = Nominatim(user_agent="tutorial")
    time.sleep(1)
    try:
        return app.geocode(address).raw
    except:
        return get_location_by_address(address)


def homepage(request):
    la=[]
    lo=[]
    na=[]
    f = open(r"C:\Users\karth\IdeaProjects\MavenBloodBank\details.txt", "r")
    if f.mode == 'r':
        contents = f.read()
        contents = contents[:-1]
    kk = contents.split("#")
    for i in range(0, len(kk)):
        name,mobileno,bloodgrp,city,state,district=str(kk[i]).split(".")
        address = city+", "+district+", "+state
        location = get_location_by_address(address)
        latitude = float(location["lat"])
        longitude = float(location["lon"])
        la.append(latitude)
        lo.append(longitude)
        na.append(name)
    return render(request,'homepage.html',{'lat':la,'names':na,'lon':lo})

def message(request,id):
    global to
    f = open(r"C:\Users\karth\IdeaProjects\MavenBloodBank\details.txt", "r")
    if f.mode == 'r':
        contents = f.read()
        contents = contents[:-1]
    kk = contents.split("#")
    for i in range(0, len(kk)):
        if(i==id):
           name,mobileno,bloodgrp,city,state,district=str(kk[i]).split(".")
           address = city + ", " + district + ", " + state
           to = mobileno
    return render(request,'msg.html',{'name':name,'address':address})

def sendmessage(request):
    global to
    to='+91'+str(to)
    mes = request.GET['msgbody']
    mes = mes + "Please update your status in BloodBank Org"
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    response = client.messages.create(
        body=mes,
        to=to, from_=settings.TWILIO_PHONE_NUMBER)

    return render(request,'success.html')

