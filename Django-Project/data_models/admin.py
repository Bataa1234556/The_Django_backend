from django.contrib import admin
from django import forms
from .models import User

class UserAdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ['username']
    search_fields = ['username']

admin.site.register(User, UserAdmin)