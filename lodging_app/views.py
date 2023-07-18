from django.conf import settings
from django.contrib.auth import login
from django.core.mail import send_mail,EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
# form imports 
from lodging_app.forms import SignUpForm,VerifyOTPForm,SignInForm,ChangeUserDetails
from django.http import HttpResponse
from .models import *
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# from rest_framework.authtoken.models import Token
import secrets
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
##checks for login
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token

# Other imports remain the same
import concurrent.futures
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from menu_app.models import *
from django.utils.crypto import get_random_string
from django.conf import settings
from datetime import timedelta

# Other imports remain the same
import phonenumbers
from django.contrib.admin.views.decorators import staff_member_required

from .task import *
from django.db.models import Q
from .forms import RoomCreationForm
from menu_app.models import *


def validate_phone_number(full_phone_number):
    try:
        parsed_number = phonenumbers.parse(full_phone_number, None)
        if phonenumbers.is_valid_number(parsed_number):
            return True
        else:
            return False
    except phonenumbers.phonenumberutil.NumberParseException:
        return False

from restaurants.celery import app


@app.task
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            country_code = form.cleaned_data.get('country_code')
            phone_number = form.cleaned_data.get('phone_number')
            
            # Add the country code to the phone number
            full_phone_number =  phone_number
            print(full_phone_number)
            if CustomUser.objects.filter(email=email, username=username).exists():
                form.add_error('email', 'Email already exists')
                return render(request, 'signup_sai.html', {'form': form})

            if CustomUser.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists')
                return render(request, 'signup_sai.html', {'form': form})

            if not validate_phone_number(full_phone_number):
                form.add_error('phone_number', 'Invalid phone number')
                return render(request, 'signup_sai.html', {'form': form})
            # generate OTP and save it to user model
            otp = get_random_string(length=6, allowed_chars='1234567890')
            user = CustomUser.objects.create_user(
                username=form.cleaned_data.get('username'),
                email=email,
                phone_number=form.cleaned_data.get('phone_number'),
                address=form.cleaned_data.get('address'),
                otp=otp,
                password=form.cleaned_data.get('password')
            )

            # to create a token
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token(user=user)

            token.key = secrets.token_urlsafe(32)
            token.created = timezone.now()
            token.expires = token.created + timedelta(days=7)
            token.save()

            # Send email with OTP asynchronously
            subject = 'Verify your email'
            message = f'Your OTP is {otp}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]

            # Use concurrent.futures to send the email in a separate thread
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(send_mail_async, subject, message, from_email, recipient_list)
            # Redirect to verify page
            return redirect('verify', email=email)
    else:
        form = SignUpForm()
    return render(request, 'signup_sai.html', {'form': form})



############################## to verify the email while signing up##################################

def verify(request, email):
    user = CustomUser.objects.get(email=email)

    if request.method == 'POST':
        form = VerifyOTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('otp')
            if otp == user.otp:
                user.is_active = True
                user.is_verified = True
                user.is_logged_in = True
                user.save()
                
                redirect('room_list')
                # Send thank you email
                subject = 'Welcome To The Family'
                from_email = settings.DEFAULT_FROM_EMAIL
                to = [email]

                html_content = render_to_string('thankyouemail_sai.html')
                text_content = strip_tags(html_content)

                msg = EmailMultiAlternatives(subject, text_content, from_email, to)
                msg.attach_alternative(html_content, 'text/html')
                msg.send()

                # Authenticate and log in the user
                login(request, user)
                user.save_token()

                if login:
                    print('successfully logged in')
                else:
                    print('failed to login')

                if request.user.is_authenticated:
                    print("Logged in")
                else:
                    print("Not logged in")

                return redirect('room_list')
            else:
                form.add_error('otp', 'Invalid OTP. Please try again.')
    else:
        form = VerifyOTPForm()

    return render(request, 'verify_sai.html', {'form': form})


#######################################logout view#######################################



