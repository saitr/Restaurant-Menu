from django import forms
from django.contrib.auth.forms import UserCreationForm
from menu_app.models import CustomUser
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
        model = CustomUser
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
    username_or_phone = forms.CharField(label='Username or Phone Number', widget=forms.TextInput(attrs={'class': 'input--style-2', 'placeholder': 'Username or Phone Number'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'input--style-2', 'placeholder': 'Password'}))

    class Meta:
        fields = ('username_or_phone', 'password')




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
    number_var = forms.CharField(
        label='Room Number',
        widget=forms.TextInput(attrs={'class': 'input--style-2', 'placeholder': 'Room Number'})
    )
    room_number = forms.ChoiceField(
        label='Is It a Room?',
        choices=[('Yes', 'Yes'), ('No', 'No')],
        widget=forms.Select(attrs={'class': 'input--style-2'})
    )
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={'class': 'input--style-2', 'placeholder': 'Description'})
    )
    room_price = forms.DecimalField(
        label='Room Price',
        widget=forms.NumberInput(attrs={'class': 'input--style-2', 'placeholder': 'Room Price'})
    )
    image1 = forms.ImageField(
        label='Image 1',
        widget=forms.FileInput(attrs={'class': 'input--style-2'})
    )
    image2 = forms.ImageField(
        label='Image 2',
        widget=forms.FileInput(attrs={'class': 'input--style-2'})
    )
    image3 = forms.ImageField(
        label='Image 3',
        widget=forms.FileInput(attrs={'class': 'input--style-2'})
    )
    image4 = forms.ImageField(
        label='Image 4',
        widget=forms.FileInput(attrs={'class': 'input--style-2'})
    )

    class Meta:
        model = Owner_Utility
        fields = ['number_var', 'room_number', 'description', 'room_price', 'image1', 'image2', 'image3', 'image4']
