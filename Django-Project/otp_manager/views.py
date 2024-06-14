from django.http import JsonResponse
from django.views import View
from django.db import transaction, IntegrityError
from django.contrib.auth import get_user_model
from .utils.send_otp_message import send_otp_message
from .models import OTP
import random
import logging
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from data_models.models import User
import requests
import json

logger = logging.getLogger(__name__)
User = get_user_model()

def generate_otp():
    return str(random.randint(100000, 999999))

class SendOTPView(View):
    def post(self, request, *args, **kwargs):
        try:
            if request.content_type == 'application/json':
                try:
                    data = json.loads(request.body)
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error: {e}")
                    return JsonResponse({'message': 'Invalid JSON.'}, status=400)
            else:
                data = request.POST

            logger.info(f"Incoming data: {data}")

            username = data.get('username')
            logger.info(f"Received username: {username}")

            if not username:
                logger.error("No username provided in the request")
                return JsonResponse({'message': 'Username not provided.'}, status=400)

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                logger.error(f"User with username {username} does not exist")
                return JsonResponse({'message': 'User with this username does not exist.'}, status=404)

            otp = generate_otp()  # Ensure generate_otp is called correctly
            OTP.objects.create(user=user, otp=otp)
            if send_otp_message(user.phone_number, otp):
                logger.info(f"OTP sent successfully to {user.phone_number}")
                return JsonResponse({'message': 'OTP sent successfully!'}, status=200)
            else:
                logger.error(f"Failed to send OTP to {user.phone_number}")
                return JsonResponse({'message': 'Failed to send OTP.'}, status=500)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return JsonResponse({'message': 'An unexpected error occurred.'}, status=500)

class VerifyOTPView(View):
    def post(self, request, *args, **kwargs):
        try:
            if request.content_type == 'application/json':
                try:
                    data = json.loads(request.body)
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error: {e}")
                    return JsonResponse({'message': 'Invalid JSON.'}, status=400)
            else:
                data = request.POST

            username = data.get('username')
            otp_entered = data.get('otp')

            if not username or not otp_entered:
                logger.error("Username or OTP not provided in the request")
                return JsonResponse({'message': 'Username or OTP not provided.'}, status=400)

            try:
                otp_obj = OTP.objects.filter(user__username=username).order_by('-created_at').first()
                if not otp_obj:
                    logger.error(f"OTP not found for user {username}")
                    return JsonResponse({'message': 'OTP not found for this user.'}, status=404)
                
                if otp_obj.otp == otp_entered:
                    logger.info(f"OTP verification successful for {username}")
                    return JsonResponse({'message': 'OTP verification successful!'}, status=200)
                else:
                    logger.warning(f"Invalid OTP entered for {username}")
                    return JsonResponse({'message': 'Invalid OTP! Please try again.'}, status=400)
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                return JsonResponse({'message': 'An unexpected error occurred.'}, status=500)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return JsonResponse({'message': 'An unexpected error occurred.'}, status=500)

