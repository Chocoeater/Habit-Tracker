from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from users import serializers

from users.models import User
from users.permissions import IsOwnerOrAdmin


# Create your views here.


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrAdmin, IsAuthenticated]
    lookup_field = "pk"

    def get_serializer_class(self):
        if getattr(self, "swagger_fake_view", False):
            return serializers.UserRetrieveSerializer

        if self.action == "list":
            if self.request.user.is_staff:
                return serializers.UserListSerializer
            return serializers.PublicUserListSerializer

        if self.action == "retrieve":
            user = self.get_object()
            if self.request.user == user or self.request.user.is_staff:
                return serializers.UserRetrieveSerializer
            return serializers.PublicUserRetrieveSerializer

        return serializers.UserRetrieveSerializer

    def create(self, request, *args, **kwargs):
        return Response(
            {"detail": "Регистрация новых пользователей доступна только через /register/"},
            status=status.HTTP_403_FORBIDDEN,
        )


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.UserCreateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer
    permission_classes = [AllowAny]
