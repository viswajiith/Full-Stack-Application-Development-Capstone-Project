from django.contrib import admin
from django.urls import path
from djangoapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dealer/<int:dealer_id>/', views.dealer_details, name='dealer_details'),
    path('dealer/<int:dealer_id>/add_review/', views.add_review, name='add_review'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('sentimentAnalyzer/', views.sentiment_analyzer, name='sentiment'),
]
