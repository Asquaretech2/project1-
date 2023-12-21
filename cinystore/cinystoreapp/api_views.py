from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
import json
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .serializers import TmdbSerializer
from .models import Movie, UserInfo
from cinystore import settings
from django.db.models import Q



from rest_framework.pagination import CursorPagination

class CustomPagination(CursorPagination):
    page_size =  6 # Set your desired page size
    ordering = '-timestamp_field'  # Use the field for sorting (timestamp or ID field)
    cursor_query_param = 'cursor'  # The name of the cursor parameter in the URL


@api_view(['GET'])
def CreateLabelGet_API(request):
    createlabel = CreateLabel.objects.all()
    # Apply pagination using your custom pagination class
    paginator = CustomPagination()
    paginated_queryset = paginator.paginate_queryset(createlabel, request)
    serializer = CreatelabelSerializer(paginated_queryset, many=True)
    next_url = paginator.get_next_link()
    prev_url = paginator.get_previous_link()

    if next_url:
        next_url = next_url.replace(request.get_host(), settings.SITE_URL)

    if prev_url:
        prev_url = prev_url.replace(request.get_host(), settings.SITE_URL)
    return Response({
        'next_url':next_url,
        'prev_url':prev_url,
        'results':serializer.data})
    # return paginator.get_paginated_response(serializer.data, next_url=next_url, prev_url=prev_url)



@api_view(['GET'])
def PostGet_API(request):
    post = PostText1.objects.all()
    # Apply pagination using your custom pagination class
    paginator = CustomPagination()
    paginated_queryset = paginator.paginate_queryset(post, request)
    serializer = PostSerializer(paginated_queryset, many= True)
    next_url = paginator.get_next_link()
    prev_url = paginator.get_previous_link()

    if next_url:
        next_url = next_url.replace(request.get_host(), settings.SITE_URL)

    if prev_url:
        prev_url = prev_url.replace(request.get_host(), settings.SITE_URL)
    return Response({
        'next_url':next_url,
        'prev_url':prev_url,
        'results':serializer.data})


@api_view(['GET'])
def TmdbMovies_API(request):
    movies = Movie.objects.all()
    # Apply pagination using your custom pagination class
    paginator = CustomPagination()
    paginated_queryset = paginator.paginate_queryset(movies, request)
    serializer = TmdbSerializer(paginated_queryset, many= True)
    next_url = paginator.get_next_link()
    prev_url = paginator.get_previous_link()

    if next_url:
        next_url = next_url.replace(request.get_host(), settings.SITE_URL)

    if prev_url:
        prev_url = prev_url.replace(request.get_host(), settings.SITE_URL)
    return Response({
        'next_url':next_url,
        'prev_url':prev_url,
        'results':serializer.data})


@api_view(['GET'])
def MoviePost_API(request, Movie_name):
    movie_posts = PostText1.objects.filter(Movie_name=Movie_name)

    paginator = CustomPagination()
    paginated_queryset = paginator.paginate_queryset(movie_posts, request)

    serializer = MoviePostSerializer(paginated_queryset, many=True)
    next_url = paginator.get_next_link()
    prev_url = paginator.get_previous_link()

    if next_url:
        next_url = next_url.replace(request.get_host(), settings.SITE_URL)

    if prev_url:
        prev_url = prev_url.replace(request.get_host(), settings.SITE_URL)
    return Response({
        'next_url':next_url,
        'prev_url':prev_url,
        'results':serializer.data})
    
@api_view(['GET'])
def Reviews_API(request, Movie_name):
    Reviews = Review.objects.filter(Movie_name = Movie_name)
    # Apply pagination using your custom pagination class
    paginator = CustomPagination()
    paginated_queryset = paginator.paginate_queryset(Reviews, request)
    serializer = ReviewSerializer(paginated_queryset, many= True)
    next_url = paginator.get_next_link()
    prev_url = paginator.get_previous_link()

    if next_url:
        next_url = next_url.replace(request.get_host(), settings.SITE_URL)

    if prev_url:
        prev_url = prev_url.replace(request.get_host(), settings.SITE_URL)
    return Response({
        'next_url':next_url,
        'prev_url':prev_url,
        'results':serializer.data})

