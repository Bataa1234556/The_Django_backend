from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views import View
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import UserSerializer
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import IntegrityError, transaction
import logging
from django.middleware.csrf import get_token

logger = logging.getLogger(__name__)

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()  
                    logger.info(f"User {user.username} created with ID {user.id}")
                    user.save()
                    token, created = Token.objects.get_or_create(user=user)
                    logger.info(f"Token created for user {user.username}")

                    return Response({'token': token.key}, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                logger.error(f"IntegrityError: {e}")
                user.delete()
                return Response({'detail': 'Error creating token.'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                return Response({'detail': 'Unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.warning(f"Invalid data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': token.key}, status=status.HTTP_200_OK)
        return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            logout(request)
            return JsonResponse({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        return JsonResponse({'error': 'User not authenticated'}, status=status.HTTP_400_BAD_REQUEST)
@ensure_csrf_cookie
def get_csrf_token(request):
    response = JsonResponse({'detail': 'CSRF cookie set'})
    csrf_token = get_token(request)
    response.set_cookie(
        'csrftoken', 
        csrf_token, 
        max_age=3600,  # Set the duration to 1 hour
        httponly=True, 
        secure=True if request.is_secure() else False
    )
    return response