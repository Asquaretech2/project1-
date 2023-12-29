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
from django.conf import settings
import random
import http.client



def marketing_dashboard(request):
    template = loader.get_template('marketing_dashboard.html')
    context = {
        'marketing_dashboard': marketing_dashboard,
    }
    return HttpResponse(template.render(context, request))



def market_signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        number = request.POST['phone_number']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('market_signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('market_signup')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 characters!!")
            return redirect('market_signup')

        if password != confirm_password:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('market_signup')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('market_signup')
        if not number:
            messages.error(request, "Please enter your phone number!")
            return redirect('market_signup')
        if not number.isdigit():
            messages.error(request, "Please enter a valid phone number!")
            return redirect('market_signup')
        if len(number) != 10 and not number.startswith('+'):
            messages.error(request, "Please enter a valid phone number!")
            return redirect('market_signup')
        if len(number) == 10:
            phone_number = '+91' + number  # Add the country code if it's not present
            if PhoneNumber.objects.filter(number=phone_number).exists():
                messages.error(request, "User already exists with this phone number!")
                return redirect('market_signup')

        myuser = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        phone_number = PhoneNumber.objects.create(number=number, email=email)
        myuser.phone_numbers.add(phone_number)
        myuser.is_marketing = True
        myuser.is_active = False
        myuser.save()
        marketing = MarketingRegister.objects.create(marketing=myuser,
                                                   email = email,
                                                   phone_number = number,
                                                   username=username, 
                                                   first_name=first_name, 
                                                   last_name=last_name)
        marketing.save()
        messages.success(request,
                         "Your Account has been created successfully!! Please check your email to confirm your email address in order to activate your account.")

        # Welcome Email
        subject = "Welcome to Cinystore Marketing Login!!"
        message = "Hello " + myuser.username + "!! \n" + "Welcome to Cinystore!! \nThank you for being a member of marketing team of our website.\n We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\n Team Cinystore !! \n"


        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        uid = urlsafe_base64_encode(force_bytes(myuser.pk))
        print(uid)

        token = generate_token.make_token(myuser)
        print(token)

        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ Cinystore Marketing Login!!"
        message2 = render_to_string('marketing_account_email_confirmation.html', {

            'name': myuser.username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        # Construct the local file path to the logo image
        logo_path = os.path.join(settings.BASE_DIR, 'cinystoreapp', 'static', 'img', 'logo.webp')

        # Attach the company logo
        with open(logo_path, "rb") as logo_file:
            logo_data = logo_file.read()
            email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [myuser.email])
            email.attach('logo.webp', logo_data, 'image/webp')  # Adjust the content type if needed
            email.send()

        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()
        otp = str(random.randint(1000, 9999))
        phone_number.otp = otp
        phone_number.save()
        send_otp(number, otp)
        request.session['number'] = number
        return redirect('otp')
    return render(request, "market_signup.html")



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



def otp(request):
    number = request.session['number']
    context = {'number': number}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = PhoneNumber.objects.filter(number=number).first()
        if otp == profile.otp:
            return redirect('marketing_dashboard')
        else:
            print('Wrong')
            context = {'message': 'Wrong OTP', 'class': 'danger', 'number': number}
            return render(request, 'market_otp.html', context)

    return render(request, 'market_otp.html', context)

def activate2(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        mymarketing = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, mymarketing.DoesNotExist):
        mymarketing = None

    if mymarketing is not None and generate_token.check_token(mymarketing, token):
        mymarketing.is_active = True
        mymarketing.save()
        login(request, mymarketing)
        return render(request, "marketing_account_activation_success.html")
    else:
        return render(request, 'marketing_account_activation_failed.html')
    

def marketing_account_activation_success(request):
    return render(request, 'marketing_account_activation_success.html')

     
# Create your views here.
def market_Logout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('market_login')


def market_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('marketing_dashboard')  # Redirect to the home page after successful login
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('market_login')
     
    return render(request, "market_login.html")  # Render the login template

