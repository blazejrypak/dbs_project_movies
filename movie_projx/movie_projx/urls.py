"""movie_projx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url, include
from movie_app import views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^special/', views.special, name='special'),
    url(r'^movies/', include('movie_app.urls'), name='movie_app'),
    url(r'^register/$', views.register, name='register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^dashboard/$', views.dashboard, name='dashboard_base'),
    url(r'^dashboard/reviews$', views.dashboard_reviews, name='dashboard_reviews'),
    url(r'^dashboard/reports$', views.dashboard_reports, name='dashboard_reports'),
    path('dashboard/reviews/remove/<int:review_id>/', views.dashboard_delete_review, name='dashboard_review_delete'),
    path('dashboard/reviews/update/<int:review_id>/', views.dashboard_update_review, name='dashboard_review_update'),
    url(r'^dashboard/account/settings$', login_required(views.dashboard_settings), name='dashboard_account_settings'),
]


