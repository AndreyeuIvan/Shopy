from django.contrib.auth import login, logout

from rest_framework import generics, permissions, status, views, response, request
from my_auth.serializers import LoginSerializer, UserSerializer, UserRegisterSerializer
from my_auth.models import User


class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request: request.Request, *args, **kwargs):

        serializer = LoginSerializer(
            data=self.request.data, context={"request": self.request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return response.Response(
            {"id": user.id, "username": user.username}, status=status.HTTP_202_ACCEPTED
        )


class LogoutView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request: request.Request, *args, **kwargs):
        logout(request)
        return response.Response(status=status.HTTP_200_OK)


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = ()


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request: request.Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request: request.Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
