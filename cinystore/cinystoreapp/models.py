#from django.contrib.auth.models import User
from django.utils import timezone
import os
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4
import os
from datetime import datetime


''' Custom Model'''
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    is_user = models.BooleanField(default=False)
    is_producer = models.BooleanField(default=False)
    is_marketing = models.BooleanField(default=False)
    phone_numbers = models.ManyToManyField('PhoneNumber', related_name='users', blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)

class PhoneNumber(models.Model):
    number = PhoneNumberField()  # Define your field for phone numbers
    email = models.EmailField(null=True, blank=True)
    otp  = models.IntegerField(null=True, blank=True)
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)

    def __str__(self):
        return str(self.number)
    
    class Meta:
        db_table = 'phone_number'

def rename(instance, filename):
    upload_to = 'Users/'
    ext = filename.split('.')[-1]
    # username = user.username
    if instance.username:
        filename = '{}_{}.{}'.format(instance.username,datetime.now(), ext)
    else:
        filename ='{}_{}.{}'.format(uuid4.hex, datetime.now(), ext)
    return os.path.join(upload_to, filename)

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    username = models.CharField(max_length=45)
    profilephoto = models.ImageField(upload_to=rename, default='Users/blank_profile.webp', null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    website = models.CharField(max_length=50)
    date_of_birth = models.DateField(max_length=100, default='2000-01-01')
    phone_number = PhoneNumberField() 
    country_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    company_brief = models.CharField(max_length=2000)
    gender = models.CharField(max_length=255)
    facebook_account = models.CharField(max_length=100)
    twitter_account = models.CharField(max_length=100)
    spotify_account = models.CharField(max_length=100)
    class Meta:
        db_table = 'user_info'


def rename_producer(instance, filename):
    upload_to = 'Producers/'
    ext = filename.split('.')[-1]
    # username = user.username
    if instance.production_house_image:
        filename = '{}_{}.{}'.format(instance.production_house,datetime.now(), ext)
    else:
        filename ='{}_{}.{}'.format(uuid4.hex, datetime.now(), ext)
    return os.path.join(upload_to, filename)

class ProducerRegister(models.Model):
    producer = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    production_house_image = models.ImageField(upload_to=rename_producer, default='Producers/blank_profile.webp', null=True)
    producer_first_name = models.CharField(max_length=100)
    producer_last_name = models.CharField(max_length=100)
    producer_email = models.CharField(max_length=100)
    production_house = models.CharField(max_length=100)
    producer_website = models.CharField(max_length=50)
    producer_phone_number = models.CharField(max_length=20)
    producer_country_name = models.CharField(max_length=100)
    producer_state = models.CharField(max_length=100)
    producer_city = models.CharField(max_length=100)
    production_house_brief = models.CharField(max_length=2000)
    producer_facebook_account = models.CharField(max_length=100)
    producer_twitter_account = models.CharField(max_length=100)
    last_login = models.DateTimeField(verbose_name='last login', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_agency = models.BooleanField(default=True)
    is_corporate = models.BooleanField(default=True)
    is_ott = models.BooleanField(default=True)
    is_individual = models.BooleanField(default=True)

    class Meta:
        db_table = 'ProducerRegister'



def path_and_rename(instance, filename):
    upload_to = 'Posters/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.Movie_name:
        filename = '{}_{}.{}'.format(instance.Movie_name,datetime.now(), ext)
    else:
        # set filename as random string
        filename = '{}_{}.{}'.format(uuid4().hex,datetime.now(), ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


def path_and_rename_post(instance, filename):
    upload_to = 'Posttext/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.Movie_name:
        filename = '{}_{}.{}'.format(instance.Movie_name,datetime.now(), ext)
    else:
        # set filename as random string
        filename = '{}_{}.{}'.format(uuid4().hex,datetime.now(), ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class Movie(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    movie_title = models.CharField(max_length=255)
    overview = models.TextField(max_length=1000)
    release_date = models.DateField(max_length=100, null=True)
    poster_path = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    genre = models.CharField(max_length=100, default=False, null=True)
    language = models.CharField(max_length=50, default=False, null=True)
    video = models.URLField(default=False, null=True)
    producer = models.CharField(max_length=100, default=False, null=True)
    director = models.CharField(max_length=100,  default=False, null=True)
    music_director = models.CharField(max_length=100, default=False, null=True)
    crew = models.CharField(max_length=100,  default=False, null=True)
    cast = models.CharField(max_length=2000, default=False, null=True)
    timestamp_field = models.DateTimeField(default=timezone.now)
    model_type = models.CharField(max_length=50, default='movies')
    like_count = models.BigIntegerField(null=True, blank=True, default='0')
    follow_count = models.BigIntegerField(null=True, blank=True, default='0')
    share_count = models.BigIntegerField(null=True, blank=True, default='0')
    comment_count = models.BigIntegerField(null=True, blank=True, default='0')
    source = models.CharField(max_length=100, null= True, blank=True, default='TMDB')
    logo = models.CharField(max_length=100, null= True, blank=True, default='TMDB/TMDB_logo.png')
    slug = models.SlugField(default=False)

    class Meta:
        ordering = ['-timestamp_field']
        db_table = 'movie'

    def __str__(self):
        return f"{self.movie_title}'s model"



class CreateLabel(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    Movie_name = models.CharField(max_length=100)
    Language = models.CharField(max_length=100)
    Genre = models.CharField(max_length=100)
    Production_house = models.CharField(max_length=50)
    Producer = models.CharField(max_length=100)
    cast = models.CharField(max_length=250)
    Director = models.CharField(max_length=100)
    Music_director = models.CharField(max_length=100)
    Poster = models.ImageField(upload_to= path_and_rename , blank=True)
    Banner = models.ImageField(upload_to= path_and_rename, blank=True)
    Release_date = models.DateField(max_length=100)
    synopsis = models.CharField(max_length=2000)
    trailer = models.CharField(max_length=255)
    timestamp_field = models.DateTimeField(auto_now_add=True)
    model_type = models.CharField(max_length=100, default='mydata')
    producer_id = models.ForeignKey('ProducerRegister', default=1, verbose_name="producer_register", on_delete=models.SET_DEFAULT, db_column='producer_id')
    Url_name = models.CharField(max_length=100,default=None, null=True)
    Other_Languages = models.CharField(max_length=100, null=True)
    lyricist = models.CharField(max_length=100, null=True)
    choreographer = models.CharField(max_length=100, null=True)
    Script_writer = models.CharField(max_length=100, null=True)
    Running_Time = models.CharField(max_length=100, null=True)
    Maturity = models.CharField(max_length=100, null=True)
    Budget = models.CharField(max_length=100, null=True)
    Distribution = models.CharField(max_length=100, null=True)
    Recording_studio = models.CharField(max_length=100, null=True)
    Graphic_designer = models.CharField(max_length=100, null=True)
    like_count = models.BigIntegerField(null=True, blank=True, default='0')
    follow_count = models.BigIntegerField(null=True, blank=True, default='0')
    share_count = models.BigIntegerField(null=True, blank=True, default='0')
    comment_count = models.BigIntegerField(null=True, blank=True, default='0')
    Singers = models.CharField(max_length=100, null=True)
    Editor = models.CharField(max_length=100, null=True)
    Cinematographer = models.CharField(max_length=100, null=True)
    source = models.CharField(max_length=100, null= True, blank=True, default='Cinystore News Network')
    logo = models.CharField(max_length=255, null= True, blank=True, default='User/blank_profile.webp')


    class Meta:
        db_table = 'Create_label'
        ordering = ['-timestamp_field']


    def __str__(self):
        return self.Movie_name

def path_and_rename_webseries_label(instance, filename):
    upload_to = 'WebSeriesPoster/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.webseries_name:
        filename = '{}_{}.{}'.format(instance.webseries_name,datetime.now(), ext)
    else:
        # set filename as random string
        filename = '{}_{}.{}'.format(uuid4().hex,datetime.now(), ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class WebSeriesLabel(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    webseries_name = models.CharField(max_length=100)
    Language = models.CharField(max_length=100)
    Genre = models.CharField(max_length=100)
    Production_house = models.CharField(max_length=50)
    Producer = models.CharField(max_length=100)
    cast = models.CharField(max_length=250)
    Director = models.CharField(max_length=100)
    season = models.CharField(max_length=100)
    episodes = models.CharField(max_length=100)
    streaming_on = models.CharField(max_length=100)
    Poster = models.ImageField(upload_to= path_and_rename_webseries_label , blank=True)
    Release_date = models.DateField(max_length=100)
    synopsis = models.CharField(max_length=2000)
    trailer = models.CharField(max_length=255)
    timestamp_field = models.DateTimeField(auto_now_add=True)
    model_type = models.CharField(max_length=100, default='webseriesdata')
    producer_id = models.ForeignKey('ProducerRegister', default=1, verbose_name="producer_register", on_delete=models.SET_DEFAULT, db_column='producer_id')
    class Meta:
        db_table = 'webseries_label'
        ordering = ['-timestamp_field']


    def __str__(self):
        return self.webseries_name

   
class Blog(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    Poster = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    content = models.CharField(max_length=5000)
    timestamp_field = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp_field']
        db_table = 'blog'



class ProducerManager(models.Manager):
    def create_producer(self, producer_first_name, producer_email, producer_password):
        producer = self.create(
            producer_first_name=producer_first_name,
            producer_email=producer_email,
            producer_password=producer_password,
        )

        # Additional logic for creating the producer
        return producer

# class ProducerRegister(models.Model):
#     id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
#     producer_first_name = models.CharField(max_length=100)
#     producer_last_name = models.CharField(max_length=100)
#     producer_password = models.CharField(max_length=100)
#     producer_confirm_password = models.CharField(max_length=100)
#     producer_email = models.CharField(max_length=100)
#     production_house = models.CharField(max_length=100)
#     producer_website = models.CharField(max_length=50)
#     producer_phone_number = models.CharField(max_length=10)
#     producer_country_name = models.CharField(max_length=100)
#     producer_state = models.CharField(max_length=100)
#     Producer_city = models.CharField(max_length=100)
#     production_house_brief = models.CharField(max_length=2000)
#     producer_facebook_account = models.CharField(max_length=100)
#     producer_twitter_account = models.CharField(max_length=100)
#     objects = ProducerManager()

#     class Meta:
#         db_table= 'producer_register'
#         verbose_name_plural = 'producer_register'

#     def __str__(self):
#         return self.producer_first_name


class PostText1(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    Movie_name = models.CharField(max_length=100)
    text = models.CharField(max_length=2000)
    Image = models.ImageField(upload_to=path_and_rename_post, blank=True)
    Heading = models.CharField(max_length=200, null=True, blank=True, default='')
    timestamp_field = models.DateTimeField(auto_now_add=True)
    model_type = models.CharField(max_length=100, default='mydata3')
    like_count = models.BigIntegerField(null=True, blank=True, default='0')
    comment_count = models.BigIntegerField(null=True, blank=True, default='0')
    share_count = models.BigIntegerField(null=True, blank=True, default='0')
    follow_count = models.BigIntegerField(null=True, blank=True, default='0')
    source = models.CharField(max_length=100, null=True, blank=True, default='Cinystore News Network')
    logo = models.CharField(max_length=255, null= True, blank=True, default='Users/blank_profile.webp')
    slug = models.SlugField(default=False)
    auto_created = True,

    class Meta:
        db_table = 'PostText'
        ordering = ['-timestamp_field']

def __str__(self):
    return self.Movie_name


def get_data(self):
    time = datetime.now()
    if self.created_at.day == time.day:
        return str(time.hour - self.created_at.hour) + "hours ago"
    else:
        if self.created_at.month == time.month:
            return str(time.day - self.created_at.day) + "days ago"
        else:
            if self.created_at.year == time.year:
                return str(time.month - self.created_at.month) + "months ago"
    return self.created_at


def __str__(self):
    return self.title


class Review(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    author = models.CharField(max_length=40, default="")
    review_date = models.DateField(max_length=100)
    stars = models.FloatField(null=True)
    comment = models.TextField(max_length=4000)
    Movie_name = models.CharField(max_length=100)
    timestamp_field = models.DateTimeField(auto_now_add=True)
    model_type = models.CharField(max_length=100, default='mydata1')
    like_count = models.BigIntegerField(null=True, blank=True, default='0')
    comment_count = models.BigIntegerField(null=True, blank=True, default='0')
    share_count = models.BigIntegerField(null=True, blank=True, default='0')
    source = models.CharField(max_length=100, null= True, blank=True)
    logo = models.CharField(max_length=255, null= True, blank=True, default='Users/blank_profile.webp')
    slug = models.SlugField(default=False)

    class Meta:
        ordering = ['-timestamp_field']
        db_table = 'review'


def __str__(self):
    return self.Movie_name

class BoxOffice(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    Movie_name = models.CharField(max_length=100)
    production_house = models.CharField(max_length=100)
    movie_collections = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    day_collections = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    weekly_collections = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    month_collections = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    timestamp_field = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp_field']
        db_table = 'box_office'


class News(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    Movie_name = models.CharField(max_length=100)
    text = models.CharField(max_length=5000)
    author = models.CharField(max_length=255)
    timestamp_field = models.DateTimeField(auto_now_add=True)
    auto_created = True,

    class Meta:
        db_table = 'news'
        ordering = ['timestamp_field']

def __str__(self):
    return self.Movie_name


def rename(instance, filename):
    upload_to = 'Users/'
    ext = filename.split('.')[-1]
    # username = user.username
    if instance.username:
        filename = '{}_{}.{}'.format(instance.username,datetime.now(), ext)
    else:
        filename ='{}_{}.{}'.format(uuid4.hex, datetime.now(), ext)
    return os.path.join(upload_to, filename)


# class UserInfo(models.Model):
#     id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
#     profilephoto = models.ImageField(upload_to=rename, default=None, null=True, blank=False)
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
#     username = models.CharField(max_length=45)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.CharField(max_length=100)
#     website = models.CharField(max_length=50)
#     date_of_birth = models.DateField(max_length=100, default='2000-01-01')
#     phone_number = models.BigIntegerField(null=False, default=0)
#     country_name = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     city = models.CharField(max_length=100)
#     company_brief = models.CharField(max_length=2000)
#     gender = models.CharField(max_length=255)
#     facebook_account = models.CharField(max_length=100)
#     twitter_account = models.CharField(max_length=100)
#     spotify_account = models.CharField(max_length=100)
#     class Meta:
#         db_table = 'user_info'

# @receiver (post_save, sender=User)
# def create_profile(sender, **kwargs):
#     if kwargs['created']:
#         user_profile = UserInfo.objects.create(user=kwargs['instance'])
#         user_profile.save()


class LikeMovies(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True, serialize=False, verbose_name='ID')
    like = models.ForeignKey(User, on_delete=models.CASCADE)
    Movie_name = models.ForeignKey('CreateLabel', default=True, verbose_name="Create_label", on_delete=models.CASCADE, db_column='Movie_name')
    movie_title = models.CharField(max_length=255, default=None)
    username = models.CharField(max_length=255, default=None)
    timestamp_field = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'like_movie'
        ordering = ['timestamp_field']


class FollowMovies(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    Movie_name = models.ForeignKey('CreateLabel', default=True, on_delete=models.CASCADE, verbose_name="Create_label", db_column='Movie_name')
    movie_title = models.CharField(max_length=255, default=None)
    username = models.CharField(max_length=255, default=None)
    timestamp_field = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'follow_movie'
        ordering = ['timestamp_field']



class LikePostText1(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True, serialize=False, verbose_name='ID')
    like = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey('PostText1', default=True, verbose_name="posttext", on_delete=models.CASCADE, db_column='post_id')
    movie_title = models.CharField(max_length=255, default=None)
    username = models.CharField(max_length=255, default=None)
    timestamp_field = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'like_post_text'
        ordering = ['timestamp_field']


class FollowPostText1(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True, serialize=False, verbose_name='ID')
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey('PostText1', default=True, verbose_name="posttext", on_delete=models.CASCADE, db_column='post_id')
    movie_title = models.CharField(max_length=255, default=None)
    username = models.CharField(max_length=255, default=None)
    timestamp_field = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'follow_post_text'
        ordering = ['timestamp_field']

class CommentPostText1(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True, serialize=False, verbose_name='ID')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.TextField(max_length=5000)
    post_id = models.ForeignKey('PostText1', default=True, verbose_name="posttext", on_delete=models.CASCADE, db_column='post_id')
    movie_title = models.CharField(max_length=255, default=None)
    username = models.CharField(max_length=255, default=None)
    timestamp_field = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'comment_post_text'
        ordering = ['timestamp_field']

    def __str__(self):
        return '%s - %s' % (self.username, self.movie_title)

class UserLogs(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField()

    class Meta:
        db_table = 'userlogs'
        ordering = ['id']

    def __str__(self):
        return self.user
    
    
## New Models

class UserLikes(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, blank= True, null=True)
    label = models.ForeignKey(CreateLabel, on_delete=models.CASCADE, blank= True, null=True)
    post = models.ForeignKey(PostText1, on_delete=models.CASCADE, blank= True, null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, blank= True, null=True)
    model_type = models.CharField(max_length=100, null=False, blank=False)
    timestamp_field = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'userlikes'
        ordering = ['timestamp_field']

    def __str__(self):
        return self.user
    
class UserFollows(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, blank= True, null=True)
    label = models.ForeignKey(CreateLabel, on_delete=models.CASCADE, blank= True, null=True)
    model_type = models.CharField(max_length=100)
    timestamp_field = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'userfollows'
        ordering = ['timestamp_field']

    def __str__(self):
        return self.user
    
class UserComments(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, blank= True, null=True)
    label = models.ForeignKey(CreateLabel, on_delete=models.CASCADE, blank= True, null=True)
    post = models.ForeignKey(PostText1, on_delete=models.CASCADE, blank= True, null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, blank= True, null=True)
    comments = models.CharField(max_length=1000)
    model_type = models.CharField(max_length=100, null=False, blank=False)
    timestamp_field = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usercomments'
        ordering = ['timestamp_field']

    def __str__(self):
        return self.user

class UserShares(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, blank= True, null=True)
    label = models.ForeignKey(CreateLabel, on_delete=models.CASCADE, blank= True, null=True)
    post = models.ForeignKey(PostText1, on_delete=models.CASCADE, blank= True, null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, blank= True, null=True)
    model_type = models.CharField(max_length=100)
    timestamp_field = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usershares'
        ordering = ['timestamp_field']

    def __str__(self):
        return self.user

class Privacy1(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    text = models.CharField(max_length=5000)
    Heading = models.CharField(max_length=200, null=True, blank=True, default='')
    timestamp_field = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'privacy'
        ordering = ['-timestamp_field']

class Terms(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    text = models.CharField(max_length=5000)
    Heading = models.CharField(max_length=200, null=True, blank=True, default='')
    timestamp_field = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'terms'
        ordering = ['-timestamp_field']

#
# from django.urls import reverse
#
#
# class Notification(models.Model):
#     tmdb_id = models.ForeignKey('Movie', null=True, blank= True, on_delete=models.CASCADE, db_column='tmdb_id')
#     label_id = models.ForeignKey('CreateLabel', on_delete=models.CASCADE, null=True, blank=True, db_column='label_id')
#     is_read = models.BooleanField(default=False)
#     timestamp_field = models.DateTimeField(auto_now_add=True)
#     message = models.CharField(max_length=255)
#     link = models.URLField()
#     class Meta:
#         db_table = 'notificaton'
#         ordering = ['-timestamp_field']
#
#
# @receiver(post_save, sender=Movie)
# def create_post_notification(sender, instance, created, **kwargs):
#     if created:
#         Notification.objects.create(
#                 tmdb_id=instance,
#                 message=f'A new tmdb movie "{instance.movie_title}" has been created',
#                 link=reverse('Label2/<str:movie_title>', args=[str(instance.id)])  # Adjust the URL as needed
#             )
#
# @receiver(post_save, sender=CreateLabel)
# def create_label_notification(sender, instance, created, **kwargs):
#     if created:
#         Notification.objects.create(
#                 label_id=instance,
#                 message=f'A new label "{instance.Movie_name}" has been created',
#                 link=reverse('labelof/<str:Movie_name>', args=[str(instance.id)])  # Adjust the URL as needed
#             )

def path_rename_video(instance, filename):
    upload_to = 'videos/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.Movie_name:
        filename = '{}_{}.{}'.format(instance.Movie_name,datetime.now(), ext)
    else:
        # set filename as random string
        filename = '{}_{}.{}'.format(uuid4().hex,datetime.now(), ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class Clips(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    Heading = models.CharField(max_length=200, null=True, blank=True, default='')
    text = models.CharField(max_length=2000)
    Movie_name = models.CharField(max_length=100)
    Video = models.FileField(upload_to= path_rename_video, null=True, verbose_name="")
    Image = models.ImageField(upload_to='Posters/', blank=True)
    timestamp_field = models.DateTimeField(auto_now_add=True)
    model_type = models.CharField(max_length=100, default='mydata2')
    like_count = models.BigIntegerField(null=True, blank=True, default=False)
    comment_count = models.BigIntegerField(null=True, blank=True, default=False)
    share_count = models.BigIntegerField(null=True, blank=True, default=False)
    source = models.CharField(max_length=100, null=True, blank=True, default='Cinystore News Network')
    logo = models.CharField(max_length=255, null=True, blank=True, default='Users/blank_profile.webp')
    slug = models.SlugField()
    auto_created = True,

    def _str_(self) -> str:
        return self.Movie_name

    class Meta:
        db_table = 'Clips'
        ordering = ['-timestamp_field']


class TopRatedMovies(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    movie_title = models.CharField(max_length=255)
    overview = models.TextField(max_length=1000)
    release_date = models.DateField(max_length=100, null=True)
    poster_path = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    genre = models.CharField(max_length=100, default=False, null=True)
    language = models.CharField(max_length=50, default=False, null=True)
    video = models.URLField(default=False, null=True)
    producer = models.CharField(max_length=100, default=False, null=True)
    director = models.CharField(max_length=100,  default=False, null=True)
    music_director = models.CharField(max_length=100, default=False, null=True)
    crew = models.CharField(max_length=100,  default=False, null=True)
    cast = models.CharField(max_length=2000, default=False, null=True)
    timestamp_field = models.DateTimeField(default=timezone.now)
    model_type = models.CharField(max_length=50, default='top_rated_movies')
    like_count = models.BigIntegerField(null=True, blank=True, default='0')
    follow_count = models.BigIntegerField(null=True, blank=True, default='0')
    share_count = models.BigIntegerField(null=True, blank=True, default='0')
    comment_count = models.BigIntegerField(null=True, blank=True, default='0')
    source = models.CharField(max_length=100, null= True, blank=True, default='TMDB/top_rated_movies')
    logo = models.CharField(max_length=100, null= True, blank=True, default='TMDB/TMDB_logo.png')
    slug = models.SlugField(default=False)

    class Meta:
        ordering = ['-timestamp_field']
        db_table = 'top_rated_movies'

    def __str__(self):
        return f"{self.movie_title}'s model"
    



class RecentMovies(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    movie_title = models.CharField(max_length=255)
    overview = models.TextField(max_length=1000)
    release_date = models.DateField(max_length=100, null=True)
    poster_path = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    genre = models.CharField(max_length=100, default=False, null=True)
    language = models.CharField(max_length=50, default=False, null=True)
    video = models.URLField(default=False, null=True)
    producer = models.CharField(max_length=100, default=False, null=True)
    director = models.CharField(max_length=100,  default=False, null=True)
    music_director = models.CharField(max_length=100, default=False, null=True)
    crew = models.CharField(max_length=100,  default=False, null=True)
    cast = models.CharField(max_length=2000, default=False, null=True)
    timestamp_field = models.DateTimeField(default=timezone.now)
    model_type = models.CharField(max_length=50, default='recent_movies')
    like_count = models.BigIntegerField(null=True, blank=True, default='0')
    follow_count = models.BigIntegerField(null=True, blank=True, default='0')
    share_count = models.BigIntegerField(null=True, blank=True, default='0')
    comment_count = models.BigIntegerField(null=True, blank=True, default='0')
    source = models.CharField(max_length=100, null= True, blank=True, default='TMDB/recent_movies')
    logo = models.CharField(max_length=100, null= True, blank=True, default='TMDB/TMDB_logo.png')
    slug = models.SlugField(default=False)

    class Meta:
        ordering = ['-timestamp_field']
        db_table = 'recent_movies'

    def __str__(self):
        return f"{self.movie_title}'s model"
    


class LikeClip(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True, serialize=False, verbose_name='ID')
    like = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey('Clips', default=True, verbose_name="clips", on_delete=models.CASCADE, db_column='post_id')
    movie_title = models.CharField(max_length=255, default=None)
    username = models.CharField(max_length=255, default=None)
    timestamp_field = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'like_clip'
        ordering = ['timestamp_field']

    def __str__(self):
        return '%s - %s' % (self.username, self.movie_title)


class FollowClip(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True, serialize=False, verbose_name='ID')
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey('Clips', default=True, verbose_name="clips", on_delete=models.CASCADE, db_column='post_id')
    movie_title = models.CharField(max_length=255, default=None)
    username = models.CharField(max_length=255, default=None)
    timestamp_field = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'follow_clip'
        ordering = ['timestamp_field']
    def __str__(self):
        return '%s - %s' % (self.username, self.movie_title)

class CommentClip(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True, serialize=False, verbose_name='ID')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.TextField(max_length=5000)
    post_id = models.ForeignKey('Clips', default=True, verbose_name="clips", on_delete=models.CASCADE, db_column='post_id')
    movie_title = models.CharField(max_length=255, default=None)
    username = models.CharField(max_length=255, default=None)
    timestamp_field = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'comment_clip'
        ordering = ['timestamp_field']

    def __str__(self):
        return '%s - %s' % (self.username, self.movie_title)
    


