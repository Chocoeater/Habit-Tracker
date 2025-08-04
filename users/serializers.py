from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from habits.serializers import PublicHabitSerializer, MyHabitSerializer
from users.models import User



class PublicUserListSerializer(ModelSerializer):
    """Сериализатор для публичного списка пользователей"""

    class Meta:
        model = User
        fields = ['id', 'username']

class UserListSerializer(ModelSerializer):
    """Сериализатор списка пользователей для админа"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'is_active']


class UserRetrieveSerializer(ModelSerializer):
    """Сериализатор для владельца и для админа"""

    habits = MyHabitSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'habits']

class PublicUserRetrieveSerializer(ModelSerializer):
    """Сериализатор для прочих пользователей"""

    public_habits = SerializerMethodField()

    def get_public_habits(self, obj):
        public_habits = obj.habit_set.filter(tag_public=True)
        return PublicHabitSerializer(public_habits, many=True, read_only=True)


    class Meta:
        model = User
        fields = ['username', 'first_name', 'date_joined', 'public_habits']


class UserCreateSerializer(ModelSerializer):
    """Сериализатор для создания пользователя"""

    class Meta:
        model = User
        fields = ["id", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email

        return token
