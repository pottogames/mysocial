from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib import auth
import requests
from .models import Stock
from django.http import JsonResponse

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowersCount
from itertools import chain
import random
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product, CartItem
# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, UserProfile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from paypalcheckoutsdk.payments import CapturesRefundRequest
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
import json
# views.py
from django.shortcuts import render, HttpResponse
from .forms import PayPalForm
from .models import UserProfile
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from django.shortcuts import render
from django.http import JsonResponse
from .models import Transaction
import openai
from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
# views.py
from django.shortcuts import render
from .models import Video
from .models import Category
from .models import Button
from .models import Category
from .models import FoodItem, WeightTracker, Chat2
from django.db import IntegrityError
import openai
from .models import FoodItem
from .models import ChatMessage  # Import the ChatMessage model
from .models import Message, PrivateMessage
from .models import Recipient
from django import template
from .models import Profile
import logging
import logging
from .models import Product, Category1  # Update import statement to import Category1
from .models import Post2
from background_task import background
from django.core.exceptions import ObjectDoesNotExist
import threading
from django.contrib.auth.decorators import login_required
from .models import Campaign1, Purchase1
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.core.files.storage import FileSystemStorage  # Import FileSystemStorage for file handling
from .models import Group
from .models import PrivateMessage
from django.views.decorators.csrf import csrf_exempt
from .models import Story

logger = logging.getLogger(__name__)
import joblib

register = template.Library()

from .models import Song, Album,Artist

from web3 import Web3, HTTPProvider

# trading_platform/views.py

import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from web3 import Web3, HTTPProvider
from .models import Wallet, ChartData

# Replace 'YOUR_INFURA_PROJECT_ID' with your Infura project ID
INFURA_PROJECT_ID = '4dd1dceeb1a64690a71aeb37ffd56930'
INFURA_URL = f'https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}'

# Initialize Web3 with Infura as the provider
web3 = Web3(HTTPProvider(INFURA_URL))

#Elias plugin
from .models import Plugin

def plugin_list(request):
    plugins = Plugin.objects.all()
    stories = Story.objects.all()
    private_messages = PrivateMessage.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
    group_messages = GroupMessage.objects.filter(group__members=request.user)
    
    # Fix for filtering notifications for the current user
    notifications = Notification.objects.filter(user=request.user)
    notifications_count = notifications.count()
    
    all_messages = list(private_messages) + list(group_messages)
    all_messages.sort(key=lambda x: x.timestamp, reverse=True)

    user_profile = Profile.objects.get(user=request.user)

    user_following_list = []
    feed = []
    messages_count = private_messages.count()

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    all_users = User.objects.all()
    user_following_all = []

    
    return render(request, 'Plugin/plugins.html',{
        'stories': stories,
        'plugins': plugins,
        'user_profile': user_profile,
        'messages_count': messages_count,
        'posts': feed_list,
        'notifications_count': notifications_count,
        'all_messages': all_messages,
        'notifications': notifications,

    })





def plugin_details(request, plugin_id):
    plugin = Plugin.objects.get(id=plugin_id)
    return render(request, 'Plugin/plugindetails.html', {'plugin': plugin})

