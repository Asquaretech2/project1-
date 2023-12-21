from django.db import models
from django.forms import fields
from .models import CreateLabel
from django import forms
from django.forms import Textarea
from .models import Review
from django.forms import ModelForm
from .models import *




class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = CreateLabel
        fields = ('Movie_name','Language','Genre','Production_house','Producer','Director','Music_director','cast','Poster','Release_date','synopsis','trailer','Banner','Other_Languages','lyricist','choreographer','Script_writer','Running_Time','Maturity','Budget','Distribution','Recording_studio','Graphic_designer', 'Url_name', 'Singers', 'Editor', 'Cinematographer')
        widgets = {
            "synopsis": Textarea(
                attrs={'rows':4, 'cols':100 }
            )
        }
        Other_Languages = forms.CharField(required=False) 
        lyricist = forms.CharField(required=False)
        Singers = forms.CharField(required=False) 
        choreographer = forms.CharField(required=False) 
        Script_writer = forms.CharField(required=False) 
        Editor = forms.CharField(required=False) 
        Running_Time = forms.CharField(required=False) 
        Maturity = forms.CharField(required=False)
        Cinematographer = forms.CharField(required=False) 
        Graphic_designer = forms.CharField(required=False) 
        Distribution = forms.CharField(required=False) 
        Budget = forms.CharField(required=False) 
        Recording_studio = forms.CharField(required=False) 
        
		
	 

class WebseriesForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = WebSeriesLabel
        fields = ('webseries_name','Language','Genre','Production_house','Producer','Director','cast','Poster','Release_date','synopsis','trailer','season','episodes','streaming_on',)
        widgets = {
            "synopsis": Textarea(
                attrs={'rows':4, 'cols':100 }
            )

        }
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author', 'Movie_name', 'stars', 'review_date', 'comment']
        widgets = {
            "comment": Textarea(
                attrs={'rows':4, 'cols':100 }
            )

        }

class BoxOfficeForm(forms.ModelForm):
    class Meta:
        model = BoxOffice
        fields = ['Movie_name', 'production_house', 'movie_collections', 'day_collections', 'weekly_collections', 'month_collections']


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['Poster', 'content']
        widgets = {
            "content": Textarea(
                attrs={'rows': 4, 'cols': 100}
            )
        }


class PostTextForm(forms.ModelForm):
    class Meta:
        model = PostText1
        fields = ['Heading','Movie_name','text','Image']
        widgets = {
            "text": Textarea(
                attrs={'rows': 4, 'cols': 100}),
            #'images': forms.ClearableFileInput(attrs={'multiple': True}),


        }

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['Movie_name', 'text', 'author']
        widgets = {
            "content": Textarea(
                attrs={'rows': 4, 'cols': 100}
            )
        }


class VideoClipsForm(forms.ModelForm):
    class Meta:
        model = Clips
        fields = ['Heading','text','Movie_name','Video','Image']
        widgets = {
            "text": Textarea(attrs={'rows': 4, 'cols': 100}),
            'Movie_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


