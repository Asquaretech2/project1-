from django.http import HttpResponse
from django.template import loader
from .forms import ContactForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url


def index(request):
    template = loader.get_template('index.html')
    context = {
        'index': index,
    }
    return HttpResponse(template.render(context, request))



def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            # Validate captcha
            captcha_id = request.POST.get('captcha_0', '')
            captcha_response = request.POST.get('captcha_1', '')

            if not CaptchaStore.objects.filter(id=captcha_id, response=captcha_response).exists():
                return HttpResponse("Incorrect captcha. Please try again.")
            form.save()  # This saves the form data to the database. Send an email to the company
            subject = 'Contact Form Submission'
            message = f"Name: {form.cleaned_data['Name']}\nEmail: {form.cleaned_data['Email']}\nSubject: {form.cleaned_data['Subject']}\nMessage: {form.cleaned_data['Message']}"
            from_email = 'settings.EMAIL_HOST_USER'
            recipient_list = ['varun.agarwal@cinystore.com']

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return redirect('contact')  # Redirect to a success page
    else:
        form = ContactForm()
    return render(request, 'contactPage.html', {'form': form})



def creator(request):
    template = loader.get_template('creatorPage.html')
    context = {
        'creator': creator,
    }
    return HttpResponse(template.render(context, request))


def faq(request):
    template = loader.get_template('faq.html')
    context = {
        'faq': faq,
    }
    return HttpResponse(template.render(context, request))


def index(request):
    return render(request, 'corporateHome.html')

def Privacy(request):
    template = loader.get_template('Privacy.html')
    context = {
        'Privacy': Privacy,
    }
    return HttpResponse(template.render(context, request))


def reviews(request):
    template = loader.get_template('reviewsPage.html')
    context = {
        'reviews': reviews,
    }
    return HttpResponse(template.render(context, request))


def terms(request):
    template = loader.get_template('terms.html')
    context = {
        'terms': terms,
    }
    return HttpResponse(template.render(context, request))