@api_view(['GET'])
def AllReview_API(request):
    reviews = Review.objects.all()
    # Apply pagination using your custom pagination class
    paginator = CustomPagination()
    paginated_queryset = paginator.paginate_queryset(reviews, request)
    serializer = ReviewSerializer(paginated_queryset, many= True)
    next_url = paginator.get_next_link()
    prev_url = paginator.get_previous_link()

    if next_url:
        next_url = next_url.replace(request.get_host(), settings.SITE_URL)

    if prev_url:
        prev_url = prev_url.replace(request.get_host(), settings.SITE_URL)
    return Response({
        'next_url':next_url,
        'prev_url':prev_url,
        'results':serializer.data})

    
@api_view(['GET'])
def Trailers_API(request):
    trailer = CreateLabel.objects.all()
    # Apply pagination using your custom pagination class
    paginator = CustomPagination()
    paginated_queryset = paginator.paginate_queryset(trailer, request)
    serializer = TrailerSerializer(paginated_queryset , many=True)
    next_url = paginator.get_next_link()
    prev_url = paginator.get_previous_link()

    if next_url:
        next_url = next_url.replace(request.get_host(), settings.SITE_URL)

    if prev_url:
        prev_url = prev_url.replace(request.get_host(), settings.SITE_URL)
    return Response({
        'next_url':next_url,
        'prev_url':prev_url,
        'results':serializer.data})


