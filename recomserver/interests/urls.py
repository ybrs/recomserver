from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .views import Similar, SimilarWithInterests, SimilarWithMatchCount

urlpatterns = [
    url(r'^similar/([0-9]+)/$', Similar.as_view()),
    # these are for debugging mostly
    url(r'^similar-with-interest/([0-9]+)/$', SimilarWithInterests.as_view()),
    url(r'^similar-with-matchcount/([0-9]+)/$', SimilarWithMatchCount.as_view()),

]