def logout_user(request):
    if request.user.is_authenticated:
        user = request.user
        user.token = None
        print('thisi sit',user.token)
        user.is_logged_in = False
        user.save()
        logout(request)
    return redirect('signin')




########################################### signin view###################################

from django.contrib.auth.hashers import check_password

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                form.add_error(None, 'Incorrect username or password')
                return render(request, 'signin_sai.html', {'form': form})

            # Use check_password to validate the password
            if not check_password(password, user.password):
                form.add_error(None, 'Incorrect username or password')
                return render(request, 'signin_sai.html', {'form': form})

            login(request, user)

            # Delete any existing tokens for the user
            user.save_token()

            user.is_logged_in = True
            user.save()

            return redirect('room_list')

    else:
        form = SignInForm()

    return render(request, 'signin_sai.html', {'form': form})




############################ user details ##################################

@login_required
def user_details(request):
    user = request.user
    users = CustomUser.objects.all()
    if request.method == 'POST':
        form = ChangeUserDetails(request.POST,request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            display_picture = form.cleaned_data['display_picture']

            request.user.username = username
            request.user.email = email
            request.user.phone_number = phone_number
            request.user.address = address
            
            # Save display picture if provided
            if display_picture:
                user.display_picture = display_picture
                
            request.user.save()
            return redirect('room_list')
    else:
        initial_data = {
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number,
            'address': user.address,
        }
        form = ChangeUserDetails(initial=initial_data)
    
    return render(request, 'my-account_sai.html', {'form': form,'users': users})

############### Room Booking views ###################

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.urls import reverse

def room_list(request):
    rooms = Owner_Utility.objects.filter(is_booked=False,room_number=True)
    return render(request, 'room_list_sai.html', {'rooms': rooms})

@login_required
def book_room(request, room_id):
    room = Owner_Utility.objects.get(id=room_id)
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        number_of_people = request.POST['number_of_people']
        # Create a new Lodge booking
        lodge = Lodge.objects.create(user=request.user, room_chosen=room, from_date=from_date, to_date=to_date,number_of_people=number_of_people)
        # Update the Owner_Utility room status
        room.is_booked = True
        room.save()
        return redirect('booking_success')
    return render(request, 'book_room_sai.html', {'room': room})

def booking_success(request):
    return render(request, 'booking_success_sai.html')


#############################  Total Bookings #######################


@login_required(login_url='signin')
def my_bookings(request):
    user = request.user
    my_bookings = Lodge.objects.filter(user=user)
    return render(request, 'my_bookings_sai.html', {'my_bookings': my_bookings})




from django.db.models import Q

@staff_member_required(login_url='signin')
def total_bookings(request):
    unpaid_bookings = Lodge.objects.filter(~Q(invoice__paid=True))
    return render(request, 'total_bookings_sai.html', {'unpaid_bookings': unpaid_bookings})


@login_required(login_url='signin')
def check_in(request, lodge_id):
    lodge = Lodge.objects.get(id=lodge_id)
    if request.user.is_superuser and not lodge.check_in:
        lodge.check_in = True
        lodge.check_in_date_time = timezone.now()
        lodge.save()
    return redirect(reverse('total-bookings'))

@login_required(login_url='signin')
def check_out(request, lodge_id):
    lodge = Lodge.objects.get(id=lodge_id)
    if request.user.is_superuser and lodge.check_in and not lodge.check_out:
        lodge.check_out = True
        lodge.check_out_date_time = timezone.now()
        lodge.save()
        # Update the Owner_Utility room status
        room = lodge.room_chosen
        room.is_booked = False
        room.save()
    return redirect(reverse('total-bookings'))


@login_required(login_url='signin')
def order_page(request):
    user = request.user

    # Get the user's booked lodges
    lodges = Lodge.objects.filter(user=user, check_out=False)

    # Calculate the total number of nights and price for each booking
    for lodge in lodges:
        lodge.total_nights = (lodge.to_date - lodge.from_date).days
        lodge.total_price = lodge.room_chosen.room_price * lodge.total_nights

    return render(request, 'order_page_sai.html', {'lodges': lodges})


from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings

@login_required(login_url='signin')
def send_order_email(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    lodges = Lodge.objects.filter(user=user, check_out=False)

    # Render the order page template to HTML string
    html_content = render_to_string('order_page_sai.html', {'lodges': lodges})

    # Create the email message
    subject = 'Your Order Details'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user.email

    email = EmailMultiAlternatives(subject, '', from_email, [to_email])

    # Attach the HTML content as alternative content
    email.attach_alternative(html_content, 'text/html')

    # Send the email
    email.send()

    # Return a response to indicate the email has been sent
    return HttpResponse('Order details sent successfully')

from django.http import HttpResponseRedirect

@login_required(login_url='signin')
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Lodge, id=booking_id)
    if booking.user == request.user and not booking.check_in and not booking.check_out:
        booking.room_chosen.is_booked = False
        booking.room_chosen.save()
        booking.delete()
    return HttpResponseRedirect(reverse('my-bookings'))



@staff_member_required
def create_room(request):
    if request.method == 'POST':
        form = RoomCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('room_list')  # Redirect to the room list page after successful creation
    else:
        form = RoomCreationForm()
    
    return render(request, 'create_room_sai.html', {'form': form})





from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings

@login_required(login_url='signin')
def generate_invoice(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    lodges = Lodge.objects.filter(user=user, check_out=True)  # Filter bookings for the selected user
    invoices = []
    
    for lodge in lodges:
        # Check if an invoice already exists for the lodge
        if not Invoice.objects.filter(lodge=lodge).exists():
            invoice = Invoice.objects.create(lodge=lodge, invoice_number="INV001")  # Create an invoice for each booking
            invoices.append(invoice)
            # Mark the invoice as paid
            invoice.paid = True
            invoice.save()
            # You can also mark the lodge as paid if needed
            lodge.check_out = True
            lodge.save()
    
    # Calculate the total price for the newly generated invoices
    total_price = sum(invoice.lodge.room_chosen.room_price for invoice in invoices)
    
    # Render the invoice template to HTML string
    html_content = render_to_string('invoice_sai.html', {'invoices': invoices, 'total_price': total_price})
    
    # Create the email message
    subject = 'Your Invoice'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user.email
    
    email = EmailMultiAlternatives(subject, '', from_email, [to_email])
    
    # Attach the HTML content as alternative content
    email.attach_alternative(html_content, 'text/html')
    
    # Send the email
    email.send()
    
    # Return the rendered invoice template
    return render(request, 'invoice_sai.html', {'invoices': invoices, 'total_price': total_price})





from django.shortcuts import redirect

@login_required(login_url='signin')
def mark_invoices_paid(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    invoices = Invoice.objects.filter(lodge__user=user)

    # Mark invoices as paid
    for invoice in invoices:
        invoice.paid = True
        invoice.save()
        # You can also mark the associated lodge as paid if needed
        invoice.lodge.check_out = True
        invoice.lodge.save()

    # Redirect back to the invoice list
    return redirect('generate_invoice', user_id=user_id)


from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse

@login_required
def send_invoice_email(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    # Render the invoice template to HTML string
    html_content = render_to_string('invoice_sai.html', {'invoice': invoice})
    
    # Create the email message
    subject = 'Invoice'
    body = 'Please find attached the invoice for your booking.'
    from_email = 'your_email@example.com'
    to_email = invoice.lodge.user.email
    
    email = EmailMultiAlternatives(subject, body, from_email, [to_email])
    
    # Attach the HTML content as alternative content
    email.attach_alternative(html_content, 'text/html')
    
    # Send the email
    email.send()
    
    # Return a response to indicate the email has been sent
    return HttpResponse('Invoice sent successfully')



    
    

def all_bookings(request):
    bookings = Lodge.objects.all()
    return render(request, 'bookings_sai.html', {'bookings': bookings})