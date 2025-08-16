from django.urls import path
from rest_framework.routers import DefaultRouter
from users.views import MyTokenObtainPairView, UserCreateAPIView
from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name


router = DefaultRouter()
router.register(r"users", views.UserViewSet, basename="users")

urlpatterns = [
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("register/", UserCreateAPIView.as_view(), name="user_create"),
] + router.urls
