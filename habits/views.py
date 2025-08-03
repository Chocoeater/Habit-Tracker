
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit


class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class =