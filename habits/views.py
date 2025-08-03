
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.paginators import MyPaginator
from habits.serializers import MyHabitSerializer


class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = MyHabitSerializer
    pagination_class = MyPaginator
