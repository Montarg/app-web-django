import json
import os
from django.utils import timezone
import webbrowser
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotAllowed 
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse 

from .models import Article, CreditPurchaseHistory, CustomerUser, Prompt, PromptHistory  # Modifier cet import


from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login 
from django.contrib.auth import logout

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile



import openai


# monapp/views.py



def index(request):
    return render(request, 'index.html')

@login_required(login_url='/login/')
def ex(request):
    return render(request, 'ex.html')

def base(request):
    return render(request, 'base.html')

def register(request):
    return render(request, 'register.html')

def modal(request):
    return render(request, 'modal.html')

def load_articles(request):
    articles = Article.objects.all()
    articles_list = list(articles.values('id', 'title', 'content'))  
    return render(request,'go.html',{'articles': articles_list})
def delete_article(request, article_id):
    print(article_id)
    if request.method == 'DELETE':
        article = get_object_or_404(Article, id=article_id)
        article.delete()
        return JsonResponse({'message': 'Article deleted'}, status=200)
    else:
        return HttpResponseNotAllowed(['DELETE'])
    
def indexx(request):
    return render(request, 'index1.html')

def logout_view(request):
    logout(request)
    return redirect('login_view')
def prompt_history_view(request):
    history = PromptHistory.objects.all().order_by('-created_at')  
    return render(request, 'prompt_history.html', {'history': history})

def login_view(request):
    return render(request, 'login.html')
def final(request):
    return render(request, 'final.html')
# monapp/views.py

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"First Name: {first_name}, Email: {email}, Password: {password}")
        print(f"POST Data: {request.POST}")

        if not all([first_name, email, password]):
            return JsonResponse({'error': 'Missing fields'}, status=400)

        try:
            user = User.objects.create_user(username=email, first_name=first_name, email=email, password=password)

            CustomerUser.objects.create(user=user)

            return JsonResponse({'message': 'User created successfully!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"Email: {email}")
        print(f"Password: {password}")

        if not all([email, password]):
            return JsonResponse({'error': 'Missing fields'}, status=400)

        print("Before authentication")

        user = authenticate(request, username=email, password=password)

        print("After authentication")

        if user is not None:
            auth_login(request, user)
            print("User authenticated and logged in successfully.")
            redirect_url = reverse('ex')
            return JsonResponse({'redirect_url': redirect_url})
        else:
            print("Invalid credentials provided.")
            return JsonResponse({'error': 'Invalid credentials'}, status=401)


#openai.api_key = "sk-9Q4O11_Evyt7WcfTARl6AN9eow41HHp4Elw0MfEPNiT3BlbkFJ_e75LgOvnmauz5TbdMnfuMV_f2L_dVtt1UA5jq4wQA"
@csrf_exempt
def generate_image(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        size = request.POST.get('resolution')
        print(size)

        print(prompt)

        if not prompt:
            return JsonResponse({'error': 'Missing prompt'}, status=400)
        if check_and_deduct_credits(request.user) == False:
            return HttpResponse(
                status=403,
                headers={
                    'HX-Trigger': json.dumps({
                        "showModal": "Crédits insuffisants !"
                    })
                }
            )
        url = "https://api.openai.com/v1/images/generations"

        api_key = "sk-yZKI_14VbChcgIuAqnzupJjae2tznKYpwnmcnpsjCKT3BlbkFJHuliVIhFtoLJVS6RXaGLgaIALsbOQGcoBlHwlA4iMA"

        headers = {
            "Authorization": f"Bearer {api_key}"
        }

        data = {
            "model": "dall-e-3",
            "prompt": prompt,  # Use the prompt from the POST request
            "n": 1,
            "size": size,
            
        }

        response = requests.post(url, headers=headers, json=data)
      
        if response.status_code == 200:
            result = response.json()
            print(result)
            image_url = result['data'][0]['url']
            print(image_url)
          
            return HttpResponse(f'<img id="generatedImage" class="img-fluid" src="{image_url}" alt="Image générée">')

        else:
            print(response.json())
            image_url = 'https://via.placeholder.com/150'
            image_response = requests.get(image_url)
           
            image_name = os.path.basename(image_url)  # Nom de fichier de l'image
            os.path.join(settings.MEDIA_ROOT, 'generated_images', image_name)
            image_content = ContentFile(image_response.content, name=image_name)
          
            prompt_instance=Prompt.objects.create(
                user_id=request.user.id,  
                description=prompt,
                created_at=timezone.now()  
            )
            prompt_history = PromptHistory(prompt=prompt_instance, image=image_content)
            prompt_history.save()
          
            error_message = response.json().get('error', {}).get('message', 'Unknown error')
            print(error_message)
            return JsonResponse(response.json())
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def check_and_deduct_credits(user):
    try:
        profile = CustomerUser.objects.get(user=user)
    except CustomerUser.DoesNotExist:
        return False  

    if profile.credits > 0:
        
        
        return True
    else:
        return False
    
@login_required
def add_credits(request):
    if request.method == 'POST':
        selected_credits = request.POST.get('selected_credits')
        custom_credits = request.POST.get('custom_credits')
        price = request.POST.get('price')  
         
        print(selected_credits)
        print(price)
        customer_user = CustomerUser.objects.get(user=request.user)

        if selected_credits:
            credits_to_add = int(selected_credits)
        elif custom_credits:
            credits_to_add = int(custom_credits)
        else:
            credits_to_add = 0

        customer_user.credits += credits_to_add
        customer_user.save()
        
        CreditPurchaseHistory.objects.create(
            user=request.user,
            amount=credits_to_add,
            price=int(price)  
        )


        return redirect('ex')  
@login_required
def credit_purchase_history(request):
        purchase_history = CreditPurchaseHistory.objects.filter(user=request.user).order_by('-timestamp')

        context = {
            'purchase_history': purchase_history
        }

        return render(request, 'history.html', context)
    