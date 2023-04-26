from django.urls import path
from .views import SignupView, EditProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "user"
urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("edit/", EditProfileView.as_view(), name="edit"),
]
