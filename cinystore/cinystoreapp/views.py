from configparser import ConfigParser
import imp
from django.http import HttpResponse,Http404
from django.template import loader
import mysql.connector as sql
from django.views.generic import ListView, CreateView
from .forms import *
import mysql.connector
from .models import Movie, PostText1, Review, CreateLabel, Blog, LikeMovies, FollowMovies,  LikePostText1, FollowPostText1
from .models import *
from django.db.models import Q
import requests
from itertools import chain
from operator import attrgetter
# from django.contrib.auth.models import User
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from cinystore import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
#from django.utils.encoding import force_bytes, force_text
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from .decorators import user_required, producer_required
from io import BytesIO
from email.mime.image import MIMEImage
from django.db.models import Sum

db = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="root",
  database="cinystore"
)
cursor = db.cursor()


def tmdb_movies(request):
    # Define your API key and base URL
    api_key = '9456c6fdcf8a04e157e45387ebf0c687'
    base_url = 'https://api.themoviedb.org/3'

    # Make the API request to fetch popular movies
    url = f'{base_url}/movie/popular'
    params = {'api_key': api_key}
    response = requests.get(url, params=params)
    data = response.json()

    # Iterate through the fetched movie data
    for movie_data in data['results']:

        if not Movie.objects.filter(movie_title=movie_data['title']).exists():
            # Fetch detailed movie information, including credits
            movie_info_response = requests.get(f'{base_url}/movie/{movie_data["id"]}', params=params)
            movie_info = movie_info_response.json()
            credits_response = requests.get(f'{base_url}/movie/{movie_data["id"]}/credits', params=params)
            credits = credits_response.json()
            videos_response = requests.get(f'{base_url}/movie/{movie_data["id"]}/videos', params=params)
            videos_data = videos_response.json()
            videos = videos_data.get('results', [])
            
            # Filter and store only the key of the official trailer
            official_trailer_keys = [video['key'] for video in videos if video.get('type') in ['Trailer', 'Teaser']]

            # Extract specific information from the movie_info dictionary
            director = [crew['name'] for crew in credits.get('crew', []) if crew['job'] == 'Director']
            cast = [actor['name'] for actor in credits.get('cast', [])]
            music_director = [crew['name'] for crew in credits.get('crew', []) if crew['job'] == 'Music']
            production_companies = [company['name'] for company in movie_info.get('production_companies', [])]
            # Create a Movie object and save it to the database
            movie = Movie(
                id=movie_data['id'],
                movie_title=movie_data['title'],
                overview=movie_data['overview'],
                release_date=movie_data['release_date'],
                poster_path=movie_data['poster_path'],
                producer=','.join(production_companies),
                language=movie_data['original_language'],
                genre=','.join([genre['name'] for genre in movie_info.get('genres', [])]),
                video=official_trailer_keys[0] if official_trailer_keys else '',
                cast=','.join(cast),
                crew=','.join(director + music_director),
                director=','.join(director),
                music_director=','.join(music_director),
                # Add other fields as needed
            )
            movie.save()
    return HttpResponse('Imported movies successfully')
    # You can also render a template if needed
    # return render(request, 'movie.html', {'movies': movies})


def top_rated(request):
    # Define your API key and base URL
    api_key = '9456c6fdcf8a04e157e45387ebf0c687'
    base_url = 'https://api.themoviedb.org/3'

    # Make the API request to fetch popular movies
    url = f'{base_url}/movie/top_rated'
    params = {'api_key': api_key}
    response = requests.get(url, params=params)
    data = response.json()

    # Iterate through the fetched movie data
    for movie_data in data['results']:

        if not TopRatedMovies.objects.filter(movie_title=movie_data['title']).exists():
            # Fetch detailed movie information, including credits
            movie_info_response = requests.get(f'{base_url}/movie/{movie_data["id"]}', params=params)
            movie_info = movie_info_response.json()
            credits_response = requests.get(f'{base_url}/movie/{movie_data["id"]}/credits', params=params)
            credits = credits_response.json()
            videos_response = requests.get(f'{base_url}/movie/{movie_data["id"]}/videos', params=params)
            videos_data = videos_response.json()
            videos = videos_data.get('results', [])
             # Filter and store only the key of the official trailer
            official_trailer_keys = [video['key'] for video in videos if video.get('type') in ['Trailer', 'Teaser']]

            # Extract specific information from the movie_info dictionary
            director = [crew['name'] for crew in credits.get('crew', []) if crew['job'] == 'Director']
            cast = [actor['name'] for actor in credits.get('cast', [])]
            music_director = [crew['name'] for crew in credits.get('crew', []) if crew['job'] == 'Music']
            production_companies = [company['name'] for company in movie_info.get('production_companies', [])]
            # Create a Movie object and save it to the database
            movie = TopRatedMovies(
                id=movie_data['id'],
                movie_title=movie_data['title'],
                overview=movie_data['overview'],
                release_date=movie_data['release_date'],
                poster_path=movie_data['poster_path'],
                producer=','.join(production_companies),
                language=movie_data['original_language'],
                genre=','.join([genre['name'] for genre in movie_info.get('genres', [])]),
                video=official_trailer_keys[0] if official_trailer_keys else '',
                cast=','.join(cast),
                crew=','.join(director + music_director),
                director=','.join(director),
                music_director=','.join(music_director),
                # Add other fields as needed
            )
            movie.save()
    return HttpResponse('Imported movies successfully')
    # You can also render a template if needed
    # return render(request, 'movie.html', {'movies': movies})


def now_playing(request):
    # Define your API key and base URL
    api_key = '9456c6fdcf8a04e157e45387ebf0c687'
    base_url = 'https://api.themoviedb.org/3'

    # Make the API request to fetch popular movies
    url = f'{base_url}/movie/now_playing'
    params = {'api_key': api_key}
    response = requests.get(url, params=params)
    data = response.json()

    # Iterate through the fetched movie data
    for movie_data in data['results']:

        if not RecentMovies.objects.filter(movie_title=movie_data['title']).exists():
            # Fetch detailed movie information, including credits
            movie_info_response = requests.get(f'{base_url}/movie/{movie_data["id"]}', params=params)
            movie_info = movie_info_response.json()
            credits_response = requests.get(f'{base_url}/movie/{movie_data["id"]}/credits', params=params)
            credits = credits_response.json()
            videos_response = requests.get(f'{base_url}/movie/{movie_data["id"]}/videos', params=params)
            videos_data = videos_response.json()
            videos = videos_data.get('results', [])
             # Filter and store only the key of the official trailer
            official_trailer_keys = [video['key'] for video in videos if video.get('type') in ['Trailer', 'Teaser']]

            # Extract specific information from the movie_info dictionary
            director = [crew['name'] for crew in credits.get('crew', []) if crew['job'] == 'Director']
            cast = [actor['name'] for actor in credits.get('cast', [])]
            music_director = [crew['name'] for crew in credits.get('crew', []) if crew['job'] == 'Music']
            production_companies = [company['name'] for company in movie_info.get('production_companies', [])]
            # Create a Movie object and save it to the database
            movie = RecentMovies(
                id=movie_data['id'],
                movie_title=movie_data['title'],
                overview=movie_data['overview'],
                release_date=movie_data['release_date'],
                poster_path=movie_data['poster_path'],
                producer=','.join(production_companies),
                language=movie_data['original_language'],
                genre=','.join([genre['name'] for genre in movie_info.get('genres', [])]),
                video=official_trailer_keys[0] if official_trailer_keys else '',
                cast=','.join(cast),
                crew=','.join(director + music_director),
                director=','.join(director),
                music_director=','.join(music_director),
                # Add other fields as needed
            )
            movie.save()
    return HttpResponse('Imported movies successfully')
    # You can also render a template if needed
    # return render(request, 'movie.html', {'movies': movies})


