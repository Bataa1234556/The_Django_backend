from django.db import models
from django.contrib.auth import get_user_model 
from phonenumber_field.formfields import PhoneNumberField
from data_models.models import User


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    otp = models.CharField(max_length=6)
    phone_number = PhoneNumberField(region='MN', required=True, help_text="Утасны Дугаар")
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user.username} - {self.otp}'
    
