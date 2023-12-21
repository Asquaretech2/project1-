# Register your models here.
from django.contrib import admin
from .models import *


class imageAdmin(admin.ModelAdmin):
        list_display = ["Movie_name", "Poster", "get_date"]

admin.site.register(Blog)
admin.site.register(BoxOffice)
admin.site.register(CreateLabel)
admin.site.register(Review)
admin.site.register(PostText1)
admin.site.register(User)
admin.site.register(UserInfo)
admin.site.register(ProducerRegister)
admin.site.register(FollowPostText1)
admin.site.register(LikePostText1)
admin.site.register(Movie)
admin.site.register(News)
admin.site.register(CommentPostText1)









