from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .forms import *
import urllib.request
import urllib.parse
import json

def home(request):
    template = loader.get_template('front-layer/home.html')
    request_top_5 = urllib.request.Request('http://exp-api:8000/home/')
    json_top_5 = urllib.request.urlopen(request_top_5).read().decode('utf-8')
    top_5 = json.loads(json_top_5)
    context = top_5
    return HttpResponse(template.render(context, request))

def pack_detail(request, pk):
    template = loader.get_template('front-layer/pack_detail.html')
    request_pack = urllib.request.Request('http://exp-api:8000/pack_detail/' + str(pk) + '/')
    json_pack = urllib.request.urlopen(request_pack).read().decode('utf-8')
    pack = json.loads(json_pack)
    context = pack
    return HttpResponse(template.render(context, request))

def user_detail(request, pk):
    template = loader.get_template('front-layer/musician_detail.html')
    request_musician = urllib.request.Request('http://exp-api:8000/musician_detail/' + str(pk) + '/')
    json_musician = urllib.request.urlopen(request_pack).read().decode('utf-8')
    musician = json.loads(json_musician)
    context = musician
    return HttpResponse(template.render(context, request))

def login(request):
    if request.method == 'GET':
        #display login form
        form = MusicianForm()
        return render(request, 'front-layer/login.html', {'form':form, 'error': ''})
    # Create new Musician form instance
    form = MusicianForm(request.POST)
    
    # Check if form is valid
    if not form.is_valid():
        #Form error, send back to login page with form errors
        return render(request, 'front-layer/login.html', {'form':form, 'error': ''})

    # Get form data
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    form_data = {'username': username, 'password': password}
    data_encoded = urllib.parse.urlencode(form_data).encode('utf-8')

    # Get next page. Currently automatically goes to home page
    next = 'front-layer/home'

    # Send form data to exp layer
    response = urllib.request.Request('http://exp-api:8000/login/', data=data_encoded, method='POST')
    # Check that exp layer says form data ok
    if response == None:
        error = "Incorrect username or password"
        return render(request, 'front-layer/login.html', {'form':form, 'error':error})

    # Can now log user in, set login cookie
    authenticator = response['response']['authenticator']
    response = HttpResponseRedirect(next)
    response.set_cookie("authenticator", authenticator)
    return response

def logout(request):
    response = HttpResponseRedirect(reverse('front-layer/home'))
    response.delete_cookie('authenticator')
    return response

def create_listing(request):
    #set cookie assigns a string name, use this name to try to get cookie
    authenticator = request.COOKIES.get('authenticator')
    #if user not logged in
    if not authenticator:
        return HttpResponseRedirect(reverse("login"))
    
    #GET request
    if request.method == 'GET':
        #Display form page
        form = ListingForm()
        return render(request, "front-layer/create_listing.html", {'form':form})

    #Otherwise, create new form instance
    form = ListingForm(request.POST)

    #Retrieve form data
    name = form.cleaned_data['name']
    description = form.cleaned_data['description']
    price = form.cleaned_data['price']
    form_data = {'name': name, 'description': description, 'price': price, 'authenticator': authenticator}

    #Send form data to exp layer
    data_encoded = urllib.parse.urlencode(form_data).encode('utf-8')
    response = urllib.request.Request('http://exp-api:8000/create_listing/', data=data_encoded, method='POST')

    #Check if exp response says we passed incorrect info
    #ADD ONCE EXP DONE!!!

    return render(request, "front-layer/create_listing_success.html")

def create_account(request):
    if request.method == 'GET':
        #display signup form
        form = MusicianForm()
        return render(request, 'front-layer/create_account.html', {'form':form})
    # Create new Musician form instance
    form = MusicianForm(request.POST)
    
    # Check if form is valid
    if not form.is_valid():
        #Form error, send back to sign-up page with an error ADD ERROR
        return render('front-layer/create_account.html')
    # Get form data
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    form_data = {'username': username, 'password': password}

    # Get next page. Currently automatically goes to home page
    next = reverse('front-layer/home')

    # Send form data to exp layer
    data_encoded = urllib.parse.urlencode(form_data).encode('utf-8')
    response = urllib.request.Request('http://exp-api:8000/create_listing/', data=data_encoded, method='POST')
    # ADD CHECKING EXP RESPONSE!!!

    # Can now log user in, set login cookie
    authenticator = response['response']['authenticator']
    response = HttpResponseRedirect(next)
    response.set_cookie("authenticator", authenticator)
    return response

    