@csrf_exempt
def connect_wallet(request):
    if request.method == 'POST':
        user = request.user
        wallet_address = request.POST.get('wallet_address')

        # Create or update the wallet in the database
        wallet, created = Wallet.objects.get_or_create(user=user, defaults={'wallet_address': wallet_address})
        if not created:
            wallet.wallet_address = wallet_address
            wallet.save()

        return JsonResponse({'success': 'Wallet connected'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def save_changes(request):
    if request.method == 'POST':
        # Here you can add code to save the chart changes to the database
        data = request.POST.get('changes')
        print('Changes saved:', data)
        return JsonResponse({'message': 'Changes saved successfully!'})
    else:
        return JsonResponse({'error': 'Invalid request method!'}, status=400)

def delete_changes(request):
    if request.method == 'DELETE':
        # Here you can add code to delete the chart changes from the database
        print('Changes deleted')
        return JsonResponse({'message': 'Changes deleted successfully!'})
    else:
        return JsonResponse({'error': 'Invalid request method!'}, status=400)

@csrf_exempt
def disconnect_wallet(request):
    if request.method == 'POST':
        user = request.user
        try:
            wallet = Wallet.objects.get(user=user)
            wallet.delete()
            return JsonResponse({'success': 'Wallet disconnected'})
        except Wallet.DoesNotExist:
            return JsonResponse({'error': 'Wallet not found'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def view_wallet_balance(request):
    user = request.user
    try:
        wallet = Wallet.objects.get(user=user)
        balance = web3.eth.get_balance(wallet.wallet_address)
        balance_in_ether = web3.fromWei(balance, 'ether')
        return JsonResponse({'balance': str(balance_in_ether) + ' ETH'})
    except Wallet.DoesNotExist:
        return JsonResponse({'error': 'Wallet not found'})

from django.http import JsonResponse
from django.shortcuts import render
import requests

API_KEY = 'UNHLWllUMuSDPrGQtDAXErJ7z8xfFsfo'
BASE_URL = 'https://financialmodelingprep.com/api/v3'

def tradeindex(request):
    search_query = request.GET.get('search', '')
    if search_query:
        stock_list = Stock.objects.filter(symbol__icontains=search_query)
        chart_data = None  # No chart data for search queries
    else:
        stock_list = Stock.objects.all()
        chart_data = get_all_chart_data()

    context = {'stock_list': stock_list, 'chart_data': chart_data}
    return render(request, 'EliasTrade/index.html', context)

def get_all_chart_data():
    all_chart_data = []
    symbols = Stock.objects.values_list('symbol', flat=True)  # Get all symbols
    for symbol in symbols:
        chart_data_for_symbol = ChartData.objects.filter(symbol=symbol).values('date', 'close')
        # Format chart data for JavaScript compatibility
        formatted_data = [{'date': data['date'], 'close': data['close']} for data in chart_data_for_symbol]
        all_chart_data.append({symbol: formatted_data})
    return all_chart_data

def stock_chart(request, symbol):
    stock = get_object_or_404(Stock, symbol=symbol)
    chart_data = get_stock_chart_data(symbol)
    context = {'stock_list': Stock.objects.all(), 'stock': stock, 'chart_data': chart_data}
    return render(request, 'EliasTrade/index.html', context)

def get_stock_chart_data(symbol):
    url = f'{BASE_URL}/historical-chart/5min/{symbol}?apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data
#Elias Paint!


from django.http import HttpResponseServerError

@login_required
def upload_song(request):
    if request.method == 'POST':
        print("Received POST request for uploading song.")
        try:
            album_id = request.POST.get('album_id')
            song_name = request.POST.get('song_name')
            song_file = request.FILES.get('song_file')
            thumbnail = request.FILES.get('thumbnail')

            print("album_id:", album_id)
            print("song_name:", song_name)
            print("song_file:", song_file)
            print("thumbnail:", thumbnail)

            # Check if the selected album exists and belongs to the current user
            album = Album.objects.filter(pk=album_id, user=request.user).first()

            # If the album doesn't exist or doesn't belong to the user, create a new one
            if not album:
                album_name = request.POST.get('new_album_name')
                if not album_name:
                    messages.error(request, 'Album name is required')
                    return redirect('upload_song')
                album = Album.objects.create(user=request.user, albumName=album_name)

            # Create a new Song instance
            song = Song(album=album, songName=song_name, song=song_file, songThumbnail=thumbnail)
            song.full_clean()  # Perform model validation before saving
            song.save()  # Save the song to the database

            messages.success(request, 'Song uploaded successfully!')
            return redirect('/music/index/') # Redirect to index view after successful upload
        except Exception as e:
            print("An error occurred while uploading the song:", e)
            messages.error(request, 'An error occurred while uploading the song. Please try again.')
            return redirect('upload_song')  # Redirect back to the upload form
    else:
        # Fetch albums belonging to the current user
        albums = Album.objects.filter(user=request.user)
        return render(request, 'music/createsong.html', {'albums': albums})


def rectap(request):
    if request.method == 'POST':
        # Validate reCAPTCHA
        recaptcha_response = request.POST.get('g-recaptcha-response', '')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        secret_key = '6Lc1aPkpAAAAAOeUz4yOVWdI-vmxiXE016lth1Kt '  # Replace with your reCAPTCHA secret key
        params = {
            'secret': secret_key,
            'response': recaptcha_response
        }
        
        import requests
        response = requests.post(url, data=params)
        result = response.json()
        
        if result['success']:
            # reCAPTCHA verification passed, process your form data here
            # Example: save form data to database or perform other actions
            return HttpResponse('reCAPTCHA verification passed. Form submitted successfully!')
        else:
            # reCAPTCHA verification failed
            return HttpResponse('reCAPTCHA verification failed. Please try again.')
    
    return render(request, 'signup.html')


def submit_form(request):
    if request.method == 'POST':
        # Validate reCAPTCHA
        recaptcha_response = request.POST.get('g-recaptcha-response', '')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        secret_key = '6LfjifkpAAAAAAcyCm4DuWxBFKqOkQM2R0NmZxtR'  # Replace with your reCAPTCHA secret key
        params = {
            'secret': secret_key,
            'response': recaptcha_response
        }
        
        import requests
        response = requests.post(url, data=params)
        result = response.json()
        
        if result['success']:
            # reCAPTCHA verification passed, process your form data here
            # Example: save form data to database or perform other actions
            return HttpResponse('reCAPTCHA verification passed. Form submitted successfully!')
        else:
            # reCAPTCHA verification failed
            return HttpResponse('reCAPTCHA verification failed. Please try again.')
    
    return render(request, 'signin.html')


def indexs(request):
    allSongs = Song.objects.all().order_by('-last_updated')
    return render(request, template_name="music/index.html", context={"allSongs" : allSongs})

from django.contrib import messages
from django.core.exceptions import ValidationError
def search_songs(request): 
    template_path = 'music/search_result.html'
    
    search_query = request.GET.get('search', None)

    if search_query: 
        search_result = Song.objects.filter(
            Q(songName__icontains=search_query) | 
            Q(album__albumName__icontains=search_query) | 
            Q(album__artist__artistName__icontains=search_query)
        ).distinct()
    else: 
        search_result = Song.objects.all()

    return render(request, template_path, {'search_result': search_result, 'search_query': search_query})

#help centers

def help(request):
    return render(request, 'help.html')


#finish help centers


#start explain page!

def explain(request):
    return render(request, 'explain.html' )


# finish explain page!
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import os
import json
from .models import AiChatMessage

def submit_form(request):
    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response', '')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        secret_key = 'YOUR_SECRET_KEY'  # Replace with your reCAPTCHA secret key
        
        data = {
            'secret': secret_key,
            'response': recaptcha_response
        }
        
        response = requests.post(url, data=data)
        result = response.json()
        
        if result['success']:
            # reCAPTCHA verification passed, process your form data here
            return HttpResponse('reCAPTCHA verification passed. Form submitted successfully!')
        else:
            # reCAPTCHA verification failed
            return HttpResponse('reCAPTCHA verification failed. Please try again.')
    
    return render(request, 'signin.html')


def submit_form(request):
    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response', '')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        secret_key = 'YOUR_SECRET_KEY'  # Replace with your reCAPTCHA secret key
        
        data = {
            'secret': secret_key,
            'response': recaptcha_response
        }
        
        response = requests.post(url, data=data)
        result = response.json()
        
        if result['success']:
            # reCAPTCHA verification passed, process your form data here
            return HttpResponse('reCAPTCHA verification passed. Form submitted successfully!')
        else:
            # reCAPTCHA verification failed
            return HttpResponse('reCAPTCHA verification failed. Please try again.')
    
    return render(request, 'signup.html')


genai.configure(api_key=os.environ.get("AIzaSyDu2jKK82ZAXY52X4jDoUb18ke5TWSAmME"))

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        # Assuming `model` is defined globally or imported properly
        chat_session = model.start_chat(
            history=[]
        )

        response = chat_session.send_message(user_message)
        bot_response = response.text

        # Save the chat message to the database
        chat_message = ChatMessage(user_message=user_message, bot_response=bot_response)
        chat_message.save()

        # Return the bot response as JSON
        return JsonResponse({'response': bot_response})

    # Handle other HTTP methods with an error response
    return JsonResponse({'error': 'Invalid request method'}, status=400)


#about us page!

def about(request):
    return render(request, 'about.html')

#about us page finish!

# not found page!
def views_404(request, exception):
    return render(request, '404.html', status=404)

#finish not found page!

def download(request):
    return render(request, 'download.html')

def delete_item(request, item_id):
    try:
        item = CartItem.objects.get(id=item_id)
        item.delete()
        return JsonResponse({'message': 'Item deleted successfully.'}, status=200)
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found.'}, status=404)
@csrf_exempt
def predict_view(request):
    if request.method == 'POST':
        # Get the API key from the request data
        api_key = request.POST.get('api_key')

        # Check if the API key is valid (you can add your validation logic here)
        if api_key != "534233434342342323432343sdsdfwrererererererfefdf":  # Replace "your_api_key" with your actual API key
            return JsonResponse({'error': 'Invalid API key'})

        # Load your trained machine learning model
        model = joblib.load('data.cvc')  # Update with the actual path

        # Get input data from the request
        input_data = request.POST.get('input_data')

        # Perform any necessary preprocessing on input_data
        # Make sure it's in the same format as the data used to train the model

        # Make predictions using your trained model
        prediction = model.predict([input_data])[0]

        # Return the prediction as a JSON response
        return JsonResponse({'prediction': prediction})

    return render(request, 'predict.html')



def create_campaign(request):
    if request.method == 'POST':
        product_link = request.POST.get('product_link')
        product_name = request.POST.get('product_name')
        image = request.FILES.get('image')

        if product_link and product_name and image:
            # Check if the uploaded file is an image
            if not image.content_type.startswith('image'):
                return HttpResponseBadRequest('Uploaded file is not an image.')

            # Save the image to the media folder
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            image_url = fs.url(filename)
            purchase_times = request.POST.get('purchase_times')  # Get purchase_times if provided

            # Check if purchase_times is provided, otherwise use a default value
            if purchase_times:
                campaign = Campaign1.objects.create(
                    product_link=product_link,
                    product_name=product_name,
                    purchase_times=purchase_times,
                    image=image_url
                )
            else:
                campaign = Campaign1.objects.create(
                    product_link=product_link,
                    product_name=product_name,
                    purchase_times=1,  # Default value
                    image=image_url
                )

            return redirect('pay', pk=campaign.pk)
    return render(request, 'ecommerce/campign_start.html')

def campaign_detail(request, pk):
    campaign = Campaign1.objects.get(pk=pk)
    return render(request, 'ecommerce/purchase_product.html', {'campaign': campaign})

from django.shortcuts import render, get_object_or_404

def paypal_payment(request):
    return render(request, 'ecommerce/purchase_success.html')
# Configure PayPal SDK

def camera(request):
    return render(request, 'camera.html')

@login_required
def pay(request, pk):
    campaign = get_object_or_404(Campaign1, pk=pk)
    
    # Assume payment is successful for demonstration purposes
    # Process payment logic...
    payment_successful = True

    if payment_successful:
        # Payment was successful
        # Example amount and product name
        amount = campaign.price
        product_name = campaign.name
        

    return render(request, 'ecommerce/purchase_product.html', {'campaign': campaign})
def fetch_messages(request):
    # Retrieve latest messages from the database
    messages = Message.objects.all().order_by('-timestamp')[:10]  # Get last 10 messages
    # Construct HTML for displaying messages
    html = ''
    for message in messages:
        html += f'<div><strong>{message.sender}</strong>: {message.content}</div>'
    return JsonResponse({'messages': html})

def send_message(request):
    if request.method == 'POST':
        message_content = request.POST.get('message')
        # Save new message to the database
        Message.objects.create(sender=request.user, content=message_content)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

@login_required
def create_post(request):
    if request.method == 'POST':
        drawing_data = request.POST.get('drawing_data')  # Assuming drawing data is sent as a base64 encoded string
        user = request.user
        if drawing_data:
            post = Post2(user=user, drawing_data=drawing_data)
            post.save()
            return redirect('index')  # Redirect to a page displaying all posts
    return render(request, 'create_post.html')

def index(request):
    posts = Post2.objects.all()
    has_drawing_posts = any(post.drawing_data for post in posts)

    return render(request, 'index.html', {'posts': posts, 'has_drawing_posts': has_drawing_posts})


@login_required(login_url='signin')
def home_ai(request):
    return render(request, 'ai/home_ai.html')

@login_required(login_url='signin')
def genarante_photo(request):
    return render(request, 'ai/genarante_photo.html')

from django.db.models import Q


from .models import Store, Product
def stores_list(request):
    stores = Store.objects.all()
  
    return render(request, 'ecommerce/product_list.html', {'stores': stores,})


def search_stores(request):
    query = request.GET.get('q')
    stores = Store.objects.all()
    if query:
        stores = stores.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    return render(request, 'ecommerce/search_results.html', {'stores': stores, 'query': query})

def create_store(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        photo = request.FILES.get('photo')
        if name and description:
            store = Store.objects.create(name=name, description=description, photo=photo, owner=request.user)
            return redirect('store_detail', store_id=store.id)  # Redirect to store detail view
    return render(request, 'ecommerce/create_store.html')

def home_food(request):
    return render(request, 'food/food_home.html')

def store_edit(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    if request.user == store.owner:
        if request.method == 'POST':
            name = request.POST.get('name')
            description = request.POST.get('description')
            photo = request.FILES.get('photo')
            if name and description:
                store.name = name
                store.description = description
                if photo:
                    store.photo = photo
                store.save()
                return redirect('store_detail', store_id=store_id)
        return render(request, 'ecommerce/store_edit.html', {'store': store})
    else:
        return redirect('store_detail', store_id=store_id)

def stores(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    products = store.products.all()
    return render(request, 'ecommerce/stores.html', {'store': store, 'products': products})

def store_products(request, store_id):
    
    store = get_object_or_404(Store, id=store_id)
    products = store.products.all()
    return render(request, 'ecommerce/stores.html', {'store': store, 'products': products})



def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    store = product.store
    if request.user == store.owner:
        if request.method == 'POST':
            name = request.POST.get('name')
            price = request.POST.get('price')
            description = request.POST.get('description')
            photo = request.FILES.get('photo')
            if name and price and description:
                product.name = name
                product.price = price
                product.description = description
                if photo:
                    product.photo = photo
                product.save()
                return redirect('store_products', store_id=store.id)
        return render(request, 'ecommerce/edit_product.html', {'product': product, 'store': store})
    else:
        return redirect('store_detail', store_id=store.id)



@login_required
def view_food_items(request):
    if request.method == 'POST':
        # Handle form submission and create new food item
        name = request.POST.get('name')
        calories = request.POST.get('calories')
        # Retrieve the image from the admin form data
        image = request.FILES.get('image')
        FoodItem.objects.create(user=request.user, name=name, calories=calories, image=image)
        return redirect('view_food_items')
    
    # Retrieve all food items from the database
    food_items = FoodItem.objects.all()
    
    context = {
        'food_items': food_items
    }
    return render(request, 'food/view_food_items.html', context)

@register.simple_tag
def group_url(group_id):
    return f'/group/{group_id}/'

@login_required
def join_group(request, group_id):
    group = Group.objects.get(id=group_id)
    # Add the current user to the group members
    group.members.add(request.user)
    return redirect('group_list')

@login_required
def leave_group(request, group_id):
    group = Group.objects.get(id=group_id)
    # Remove the current user from the group members
    group.members.remove(request.user)
    return redirect('group_list')


def search_results(request):
    query = request.GET.get('query')
    search_results = []  # Initialize search_results as an empty list

    if query:
        # Perform search query
        user_results = User.objects.filter(username__icontains=query)

        # Retrieve profiles for the users found in the search
        for user in user_results:
            try:
                profile = user.profile  # Assuming OneToOneField with User
                search_results.append(profile)
            except ObjectDoesNotExist:
                pass  # Handle the case where the profile does not exist

    else:
        # If no query parameter is provided, show all users
        search_results = Profile.objects.all()

    return render(request, 'chats/search_results.html', {'search_results': search_results})

@login_required(login_url='signin')
def search1(request):
    try:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        if request.method == 'POST':
            username = request.POST['username']
            username_object = User.objects.filter(username__icontains=username)

            username_profile = []
            username_profile_list = []

            for users in username_object:
                username_profile.append(users.id)

            for ids in username_profile:
                profile_lists = Profile.objects.filter(id_user=ids)
                username_profile_list.append(profile_lists)
            
            username_profile_list = list(chain(*username_profile_list))
        else:
            # Initialize username_profile_list here
            username_profile_list = []

            # Your logic to populate username_profile_list based on user_profile goes here
            # For example:
            # username_profile_list = Profile.objects.filter(some_criteria=user_profile)

    except Profile.DoesNotExist:
        # Handle the case where the profile does not exist
        user_profile = None

        # Ensure that username_profile_list is initialized if there is no user_profile
        username_profile_list = []

    return render(request, 'chats/search1.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})
from .models import Group, GroupMessage
@login_required(login_url='signin')
def group_chat(request, group_id):
        
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)


    username_profile = []
    username_profile_list = []

    

           
            
    username_profile_list = list(chain(*username_profile_list))

            # Initialize username_profile_list here
    username_profile_list = []

            # Your logic to populate username_profile_list based on user_profile goes here
            # For example:
            # username_profile_list = Profile.objects.filter(some_criteria=user_profile)

        # Handle the case where the profile does not exist

        # Ensure that username_profile_list is initialized if there is no user_profile
    username_profile_list = []

        # Fetch notifications for the current user
    notifications = Notification.objects.filter(user=request.user)
     # Retrieve private and group messages
    private_messages = PrivateMessage.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
    group_messages = GroupMessage.objects.filter(group__members=request.user)
    stories = Story.objects.all()
    private_messages = PrivateMessage.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
    group_messages = GroupMessage.objects.filter(group__members=request.user)
    notifications = Notification.objects.filter(user=request.user)
    notifications_count = notifications.count()
    # Combine messages
    all_messages = list(private_messages) + list(group_messages)
    all_messages.sort(key=lambda x: x.timestamp, reverse=True)
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    # Combine messages
    all_messages = list(private_messages) + list(group_messages)
    all_messages.sort(key=lambda x: x.timestamp, reverse=True)
    group = Group.objects.get(id=group_id)
    messages = GroupMessage.objects.filter(group=group)
    return render(request, 'chats/group_chat.html',{
        'stories': stories,
        'user_profile': user_profile,
        'group': group,
        'messages': messages,
        'all_messages': all_messages,
        'notifications': notifications,
    })
@login_required(login_url='signin')
def send_group_message(request, group_id):
    group = Group.objects.get(id=group_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            group = Group.objects.get(id=group_id)
            GroupMessage.objects.create(group=group, sender=request.user, content=content)
    return redirect('group_chat', group_id=group_id)


def group_list(request):
    groups = Group.objects.all()
    return render(request, 'chats/group_list.html', {'groups': groups})
import mimetypes



def serialize_stories(stories):
    serialized_stories = []
    for story in stories:
        serialized_story = {
            'id': story.id,
            'author': story.author,
            'media_url': story.media_file.url,
            'media_type': story.media_type,
        }
        serialized_stories.append(serialized_story)
    return serialized_stories

def stories_api(request):
    stories = Story.objects.all()
    serialized_stories = serialize_stories(stories)
    return JsonResponse(serialized_stories, safe=False)


def upload_story(request):
    if request.method == 'POST':
        author_username = request.POST.get('author')
        media_file = request.FILES.get('media_file')

        # Basic validation
        if not all([author_username, media_file]):
            messages.error(request, "Please provide all the required information.")
            return redirect('create_story')

        # Get the User instance corresponding to the author username
        try:
            author = User.objects.get(username=author_username)
        except User.DoesNotExist:
            messages.error(request, f"User with username '{author_username}' does not exist.")
            return redirect('create_story')

        # Determine media type based on the file's MIME type
        mime_type, _ = mimetypes.guess_type(media_file.name)
        if mime_type:
            if mime_type.startswith('image'):
                media_type = 'image'
            elif mime_type.startswith('video'):
                media_type = 'video'
            else:
                messages.error(request, "Unsupported media type.")
                return redirect('upload_story')
        else:
            messages.error(request, "Could not determine media type.")
            return redirect('upload_story')

        # Create a new story instance and save it
        story = Story(author=author, media_file=media_file, media_type=media_type)
        story.save()

        # Redirect to the index page or any oth er page you prefer
        return redirect('Eliasdaily')
    else:
        return render(request, 'upload_story.html')
@login_required
def Eliasdaily(request):
    dailys = Story.objects.all() 
    private_messages = PrivateMessage.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
    group_messages = GroupMessage.objects.filter(group__members=request.user)
    
    # Fix for filtering notifications for the current user
    notifications = Notification.objects.filter(user=request.user)
    notifications_count = notifications.count()
    
    all_messages = list(private_messages) + list(group_messages)
    all_messages.sort(key=lambda x: x.timestamp, reverse=True)

    user_profile = Profile.objects.get(user=request.user)

    user_following_list = []
    feed = []
    messages_count = private_messages.count()




    
    username_profile_list = []
    return render(request, 'story_home.html',{
        'stories': dailys,
        'user_profile': user_profile,
        'messages_count': messages_count,
        'notifications_count': notifications_count,
        'all_messages': all_messages,
        'notifications': notifications,

    })
@login_required
def all_messages(request):
    # Retrieve private and group messages
    private_messages = PrivateMessage.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
    group_messages = GroupMessage.objects.filter(group__members=request.user)
    stories = Story.objects.all()
    private_messages = PrivateMessage.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
    group_messages = GroupMessage.objects.filter(group__members=request.user)
    notifications = Notification.objects.filter(user=request.user)
    notifications_count = notifications.count()
    # Combine messages
    all_messages = list(private_messages) + list(group_messages)
    all_messages.sort(key=lambda x: x.timestamp, reverse=True)
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    # Combine messages
    all_messages = list(private_messages) + list(group_messages)
    all_messages.sort(key=lambda x: x.timestamp, reverse=True)

    # Debugging: Print all_messages to check if they are retrieved
    print(all_messages)

    # Render the template with messages
    return render(request, 'chats/all_messages.html',{
        'stories': stories,
        'user_profile': user_profile,
        'all_messages': all_messages,
        'notifications': notifications,
    })

@login_required(login_url='signin')
def create_group(request):
    user = request.user
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')  # Retrieve uploaded image file

        # Check if title is provided
        if title:
            # Create a new group object with the received data
            group = Group.objects.create(title=title, description=description, image=image)

            # Redirect to the group detail page after successful creation
            return redirect('group_chat', group_id=group.id)
        else:
            return render(request, 'chats/creategorup.html', {'error_message': 'Group title is required.'})
    else:
        return render(request, 'chats/creategorup.html')
from django.contrib import admin

from django.db.models import Q
from django.http import HttpResponseBadRequest
@login_required
def private_chat(request, recipient_id):
    user = request.user
    recipient = get_object_or_404(User, id=recipient_id)
    error_message = ''
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            PrivateMessage.objects.create(sender=user, recipient=recipient, content=content)
            
            # Create a notification for the recipient
        Notification.objects.create(
        user=recipient,
        notification_type='example_notification',
        user_profile=user_profile,
        from_user=request.user,
        content='This is an example notification content.'
        )   
    else:
            error_message = 'Content cannot be empty'

    private_messages = PrivateMessage.objects.filter(
        (Q(sender=user, recipient=recipient) | Q(sender=recipient, recipient=user))
    ).order_by('timestamp')[:50]

    return render(request, 'chats/private_chat.html', {'recipient': recipient, 'private_messages': private_messages, 'error_message': error_message})

@login_required
def send_private_message(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    error_message = ''

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            PrivateMessage.objects.create(sender=request.user, recipient=recipient, content=content)
            
            # Create a notification for the recipient
            Notification.objects.create(
                user=recipient,
                from_user=request.user,
                notification_type='sent you a private message'
            )
            
            return redirect('private_chat', recipient_id=recipient_id)
        else:
            error_message = 'Content cannot be empty'

    private_messages = PrivateMessage.objects.filter(
        (Q(sender=request.user, recipient=recipient) | Q(sender=recipient, recipient=request.user))
    ).order_by('timestamp')[:50]

    return render(request, 'chats/private_chat.html', {'recipient': recipient, 'private_messages': private_messages, 'error_message': error_message})


@login_required
def track_weight(request):
    try:
        # Attempt to get the WeightTracker record for the current user
        weight_tracker, created = WeightTracker.objects.get_or_create(user=request.user)

        if request.method == 'POST':
            # Update the weight if a new weight is submitted
            new_weight = request.POST.get('weight')
            weight_tracker.weight = new_weight
            weight_tracker.save()

            # Calculate BMI based on weight and height (assuming height is stored in WeightTracker model)
            height = weight_tracker.height  # Assuming height is stored in WeightTracker model
            if height and new_weight:
                bmi = calculate_bmi(float(new_weight), float(height))  # Convert to float in case input is string
                # Update BMI in WeightTracker model
                weight_tracker.bmi = bmi
                weight_tracker.save()

        # Get the current user's food items
        food_items = FoodItem.objects.filter(user=request.user)

        context = {
            'weight': weight_tracker.weight,
            'bmi': weight_tracker.bmi,
            'food_items': food_items,
        }
        return render(request, 'food/track_weight.html', context)
    except IntegrityError:
        # Handle the case where a duplicate record is encountered
        # Redirect the user to an error page or handle the error as appropriate
        return render(request, 'food/error.html')

def calculate_bmi(weight, height):
    # Calculate BMI
    if height <= 0:
        return None  # Return None if height is invalid to avoid division by zero
    height_in_meters = height / 100  # Convert height from cm to meters
    bmi = weight / (height_in_meters ** 2)
    return bmi
from django.views.decorators.http import require_POST

@login_required
def view_notifications(request):
    # Fetch notifications for the current user
    notifications = Notification.objects.filter(user=request.user)
     # Retrieve private and group messages
    private_messages = PrivateMessage.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
    group_messages = GroupMessage.objects.filter(group__members=request.user)
    stories = Story.objects.all()
    private_messages = PrivateMessage.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
    group_messages = GroupMessage.objects.filter(group__members=request.user)
    notifications = Notification.objects.filter(user=request.user)
    notifications_count = notifications.count()
    # Combine messages
    all_messages = list(private_messages) + list(group_messages)
    all_messages.sort(key=lambda x: x.timestamp, reverse=True)
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    # Combine messages
    all_messages = list(private_messages) + list(group_messages)
    all_messages.sort(key=lambda x: x.timestamp, reverse=True)

    context = {
        'notifications': notifications
    }
    return render(request, 'notifications.html',{
        'stories': stories,
        'user_profile': user_profile,
        'all_messages': all_messages,
        'notifications': notifications,
        'context':context,
    })

@require_POST
def delete_message(request):
    message_id = request.POST.get('message_id')
    try:
        message = ChatMessage.objects.get(id=message_id)
        message.delete()
        return JsonResponse({'success': True})
    except ChatMessage.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Message does not exist'})

@login_required(login_url='signin')
def chat2(request):
    if request.method == 'POST':
        # Get the message text from the form
        message_text = request.POST.get('message')
        if message_text:
            # Create a new ChatMessage with the current user's ID and message text
            ChatMessage.objects.create(user=request.user, message=message_text)
        
        # Handle file upload if there's a file in the request
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            # Process the uploaded file here, such as saving it to the server
            handle_uploaded_file(uploaded_file)

        # Redirect to prevent form resubmission
        return redirect('chat2')

    # Retrieve chat messages from the database
    chat_messages = get_chat_messages()

    return render(request, 'food/chat.html', {'chat_messages': chat_messages})

def handle_uploaded_file(uploaded_file):
    # Specify the destination directory where the file will be saved
    destination_dir = 'static/videos'  # Ensure this directory exists in your project

    # Create the directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Write the uploaded file to the destination directory
    with open(os.path.join(destination_dir, uploaded_file.name), 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

def get_chat_messages():
    # Query the database to retrieve chat messages
    messages = ChatMessage.objects.all().order_by('-timestamp')[:10]  # Example: Retrieve the 10 most recent messages
    return messages

from moviepy.editor import VideoFileClip
import os
from pathlib import Path

# Construct directory path using pathlib
video_folder_path = Path("media") / "video"


# Combine folder path and file name
video_file_path = video_folder_path

# Convert to string if necessary
video_file_path_str = str(video_file_path)

from django.http import HttpResponseServerError
from django.contrib.auth.decorators import login_required

@login_required(login_url='signin')
def create_video(request):
    if request.method == 'POST':
        element_name = request.POST.get('element_name')
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        new_category_name = request.POST.get('new_category')
        image = request.FILES.get('image')
        video_file = request.FILES.get('video')  # Retrieve the uploaded video file

        # If a new category name is provided, create a new category
        if new_category_name:
            category, created = Category.objects.get_or_create(name=new_category_name)
        else:
            category = Category.objects.get(id=category_id)

        # Create the Product object with the provided data
        video = Video(
            element_name=element_name,
            title=title,
            category=category,
            video=video_file,  # Save the uploaded video file, if provided
            user=request.user  # Associate the product with the authenticated user

        )

        if image:  # If an image is provided, save it to the product
            video.image.save(image.name, image, save=True)

        video.save()  # Save the product object to the database

        return redirect('presentation_videos')

    categories = Category.objects.all()
    return render(request, 'create_video.html', {'categories': categories})
from django.http import Http404
from .models import Button, Category  # Import your Button and Category models
@login_required(login_url='signin')
def change_category(request, category_id=None):
    if request.method == 'POST':
        selected_button_id = request.POST.get('selected_button')
        new_category_id = request.POST.get('category_id')

        try:
            # Convert IDs to integers
            selected_button_id = int(selected_button_id)
            new_category_id = int(new_category_id)
        except (ValueError, TypeError):
            return render(request, 'error.html', {'message': 'Invalid button or category ID'})

        # Retrieve the button object
        button = Button.objects.filter(id=selected_button_id).first()
        if button is None:
            return render(request, 'error.html', {'message': 'Button does not exist'})

        # Retrieve the new category object
        new_category = Category.objects.filter(id=new_category_id).first()
        if new_category is None:
            return render(request, 'error.html', {'message': 'New category does not exist'})

        # Update the category of the button
        button.category = new_category
        button.save()

        # Redirect to the presentation_videos view with the selected category ID
        return redirect('presentation_videos', category_id=new_category_id)

    # If the request method is not POST, render the form
    categories = Category.objects.all()
    buttons = Button.objects.all()
    return render(request, 'change_category.html', {'categories': categories, 'buttons': buttons})
from moviepy.editor import VideoFileClip
import os
from pathlib import Path

# Construct directory path using pathlib
video_folder_path = Path("media") / "video"


# Combine folder path and file name
video_file_path = video_folder_path

# Convert to string if necessary
video_file_path_str = str(video_file_path)

from django.http import HttpResponseServerError
from django.contrib.auth.decorators import login_required





from .models import Video, Like, Notification
from django.db import IntegrityError, transaction
@login_required
def like_video(request, video_id):
    try:
        with transaction.atomic():
            video = get_object_or_404(Video, id=video_id)
            user = request.user
            already_liked = Like.objects.filter(video=video, user=user).exists()

            if already_liked:
                Like.objects.filter(video=video, user=user).delete()
                liked = False
            else:
                # Increment likes_count only if it's currently 0
                if video.likes_count == 0:
                    video.likes_count += 1
                Like.objects.create(video=video, user=user)
                liked = True

                # Create a notification if the video owner is different from the user
                if video.user != user:
                    Notification.objects.create(
                        user=video.user,
                        from_user=user,
                        notification_type='liked your video'
                    )

            video.save()

            return JsonResponse({'liked': liked, 'likes_count': video.likes_count})
    except IntegrityError as e:
        # Handle database integrity errors
        return JsonResponse({'error': 'Database error: {}'.format(str(e))}, status=500)
    except Exception as e:
        # Handle other unexpected errors
        return JsonResponse({'error': str(e)}, status=500)

from .models import Messages  # Update import statement to import Category1
from django.forms.models import model_to_dict


from django.shortcuts import get_object_or_404


@login_required(login_url='signin')
def share_video(request, video_id):
    if request.method == 'POST':
        video = get_object_or_404(Video, pk=video_id)
        video.share_count += 1
        video.save()
        return JsonResponse({'share_count': video.share_count})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
from django.utils import timezone

@login_required
def video_messages(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    messages = Messages.objects.filter(video=video)
    messages_count = messages.count()

    if request.method == 'POST':
        message_content = request.POST.get('message_content')
        messages_count += 1

        if message_content:
            # Create a new message for the video
            message = Messages.objects.create(video=video, user=request.user, content=message_content)

            # Create a notification for the video owner
            if video.user != request.user:
                Notification.objects.create(
                    user=video.user,
                    from_user=request.user,
                    notification_type='commented on your video'
                )

    return render(request, 'video_messages.html', {'video': video, 'messages': messages, 'messages_count': messages_count})
from django.contrib.admin.views.decorators import staff_member_required

from .models import ReportedMessage


@staff_member_required
def view_reports(request):
    reported_messages = Message.objects.filter(reported=True)
    return render(request, 'video_messages.html', {'reported_messages': reported_messages})

@login_required(login_url='signin')
def report_message(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        # Render a template indicating that the message was not found
        return render(request, 'message_not_found.html')
    
    if request.method == 'POST':
        report_reason = request.POST.get('report_reason')
        if report_reason:
            ReportedMessage.objects.create(message=message, reported_by=request.user, report_reason=report_reason)
            # Redirect the user to a success page
            return redirect('report_success')
        else:
            # Render a template indicating that a report reason is required
            return render(request, 'report_reason_required.html', status=400)
    else:
        # Render a template indicating an invalid request method
        return render(request, 'invalid_request_method.html', status=405)

@login_required(login_url='signin')
def presentation_videos(request):
    user = request.user

    if request.method == 'POST':
        # Handle POST request when a category is selected
        selected_category_id = request.POST.get('selected_category')
        search_query = request.POST.get('search_query')

        # Update the category names if necessary
        categories = Category.objects.all()
        for category in categories:
            new_name = request.POST.get(f'category_name_{category.id}')
            if new_name:
                category.name = new_name
                category.save()

        # Filter videos based on the selected category ID
        videos = Video.objects.all()

        if selected_category_id:
            videos = videos.filter(category_id=selected_category_id)

        # Filter videos based on the search query
        if search_query:
            videos = videos.filter(title__icontains=search_query)

        # Include the comment count and share count for each video
        for video in videos:
            video.messages_count = Messages.objects.filter(video=video).count()
            # Assuming `share_count` is a field in the Video model
            # You may need to adjust this according to your actual model
            video.share_count = video.share_count

            # Recommendation logic: Check if video is recommended for the user
            if is_video_recommended_for_user(video, user):
                video.recommended = 'V'
            else:
                video.recommended = 'X'

        return render(request, 'presentation_videos.html', {'categories': categories, 'videos': videos})

    else:
        # If it's not a POST request, display all videos initially
        categories = Category.objects.all()
        videos = Video.objects.all()

        # Include the comment count and share count for each video
        for video in videos:
            video.messages_count = Messages.objects.filter(video=video).count()
            # Assuming `share_count` is a field in the Video model
            # You may need to adjust this according to your actual model
            video.share_count = video.share_count

            # Recommendation logic: Check if video is recommended for the user
            if is_video_recommended_for_user(video, user):
                video.recommended = 'V'
            else:
                video.recommended = 'X'

        return render(request, 'presentation_videos.html', {'categories': categories, 'videos': videos})

@login_required(login_url='signin')
def viral(request):
    user = request.user

    # Your existing code for fetching data goes here
    stories = Story.objects.all()
    private_messages = PrivateMessage.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
    group_messages = GroupMessage.objects.filter(group__members=request.user)
    notifications = Notification.objects.filter(user=request.user)
    notifications_count = notifications.count()
    # Combine messages
    all_messages = list(private_messages) + list(group_messages)
    all_messages.sort(key=lambda x: x.timestamp, reverse=True)

    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    user_following = FollowersCount.objects.filter(follower=request.user.username)

    if request.method == 'POST':
        # Handle POST request for search functionality
        search_query = request.POST.get('search_query')
        videos = Video.objects.all()

        if search_query:
            # Filter videos based on search query (category, title)
            videos = videos.filter(
                Q(category__name__icontains=search_query) |  # Search by category
                Q(title__icontains=search_query)            # Search by title
            )

        # Calculate recommendation percentage for each video
        for video in videos:
            video.recommended = 'V' if is_video_recommended_for_user(video, user) else 'X'
            video.recommendation_percentage = calculate_recommendation_percentage(video, user)

        return render(request, 'viral.html', {
            'stories': stories,
            'videos': videos,
            'user_profile': user_profile,
            'all_messages': all_messages,
            'notifications': notifications,
        })

    else:
        # Handle GET request for initial page load
        videos = Video.objects.all()

        # Calculate recommendation percentage for each video
        for video in videos:
            video.recommended = 'V' if is_video_recommended_for_user(video, user) else 'X'
            video.recommendation_percentage = calculate_recommendation_percentage(video, user)

        return render(request, 'viral.html', {
            'stories': stories,
            'videos': videos,
            'user_profile': user_profile,
            'all_messages': all_messages,
            'notifications': notifications,
        })


def is_video_recommended_for_user(video, user):
    # Recommendation logic - check if video's category matches any of the user's interests
    user_interests = user.interests.all()
    video_category = video.category
    for interest in user_interests:
        if interest.category == video_category:
            return True
    return False

def calculate_recommendation_percentage(video, user):
    # Calculate recommendation percentage based on user's interests and video's category
    user_interests = user.interests.all()
    video_category = video.category
    matching_interests = sum(1 for interest in user_interests if interest.category == video_category)
    total_interests = user_interests.count()
    return int((matching_interests / total_interests) * 100) if total_interests > 0 else 0

def is_video_recommended_for_user(video, user):
    """
    Simple recommendation logic:
    Check if the video's category matches any of the user's interests.
    You can replace this with more sophisticated recommendation algorithms.
    """
    user_interests = user.interests.all()
    video_category = video.category
    for interest in user_interests:
        if interest.category == video_category:
            return True
    return False











def chat (request):
       return render(request, 'ai/app_ai.html')
 
from django.http import FileResponse





@login_required(login_url='signin')
def download_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    
    # Increment the download count for the video
    video.download_count += 1
    video.save()

    # Perform the download logic
    # Return the video file as a response
    # Assuming `video_file` is the field in the Video model containing the video file
    if video.video_file:
        return FileResponse(video.video_file.open('rb'), as_attachment=True, filename=f'{video.id}_video.mp4')
    else:
        # Handle the case where the video file is not available
        # Redirect back to the presentation_videos page or show an error message
        return redirect('presentation_videos')

@login_required
def process_payment(request, store_id):
    if request.method == 'POST':
        # Retrieve the store associated with the given store_id
        store = get_object_or_404(Store, id=store_id)

        # Retrieve the email submitted in the form
        email = request.POST.get('email')

        # Check if a user exists with the submitted email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Handle case where user doesn't exist with the submitted email
            return HttpResponse('User with this email does not exist.', status=400)

        # Store the email in the user's session for later use
        request.session['recipient_email'] = email

        # Calculate the amount to transfer to the store's email
        # For demonstration purposes, let's assume the amount is fixed for every purchase
        store_share = 0.97  # Store's share (97%)
        paypal_share = 0.03  # Your PayPal account's share (3%)
        amount = 100  # Example amount

        # Creating a default product
        default_product = Product.objects.create(
            name='Default Product',
            price=10.00,
            description='This is the default product.',
            store=store  # Associate the product with the given store
        )

        # Using the default product when creating a transaction
        Transaction.objects.create(
            user=user,
            product=default_product,
            amount_paid=amount * store_share
        )

        # Redirect or return a success response
        return HttpResponse('Payment processed successfully.')

    else:
        # Handle case where request method is not POST
        return HttpResponse('Method not allowed.', status=405)

def payment_failed(request):
    # Your view logic here
    return render(request, 'ecommerce/payment_failure.html')

def edit_product(request, pk):
    # Retrieve the product object from the database
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        # Update product details based on form data
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')

        # Handle product photo upload if a new photo is provided
        if 'photo' in request.FILES:
            product.photo = request.FILES['photo']

        # Save the updated product object
        product.save()

        # Redirect to a page showing the updated product details
        return redirect('product_detail', pk=pk)

    return render(request, 'ecommerce/edit_product.html', {'product': product})

@login_required
def payment_successful(request):
    # Process payment logic...
    payment_successful = True  # Example flag indicating payment success or failure

    if payment_successful:
        # Payment was successful
        amount = 100  # Example amount
        product_name = 'Default Product'  # Example product name
        
        # Create a notification for the user about the successful payment
        Notification.objects.create(
            user=request.user,
            notification_type='payment_successful',
            message=f'Your payment of {amount} for {product_name} was successful.'
        )

        return render(request, 'ecommerce/payment_success.html', {'amount': amount, 'product_name': product_name})
    else:
        # Payment failed
        return render(request, 'ecommerce/payment_failure.html')

def buy_with_paypal2(request):
    if request.method == 'POST':
        # Handle payment processing and capture here
        # Calculate amounts for the user and your PayPal account
        user_share = 0.97  # User's share (97%)
        paypal_share = 0.03  # Your PayPal account's share (3%)

        # Example: Amount is 100 units
        amount = 100
        user_amount = amount * user_share
        paypal_amount = amount * paypal_share

        # Perform PayPal payment processing here
        # Redirect to payment_successful view upon successful payment

    return render(request, 'ecommerce/cart.html')

@login_required(login_url='signin')
def earn(request):
    return render(request,'ecommerce/earn.html')
from django.core.exceptions import MultipleObjectsReturned

@login_required
def dashboard(request):
    user = request.user

    try:
        # Retrieve the store associated with the current user
        store = Store.objects.get(owner=user)
    except Store.DoesNotExist:
        store = None
    except MultipleObjectsReturned:
        # Handle the case where multiple stores are associated with the user
        # You can choose one of the stores or handle it based on your application logic
        stores = Store.objects.filter(owner=user)
        store = stores.first()

    # Retrieve transactions for the user
    transactions = Transaction.objects.filter(user=user)
    total_spent = sum(transaction.amount_paid for transaction in transactions)
    total_orders = transactions.count()

    context = {
        'user': user,
        'total_spent': total_spent,
        'total_orders': total_orders,
        'store': store,
    }

    return render(request, 'ecommerce/dashboard_start.html', context)
def buy_with_paypal(request):
    if request.method == 'POST':
        # Handle payment processing and capture here
        # Calculate amounts for the user and your PayPal account
        user_share = 0.97  # User's share (97%)
        paypal_share = 0.03  # Your PayPal account's share (3%)

        # Example: Amount is 100 units
        amount = 100
        user_amount = amount * user_share
        paypal_amount = amount * paypal_share

        # Perform PayPal payment processing here
        # Redirect to payment_successful view upon successful payment

    return render(request, 'ecommerce/product_detail.html')


def process_payment(request):
    if request.method == 'POST':
        # Payment processing logic goes here
        # This view will handle the POST request sent from the form

        # Assuming payment processing is successful
        success_message = "Your Paypal gmail accept"
        data = {'success': True, 'message': success_message}

        return JsonResponse(data)
    else:
        # If the request method is not POST, return an error message
        error_message = "Invalid request method."
        data = {'success': False, 'message': error_message}

        return JsonResponse(data, status=400)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
    

class ProductListView(ListView):
    model = Product
    template_name = 'ecommerce/product_list.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'ecommerce/product_detail.html'
    context_object_name = 'product'

from django import forms
class PayPalForm(forms.Form):
    user_email = forms.EmailField(label='Your PayPal Email')
from django.shortcuts import render, get_object_or_404
from .models import Product, Review

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    ratings = Review.objects.filter(product=product)
    context = {
        'product': product,
        'ratings': ratings,
    }
    return render(request, 'ecommerce/product_detail.html', context)
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed


def submit_review(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        rating = request.POST.get('rate')

        # Validate rating field
        if rating is not None and rating != '':
            # Validate review text
            if rating:
                # Save review to database
                Review.objects.create(user=request.user, product=product, rating=rating)
                return redirect('product_detail', pk=product_id)  # Redirect to product detail page
            else:
                # Render template with error message
                return render(request, 'ecommerce/product_detail.html', {'error_message': "Review text is required"})
        else:
            # Handle invalid rating
            return HttpResponse("Invalid rating provided")

    # If not a POST request, return a method not allowed response
    return HttpResponseNotAllowed(['POST'])



def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    # Delete the product
    product.delete()
    
    # Redirect to the appropriate page after deletion (e.g., store products page)
    return redirect('store_products', store_id=product.store_id)

def get_product_details(request):
    # Fetch product details from the database or any other source
    # For demonstration, assuming product amount and description are fetched from the database
    product_amount = 100  # Example product amount in cents
    product_description = "Product Description"  # Example product description

    # Return product details as JSON response
    return JsonResponse({'amount': product_amount, 'description': product_description})

def upload_product(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    error_message = None
    products = None

    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        photo = request.FILES.get('photo')

        # Check if all required fields are provided
        if name and price and description and photo:
            # Create the product without category
            product = Product.objects.create(
                name=name,
                price=price,
                description=description,
                photo=photo,
                store=store
            )

            # Redirect to the user's dashboard after successful product upload
            return redirect('dashboard_start')
        else:
            error_message = "Please fill in all the fields"
    else:
        error_message = None

    # Fetch all categories to pass to the template for rendering the category selection dropdown

    return render(request, 'ecommerce/upload_product.html', {'products': products, 'error_message': error_message, 'store_id': store_id})
@login_required
def user_dashboard(request):
    if hasattr(request.user, 'userprofile'):
        uploaded_products = request.user.userprofile.uploaded_products.all()
        return render(request, 'ecommerce/user_dashboard.html', {'uploaded_products': uploaded_products})
    else:
        # Handle the case where user profile doesn't exist
        error_message = "User profile does not exist."
        return render(request, 'ecommerce/user_dashboard.html', {'error_message': error_message})

def all_products(request):
    products = Product.objects.all()
    campaigns = Campaign1.objects.all()
    return render(request, 'ecommerce/product_list.html', {'campaigns': campaigns}, {'products': products})
@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    user = request.user  # Access the currently logged-in user
    cart_item, created = CartItem.objects.get_or_create(user=user, product=product)
    if created:
        cart_item.added_at = timezone.now()  # Set the added_at field to the current datetime
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(pk=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def cart(request):
    cart_items = CartItem.objects.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'ecommerce/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def cart_detail(request):
    cart_items = CartItem.objects.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'ecommerce/cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})

class ProductListView(ListView):
    model = Product
    template_name = 'ecommerce/product_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'ecommerce/product_detail.html'
    context_object_name = 'product'


class Cart(ListView):
    model = CartItem
    template_name = 'ecommerce/cart.html'
    context_object_name = 'cart_items'

class Cart_Detail(ListView):
    model = CartItem
    template_name = 'ecommerce/cart_detail.html'
    context_object_name = 'cart_items'

from .models import Notification, Story, PrivateMessage, GroupMessage






@login_required(login_url='signin')
def index(request):
    stories = Story.objects.all()
    private_messages = PrivateMessage.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
    group_messages = GroupMessage.objects.filter(group__members=request.user)
    
    # Fix for filtering notifications for the current user
    notifications = Notification.objects.filter(user=request.user)
    notifications_count = notifications.count()
    
    all_messages = list(private_messages) + list(group_messages)
    all_messages.sort(key=lambda x: x.timestamp, reverse=True)

    user_profile = Profile.objects.get(user=request.user)

    user_following_list = []
    feed = []
    messages_count = private_messages.count()

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))
    return render(request, 'index.html',{
        'stories': stories,
        'user_profile': user_profile,
        'messages_count': messages_count,
        'posts': feed_list,
        'notifications_count': notifications_count,
        'all_messages': all_messages,
        'notifications': notifications,
        'suggestions_username_profile_list': suggestions_username_profile_list[:4]

    })

from .models import UserProfile2

from django.contrib import messages
from django.http import Http404




@login_required(login_url='signin')
def profile(request, pk):
    stories = Story.objects.all()
    private_messages = PrivateMessage.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
    group_messages = GroupMessage.objects.filter(group__members=request.user)
    
    # Fix for filtering notifications for the current user
    notifications = Notification.objects.filter(user=request.user)
    notifications_count = notifications.count()
    
    all_messages = list(private_messages) + list(group_messages)
    all_messages.sort(key=lambda x: x.timestamp, reverse=True)

    user_profile = Profile.objects.get(user=request.user)

    user_following_list = []
    feed = []
    messages_count = private_messages.count()

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Forget'
    else:
        button_text = 'Remember'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    return render(request, 'profile.html',{
        'stories': stories,
        'user_profile': user_profile,
        'messages_count': messages_count,
        'notifications_count': notifications_count,
        'all_messages': all_messages,
        'notifications': notifications,
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,

    })

@login_required(login_url='signin')
def delete_post(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_id)
        # Check if the user requesting deletion is the owner of the post
        if post.user == request.user:
            post.delete()
            return redirect('profile', pk=request.user.username)
        else:
            # Handle unauthorized deletion attempt
            # You can redirect to an error page or show a message
            pass
    # Handle invalid request method or other cases
    return redirect('index')  # Redirect to a suitable page



@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

from django.utils import timezone
from .models import Notification

def post_detail(request, pk):
    # Retrieve the post object based on the provided pk (primary key)
    post = get_object_or_404(Post, pk=pk)
    
    # Render the post detail template with the post object
    return render(request, 'index.html', {'post': post})
def mobile(request):
    return render(request, 'uploadpost.html')

@login_required(login_url='signin')
def uploadm(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return render(request, 'uploadpost.html')

@login_required(login_url='signin')
def gosearch(request):
    stories = Story.objects.all()
    private_messages = PrivateMessage.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
    group_messages = GroupMessage.objects.filter(group__members=request.user)
    
    # Fix for filtering notifications for the current user
    notifications = Notification.objects.filter(user=request.user)
    notifications_count = notifications.count()
    
    all_messages = list(private_messages) + list(group_messages)
    all_messages.sort(key=lambda x: x.timestamp, reverse=True)

    user_profile = Profile.objects.get(user=request.user)

    user_following_list = []
    feed = []
    messages_count = private_messages.count()



    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    all_users = User.objects.all()
    user_following_all = []

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    
    username_profile_list = []
    return render(request, 'searchgo.html',{
        'stories': stories,
        'user_profile': user_profile,
        'messages_count': messages_count,
        'posts': feed_list,
        'notifications_count': notifications_count,
        'all_messages': all_messages,
        'notifications': notifications,

    })
@login_required(login_url='signin')
def search(request):

    stories = Story.objects.all()
    private_messages = PrivateMessage.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
    group_messages = GroupMessage.objects.filter(group__members=request.user)
    
    # Combine messages
    all_messages = list(private_messages) + list(group_messages)
    all_messages.sort(key=lambda x: x.timestamp, reverse=True)

    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    feed = []
# user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)


    username_profile_list = []


    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')
    


@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    stories = Story.objects.all()
    private_messages = PrivateMessage.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
    group_messages = GroupMessage.objects.filter(group__members=request.user)
    notifications = Notification.objects.filter(user=request.user)
    notifications_count = notifications.count()
    # Combine messages
    all_messages = list(private_messages) + list(group_messages)
    all_messages.sort(key=lambda x: x.timestamp, reverse=True)

    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    user_following = FollowersCount.objects.filter(follower=request.user.username)
    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        return redirect('settings')
    return render(request, 'setting.html',{
        'stories': stories,
        'user_profile': user_profile,
        'all_messages': all_messages,
        'notifications': notifications,
    })

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')
from django.http import HttpResponseRedirect

def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')

from django.contrib import auth


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')



from typing import Protocol
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .decorators import user_not_authenticated
from .tokens import account_activation_token


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('homepage')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')
