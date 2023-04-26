from django.urls import path
from .views import SignupView, EditProfileView, get_user
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "user"
urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("edit/", EditProfileView.as_view(), name="edit"),
    path('<int:user_id>/', get_user, name='get_user'),
]
