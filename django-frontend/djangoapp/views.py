import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Express backend base URL
EXPRESS_BASE = 'http://localhost:3030'

def index(request):
    try:
        res = requests.get(f'{EXPRESS_BASE}/dealers')
        dealers = res.json()
    except:
        dealers = []
    return render(request, 'home.html', {'dealers': dealers})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def dealer_details(request, dealer_id):
    dealer = {}
    reviews = []
    try:
        d = requests.get(f'{EXPRESS_BASE}/dealer/{dealer_id}')
        dealer = d.json()
    except:
        dealer = {}
    try:
        r = requests.get(f'{EXPRESS_BASE}/dealer/reviews/{dealer_id}')
        reviews = r.json()
    except:
        reviews = []
    return render(request, 'dealer_details.html', {'dealer': dealer, 'reviews': reviews})

@login_required
def add_review(request, dealer_id):
    if request.method == 'POST':
        payload = {
            'dealer_id': dealer_id,
            'name': request.user.username,
            'review': request.POST.get('review'),
            'rating': int(request.POST.get('rating', 5))
        }
        try:
            res = requests.post(f'{EXPRESS_BASE}/dealer/{dealer_id}/add_review', json=payload)
            if res.status_code == 201:
                messages.success(request, 'Review added')
            else:
                messages.error(request, 'Could not add review')
        except:
            messages.error(request, 'Error contacting review service')
        return redirect('dealer_details', dealer_id=dealer_id)
    else:
        return render(request, 'add_review.html', {'dealer_id': dealer_id})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def sentiment_analyzer(request):
    result = None
    if request.method == 'POST':
        text = request.POST.get('text', '')
        sid = SentimentIntensityAnalyzer()
        result = sid.polarity_scores(text)
    return render(request, 'sentiment.html', {'result': result})