def index(request):
    mydata = CreateLabel.objects.all().order_by('-timestamp_field')
    template = loader.get_template('index.html')
    context = {
        'mydata': mydata,
    }
    return HttpResponse(template.render(context, request))

def notification(request):
    mydata = CreateLabel.objects.all().order_by('-timestamp_field')
    template = loader.get_template('notification.html')
    context = {
        'mydata': mydata,
    }
    return HttpResponse(template.render(context, request))



def publicfeed(request):
    mydata = CreateLabel.objects.all().order_by('-timestamp_field')
    mydata1 = Review.objects.all().order_by('-timestamp_field')
    movies = Movie.objects.all().order_by('-timestamp_field')
    mydata3 = PostText1.objects.all().order_by('-timestamp_field')
    mydata2 = Clips.objects.all().order_by('-timestamp_field')

    try:
        movies = Movie.objects.all().order_by('-timestamp_field')
    except Movie.DoesNotExist:
        movies = []
    try:
        mydata = CreateLabel.objects.all().order_by('-timestamp_field')
    except CreateLabel.DoesNotExist:
        mydata = []
    try:
        mydata1 = Review.objects.all().order_by('-timestamp_field')
    except Review.DoesNotExist:
        mydata1 = []
    try:
        mydata3 = PostText1.objects.all().order_by('-timestamp_field')
    except PostText1.DoesNotExist:
        mydata3 = []

    try:
        mydata2 = Clips.objects.all().order_by('-timestamp_field')
    except Clips.DoesNotExist:
        mydata2 = []

    Publicfeed = sorted(list(mydata) + list(movies) + list(mydata1) + list(mydata3) + list(mydata2),
                        key=lambda x: x.timestamp_field, reverse=True
                        )
    producerDetails = ProducerRegister.objects.all()

    context = {'Publicfeed': Publicfeed,'producerDetails':producerDetails}

    return render(request, 'publicfeed.html', context)

def Masonry(request):
    mydata = CreateLabel.objects.all()
    template = loader.get_template('Masonry.html')
    context = {
        'Masonry': mydata,
    }
    return HttpResponse(template.render(context, request))

def StickySidebars(request):
    mydata = CreateLabel.objects.all()
    template = loader.get_template('StickySidebars.html')
    context = {
        'StickySidebars': mydata,
    }
    return HttpResponse(template.render(context, request))

# Create your views here.
def auth_Logout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('auth_login')


def auth_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Feedpage')  # Redirect to the home page after successful login
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('auth_login')
     
    return render(request, "auth_login.html")  # Render the login template


