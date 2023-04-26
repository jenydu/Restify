from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import LoginView, RegisterView, LogoutView, ProfileViewView, ProfileEditView

app_name = 'accounts'
urlpatterns = [
    path('register/', RegisterView.as_view(),name='register'),
    path('login/', LoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(), name="logout"),

    path('profile/view/', ProfileViewView.as_view(), name="profile_view"),
    path('profile/edit/', ProfileEditView.as_view(), name="profile_edit"),
]