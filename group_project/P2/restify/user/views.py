from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from .models import User
from .serializers import SignupSerializer, EditProfileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


"""class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # user = serializer.validated_data["user"]
        token = serializer.validated_data["token"]
        refresh_token = serializer.validated_data["refresh"]
        response = Response(
            {
                "access_token": token,
                "refresh_token": refresh_token,
            },
            status=status.HTTP_200_OK,
        )
        response.set_cookie(key="jwt", value=token, httponly=True)
        return response
"""


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# not required for P2
"""
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "You have been logged out."})
        except Exception as e:
            return Response({"error": str(e)}, status=400)
"""


class EditProfileView(RetrieveUpdateAPIView):
    serializer_class = EditProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
