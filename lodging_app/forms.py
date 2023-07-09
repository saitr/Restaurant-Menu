from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import *
#######################Sign UP form##################################
import phonenumbers

def validate_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        if phonenumbers.is_valid_number(parsed_number):
            return True
        else:
            return False
    except phonenumbers.phonenumberutil.NumberParseException:
        return False
    

class SignUpForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-2', 'placeholder': 'UserName'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input--style-2','placeholder': 'Password'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input--style-2','placeholder': 'Email'}))
    country_code = forms.ChoiceField(choices=[('+91', '+91 - India'),('+92', '+92 - Pakistan')], widget=forms.Select(attrs={'class': 'input--style-2'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-2','placeholder': 'Phone Number'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-2','placeholder': 'Address'}))

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'country_code', 'phone_number', 'address')

    def clean_phone_number(self):
        country_code = self.cleaned_data.get('country_code')
        phone_number = self.cleaned_data.get('phone_number')
        full_phone_number = ''

        if country_code and phone_number:
            full_phone_number = country_code + phone_number

        if not validate_phone_number(full_phone_number):
            raise forms.ValidationError('Invalid phone number')

        return full_phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    
################# verifying the otp form #########################

class VerifyOTPForm(forms.Form):
    otp = forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-2', 'placeholder': 'OTP'}),max_length=6)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['otp'].error_messages = {'invalid': 'Invalid OTP. Please try again.'}

###################Signin form#################################

class SignInForm(forms.Form):
    username= forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-2', 'placeholder': 'UserName'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input--style-2','placeholder': 'Password'}))
    class Meta:
        model = User
        fields = ('username', 'password')




################## changing the user_details form #####################

class ChangeUserDetails(forms.Form):
    # username = forms.CharField(max_length=100,label='Username:')
    username= forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-2', 'placeholder': 'UserName'}))
    # email = forms.EmailField(label='Email:')
    email= forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input--style-2', 'placeholder': 'Email'}))
    # phone_number = forms.IntegerField(label="Phone Number:")
    phone_number= forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input--style-2', 'placeholder': 'Phone Number'}))
    # address = forms.CharField(max_length=100,label = 'Address:')
    address= forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-2', 'placeholder': 'Address'}))
    display_picture = forms.FileField(label='Change Display Picture',required=False)



############################ Room Creation Form ########################


class RoomCreationForm(forms.ModelForm):
    class Meta:
        model = Owner_Utility
        fields = ['number_var', 'room_number','description', 'room_price', 'image1', 'image2', 'image3', 'image4']