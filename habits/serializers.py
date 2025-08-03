from rest_framework.serializers import ModelSerializer

from habits.models import Habit
from habits import validators


class MyHabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = ['place', 'time_to_do', 'action', 'frequency', 'tag_pleasant_habit', 'linked_habit', 'reward', 'duration', 'tag_public']

    def validate(self, attrs):
        validators.validate_mutually_exclusive_fields(attrs)
        validators.validate_pleasant_and_useful_habit(attrs)
        validators.validate_duration(attrs)
        validators.validate_frequency(attrs)
        return attrs