from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from cinystore import settings
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from cinystoreapp.tokens import generate_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from cinystoreapp.models import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.views import View
import random
import http.client
from django.conf import settings


def index(request):
    return render(request, 'corporateHome.html')



def send_otp(number, otp):
    print("FUNCTION CALLED")
    conn = http.client.HTTPSConnection("api.msg91.com")
    authkey = settings.AUTH_KEY
    headers = { 'content-type': "application/json" }
    senderid = 'cinystore'
    templateid = '6583eebdd6fc0518e471ba43'
    
    url = "https://control.msg91.com/api/v5/otp?template_id="+templateid+"&mobile="+number+"&otp="+otp+"&sender="+senderid+"&authkey="+authkey+"&country=91"
    # url = "http://api.msg91.com/api/sendotp.php?otp="+otp+"&message="+"Your%20otp%20is%20"+otp +"&sender="+senderid+"&mobile="+number+"&authkey="+authkey+"&country=91"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data)
    return None


# def login_attempt(request):
#     if request.method == 'POST':
#         number = request.POST.get('phone_number')
#         user = PhoneNumber.objects.filter(number=number).first()
#         if user is None:
#             context = {'message': 'User not found', 'class': 'danger'}
#             return render(request, 'Business.html', context)

#         otp = str(random.randint(1000, 9999))
#         user.otp = otp
#         user.save()
#         send_otp(mobile, otp)
#         request.session['mobile'] = mobile
#         return redirect('login_otp')
#     return render(request, 'Business.html')


# def login_otp(request):
#     number = request.session['phone_number']
#    
#  context = {'number': number}
#     if request.method == 'POST':
#         otp = request.POST.get('otp')
#         profile = PhoneNumber.objects.filter(number=number).first()

#         if otp == profile.otp:
#             user = User.objects.get(id=profile.user.id)
#             login(request, user)
#             return redirect('producer_dashboard')
#         else:
#             context = {'message': 'Wrong OTP', 'class': 'danger', 'number': number}
#             return render(request, 'login_otp.html', context)

#     return render(request, 'login_otp.html', context)




def otp_page(request):
    number = request.session['number']
    context = {'number': number}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = PhoneNumber.objects.filter(number=number).first()
        if otp == profile.otp:
            return redirect('select_page')
        else:
            print('Wrong')
            context = {'message': 'Wrong OTP', 'class': 'danger', 'number': number}
            return render(request, 'otpPage.html', context)

    return render(request, 'otpPage.html', context)


