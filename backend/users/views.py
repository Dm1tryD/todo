from django.contrib.auth import logout, login
from rest_framework import views, generics, response, permissions, authentication
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return


class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return response.Response(UserSerializer(user).data)


class LogoutView(views.APIView):

    def get(self, request):
        logout(request)
        return response.Response()


class RegisterView(generics.CreateAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)

    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