@api_view(['GET'])
def ProducerInfo_API(request):
    producer = ProducerRegister.objects.all()
    serializer = ProducerInfoSerializer(producer, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def CombinedFeed_API(request):

    paginator = PageNumberPagination()
    paginator.page_size = 6  # Set your desired page size

    # Fetch data from different models
    feed = PostText1.objects.all()
    tmdb = Movie.objects.all()
    label = CreateLabel.objects.all()
    reviews = Review.objects.all()

    # Combine the data
    combined_data = list(feed) + list(tmdb) + list(label) + list(reviews)

    # Sort the combined data based on timestamp
    combined_data = sorted(combined_data, key=lambda x: x.timestamp_field, reverse=True)

    # Paginate the combined data
    paginated_data = paginator.paginate_queryset(combined_data, request)

    # Serialize the paginated data
    serialized_data = []
    for item in paginated_data:
        if isinstance(item, PostText1):
            serialized_data.append(posttext_serializer_feedpage(item).data)
        elif isinstance(item, Movie):
            serialized_data.append(tmdb_serializer_feedpage(item).data)
        elif isinstance(item, CreateLabel):
            serialized_data.append(createlabel_serializer_feedpage(item).data)
        elif isinstance(item, Review):
            serialized_data.append(review_srializer_feedpage(item).data)
    
    next_url = paginator.get_next_link()
    prev_url = paginator.get_previous_link()

    if next_url:
        next_url = next_url.replace(request.get_host(), settings.SITE_URL)

    if prev_url:
        prev_url = prev_url.replace(request.get_host(), settings.SITE_URL)
    return Response({
        'next_url':next_url,
        'prev_url':prev_url,
        'results':serialized_data})



import requests
from datetime import datetime
import cinystore.settings as settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .models import PhoneNumber, UserInfo, UserLogs

@api_view(['POST'])
def get_user_token(request):
    data = json.loads(request.body.decode('utf-8'))
    token = data['token']
    # token = "77a987e6969c4e0397f8fdf58ad6655e"
    CustomUser = get_user_model()
    print(CustomUser)

    url = 'https://cinystore.authlink.me'
    headers = {
        'clientId': settings.OTPless_CLIENT_ID,
        'clientSecret': settings.OTPless_CLIENT_SECRET_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        "token": token
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.status_code)
    json_response = response.json()
    user_data = json_response.get('data', json_response.get('user', {}))

    if response.status_code == 200 and user_data != {}:
        # Assuming the response contains user information

        # print('user_data:',user_data)
        try: 
            mobile = json_response.get('data').get('userMobile')
            email = json_response.get('data').get('userEmail')
            username = json_response.get('data').get('userName')
            timestamp = json_response.get('data').get('timestamp')
        except:
            mobile = json_response.get('user').get('waNumber')
            username = json_response.get('user').get('waName')
            timestamp = json_response.get('user').get('timestamp')

        # Check if the user already exists in the Django User model
        
        if CustomUser.objects.filter(username=username).exists():
            user = CustomUser.objects.get(username=username)
            user.last_login = timestamp
            # Update email in CustomUser model
            user.email = email
            user.save()
            # Update email in PhoneNumber model
            phone_number = PhoneNumber.objects.get(number=mobile)
            phone_number.email = email
            phone_number.save()
            user_info = UserInfo.objects.get(user_id=user.id)
            user_info.email = email
            user_info.save()
            
            #Adding user to userlogs table
            user_id = user.id
            login_time = datetime.now()
            login_log = UserLogs.objects.create(user_id=user_id, login_time=login_time)
            login_log.save()

            return Response({
                "status": 200, 
                "username": username,
                "email": email,
                "phone_number": mobile,
                "uid": user.phone_numbers.first().uid
            })
        else:
            user = CustomUser.objects.create_user(username=username,email=email)
            phone_number = PhoneNumber.objects.create(number=mobile, email = email) # Create a phone number instance
            user.phone_numbers.add(phone_number) # Associate the phone number with the user
            user.last_login = timestamp
            user.first_name= username.split(' ')[0]
            user.last_name= username.split(' ')[1] if len(username.split(' ')) > 1 else None
            user.is_user = True
            user.is_active = True
            user.save()
            customer = UserInfo.objects.create(user_id=user.id)
            customer.username = username
            customer.first_name = username.split(' ')[0]
            customer.last_name = username.split(' ')[1] if len(username.split(' ')) > 1 else None
            customer.email = email 
            customer.phone_number = mobile
            customer.save()

            #Adding user to userlogs table
            user_id = user.id
            login_time = datetime.now()
            login_log = UserLogs.objects.create(user_id=user_id, login_time=login_time)
            login_log.save()
            
            return Response({
                "status": 200,
                "username": username,
                "email": email,
                "phone_number": mobile, 
                "uid": phone_number.uid
            })
    else:
        # Handle the error if the request fails
        print(f"Request failed with status code: {response.status_code}")
        return Response({
            'status': 400,
            'message': 'Request failed!'
        })
    

@api_view(['POST'])
def LikePostAPI_Feedpage(request):
    data = json.loads(request.body)
    model_type = data.get('model_type')

    if data.get('post_id') is None:
        return Response({
            'status': 400,
            'message': 'Post_id not passed!' 
        })
    if data.get('uid') is None:
        return Response({
            'status': 400,
            'message': 'uid not passed!'
        })
    if data.get('model_type') is None:
        return Response({
            'status': 400,
            'message': 'model_type not passed!'
        })
    
    if model_type == 'movies':
        post_id = data.get('post_id')
        uid = data.get('uid')
        movie_obj = Movie.objects.get(id=post_id)
        try:
            phone_number_obj = PhoneNumber.objects.get(uid=uid)
            user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
            print(user_obj)
        except PhoneNumber.DoesNotExist:
            user_obj = UserInfo.objects.get(email=phone_number_obj.email)
        # Create a new instance of the Userlike model with the provided values
        if UserLikes.objects.filter(movie=movie_obj, user_id=user_obj.user_id, model_type = model_type).exists():
            return Response({
                'status': 400,
                'message': 'Like already exists!'
            })
        else: 
            like_post = UserLikes.objects.create(movie=movie_obj, user_id=user_obj.user_id, model_type = model_type)
            # update the like in the movie table
            like_count = Movie.objects.get(id=post_id).like_count
            Movie.objects.filter(id=post_id).update(like_count=like_count+1)

            return Response({
                'status': 200,
                'message': 'Like Recorded!'
            })
    # model for CreateLabel
    elif model_type == 'mydata':
        post_id = data.get('post_id')
        uid = data.get('uid')
        label_obj = CreateLabel.objects.get(id=post_id)
        try:
            phone_number_obj = PhoneNumber.objects.get(uid=uid)
            user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
            print(user_obj)
        except PhoneNumber.DoesNotExist:
            user_obj = UserInfo.objects.get(email=phone_number_obj.email)
        
        if UserLikes.objects.filter(label=label_obj, user_id=user_obj.user_id, model_type = model_type).exists():
            return Response({
                'status': 400,
                'message': 'Like already exists!'
            })
        else:
            # Create a new instance of the UserLikes model with the provided values
            like_post = UserLikes.objects.create(label=label_obj, user_id=user_obj.user_id, model_type = model_type)

            #update the like in the createlabel table
            like_count = CreateLabel.objects.get(id=post_id).like_count
            CreateLabel.objects.filter(id=post_id).update(like_count=like_count+1)
            return Response({
                'status': 200,
                'message': 'Like Recorded!'
            })
    # model for PostText
    elif model_type == 'mydata3':      
        post_id = data.get('post_id')
        uid = data.get('uid')
        post_obj = PostText1.objects.get(id=post_id)
        
        try:
            phone_number_obj = PhoneNumber.objects.get(uid=uid)
            user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
            print(user_obj)
        except PhoneNumber.DoesNotExist:
            user_obj = UserInfo.objects.get(email=phone_number_obj.email)
        if UserLikes.objects.filter(post=post_obj, user_id=user_obj.user_id, model_type = model_type).exists():
            return Response({
                'status': 400,
                'message': 'Like already exists!'
            })
        else:                
            # Create a new instance of the UserLikes model with the provided values
            like_post = UserLikes.objects.create(post=post_obj, user_id=user_obj.user_id, model_type = model_type)
            
            # update the like in the post table
            like_count = PostText1.objects.get(id=post_id).like_count
            PostText1.objects.filter(id=post_id).update(like_count=like_count+1)

            return Response({
                'status': 200,
                'message': 'Like Recorded!'
            })
    # model for Reviews
    elif model_type == 'mydata1':      
        post_id = data.get('post_id')
        uid = data.get('uid')
        review_obj = Review.objects.get(id=post_id)
        try:
            phone_number_obj = PhoneNumber.objects.get(uid=uid)
            user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
            print(user_obj)
        except PhoneNumber.DoesNotExist:
            user_obj = UserInfo.objects.get(email=phone_number_obj.email)
        
        if UserLikes.objects.filter(review = review_obj, user_id=user_obj.user_id, model_type = model_type).exists():
            return Response({
                'status': 400,
                'message': 'Like already exists!'
            })
        else:    
            # Create a new instance of the UserLikes model with the provided values
            like_post = UserLikes.objects.create(review=review_obj, user_id=user_obj.user_id, model_type = model_type)

            # update the like in the review table
            like_count = Review.objects.get(id=post_id).like_count
            Review.objects.filter(id=post_id).update(like_count=like_count+1)

            return Response({
                'status': 200,
                'message': 'Like Recorded!'
            })
    else:
        return Response({
            'status': 400,
            'message': 'Invalid model_type!'
        })
    
    
from django.utils.html import escape

@api_view(['POST'])
def CommentsAPI_Feedpage(request):
    data = json.loads(request.body)
    model_type = data.get('model_type')
    comment = data.get('comments')

    if data.get('post_id') is None:
        return Response({
            'status': 400,
            'message': 'Post_id not passed!' 
        })
    if data.get('uid') is None:
        return Response({
            'status': 400,
            'message': 'uid not passed!'
        })
    if data.get('model_type') is None:
        return Response({
            'status': 400,
            'message': 'model_type not passed!'
        })
    if data.get('comments') == "":
        return Response({
            'status': 400,
            'message': 'comment cannot be Null!'
        })
    if data.get('comments') is None:
        return Response({
            'status': 400,
            'message': 'comment not passed!'
        })
    
    sanitized_comment = escape(comment)

    if model_type == 'movies':
        post_id = data.get('post_id')
        uid = data.get('uid')
        movie_obj = Movie.objects.get(id=post_id)
        
        try:
            phone_number_obj = PhoneNumber.objects.get(uid=uid)
            user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
            print(user_obj)
        except PhoneNumber.DoesNotExist:
            user_obj = UserInfo.objects.get(email=phone_number_obj.email)

        # Create a new instance of the Userlike model with the provided values
        comment_post = UserComments.objects.create(movie=movie_obj, user_id=user_obj.user_id, comments = sanitized_comment, model_type = model_type)

        # update the comment in the movie table
        comment_count = Movie.objects.get(id=post_id).comment_count
        Movie.objects.filter(id=post_id).update(comment_count=comment_count+1)

        return Response({
            'status': 200,
            'message': 'Comment Recorded!'
        })
    # model for CreateLabel
    elif model_type == 'mydata':
        post_id = data.get('post_id')
        uid = data.get('uid')
        label_obj = CreateLabel.objects.get(id=post_id)
        
        try:
            phone_number_obj = PhoneNumber.objects.get(uid=uid)
            user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
            print(user_obj)
        except PhoneNumber.DoesNotExist:
            user_obj = UserInfo.objects.get(email=phone_number_obj.email)

        # Create a new instance of the UserLikes model with the provided values
        comment_post = UserComments.objects.create(label=label_obj, user_id=user_obj.user_id, comments = sanitized_comment, model_type = model_type)

        #update the comment in the createlabel table
        comment_count = CreateLabel.objects.get(id=post_id).comment_count
        CreateLabel.objects.filter(id=post_id).update(comment_count=comment_count+1)

        return Response({
            'status': 200,
            'message': 'Comment Recorded!'
        })
    # model for PostText
    elif model_type == 'mydata3':
        post_id = data.get('post_id')
        uid = data.get('uid')
        post_obj = PostText1.objects.get(id=post_id)

        try:
            phone_number_obj = PhoneNumber.objects.get(uid=uid)
            user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
            print(user_obj)
        except PhoneNumber.DoesNotExist:
            user_obj = UserInfo.objects.get(email=phone_number_obj.email)

        # Create a new instance of the UserLikes model with the provided values
        comment_post = UserComments.objects.create(post=post_obj, user_id=user_obj.user_id, comments = sanitized_comment, model_type = model_type)
        
        # update the comment in the post table
        comment_count = PostText1.objects.get(id=post_id).comment_count
        PostText1.objects.filter(id=post_id).update(comment_count=comment_count+1)

        return Response({
            'status': 200,
            'message': 'Comment Recorded!'
        })
    # model for Reviews
    elif model_type == 'mydata1':
        post_id = data.get('post_id')
        uid = data.get('uid')
        review_obj = Review.objects.get(id=post_id)

        try:
            phone_number_obj = PhoneNumber.objects.get(uid=uid)
            user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
            print(user_obj)
        except PhoneNumber.DoesNotExist:
            user_obj = UserInfo.objects.get(email=phone_number_obj.email)

        # Create a new instance of the UserLikes model with the provided values
        comment_post = UserComments.objects.create(review=review_obj, user_id=user_obj.user_id, comments = sanitized_comment, model_type = model_type)

        # update the comment in the review table
        comment_count = Review.objects.get(id=post_id).comment_count
        Review.objects.filter(id=post_id).update(comment_count=comment_count+1)

        return Response({
            'status': 200,
            'message': 'Comment Recorded!'
        })
    else:
        return Response({
            'status': 400,
            'message': 'Invalid model_type!'
        })
    

@api_view(['POST'])
def SharePostAPI_Feedpage(request):
    data = json.loads(request.body)
    model_type = data.get('model_type')

    if data.get('post_id') is None:
        return Response({
            'status': 400,
            'message': 'Post_id not passed!' 
        })
    if data.get('uid') is None:
        return Response({
            'status': 400,
            'message': 'uid not passed!'
        })
    if data.get('model_type') is None:
        return Response({
            'status': 400,
            'message': 'model_type not passed!'
        })
    
    if model_type == 'movies':
        post_id = data.get('post_id')
        uid = data.get('uid')
        movie_obj = Movie.objects.get(id=post_id)
        
        try:
            phone_number_obj = PhoneNumber.objects.get(uid=uid)
            user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
            print(user_obj)
        except PhoneNumber.DoesNotExist:
            user_obj = UserInfo.objects.get(email=phone_number_obj.email)

        # Create a new instance of the Userlike model with the provided values
        share_post = UserShares.objects.create(movie=movie_obj, user_id=user_obj.user_id, model_type = model_type)

        # update the share in the movie table
        share_count = Movie.objects.get(id=post_id).share_count
        Movie.objects.filter(id=post_id).update(share_count=share_count+1)

        return Response({
            'status': 200,
            'message': 'Share Recorded!'
        })
    # model for CreateLabel
    elif model_type == 'mydata':
        post_id = data.get('post_id')
        uid = data.get('uid')
        label_obj = CreateLabel.objects.get(id=post_id)
        
        try:
            phone_number_obj = PhoneNumber.objects.get(uid=uid)
            user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
            print(user_obj)
        except PhoneNumber.DoesNotExist:
            user_obj = UserInfo.objects.get(email=phone_number_obj.email)

        # Create a new instance of the UserLikes model with the provided values
        share_post = UserShares.objects.create(label=label_obj, user_id=user_obj.user_id, model_type = model_type)

        #update the share in the createlabel table
        share_count = CreateLabel.objects.get(id=post_id).share_count
        CreateLabel.objects.filter(id=post_id).update(share_count=share_count+1)

        return Response({
            'status': 200,
            'message': 'Share Recorded!'
        })
    # model for PostText
    elif model_type == 'mydata3':
        post_id = data.get('post_id')
        uid = data.get('uid')
        post_obj = PostText1.objects.get(id=post_id)

        try:
            phone_number_obj = PhoneNumber.objects.get(uid=uid)
            user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
            print(user_obj)
        except PhoneNumber.DoesNotExist:
            user_obj = UserInfo.objects.get(email=phone_number_obj.email)

        # Create a new instance of the UserLikes model with the provided values
        share_post = UserShares.objects.create(post=post_obj, user_id=user_obj.user_id, model_type = model_type)
        
        # update the share in the post table
        share_count = PostText1.objects.get(id=post_id).share_count
        PostText1.objects.filter(id=post_id).update(share_count=share_count+1)

        return Response({
            'status': 200,
            'message': 'Share Recorded!'
        })
    # model for Reviews
    elif model_type == 'mydata1':
        post_id = data.get('post_id')
        uid = data.get('uid')   
        review_obj = Review.objects.get(id=post_id)

        try:
            phone_number_obj = PhoneNumber.objects.get(uid=uid)
            user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
            print(user_obj)
        except PhoneNumber.DoesNotExist:
            user_obj = UserInfo.objects.get(email=phone_number_obj.email)

        # Create a new instance of the UserLikes model with the provided values
        share_post = UserShares.objects.create(review=review_obj, user_id=user_obj.user_id, model_type = model_type)

        # update the share in the review table
        share_count = Review.objects.get(id=post_id).share_count
        Review.objects.filter(id=post_id).update(share_count=share_count+1)

        return Response({
            'status': 200,
            'message': 'Share Recorded!'
        })
    else:
        return Response({
            'status': 400,
            'message': 'Invalid model_type!'
        })
    

@api_view(['POST'])
def FollowLabels_API(request):
    data = json.loads(request.body)
    model_type = data.get('model_type')

    if data.get('post_id') is None:
        return Response({
            'status': 400,
            'message': 'Post_id not passed!' 
        })
    if data.get('uid') is None:
        return Response({
            'status': 400,
            'message': 'uid not passed!'
        })
    if data.get('model_type') is None:
        return Response({
            'status': 400,
            'message': 'model_type not passed!'
        })
    if model_type == 'movies':
        post_id = data.get('post_id')
        uid = data.get('uid')
        movie_obj = Movie.objects.get(id=post_id)
        
        try:
            phone_number_obj = PhoneNumber.objects.get(uid=uid)
            user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
            print(user_obj)
        except PhoneNumber.DoesNotExist:
            user_obj = UserInfo.objects.get(email=phone_number_obj.email)

        if UserFollows.objects.filter(movie=movie_obj, user_id=user_obj.user_id, model_type=model_type).exists():
            return Response({
                'status': 400,
                'message': 'Follow already exists!'
            })
        else:
                
            # Create a new instance of the Userlike model with the provided values
            follow_post = UserFollows.objects.create(movie=movie_obj, user_id=user_obj.user_id, model_type = model_type)

            # update the follow in the movie table
            follow_count = Movie.objects.get(id=post_id).follow_count
            Movie.objects.filter(id=post_id).update(follow_count=follow_count+1)

            return Response({
                'status': 200,
                'message': 'Follow Recorded!'
            })
    
    # model for CreateLabel
    elif model_type == 'mydata':
        post_id = data.get('post_id')
        uid = data.get('uid')
        label_obj = CreateLabel.objects.get(id=post_id)
        
        try:
            phone_number_obj = PhoneNumber.objects.get(uid=uid)
            user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
            print(user_obj)
        except PhoneNumber.DoesNotExist:
            user_obj = UserInfo.objects.get(email=phone_number_obj.email)

        if UserFollows.objects.filter(label=label_obj, user_id=user_obj.user_id, model_type=model_type).exists():
            return Response({
                'status': 400,
                'message': 'Follow already exists!'
            })
        else:
            # Create a new instance of the UserLikes model with the provided values
            follow_post = UserFollows.objects.create(label=label_obj, user_id=user_obj.user_id, model_type = model_type)

            #update the follow in the createlabel table
            follow_count = CreateLabel.objects.get(id=post_id).follow_count
            CreateLabel.objects.filter(id=post_id).update(follow_count=follow_count+1)

            return Response({
                'status': 200,
                'message': 'Follow Recorded!'
            })
    else: 
        return Response({
            'status': 400,
            'message': 'Invalid model_type!'
        })
    
    
@api_view(['POST'])
def UserInformation_API(request):
    data = json.loads(request.body)
    uid = data.get('uid')
    if uid is None:
        return Response({
            'status': 400,
            'message': 'uid not passed!'
        })
    print(uid)
    try:
        phone_number_obj = PhoneNumber.objects.get(uid=uid)
        user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
        print(user_obj)
    except PhoneNumber.DoesNotExist:
        user_obj = UserInfo.objects.get(email=phone_number_obj.email)
    print(user_obj)
    serializer = UserInfoSerializer(user_obj)
    return Response(serializer.data)


@api_view(['GET'])
def TermsGet_API(request):
    terms = Terms.objects.all()
    serializer = terms_serializer(terms, many=True)

    return Response({
        'results': serializer.data
    })

@api_view(['GET'])
def PrivacyGet_API(request):
    privacy = Privacy1.objects.all()
    serializer = privacy_serializer(privacy, many=True)

    return Response({
        'results': serializer.data
    })


@api_view(['POST'])
def SearchResults_API(request):
    data = json.loads(request.body)
    print(data)
    search_query = data['search_query']
    result_dict = {}
    # Search for movies

    search_results_Movie = Movie.objects.filter(Q(genre__icontains=search_query) | 
                                                Q(movie_title__icontains = search_query) | 
                                                Q(language__icontains=search_query) |
                                                Q(producer__icontains=search_query) |
                                                Q(director__icontains=search_query) |
                                                Q(music_director__icontains=search_query) |
                                                Q(crew__icontains=search_query) |
                                                Q(cast__icontains=search_query) 
                                                ).values()
    result_dict['International_movies']= (search_results_Movie)
    
    # Search for labels
    search_results_CreateLabel = CreateLabel.objects.filter(Q(Language__icontains=search_query) |
                                                            Q(Movie_name__icontains=search_query) |
                                                            Q(Genre__icontains=search_query) |
                                                            Q(Production_house__icontains=search_query) |
                                                            Q(Producer__icontains=search_query) |
                                                            Q(cast__icontains=search_query) |
                                                            Q(Director__icontains=search_query) |
                                                            Q(Music_director__icontains=search_query) |
                                                            Q(Other_Languages__icontains=search_query) |
                                                            Q(lyricist__icontains=search_query) |
                                                            Q(choreographer__icontains=search_query) |
                                                            Q(Script_writer__icontains=search_query) |
                                                            Q(Distribution__icontains=search_query) | 
                                                            Q(Singers__icontains=search_query) |
                                                            Q(Editor__icontains=search_query) |
                                                            Q(Cinematographer__icontains=search_query)
                                                            ).values()
    result_dict['Label']=(search_results_CreateLabel)

    # Search for posts
    search_results_Post = PostText1.objects.filter(Movie_name__icontains=search_query).values()
    result_dict['Post']= (search_results_Post)
    
    # Search for reviews
    search_results_Review = Review.objects.filter(
                                                    Q(author__icontains=search_query) |
                                                    Q(Movie_name__icontains=search_query)).values()
    result_dict['Reviews']= (search_results_Review)

    return Response({
        'status': 200,
        'result_dict': result_dict
    })