def register_page(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        number = request.POST['phone_number']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('register_page')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('register_page')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 characters!!")
            return redirect('register_page')

        if password != confirm_password:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('register_page')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('register_page')
        if not number:
            messages.error(request, "Please enter your phone number!")
            return redirect('register_page')
        if not number.isdigit():
            messages.error(request, "Please enter a valid phone number!")
            return redirect('register_page')
        if len(number) != 10 and not number.startswith('+'):
            messages.error(request, "Please enter a valid phone number!")
            return redirect('register_page')
        if len(number) == 10:
            phone_number = '+91' + number  # Add the country code if it's not present
            if PhoneNumber.objects.filter(number=phone_number).exists():
                messages.error(request, "User already exists with this phone number!")
                return redirect('register_page')

        myuser = User.objects.create_user(username=username, email=email, password=password)
        phone_number = PhoneNumber.objects.create(number=number, email=email)
        myuser.phone_numbers.add(phone_number)
        myuser.is_producer = True
        myuser.is_active = False
        myuser.save()
        customer = ProducerRegister.objects.create(producer=myuser,
                                                   producer_email = email,
                                                   producer_phone_number = number,
                                                   production_house=username)
        customer.save()
        otp = str(random.randint(1000, 9999))
        phone_number.otp = otp
        phone_number.save()
        send_otp(number, otp)
        request.session['number'] = number
        return redirect('welcome_page')
    return render(request, "registerPage.html")



def activate1(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        myproducer = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, myproducer.DoesNotExist):
        myproducer = None

    if myproducer is not None and generate_token.check_token(myproducer, token):
        myproducer.is_active = True
        myproducer.save()
        login(request, myproducer)
        return render(request, "producer_activation_success.html")
    else:
        return render(request, 'producer_activation_failed.html')


def producer_activation_success(request):
    return render(request, 'producer_activation_success.html')


def Business(request):
    if request.method == 'POST':
        username = request.POST['production_house']
        producer_password = request.POST['producer_password']
        try:
            users = User.objects.get(Q(username=username) | Q(email=username))
            myproducer = authenticate(request, username = users, password=producer_password)
        except:
            messages.error(request, "User Does not exist, Please Register")
            return redirect('Business')
        if myproducer is not None:
            login(request, myproducer)
            producer_info = ProducerRegister.objects.get(producer = myproducer)
            producer_first_name = producer_info.producer_first_name
            return redirect(f'/producerdashboard/{producer_info.production_house}/')
        else:
            messages.error(request, "Invalid Credentials!!")
            return redirect('Business')
    return render(request, "Business.html")


def Producerlogoutpage(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('Business')


def select_page(request):
    if request.method == 'POST':
        selected_label = request.POST.get('label')
        if selected_label == 'individual':
            return redirect('Individual_page')
        elif selected_label == 'corporate':
            return redirect('corporate_page')
        elif selected_label == 'ott':
            return redirect('ott_page')
        elif selected_label == 'agency':
            return redirect('agency_page')
    return render(request, 'selectPage.html')

def welcome_page(request):
    template = loader.get_template('welcomePage.html')
    context = {
        'welcome_page': welcome_page,
    }
    return HttpResponse(template.render(context, request))


def businessBase(request):
    template = loader.get_template('businessBase.html')
    context = {
        'businessBase': businessBase,
    }
    return HttpResponse(template.render(context, request))


def corporateBase(request):
    template = loader.get_template('corporateBase.html')
    context = {
        'corporateBase': corporateBase,
    }
    return HttpResponse(template.render(context, request))


def corporateHome(request):
    template = loader.get_template('corporateHome.html')
    context = {
        'corporateHome': corporateHome,
    }
    return HttpResponse(template.render(context, request))


def Individual_page(request):
    if request.method == "POST":
        user = request.user
        username = user.username
        email = user.email
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        production_house = request.POST['production_house']
        website = request.POST['website']
        country_name = request.POST['country_name']
        state = request.POST['state']
        city = request.POST['city']
        company_brief = request.POST['company_brief']


        # Create a CorporateRegister instance and save it
        individual_user = IndividualRegister(
            producer=user,
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            production_house=production_house,
            website=website,
            country_name=country_name,
            state=state,
            city=city,
            company_brief=company_brief,
            is_active=True  # Set to True by default, you can modify this based on your requirements
        )
        individual_user.save()
        return redirect('business')

    return render(request, 'IndividualPage.html')




def corporate_page(request):
    if request.method == "POST":
        user = request.user
        username = user.username
        email = user.email
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        production_house = request.POST['production_house']
        website = request.POST['website']
        country_name = request.POST['country_name']
        state = request.POST['state']
        city = request.POST['city']
        company_brief = request.POST['company_brief']


        # Create a CorporateRegister instance and save it
        corporate_user = CorporateRegister(
            producer=user,
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            production_house=production_house,
            website=website,
            country_name=country_name,
            state=state,
            city=city,
            company_brief=company_brief,
            is_active=True  # Set to True by default, you can modify this based on your requirements
        )
        corporate_user.save()

        return redirect('business')

    return render(request, 'corporatePage.html')



def ott_page(request):
    if request.method == "POST":
        user = request.user
        username = user.username
        email = user.email
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        production_house = request.POST['production_house']
        website = request.POST['website']
        country_name = request.POST['country_name']
        state = request.POST['state']
        city = request.POST['city']
        company_brief = request.POST['company_brief']


        # Create a CorporateRegister instance and save it
        ott_user = OttRegister(
            producer=user,
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            production_house=production_house,
            website=website,
            country_name=country_name,
            state=state,
            city=city,
            company_brief=company_brief,
            is_active=True  # Set to True by default, you can modify this based on your requirements
        )
        ott_user.save()

        return redirect('business')

    return render(request, 'OttPage.html')


def agency_page(request):
    if request.method == "POST":
        user = request.user
        username = user.username
        email = user.email
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        production_house = request.POST['production_house']
        website = request.POST['website']
        country_name = request.POST['country_name']
        state = request.POST['state']
        city = request.POST['city']
        company_brief = request.POST['company_brief']

        # Create a CorporateRegister instance and save it
        agency_user = AgencyRegister(
            producer=user,
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            production_house=production_house,
            website=website,
            country_name=country_name,
            state=state,
            city=city,
            company_brief=company_brief,
            is_active=True  # Set to True by default, you can modify this based on your requirements
        )
        agency_user.save()
        return redirect('business')

    return render(request, 'Agency_Page.html')












