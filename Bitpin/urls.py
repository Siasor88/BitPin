"""
URL configuration for Bitpin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rating_app.views.PostViews import PostListView
from rating_app.views.RatingViews import *


urlpatterns = [
    path("admin/", admin.site.urls),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<uuid:post_id>/rate/', SubmitRatingView.as_view(), name='submit-rating'),
]
