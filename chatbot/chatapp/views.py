from django.shortcuts import render

from django.http import JsonResponse
import pickle


from django.http import JsonResponse
import pickle


from django.http import JsonResponse
import pickle

import io
import base64




from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.serializers import serialize

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.serializers import serialize

class SignupAPI(APIView):
    def post(self, request):
        User = get_user_model()
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not username or not email or not password:
            return Response({'error': 'Username, email, and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email is already taken'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    


class LoginAPI(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if user:
            # Create token
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key,'user_id':user.id}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

def user_list(request):
    # Retrieve all user objects from the database
    users = User.objects.all()
    # Serialize the user data
    user_data = serialize('json', users)
    # Return the user data as JSON response
    return JsonResponse(user_data, safe=False)




from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChatHistory
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import json

User = get_user_model()

@csrf_exempt
def save_chat_history(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get("user_id")
        chat_log = data.get("chat_log", "")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)

        # Save the chat history for the user
        ChatHistory.objects.create(user=user, chat_log=chat_log)
        return JsonResponse({"status": "Chat history saved."})
    return JsonResponse({"error": "Invalid request method."}, status=400)

def get_chat_history(request):
    user_id = request.GET.get("user_id")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    try:
        # Get the most recent chat history for the user
        chat_history = ChatHistory.objects.filter(user=user).order_by('-created_at').first()
        if chat_history:
            return JsonResponse({"chat_log": chat_history.chat_log})
        else:
            return JsonResponse({"chat_log": ""})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
