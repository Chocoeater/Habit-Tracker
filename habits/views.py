from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from habits.models import Habit
from habits.paginators import MyPaginator
from habits.permissions import IsOwnerOrAdmin
from habits.serializers import MyHabitSerializer, PublicHabitSerializer


class HabitViewSet(ModelViewSet):
    pagination_class = MyPaginator
    serializer_class = MyHabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            # Для генерации схемы - возвращаем пустой queryset
            return Habit.objects.none()
        if self.request.user.is_staff:
            return Habit.objects.all()
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PublicHabitViewSet(ReadOnlyModelViewSet):
    pagination_class = MyPaginator
    serializer_class = PublicHabitSerializer

    def get_queryset(self):
        return Habit.objects.filter(tag_public=True)
