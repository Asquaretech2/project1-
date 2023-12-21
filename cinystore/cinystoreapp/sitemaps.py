from django.contrib import sitemaps
from django.urls import reverse



class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'
    protocol = 'http'

    def items(self):
        return [
            'Home',
            'auth_login',
            'Authregister',
            'Browsemovies',
            'CalendarAndEvents',
            'ChangePassword',
            'Feedpage',
            'Createlabel',
            'Groups',
            'generalblogs',
            'MoviePhotos',
            'MovieVideos',
            'Newsfeed',
            'publicfeed',
            'producerphotoupload',
            'Producerregisterpage',
            'Business',
            'Producerlogoutpage',
            'producerhead',
            'producerdashboard',
            'producervideoupload',
            'badges',
            'stats',
            'music',
            'Usertrailer',
            'head',
            'Poster',
            'genreviews',
            'StickySidebars',
            'Masonry',
            'movies',
            'review',
            'faq',
            'career',
            'activation_success',
            'producer_activation_success',
            'auth_Logout',
            'disclaimer',
            'Box_office',
            'genBox_office',
            'error',
            'genblog',
            'blog',
            'Indianmovies',
            'Internationalmovies',
            'Managelabel',
            'producerbase',
            'web_createlabel',
            'web_createlabel1',
            'labels',
            'episodeupload',
            'episodeupload2',
            'episodeupload1',
            'userreviews',
            'PostTextView',
            'PostText',
            'socialuserlogin',
            'comingsoonlabel',
            'Newsform',
            'reset_password',
            'check_username',
            'change_password',
            'PersonalInformation',
            'UpdatePersonalInformation',
            'check_movie_exists',
            'producer_reset_password',
            'profile',
            'UpdateProfile',
            'producer_change_password',
            'Advantages',
            'Pricing',
            'Privacy',
            'terms',
            'browsemovies',
            'webseries_label',
            'searchresult',
            'Privacy_form',
            'terms_form',
            'notification',
            # 'moviestats/<str:Movie_name>/',
            # 'ProducerResetConfirm/<uid64>/<token>/',
            # 'labelof/<str:Movie_name>/',
            # 'publiclabel/<str:Movie_name>/',
            # 'like_movie/<str:Movie_name>/',
            # 'follow_movie/<str:Movie_name>/',
            # 'like_post_text/<int:id>/',
            # 'follow_post_text/<int:id>/',
            # 'comment_post_text/<int:id>/',
            # 'promo/<str:Movie_name>/',
            # 'post_promo/<str:Movie_name>/',
            # 'tmdb_promo/<:movie_title>/',
            # 'review_promo/<str:Movie_name>/',
            # 'ResetConfirm/<uid64>/<token>/',
            # 'producerdashboard/<str:production_house>/',
            # 'Label2/<:movie_title>/',
            # 'Labeltmdb/<:movie_title>/',
            # 'activate/<uid64>/<token>/',
            # 'activate1/<uid64>/<token>/',
            # 'userreview_label/<str:Movie_name>/',
            # 'review_label/<str:Movie_name>/',
            # 'Box_office_label/<str:Movie_name>/',
            # 'producermanagelabel/<str:Movie_name>/',
            # 'templates/<str:Movie_name>/',
        ]

    def location(self, item):
        return reverse(item)