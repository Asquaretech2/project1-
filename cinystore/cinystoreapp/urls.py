from django.urls import path
from django.urls import path, include
from django.contrib import admin
from . import views
from . import api_views
from .api_views import *
from corporate.views import index

urlpatterns = [
    path('', views.index, name='index'),
    path('auth_login/', views.auth_login, name='auth_login'),
    path('Authregister/', views.Authregister, name='Authregister'),
    path('home/', views.Home, name='Home'),
    path('Browsemovies/', views.Browsemovies, name='Browsemovies'),
    path('CalendarAndEvents/', views.CalendarAndEvents, name='CalendarAndEvents'),
    path('ChangePassword/', views.ChangePassword, name='ChangePassword'),
    path('Feedpage/', views.Feedpage, name='Feedpage'),
    path('Createlabel/', views.Createlabel, name='Createlabel'),
    path('Groups/', views.Groups, name='Groups'),
    path('generalblogs/', views.generalblogs, name='generalblogs'),
    path('MoviePhotos/', views.MoviePhotos, name='MoviePhotos'),
    path('MovieVideos/', views.MovieVideos, name='MovieVideos'),
    path('Newsfeed/', views.Newsfeed, name='Newsfeed'),
    path('publicfeed/', views.publicfeed, name='publicfeed'),
    path('producerphotoupload/', views.producerphotoupload, name='producerphotoupload'),
    path('Producerregisterpage/', views.Producerregisterpage, name='Producerregisterpage'),
    path('Business/', views.Business, name='Business'),
    path('Producerlogoutpage/', views.Producerlogoutpage, name='Producerlogoutpage'),
    path('producerhead/', views.producerhead, name='producerhead'),
    path('producerdashboard/<str:production_house>/', views.producerdashboardwithmovie, name='producerdashboard'),
    path('producerdashboard/', views.producerdashboard, name='producerdashboard'),
    path('producervideoupload/', views.producervideoupload, name='producervideoupload'),
    path('badges/', views.badges, name='badges'),
    path('stats/', views.stats, name='stats'),
    path('music/', views.music, name='music'),
    path('corporate/', views.corporate, name='corporate'),
    path('Usertrailer/', views.Usertrailer, name='Usertrailer'),
    path('head/', views.head, name='head'),
    path('Poster/', views.Poster, name='Poster'),
    path('genreviews/', views.genreviews, name='genreviews'),
    path('StickySidebars/', views.StickySidebars, name='StickySidebars'),
    path('Masonry/', views.Masonry, name='Masonry'),
    path('movies/', views.tmdb_movies, name='movies'),
    path('now_playing/', views.now_playing, name='now_playing'),
    path('top_rated/', views.top_rated, name='top_rated'),
    path('Label2/<path:movie_title>/', views.Label2, name='Label2'),
    path('Labeltmdb/<path:movie_title>/', views.Labeltmdb, name='Labeltmdb'),
    path("review/", views.review, name="review"),
    path("faq/", views.faq, name="faq"),
    path("career/", views.career, name="career"),
    path('activate/<uid64>/<token>', views.activate, name='activate'),
    path('activate1/<uid64>/<token>', views.activate1, name='activate1'),
    path('activation_success/', views.activation_success, name='activation_success'),
    path('producer_activation_success/', views.producer_activation_success, name='producer_activation_success'),
    path('auth_Logout/', views.auth_Logout, name='auth_Logout'),
    path("disclaimer/", views.disclaimer, name="disclaimer"),
    path('userreview_label/<str:Movie_name>/', views.userreview_label, name='userreview_label'),
    path('review_label/<str:Movie_name>/', views.review_label, name='review_label'),
    path('Box_office/',views.Box_office, name="Box_office"),
    path('genBox_office/', views.genBox_office, name="genBox_office"),
    path('Box_office_label/<str:Movie_name>/',views.Box_office_label, name="Box_office_label"),
    path('error/', views.error_view, name='error'),
    path('genblog/', views.genblog, name='genblog'),
    path('blog/', views.blog, name='blog'),
    path('Indianmovies/', views.Indianmovies, name="Indianmovies"),
    path('Internationalmovies/', views.Internationalmovies, name="Internationalmovies"),
    path('Managelabel/', views.Managelabel, name='Managelabel'),
    path('producerbase/', views.producerbase,  name='producerbase'),
    path('web_createlabel/', views.web_createlabel, name='web_createlabel'),
    path('web_createlabel1/', views.web_createlabel1, name='web_createlabel1'),
    path('labels/', views.labels, name='labels'),
    path('episodeupload/', views.episodeupload, name='episodeupload'),
    path('episodeupload2/', views.episodeupload2, name='episodeupload2'),
    path('episodeupload1/', views.episodeupload1, name='episodeupload1'),
    path('producermanagelabel/<str:Movie_name>/', views.producermanagelabel, name='producermanagelabel'),
    path('templates/<str:Movie_name>/', views.templates, name='templates'),
    path('userreviews/', views.userreviews, name='userreviews'),
    path('PostTextView/', views.PostTextView, name='PostTextView'),
    path('PostText/', views.PostText, name='PostText'),
    path('socialuserlogin/', views.socialuserlogin, name='socialuserlogin'),
    path('comingsoonlabel/', views.comingsoonlabel, name='comingsoonlabel'),
    path('Newsform/', views.Newsform, name='Newsform'),
    path('reset_password/',views.reset_password, name="reset_password"),
    path('ResetConfirm/<uid64>/<token>/', views.ResetConfirm, name='ResetConfirm'),
    path('check_username_availability', views.check_username_availability, name='check_username_availability'),
    path('check_email_availability', views.check_email_availability, name='check_email_availability'),
    path('change_password/', views.change_password, name='change_password'),
    path('PersonalInformation/', views.PersonalInformation, name='PersonalInformation'),
    path('UpdatePersonalInformation/', views.PersonalInformation_update, name='UpdatePersonalInformation'),
    path('labelof/<str:Movie_name>/', views.labelof, name='labelof'),
    path('publiclabel/<str:Movie_name>/', views.publiclabel, name='publiclabel'),
    path('like_movie/<str:Movie_name>/', views.like_movie, name='like_movie'),
    path('follow_movie/<str:Movie_name>/', views.follow_movie, name='follow_movie'),
    path('like_post_text/<int:id>/', views.like_post_text, name='like_post_text'),
    path('follow_post_text/<int:id>/', views.follow_post_text, name='follow_post_text'),
    path('comment_post_text/<int:id>/', views.comment_post_text, name='comment_post_text'),
    path('check_movie_exists/', views.check_movie_exists, name='check_movie_exists'),
    path('producer_reset_password/', views.producer_reset_password, name= 'producer_reset_password'),
    path('ProducerResetConfirm/<uid64>/<token>/', views.ProducerResetConfirm, name='ProducerResetConfirm'),
    path('profile/', views.profile, name='profile'),
    path('UpdateProfile/', views.UpdateProfile, name='UpdateProfile'),
    path('producer_change_password/', views.producer_change_password, name='producer_change_password'),
    path('Advantages/', views.Advantages, name ='Advantages'),
    path('Pricing/', views.Pricing, name ='Pricing'),
    path('Privacy/', views.Privacy, name ='Privacy'),
    path('terms/', views.terms, name ='terms'),
    path('moviestats/<str:Movie_name>/', views.moviestats, name ='moviestats'),
    path('browsemovies/', views.Browsemovies_login, name='browsemovies'),
    path('webseries_label/', views.webseries_label, name='webseries_label'),
    path('searchresult/', views.searchresult, name='searchresult'),
    path('Privacy_form/', views.Privacy_form, name='Privacy_form'),
    path('terms_form/', views.terms_form, name='terms_form'),
    path('notification/', views.notification, name='notification'),
    path('promo/<str:Movie_name>/', views.promo, name='promo'),
    path('post_promo/<str:Movie_name>/', views.post_promo, name='post_promo'),
    path('tmdb_promo/<path:movie_title>/', views.tmdb_promo, name='tmdb_promo'),
    path('review_promo/<str:slug>/', views.review_promo, name='review_promo'),
    path('promo/<str:slug>/', views.promo, name='promo'),
    path('post_promo/<str:slug>/', views.post_promo, name='post_promo'),
    path('tmdb_promo/<path:movie_title>/', views.tmdb_promo, name='tmdb_promo'),
    path('review_promo/<str:slug>/', views.review_promo, name='review_promo'),
    path('clip_promo/<str:Movie_name>/', views.clip_promo, name='clip_promo' ),
    path('Clip/', views.Clip, name='Clip'),
    path('like_clip/<int:id>/', views.like_clip, name='like_clip'),
    path('follow_clip/<int:id>/', views.follow_clip, name='follow_clip'),
    path('comment_clip/<int:id>/', views.comment_clip, name='comment_clip'),

    # URL Paths for the API
    #path('PersonalInfo_API', api_views.PersonalInfo_API, name= 'PersonalInfo_Api'),
    path('CreateLabelGet_API', api_views.CreateLabelGet_API, name = 'CreateLabelGet_API'),
    path('PostGet_API', api_views.PostGet_API, name='PostGet_API'),
    path('TmdbMovies_API', api_views.TmdbMovies_API, name='TmdbMovies_API'),
    path('MoviePost_API/<str:Movie_name>', api_views.MoviePost_API, name = 'MoviePost_API'),
    path('Reviews_API/<str:Movie_name>', api_views.Reviews_API, name = 'Reviews_API'),
    path('Trailers_API/', api_views.Trailers_API, name = 'Trailers_API'),
    path('AllReview_API', api_views.AllReview_API, name = 'AllReview_API'),
    path('ProducerInfo_API/', api_views.ProducerInfo_API, name = 'ProducerInfo_API'),
    path('CombinedFeed_API', api_views.CombinedFeed_API, name = 'CombinedFeed_API'),
    path('get_user_token/', api_views.get_user_token, name = 'get_user_token'),
    
    path('LikePostAPI_Feedpage/', api_views.LikePostAPI_Feedpage, name = 'LikePostAPI_Feedpage'),
    path('CommentsAPI_Feedpage/', api_views.CommentsAPI_Feedpage, name = 'CommentsAPI_Feedpage'),
    path('SharePostAPI_Feedpage/', api_views.SharePostAPI_Feedpage, name = 'SharePostAPI_Feedpage'),
    path('FollowLabels_API/', api_views.FollowLabels_API, name = 'FollowLabels_API'),
    path('UserInformation_API/', api_views.UserInformation_API, name = 'UserInformation_API'),
    path('SearchResults_API/', api_views.SearchResults_API, name = 'SearchResults_API'),
    path('PrivacyGet_API/', api_views.PrivacyGet_API, name='PrivacyGet_API'),
    path('TermsGet_API/', api_views.TermsGet_API, name='TermsGet_API'),

]