def Authregister(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('Authregister')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('Authregister')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('Authregister')

        if password != confirm_password:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('Authregister')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('Authregister')

        myuser = User.objects.create_user(username=username, email=email, password=password)
        myuser.is_user = True
        myuser.is_active = False
        myuser.save()
        customer = UserInfo.objects.create(user=myuser)
        customer.username = username
        customer.email= email
        customer.save()
        messages.success(request,
                         "Your Account has been created successfully!! Please check your email to confirm your email address in order to activate your account.")

        # Welcome Email
        subject = "Welcome to Cinystore Login!!"
        message = "Hello " + myuser.username + "!! \n" + "Welcome to Cinystore!! \nThank you for visiting our website.\n We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\n Cinystore !! \n"


        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        uid = urlsafe_base64_encode(force_bytes(myuser.pk))
        print(uid)

        token = generate_token.make_token(myuser)
        print(token)

        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ Cinystore Login!!"
        message2 = render_to_string('email_confirmation.html', {

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

        return redirect('auth_login')

    return render(request, "Authregister.html")


def activate(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return render(request, 'activation_success.html')
        return redirect('auth_login')
    else:
        return render(request, 'activation_failed.html')

def activation_success(request):
    return render(request, 'activation_success.html')


def error_view(request):
    # Custom logic for handling the error
    return render(request, 'error.html')

def Browsemovies(request):
    template = loader.get_template('Browsemovies.html')
    class Browsemovies(ListView):
        Movie_name = ""
        synopsis = ""
        Production_house = ""
        Poster = ""

    mydata = CreateLabel.objects.all().order_by('-timestamp_field')
    # api_key = "9456c6fdcf8a04e157e45387ebf0c687"
    # url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}"
    # response = requests.get(url)
    # movies = response.json()["results"]
    movies = Movie.objects.all().order_by('-timestamp_field')
    context = {'mydata': mydata, 'movies': movies}
    Browsemovies = list(chain(mydata, movies))

    return render(request, 'Browsemovies.html', context)


@login_required(login_url='/auth_login/')
@user_required
def Browsemovies_login(request):
    template = loader.get_template('Browsemovies_login.html')
    class Browsemovies(ListView):
        Movie_name = ""
        synopsis = ""
        Production_house = ""
        Poster = ""

    mydata = CreateLabel.objects.all().order_by('-timestamp_field')
    # api_key = "9456c6fdcf8a04e157e45387ebf0c687"
    # url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}"
    # response = requests.get(url)
    # movies = response.json()["results"]
    movies = Movie.objects.all().order_by('-timestamp_field')
    context = {'mydata': mydata, 'movies': movies}
    Browsemovies_login = list(chain(mydata, movies))

    return render(request, 'Browsemovies_login.html', context)




def CalendarAndEvents(request):
    mydata = CreateLabel.objects.all()
    template = loader.get_template('CalendarAndEvents.html')
    context = {
        'CalendarAndEvents':mydata,
    }
    return HttpResponse(template.render(context, request))


def ChangePassword(request):
    template = loader.get_template('ChangePassword.html')
    context = {
        'ChangePassword':ChangePassword,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/auth_login/')
@user_required
def Feedpage(request):

    '''
    This code is to get user Information and pass it in "head.html as dictionary {'head': userdata}
    
    '''
    username = request.user.username
    # Retrieve a queryset of records with the desired username
    matching_records = UserInfo.objects.filter(username=username)
    # Check if any records with the desired username exist
    username_exists = matching_records.exists()

    if username_exists:
        userdata = UserInfo.objects.filter(username=username)
    else:
        userdata = User.objects.filter(username=username)

    ## user information storing ends here 
	

    mydata = CreateLabel.objects.filter ().order_by('-timestamp_field')
    mydata1 = Review.objects.all().order_by('-timestamp_field')
    movies = Movie.objects.all().order_by('-timestamp_field')
    recent_movies = RecentMovies.objects.all().order_by('-timestamp_field')
    top_rated_movies = TopRatedMovies.objects.all().order_by('-timestamp_field')
    mydata2 = Clips.objects.all().order_by('-timestamp_field')
    
    try:
        movies = Movie.objects.all().order_by('-timestamp_field')
    except Movie.DoesNotExist:
        movies =[]
    try:
        mydata1 = Review.objects.all().order_by('-timestamp_field')
    except Review.DoesNotExist:
        mydata1 =[]
    try:
        mydata3 = PostText1.objects.all().order_by('-timestamp_field')
    except PostText1.DoesNotExist:
        mydata3 =[]
    try:
        recent_movies = RecentMovies.objects.all().order_by('-timestamp_field')
    except RecentMovies.DoesNotExist:
        recent_movies = []
    try:
        top_rated_movies = TopRatedMovies.objects.all().order_by('-timestamp_field')
    except TopRatedMovies.DoesNotExist:
        top_rated_movies = []
    try:
        mydata2 = Clips.objects.all().order_by('-timestamp_field')
    except Clips.DoesNotExist:
        mydata2 = []

    
    producerDetails = ProducerRegister.objects.all()

    combined_data = sorted(list(mydata) +list(movies) +list(mydata1) +list(mydata2) +list(mydata3) +list(recent_movies) +list(top_rated_movies), 
    key=lambda x: x.timestamp_field, reverse=True
    )

    context = {'combined_data': combined_data, 'head': userdata, 'producerDetails': producerDetails}

    return render(request, 'Feedpage.html', context)

@login_required(login_url='/Business/')
@producer_required
def Createlabel(request):
    if request.method == 'POST':
        producer_name = request.user
        producer = ProducerRegister.objects.get(production_house=producer_name)
        production_house = ProducerRegister.objects.get(production_house=producer_name).production_house
        producer_logo = ProducerRegister.objects.get(production_house=producer_name).production_house_image

        if User.objects.filter(username=producer_name).exists():
            form = ImageForm(request.POST, request.FILES)    
            producer = ProducerRegister.objects.get(production_house=producer_name)
            if form.is_valid():
                form.save()
                Movie_name=form.cleaned_data['Movie_name']
                CreateLabel.objects.filter(Movie_name = Movie_name).update(producer_id=producer)
                CreateLabel.objects.filter(Movie_name = Movie_name).update(source=production_house)
                CreateLabel.objects.filter(Movie_name = Movie_name).update(logo=producer_logo)
                
                return redirect('producerdashboard')
            else:
                img_obj = form.instance
                return render(request, 'Createlabel.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()
    return render(request, 'Createlabel.html', {'form': form})


@login_required(login_url='/auth_login/')
@user_required
def Groups(request):
    
    '''
    This code is to get user Information and pass it in "head.html as dictionary {'head': userdata}
    
    '''
    username = request.user.username
    # Retrieve a queryset of records with the desired username
    matching_records = UserInfo.objects.filter(username=username)
    # Check if any records with the desired username exist
    username_exists = matching_records.exists()

    if username_exists:
        userdata = UserInfo.objects.filter(username=username)
    else:
        userdata = User.objects.filter(username=username)

    ## user information storing ends here 
	

    template = loader.get_template('Groups.html')
    context = {'Groups': Groups,'head': userdata }
    return HttpResponse(template.render(context, request))


def genreviews(request):
    mydata = Review.objects.all()
    template = loader.get_template('genreviews.html')
    context = {
        'genreviews': mydata,
    }
    return HttpResponse(template.render(context, request))
    
@login_required(login_url='/auth_login/')
@user_required
def userreviews(request):
  
    '''
    This code is to get user Information and pass it in "head.html as dictionary {'head': userdata}
    
    '''
    username = request.user.username
    # Retrieve a queryset of records with the desired username
    matching_records = UserInfo.objects.filter(username=username)
    # Check if any records with the desired username exist
    username_exists = matching_records.exists()

    if username_exists:
        userdata = UserInfo.objects.filter(username=username)
    else:
        userdata = User.objects.filter(username=username)

    ## user information storing ends here 
    
    mydata = Review.objects.all()
    template = loader.get_template('userreviews.html')
    context = {
        'userreviews': mydata,'head': userdata
    }
    return HttpResponse(template.render(context, request))

def head(request):
    mydata = User.objects.all()
    template = loader.get_template('head.html')
    context = {
        'head': mydata,
    }
    return HttpResponse(template.render(context, request))


def generalblogs(request):
    template = loader.get_template('generalblogs.html')
    context = {
        'generalblogs': generalblogs,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/auth_login/')
@user_required
def MoviePhotos(request):
    mydata = CreateLabel.objects.all()
    template = loader.get_template('MoviePhotos.html')
    context = {
        'MoviePhotos': mydata,
    }
    return HttpResponse(template.render(context, request))


def Poster(request):
    if request.method =='POST':
        form = MoviePhotosForm(request.POST, request.FILES)
        if form .is_valid():
            form.save()
            return redirect('Createlabel')
        else:
              form = MoviePhotosForm()
        return render(request, 'MoviePhotos.html', {'form':form})

@login_required(login_url='/auth_login/')
@user_required
def MovieVideos(request):
    template = loader.get_template('MovieVideos.html')
    context = {
        'MovieVideos': MovieVideos,
    }
    return HttpResponse(template.render(context, request))


def PostText(request):
    if request.method == 'POST':
        form = PostTextForm(request.POST, request.FILES)
        production_house_name = request.user
        print('production house name', production_house_name)
        producer = ProducerRegister.objects.get(production_house=production_house_name)
        production_house = ProducerRegister.objects.get(production_house=production_house_name).production_house
        producer_logo = ProducerRegister.objects.get(production_house=production_house_name).production_house_image
        # list of movies produced by the production house
        movies = CreateLabel.objects.filter(producer_id=producer)
        movie_list = [movie.Movie_name for movie in movies]    
        print(movie_list, 'movie names', production_house_name, 'production house name')

        # if the movie name is not in the list of movies produced by the production house
        # then return an error message and if the movie name is in the list of movies produced by the production house
        # then save the form and update the production house name
        if form.is_valid():
            Movie_name = form.cleaned_data['Movie_name']
            # Check if the movie exists in CreateLabel database
            if CreateLabel.objects.filter(Movie_name=Movie_name).exists() and Movie_name in movie_list:
                form.save()  # Save the post if the movie exists
                PostText1.objects.filter(Movie_name = Movie_name).update(source=production_house)
                PostText1.objects.filter(Movie_name = Movie_name).update(logo=producer_logo)
                return redirect('PostText')  # Redirect to a success view
            elif Movie_name not in movie_list:
                messages.error(request, "You have not produced this movie!!")
                print('error occured while posting text')
                return redirect('PostText')
            else:
                messages.error(request, "Create A Label For The Movie To Post!")
                return render(request, 'PostText.html', {'form': form, 'message': messages.error})
    return render(request, 'PostText.html')


def PostTextView(request):
    mydata = PostText1.objects.all()
    template = loader.get_template('PostTextView.html')
    context = {
        'PostTextView': mydata,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/auth_login/')
@user_required
def Newsfeed(request):
    mydata = Movie.objects.all()
    template = loader.get_template('Newsfeed.html')
    context = {
        'Newsfeed': mydata,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/auth_login/')
@user_required
def producerphotoupload(request):
    template = loader.get_template('producerphotoupload.html')
    context = {
        'producerphotoupload': producerphotoupload,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/auth_login/')
@user_required
def producervideoupload(request):
    template = loader.get_template('producervideoupload.html')
    context = {
        'producervideoupload': producervideoupload,
    }
    return HttpResponse(template.render(context, request))



@login_required(login_url='/auth_login/')
@user_required
def badges(request):
    '''
    This code is to get user Information and pass it in "head.html as dictionary {'head': userdata}
    
    '''
    username = request.user.username
    # Retrieve a queryset of records with the desired username
    matching_records = UserInfo.objects.filter(username=username)
    # Check if any records with the desired username exist
    username_exists = matching_records.exists()

    if username_exists:
        userdata = UserInfo.objects.filter(username=username)
    else:
        userdata = User.objects.filter(username=username)

    ## user information storing ends here 
    mydata = CreateLabel.objects.all()
    template = loader.get_template('badges.html')
    context = {
        'badges': mydata,'head': userdata
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/auth_login/')
@user_required
def music(request):
    '''
    This code is to get user Information and pass it in "head.html as dictionary {'head': userdata}
    
    '''
    username = request.user.username
    # Retrieve a queryset of records with the desired username
    matching_records = UserInfo.objects.filter(username=username)
    # Check if any records with the desired username exist
    username_exists = matching_records.exists()

    if username_exists:
        userdata = UserInfo.objects.filter(username=username)
    else:
        userdata = User.objects.filter(username=username)

    ## user information storing ends here 
    mydata = CreateLabel.objects.all()
    template = loader.get_template('music.html')
    context = {
        'music': mydata,'head': userdata
    }
    return HttpResponse(template.render(context, request))




def Producerregisterpage(request):
    if request.method == "POST":
        production_house_image = request.POST['production_house_image']
        producer_first_name = request.POST['producer_first_name']
        producer_last_name = request.POST['producer_last_name']
        producer_password = request.POST['producer_password']
        producer_confirm_password = request.POST['producer_confirm_password']
        producer_email = request.POST['producer_email']
        production_house = request.POST['production_house']
        producer_website = request.POST['producer_website']
        producer_phone_number = request.POST['producer_phone_number']
        producer_country_name = request.POST['producer_country_name']
        producer_state = request.POST['producer_state']
        producer_city = request.POST['producer_city']
        production_house_brief = request.POST['production_house_brief']
        producer_facebook_account = request.POST['producer_facebook_account']
        producer_twitter_account = request.POST['producer_twitter_account']
        # if ProducerRegister.objects.filter(producer_first_name=producer_first_name):
        #     messages.error(request, "first_name already exist! Please try some other first_name.")
        #     return redirect('index')

        if ProducerRegister.objects.filter(producer_email=producer_email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('Producerregisterpage')

        if len(producer_first_name) > 20:
            messages.error(request, "Producer_first_name must be under 20 charcters!!")
            return redirect('Producerregisterpage')

        if producer_password != producer_confirm_password:
            messages.error(request, "Producer password didn't matched!!")
            return redirect('Producerregisterpage')

        
        myuser = User.objects.create_user(username = production_house, email=producer_email, password=producer_password)
        myuser.is_producer = True
        myuser.is_active = False
        myuser.save()
        customer = ProducerRegister.objects.create(producer=myuser)
        customer.email= producer_email
        customer.production_house_image = production_house_image
        customer.producer_first_name=producer_first_name
        customer.producer_email=producer_email
        customer.producer_last_name = producer_last_name
        customer.producer_website = producer_website
        customer.production_house = production_house
        customer.producer_phone_number = producer_phone_number
        customer.producer_country_name = producer_country_name
        customer.producer_city = producer_city
        customer.producer_state = producer_state
        customer.production_house_brief = production_house_brief
        customer.producer_twitter_account = producer_twitter_account
        customer.producer_facebook_account = producer_facebook_account
        #user.is_active = False
        customer.save()
        messages.success(request,
                         "Your Producer Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")

        # Welcome Email
        subject = "Welcome to Cinystore Login as Producer!!"
        message = "Hello " + customer.producer_first_name + "!! \n" + "Welcome to Cinystore!! \nThank you for visiting our website.\n We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\n" + customer.producer_first_name + "!! \n"
        from_email = settings.EMAIL_HOST_USER
        to_list = [customer.producer_email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        uid = urlsafe_base64_encode(force_bytes(customer.pk))
        print(uid)

        token = generate_token.make_token(customer)
        print(token)

        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ Cinystore producer Login!!"
        message2 = render_to_string('producer_email_confirmation.html', {

            'name': customer.producer_first_name,
            'domain':  settings.SITE_URL,
            'uid': urlsafe_base64_encode(force_bytes(customer.pk)),
            'token': generate_token.make_token(customer)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [customer.producer_email],
        )
        email.fail_silently = True
        email.send()

        return redirect('Business')

    return render(request, "Producerregisterpage.html")


def activate1(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        myproducer = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, myproducer.DoesNotExist):
        myproducer = None

    if myproducer is not None and generate_token.check_token(myproducer, token):
        myproducer.is_active = True
        # user.profile.signup_confirmation = True
        myproducer.save()
        login(request, myproducer)
        #messages.success(request, "Your Account has been activated!!")
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
            #messages.success(request, "Logged In Sucessfully!!")
            return redirect(f'/producerdashboard/{producer_info.production_house}/')
        else:
            messages.error(request, "Invalid Credentials!!")
            return redirect('Business')
    return render(request, "Business.html")

def Producerlogoutpage(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('Business')


@login_required(login_url='/Business/')
@producer_required
def stats(request):
    mydata = CreateLabel.objects.all()
    template = loader.get_template('stats.html')
    context = {
        'stats': stats,
    }
    return HttpResponse(template.render(context, request))

    
@login_required(login_url='/Business/')
@producer_required
def moviestats(request, Movie_name):
    posts = PostText1.objects.filter(Movie_name=Movie_name)

    # Count all the likes for the filtered posts
    total_likes = posts.aggregate(Sum('like_count'))['like_count__sum'] or 0

    # Count all the follows for the filtered posts
    total_follows = posts.aggregate(Sum('follow_count'))['follow_count__sum'] or 0

    
    # Count all the share for the filtered posts
    total_shares = posts.aggregate(Sum('share_count'))['share_count__sum'] or 0


    # Count all the comment for the filtered posts
    total_comments = posts.aggregate(Sum('comment_count'))['comment_count__sum'] or 0

    


    mydata = CreateLabel.objects.filter(Movie_name=Movie_name)
    mydata3 = PostText1.objects.filter(Movie_name=Movie_name).order_by('-like_count')
    template = loader.get_template('moviestats.html')
    context = {
        'moviestats': mydata,
        'total_likes':total_likes,
        'total_follows':total_follows,
        'total_shares': total_shares,
        'total_comments': total_comments,
        'mydata3':mydata3,

    }
    return HttpResponse(template.render(context, request))

def corporate(request):
   template = loader.get_template('corporateHome.html')
   context = {
       'corporate': corporate,
   }
   return HttpResponse(template.render(context, request))

@login_required(login_url='/auth_login/')
@user_required
def faq(request):
    template = loader.get_template('faq.html')
    context = {
        'faq': faq,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/auth_login/')
@user_required
def career(request):
    template = loader.get_template('career.html')
    context = {
        'career': career,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/auth_login/')
@user_required
def disclaimer(request):
    template = loader.get_template('disclaimer.html')
    context = {
        'disclaimer': disclaimer,
    }
    return HttpResponse(template.render(context, request))


def Labeltmdb(request, movie_title):
    mydata = Movie.objects.filter(movie_title=movie_title)
    recent_movies = RecentMovies.objects.filter(movie_title=movie_title)
    top_rated_movies = TopRatedMovies.objects.filter(movie_title=movie_title)
    template = loader.get_template('Labeltmdb.html')
    context = {
        'Labeltmdb': {'mydata': mydata, 'recent_movies': recent_movies, 'top_rated_movies': top_rated_movies},
    }
    return HttpResponse(template.render(context, request))


def Label2(request, movie_title):
    mydata = Movie.objects.filter(movie_title=movie_title)
    template = loader.get_template('Label2.html')
    context = {
        'Label2': mydata,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/auth_login/')
@user_required
@csrf_protect
def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        myuser = request.user.username
        myuser_logo = UserInfo.objects.get(username=myuser).profilephoto
        if form.is_valid():
            form.save()
            Movie_name=form.cleaned_data['Movie_name']
            Review.objects.filter(author = myuser).update(source=myuser)
            Review.objects.filter(author = myuser).update(logo=myuser_logo)
            Review.objects.filter(Movie_name=Movie_name).update(slug=''.join(Movie_name.split(' ')))
            return render(request, 'review.html', {'form': form})
    else:
        form = ReviewForm()
    return render(request, 'review.html', {'form': form})


def review_label(request, Movie_name):
    mydata = Review.objects.filter(Movie_name=Movie_name)
    template = loader.get_template('review_label.html')
    context = {
        'review_label': mydata,
    }
    return HttpResponse(template.render(context, request))

def userreview_label(request, Movie_name):
    mydata = Review.objects.filter(Movie_name=Movie_name)
    template = loader.get_template('userreview_label.html')
    context = {
        'userreview_label': mydata,
    }
    return HttpResponse(template.render(context, request))


def Home(request): 
    template = loader.get_template('Home.html')
    mydata = CreateLabel.objects.all().order_by('-timestamp_field')
    api_key = "9456c6fdcf8a04e157e45387ebf0c687"
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}"
    response = requests.get(url)
    movies = response.json()["results"]
    movies = Movie.objects.all()
    mydata1 = Review.objects.all().values()
    mydata2 = BoxOffice.objects.all().values()

    context = {
        'mydata': mydata,
        'movies': movies,
        'mydata1': mydata1,
        'publictrailer': mydata,
        'genBox_office': mydata2,
    }
    return HttpResponse(template.render(context, request))


def Box_office_label(request, Movie_name):
    mydata = BoxOffice.objects.filter(Movie_name=Movie_name)
    template = loader.get_template('Box_office_label.html')
    context = {
        'Box_office_label': mydata,
    }
    return HttpResponse(template.render(context, request))


def genBox_office(request):
    mydata = BoxOffice.objects.all()
    template = loader.get_template('genBox_office.html')
    context = {
        'genBox_office': mydata,
    }
    return HttpResponse(template.render(context, request))


@csrf_protect
def Box_office(request):
    if request.method == 'POST':
        form = BoxOfficeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'Box_office.html', {'form': form})
    else:
        form = BoxOfficeForm()
    return render(request, 'Box_office.html', {'form': form})


@login_required(login_url='/auth_login/')
@user_required
def Indianmovies(request):
    
    '''
    This code is to get user Information and pass it in "head.html as dictionary {'head': userdata}
    
    "'''
    username = request.user.username
    # Retrieve a queryset of records with the desired username
    matching_records = UserInfo.objects.filter(username=username)
    # Check if any records with the desired username exist
    username_exists = matching_records.exists()

    if username_exists:
        userdata = UserInfo.objects.filter(username=username)
    else:
        userdata = User.objects.filter(username=username)

    ## user information storing ends here 
	
    template = loader.get_template('Indianmovies.html')
    mydata = CreateLabel.objects.all()
    context = {
        'mydata': mydata, 'head': userdata
    }
    return HttpResponse(template.render(context, request))

def Internationalmovies(request):
    template = loader.get_template('Internationalmovies.html')
    api_key = "9456c6fdcf8a04e157e45387ebf0c687"
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}"
    response = requests.get(url)
    movies = response.json()["results"]
    movies = Movie.objects.all().order_by('-timestamp_field')
    context = {
        'movies': movies,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/Business/')
@producer_required
def producerdashboardwithmovie(request, production_house):
    production_house = request.user
    template = loader.get_template('producerdashboard.html')
    producer = ProducerRegister.objects.get(production_house=production_house)
    mydata = CreateLabel.objects.filter(producer_id=producer)
    context = {
        'producerdashboard':mydata,
    }
    return HttpResponse(template.render(context, request))


def producerbase(request):
    template = loader.get_template('producerbase.html')
    context = {
        'producerbase':producerbase,
    }
    return HttpResponse(template.render(context, request))

def producerdashboard(request):
    production_house = request.user
    template = loader.get_template('producerdashboard.html')
    producer = ProducerRegister.objects.get(production_house=production_house)
    mydata = CreateLabel.objects.filter(producer_id=producer)
    context = {
        'producerdashboard':mydata,
    }
    return HttpResponse(template.render(context, request))

def producerhead(request):
    template = loader.get_template('producerhead.html')
    context = {
        'producerhead': producerhead
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/Business/')
@producer_required
def Managelabel(request):
    production_house = request.user
    template = loader.get_template('Managelabel.html')
    producer = ProducerRegister.objects.get(production_house=production_house)
    mydata = CreateLabel.objects.filter(producer_id=producer)
    context = {
        'Managelabel': mydata,
    }
    return HttpResponse(template.render(context, request))

def genblog(request):
    mydata = Blog.objects.all()
    template = loader.get_template('jason.html')
    context = {
        'genblog': mydata
    }
    return HttpResponse(template.render(context, request))

@csrf_protect
def blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'blog.html', {'form': form})
    else:
        form = BlogForm()
    return render(request, 'blog.html', {'form': form})

@login_required(login_url='/auth_login/')
@user_required
def Usertrailer(request):
    '''
    This code is to get user Information and pass it in "head.html as dictionary {'head': userdata}
    
    "'''
    username = request.user.username
    # Retrieve a queryset of records with the desired username
    matching_records = UserInfo.objects.filter(username=username)
    # Check if any records with the desired username exist
    username_exists = matching_records.exists()

    if username_exists:
        userdata = UserInfo.objects.filter(username=username)
    else:
        userdata = User.objects.filter(username=username)

    ## user information storing ends here 
	
    mydata = CreateLabel.objects.all()
    template = loader.get_template('Usertrailer.html')
    context = {
        'Usertrailer': mydata, 'head': userdata
    }
    return HttpResponse(template.render(context, request))


def web_createlabel(request):
    template = loader.get_template('web_createlabel.html')
    context = {
        'web_createlabel': web_createlabel
    }
    return HttpResponse(template.render(context, request))


def web_createlabel1(request):
    template = loader.get_template('web_createlabel1.html')
    context = {
        'web_createlabel1': web_createlabel1
    }
    return HttpResponse(template.render(context, request))

def labels(request):
    template = loader.get_template('labels.html')
    context = {
        'labels': labels
    }
    return HttpResponse(template.render(context, request))

def episodeupload(request):
    template = loader.get_template('episodeupload.html')
    context = {
        'episodeupload': episodeupload
    }
    return HttpResponse(template.render(context, request))


def episodeupload2(request):
    template = loader.get_template('episodeupload2.html')
    context = {
        'episodeupload2': episodeupload2
    }
    return HttpResponse(template.render(context, request))


def episodeupload1(request):
    template = loader.get_template('episodeupload1.html')
    context = {
        'episodeupload1': episodeupload1
    }
    return HttpResponse(template.render(context, request))

def producermanagelabel(request, Movie_name):
    mydata = CreateLabel.objects.filter(Movie_name=Movie_name)
    template = loader.get_template('producermanagelabel.html')
    context = {
        'producermanagelabel': mydata
    }
    return HttpResponse(template.render(context, request))



def templates(request, Movie_name):
    Label1 = CreateLabel.objects.filter(Movie_name=Movie_name)
    template = loader.get_template('templates.html')
    context = {
        'Label1':Label1,
    }
    return HttpResponse(template.render(context, request))


def socialuserlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "Logged In Successfully!!!")
                return redirect('Feedpage')  # Redirect to the user dashboard page after successful login
            else:
                return render(request, 'socialuserlogin.html', {'error': 'This account is inactive..'})

    return render(request, "socialuserlogin.html")

def comingsoonlabel(request):
    template = loader.get_template('comingsoonlabel.html')
    context = {
        'comingsoonlabel': comingsoonlabel,
    }
    return HttpResponse(template.render(context, request))

@csrf_protect
def Newsform(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'Newsform.html', {'form': form})
    else:
        form = NewsForm()
    return render(request, 'Newsform.html', {'form': form})

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email',False)
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print(uid)
            token = generate_token.make_token(user)
            print(token)
            current_site = get_current_site(request)
            
            #Reset Password Email

            email_subject = "Reset your Password!!"
            message3 = render_to_string('reset_password_email.html', {

                'name': user.username,
                'domain': settings.SITE_URL,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })
            email = EmailMessage(
                email_subject,
                message3,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            email.fail_silently = True
            email.send()
            messages.success(request, 'A password reset link has been sent to your email.')
            # return redirect('reset_password')
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email.')
            return redirect('reset_password')
    return render(request, 'reset_password.html')


def ResetConfirm(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=uid)
        if user is not None and generate_token.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user=user, data=request.POST)
                if form.is_valid():
                    form.save()  # Save the new password for the user
                    messages.success(request, "Password set successfully!")
                    return redirect('auth_login')
                else:
                    return redirect('reset_password')
            else:
                form = SetPasswordForm(user=user)
                args = {'form': form}
                return render(request, 'reset_password_form.html', args)
        else:
            return render(request, 'reset_password_failed.html')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Password set not successful.")
        return redirect('reset_password')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data = request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('PersonalInformation')
        else:
            return redirect('/PersonalInformation/change_password')
    else:
        form = PasswordChangeForm(user = request.user)
        args = {'form':form}
        return render(request, 'change_password.html',args)

def check_username_availability(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        try:
            user = User.objects.get(username=username)
            return JsonResponse({'available': False})
        except User.DoesNotExist:
            return JsonResponse({'available': True})
        
def check_email_availability(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        try:
            user = User.objects.get(email=email)
            return JsonResponse({'available': False})
        except User.DoesNotExist:
            return JsonResponse({'available': True})


@login_required(login_url='/auth_login/')
@user_required
def PersonalInformation(request):
    username = request.user.username

    # Retrieve a queryset of records with the desired username
    matching_records = UserInfo.objects.filter(username=username)
    # Check if any records with the desired username exist
    username_exists = matching_records.exists()
    if username_exists:
        mydata = UserInfo.objects.filter(username=username)
    else:
        mydata = User.objects.filter(username=username)

    context = {
        'PersonalInformation': mydata, 
        'head': mydata  
    }
    return render(request, 'PersonalInformation.html', context)


@login_required(login_url='/auth_login/')
@user_required
def PersonalInformation_update(request):
    username = request.user.username
    # Retrieve a queryset of records with the desired username
    matching_records = UserInfo.objects.filter(username=username)
    # Check if any records with the desired username exist
    username_exists = matching_records.exists()
    if username_exists:
        mydata = UserInfo.objects.filter(username=username)
    else:
        mydata = User.objects.filter(username=username)
       
 
    if request.method == 'POST':
        user_info, created = UserInfo.objects.get_or_create(user=request.user)
        user_info.username = request.POST['username']
        # user_info.profilephoto = request.FILES.get('profile_photo')
        try:
            if request.FILES.get('profile_photo'):
                user_info.profilephoto = request.FILES.get('profile_photo')
            else:
                value = UserInfo.get('profilephoto', 'null')
                user_info.profilephoto = value 
        except:
            pass

        user_info.first_name = request.POST['first_name']
        user_info.last_name = request.POST['last_name']
        user_info.website = request.POST['website']
        user_info.email = request.POST['email']
        # user_info.date_of_birth = request.POST['date_of_birth']
        try:
            if request.POST['date_of_birth'] == "":
                value = UserInfo.get('date_of_birth', None)
                user_info.date_of_birth = value 
            else:
                user_info.date_of_birth =  request.POST['date_of_birth']
        except:
            pass
        user_info.phone_number = request.POST['phone_number']
        user_info.country_name = request.POST['country_name']
        user_info.state = request.POST['state']
        user_info.city = request.POST['city']
        user_info.company_brief = request.POST['company_brief']
        user_info.gender = request.POST['gender']
        user_info.facebook_account = request.POST['facebook_account']
        user_info.twitter_account = request.POST['twitter_account']
        user_info.spotify_account = request.POST['spotify_account']
        
        user_info.save()

        return redirect('PersonalInformation')  # Redirect back to the same page after saving
    else:
        context = {
            'PersonalInformation': mydata,
        }
        return render(request, 'PersonalInformationform.html', context)
    
    
@login_required(login_url='/auth_login/')
@user_required
def labelof(request, Movie_name):
    mydata = CreateLabel.objects.filter(Movie_name=Movie_name)
    mydata2 = PostText1.objects.filter(Movie_name=Movie_name).order_by('-timestamp_field')
    mydata1 = Clips.objects.filter(Movie_name=Movie_name).order_by('-timestamp_field')
    mydata3 = CommentPostText1.objects.filter(movie_title=Movie_name).order_by('-timestamp_field')
    mydata4 = CommentClip.objects.filter(movie_title=Movie_name).order_by('-timestamp_field')
    # id = request.GET.get('id')
    # # Retrieve a queryset of records with the desired 'id'
    # matching_records = PostText1.objects.filter(id=id)
    #
    # # Check if any records with the desired 'id' exist
    # if matching_records.exists():
    #     mydata3 = CommentPostText1.objects.filter(Movie_name=matching_records[0]).order_by('-timestamp_field')
    # else:
    #     mydata3 = CommentPostText1.objects.none()
    all_data = list(chain(mydata, mydata2, mydata3, mydata1, mydata4))
    all_data.sort(key=attrgetter('timestamp_field'), reverse=True)
    template = loader.get_template('labelof.html')
    context = {
        'labelof': all_data,
        'mydata':mydata,
        'PostTextView':mydata2,
        'CommentPostText':mydata3,
        'CommentClip': mydata4,
        'ClipsView': mydata1,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/auth_login/')
@user_required
def like_movie(request, Movie_name):
    user = request.user.username
    Movie_id = get_object_or_404(CreateLabel, Movie_name=Movie_name)
    like = User.objects.get(username=user)
    movie_title = None
    username = None

    # Check if the user has already liked the movie
    if LikeMovies.objects.filter(like=like, Movie_name=Movie_id).exists():
        messages.warning(request, "You have already liked this movie.")
    else:
        LikeMovies.objects.get_or_create(like=request.user, Movie_name=Movie_id, movie_title=Movie_name, username=user)
        like_count = LikeMovies.objects.filter(Movie_name=Movie_id).count()
        CreateLabel.objects.filter(Movie_name=Movie_name).update(like_count=like_count)
        messages.success(request, "You liked the movie.")

    return redirect(f'/labelof/{Movie_name}')

@login_required(login_url='/auth_login/')
@user_required
def follow_movie(request, Movie_name):
    user = request.user.username
    Movie_id = get_object_or_404(CreateLabel, Movie_name=Movie_name)
    follower = User.objects.get(username=user)
    movie_title = None
    username = None

    # Check if the user has already liked the movie
    if FollowMovies.objects.filter(follower=follower, Movie_name=Movie_id).exists():
        messages.warning(request, "You have already followed this movie.")
    else:
        FollowMovies.objects.get_or_create(follower=request.user, Movie_name=Movie_id, movie_title=Movie_name, username=user)
        follow_count = FollowMovies.objects.filter(Movie_name=Movie_id).count()
        CreateLabel.objects.filter(Movie_name=Movie_name).update(follow_count=follow_count)
        messages.success(request, "You followed the movie.")

    return redirect(f'/labelof/{Movie_name}')



@login_required(login_url='/auth_login/')
@user_required
def like_post_text(request, id):
    user = request.user.username
    posttext = get_object_or_404(PostText1, id=id)

    # Check if the user has already liked the post
    if LikePostText1.objects.filter(like_id=request.user, post_id=posttext).exists():
        return JsonResponse({'success': False, 'message': 'You have already liked this post.'})
    else:
        # Create a like for the post
        LikePostText1.objects.create(
            like=request.user,
            post_id=posttext,
            movie_title=posttext.Movie_name,
            username=user
        )
        # Update like count for the post
        like_count = LikePostText1.objects.filter(post_id=posttext).count()
        PostText1.objects.filter(id=id).update(like_count=like_count)
        return JsonResponse({'success': True, 'like_count': like_count})

@login_required(login_url='/auth_login/')
@user_required
def follow_post_text(request, id):
    user = request.user.username
    posttext = get_object_or_404(PostText1, id=id)
    follower_id = User.objects.get(username=user)
    Movie_name = get_object_or_404(PostText1, id=id)
    Movie_title = posttext.Movie_name

    # Check if the user has already liked the post
    if FollowPostText1.objects.filter(follower=follower_id, post_id=posttext).exists():
        return JsonResponse({'success': False, 'message': 'You have already followed this post.'})
    else:
        # Create a follow for the post
        FollowPostText1.objects.create(follower=request.user,
                                 post_id=posttext,
                                 movie_title=posttext.Movie_name,
                                 username=user)
        # Update like count for the post
        follow_count = FollowPostText1.objects.filter(post_id=posttext).count()
        PostText1.objects.filter(id=id).update(follow_count=follow_count)
        return JsonResponse({'success': True, 'follow_count': follow_count})


@login_required(login_url='/auth_login/')
@user_required
def comment_post_text(request, id):
    user = request.user.username
    posttext = get_object_or_404(PostText1, id=id)
    commenter = User.objects.get(username=user)
    post_id = get_object_or_404(PostText1, id=id)
    Movie_title = posttext.post_id
    if request.method == 'POST':
        comments = request.POST['comments']
        CommentPostText1.objects.create(commenter=request.user, post_id=posttext, comments=comments, movie_title=Movie_title, username=user)
        return JsonResponse({'success': True, 'comment_id': post_id})
    else:
        return JsonResponse({'success': False, 'message': 'Comment text is required.'})


def publiclabel(request, Movie_name):
    mydata = CreateLabel.objects.filter(Movie_name=Movie_name).order_by('-timestamp_field')
    mydata2 = PostText1.objects.filter(Movie_name=Movie_name).order_by('-timestamp_field')
    all_data = list(chain(mydata, mydata2))
    all_data.sort(key=attrgetter('timestamp_field'), reverse=True)
    template = loader.get_template('publiclabel.html')
    context = {
        'publiclabel': all_data,
        'mydata':mydata,
        'PostTextView':mydata2,
    }
    return HttpResponse(template.render(context, request))

def check_movie_exists(request):
    if request.method == 'GET':
        Movie_name = request.GET.get('Movie_name')
        try:
            Movie = CreateLabel.objects.get(Movie_name=Movie_name)
            return JsonResponse({'available': False})
        except CreateLabel.DoesNotExist:
            return JsonResponse({'available': True})


def producer_reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('producer_email',False)
        print('email:',email)
        try:
            user = User.objects.get(email = email)
            print('user:',user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print(uid)
            token = generate_token.make_token(user)
            print(token)
            current_site = get_current_site(request)
            
            #Reset Password Email

            email_subject = "Reset your Password!!"
            message3 = render_to_string('producer_reset_password_email.html', {
                'name': user.username,
                'domain': settings.SITE_URL,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })
            email = EmailMessage(
                email_subject,
                message3,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            email.fail_silently = True
            email.send()
            messages.success(request, 'A password reset link has been sent to your email.')
            # return redirect('producer_reset_password')
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email.')
            return redirect('producer_reset_password')
    return render(request, 'producer_reset_password.html')

def ProducerResetConfirm(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=uid)
        if user is not None and generate_token.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user=user, data=request.POST)
                if form.is_valid():
                    form.save()  # Save the new password for the user
                    messages.success(request, "Password set successfully!")
                    return redirect('/Business/')
                else:
                    return redirect('producer_reset_password')
            else:
                form = SetPasswordForm(user=user)
                args = {'form': form}
                return render(request, 'producer_reset_password_form.html', args)
        else:
            return render(request, 'producer_reset_password_failed.html')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Password set not successful.")
        return redirect('producer_reset_password')
    

@login_required(login_url='/Business/')
@producer_required
def profile(request):
    producer = request.user
    mydata = ProducerRegister.objects.filter(production_house = producer)
    template = loader.get_template('profile.html')
    context = {
        'profile': mydata
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/Business/')
@producer_required
def UpdateProfile(request):

    producer = request.user
    # Retrieve a queryset of records with the desired username
    matching_records = ProducerRegister.objects.filter(production_house = producer)
    # Check if any records with the desired username exist 
    producer_exists = matching_records.exists()
    if producer_exists:
        mydata = ProducerRegister.objects.filter(production_house = producer)
    
       
    if request.method == 'POST':
        producer_info, created = ProducerRegister.objects.get_or_create(production_house=request.user)
        try:
            if request.FILES.get('production_house_image'):
                producer_info.production_house_image = request.FILES.get('production_house_image')
            else:
                value = ProducerRegister.get('production_house_image', 'null')
                producer_info.production_house_image = value 
        except:
            pass
        producer_info.producer_first_name = request.POST['producer_first_name']
        producer_info.producer_last_name = request.POST['producer_last_name']
        producer_info.producer_website = request.POST['producer_website']
        producer_info.producer_email = request.POST['producer_email']
        producer_info.producer_phone_number = request.POST['producer_phone_number']
        producer_info.producer_country_name = request.POST['producer_country_name']
        producer_info.producer_state = request.POST['producer_state']
        producer_info.producer_city = request.POST['producer_city']
        producer_info.production_house_brief = request.POST['production_house_brief']
        producer_info.producer_facebook_account = request.POST['producer_facebook_account']
        producer_info.producer_twitter_account = request.POST['producer_twitter_account']
        
        producer_info.save()
        return redirect('/profile/')  # Redirect back to the same page after saving
    else:
        context = {
            'profile': mydata,
        }
        return render(request, 'ProfileUpdate.html', context)


@login_required(login_url='/Business/')
@producer_required
def producer_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data = request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/profile/')
        else:
            return redirect('/producer_change_password/')
    else:
        form = PasswordChangeForm(user = request.user)
        args = {'form':form}
        return render(request, 'producer_change_password.html',args)
    

def Advantages(request):
    template = loader.get_template('Advantages.html')
    context = {
        'Advantages': Advantages,
    }
    return HttpResponse(template.render(context, request))


def Pricing(request):
    template = loader.get_template('Pricing.html')
    context = {
        'Pricing': Pricing,
    }
    return HttpResponse(template.render(context, request))


def Privacy(request):
    mydata = Privacy1.objects.all().order_by('-timestamp_field')
    template = loader.get_template('Privacy.html')
    context = {
        'Privacy': mydata,
    }
    return HttpResponse(template.render(context, request))

def terms(request):
    mydata = Terms.objects.all().order_by('-timestamp_field')
    template = loader.get_template('terms.html')
    context = {
        'terms': mydata,
    }
    return HttpResponse(template.render(context, request))


def page_not_found(request, exception):
    return render(request, '404.html')


@login_required(login_url='/Producerloginpage/')
def webseries_label(request):
    if request.method == 'POST':
        producer_name = request.user
        if User.objects.filter(username=producer_name).exists():
            form = WebseriesForm(request.POST, request.FILES)
            producer = ProducerRegister.objects.get(production_house=producer_name)
            if form.is_valid():
                form.save()
                webseries_name=form.cleaned_data['webseries_name']
                WebSeriesLabel.objects.filter(webseries_name= webseries_name).update(producer_id=producer)
                return redirect('producerdashboard')
            else:
                img_obj = form.instance
                return render(request, 'WebSeries.html', {'form': form, 'img_obj': img_obj})
    else:
        form = WebseriesForm()
    return render(request, 'WebSeries.html', {'form': form})


def searchresult(request):
    template = loader.get_template('searchresult.html')
    username = request.user.username
    # Retrieve a queryset of records with the desired username
    matching_records = UserInfo.objects.filter(username=username)
    # Check if any records with the desired username exist
    username_exists = matching_records.exists()
    if username_exists:
        userdata = UserInfo.objects.filter(username=username)
    else:
        userdata = User.objects.filter(username=username)
    if request.method == "GET":
        search_query = request.GET.get('search', '').split(" ")
        if search_query is not None:
            queryset_list1 = Q()
            queryset_list2 = Q()
            queryset_list3 = Q()
            for query in search_query:
                queryset_list1 |= (
                        Q(Language__icontains=query) |
                        Q(Movie_name__icontains=query) |
                        Q(Genre__icontains=query) |
                        Q(Production_house__icontains=query) |
                        Q(Producer__icontains=query) |
                        Q(cast__icontains=query) |
                        Q(Director__icontains=query) |
                        Q(Music_director__icontains=query) |
                        Q(Other_Languages__icontains=query) |
                        Q(lyricist__icontains=query) |
                        Q(choreographer__icontains=query) |
                        Q(Script_writer__icontains=query) |
                        Q(Distribution__icontains=query) |
                        Q(Singers__icontains=query) |
                        Q(Editor__icontains=query) |
                        Q(Cinematographer__icontains=query)
                )
                queryset_list2 |= (
                    Q(author__icontains=query) |
                    Q(Movie_name__icontains=query)
                )

                queryset_list3 |= (
                        Q(Movie_name__icontains=query)
                )

            try:
                mydata = CreateLabel.objects.filter(queryset_list1).distinct().order_by('-timestamp_field')
            except CreateLabel.DoesNotExist:
                mydata = []
            try:
                mydata1 = Review.objects.filter(queryset_list2).distinct().order_by('-timestamp_field')
            except Review.DoesNotExist:
                mydata1 = []
            try:
                mydata3 = PostText1.objects.filter(queryset_list3).distinct().order_by('-timestamp_field')
            except PostText1.DoesNotExist:
                mydata3 = []
            combined_data = sorted(list(mydata) + list(mydata1) + list(mydata3),
                                   key=lambda x: x.timestamp_field, reverse=True
                                   )
            context = {'combined_data': combined_data, 'head': userdata}
        else:
            context = {
                'combined_data': []
            }
    return HttpResponse(template.render(context, request))


@csrf_protect
def Privacy_form(request):
    if request.method == 'POST':
        Heading = request.POST['Heading']
        text = request.POST['text']
        privacy_instance = Privacy1(Heading=Heading, text=text)
        # Save the instance to the database
        privacy_instance.save()
        return render(request, 'Privacy_form.html')
    return render(request, 'Privacy_form.html')


@csrf_protect
def terms_form(request):
    if request.method == 'POST':
        Heading = request.POST['Heading']
        text = request.POST['text']
        terms_instance = Terms(text=text, Heading=Heading)
        # Save the instance to the database
        terms_instance.save()
        return render(request, 'Terms_form.html')
    return render(request, 'Terms_form.html')





def promo(request, Movie_name):
    mydata = CreateLabel.objects.filter(Movie_name=Movie_name).order_by('-timestamp_field')
    mydata2 = PostText1.objects.filter(Movie_name=Movie_name).order_by('-timestamp_field')
    mydata1 = Review.objects.filter(Movie_name=Movie_name).order_by('-timestamp_field')
    mydata3 = CreateLabel.objects.all().order_by('-timestamp_field')
    all_data = list(chain(mydata, mydata2, mydata1, mydata3))
    all_data.sort(key=attrgetter('timestamp_field'), reverse=True)
    template = loader.get_template('promo.html')
    context = {
        'promo': all_data,
        'mydata':mydata,
        'mydata1':mydata1,
        'PostTextView':mydata2,
        'Createlabel':mydata3,
    }
    return HttpResponse(template.render(context, request))


def post_promo(request, Movie_name):
    mydata = CreateLabel.objects.filter(Movie_name=Movie_name).order_by('-timestamp_field')
    mydata2 = PostText1.objects.filter(Movie_name=Movie_name).order_by('-timestamp_field')
    template = loader.get_template('post_promo.html')
    context = {
        'post_promo':mydata2,
        'mydata': mydata,
    }
    return HttpResponse(template.render(context, request))

def tmdb_promo(request, movie_title):
    mydata = Movie.objects.filter(movie_title=movie_title).order_by('-timestamp_field')
    template = loader.get_template('tmdb_promo.html')
    context = {
        'tmdb_promo': mydata,
    }
    return HttpResponse(template.render(context, request))

def review_promo(request, slug):
    mydata = Review.objects.all().order_by('-timestamp_field')
    mydata1 = Review.objects.filter(slug=slug).order_by('-timestamp_field')
    template = loader.get_template('review_promo.html')
    context = {
        'review_promo': mydata1,
        'mydata': mydata,
    }
    return HttpResponse((template.render(context, request)))



def Clip(request):
    if request.method == 'POST' and request.FILES:
        form = VideoClipsForm(request.POST, request.FILES)
        production_house_name = request.user
        print('production house name', production_house_name)
        producer = ProducerRegister.objects.get(production_house=production_house_name)
        production_house = ProducerRegister.objects.get(production_house=production_house_name).production_house
        producer_logo = ProducerRegister.objects.get(production_house=production_house_name).production_house_image
        # list of movies produced by the production house
        movies = CreateLabel.objects.filter(producer_id=producer)
        movie_list = [movie.Movie_name for movie in movies] 
        if form.is_valid():
            Movie_name = form.cleaned_data['Movie_name']
            # Check if the movie exists in CreateLabel database
            if CreateLabel.objects.filter(Movie_name=Movie_name).exists() and Movie_name in movie_list:
                form.save()  # Save the post if the movie exists
                Clips.objects.filter(Movie_name = Movie_name).update(source=production_house)
                Clips.objects.filter(Movie_name = Movie_name).update(logo=producer_logo)
                Clips.objects.filter(Movie_name = Movie_name).update(slug = ''.join(Movie_name.split(' ')))
                return redirect('Clip')  # Redirect to a success view
            elif Movie_name not in movie_list:
                messages.error(request, "You have not produced this movie!!")
                print('error occured while posting text')
                return redirect('Clip')
            else:
                messages.error(request, "Create A Label For The Movie To Post!")
                return render(request, 'Clips.html', {'form': form, 'message': messages.error})
    else:
        form = VideoClipsForm()
    return render(request, 'Clips.html', {'form': form})


def clip_promo(request, Movie_name):
    mydata = CreateLabel.objects.filter(Movie_name=Movie_name).order_by('-timestamp_field')
    mydata2 = Clips.objects.filter(Movie_name=Movie_name).order_by('-timestamp_field')
    template = loader.get_template('clip_promo.html')
    context = {
        'clip_promo':mydata2,
        'mydata': mydata,
    }
    return HttpResponse(template.render(context, request))





@login_required(login_url='/auth_login/')
@user_required
def like_clip(request, id):
    user = request.user.username
    clip = get_object_or_404(Clips, id=id)

    # Check if the user has already liked the post
    if LikeClip.objects.filter(like_id=request.user, post_id=clip).exists():
        return JsonResponse({'success': False, 'message': 'You have already liked this post.'})
    else:
        # Create a like for the post
        LikeClip.objects.create(
            like=request.user,
            post_id=clip,
            movie_title=clip.Movie_name,
            username=user
        )
        # Update like count for the post
        like_count = LikeClip.objects.filter(post_id=clip).count()
        Clips.objects.filter(id=id).update(like_count=like_count)
        return JsonResponse({'success': True, 'like_count': like_count})

@login_required(login_url='/auth_login/')
@user_required
def follow_clip(request, id):
    user = request.user.username
    clip = get_object_or_404(Clips, id=id)
    follower_id = User.objects.get(username=user)
    Movie_name = get_object_or_404(Clips, id=id)
    Movie_title = clip.Movie_name

    # Check if the user has already liked the post
    if FollowClip.objects.filter(follower=follower_id, post_id=clip).exists():
        return JsonResponse({'success': False, 'message': 'You have already followed this post.'})
    else:
        # Create a follow for the post
        FollowClip.objects.create(follower=request.user,
                                 post_id=clip,
                                 movie_title=clip_promo.Movie_name,
                                 username=user)
        # Update like count for the post
        follow_count = FollowClip.objects.filter(post_id=clip).count()
        Clips.objects.filter(id=id).update(follow_count=follow_count)
        return JsonResponse({'success': True, 'follow_count': follow_count})


@login_required(login_url='/auth_login/')
@user_required
def comment_clip(request, id):
    user = request.user.username
    clip = get_object_or_404(Clips, id=id)
    commenter = User.objects.get(username=user)
    post_id = get_object_or_404(Clips, id=id)
    Movie_title = clip.post_id
    if request.method == 'POST':
        comments = request.POST['comments']
        CommentPostText1.objects.create(commenter=request.user, post_id=clip, comments=comments, movie_title=Movie_title, username=user)
        return JsonResponse({'success': True, 'comment_id': post_id})
    else:
        return JsonResponse({'success': False, 'message': 'Comment text is required.'})

