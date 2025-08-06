from rest_framework.exceptions import ValidationError


def validate_mutually_exclusive_fields(attrs, instance=None):
    """Валидация, что выбрано либо приятная привычка, либо вознаграждение"""

    linked_habit = attrs.get("linked_habit", None)
    reward = attrs.get("reward", None)

    if instance:
        if linked_habit is None:
            linked_habit = instance.linked_habit
        if reward is None:
            reward = instance.reward

    if linked_habit and reward:
        raise ValidationError("Укажите либо вознаграждение, либо вознаграждающую привычку.")
    if not linked_habit and not reward:
        raise ValidationError(
            "Должно быть указано либо вознаграждение (поле reward), либо вознаграждающая привычка (linked_habit)."
        )


def validate_pleasant_and_useful_habit(attrs, instance=None):
    """Валидация, что приятная привычка не ссылается на полезную, приятную и не имеет вознаграждения,
    а полезная привычка ссылается только на приятную"""

    tag_pleasant_habit = attrs.get("tag_pleasant_habit", None)
    linked_habit = attrs.get("linked_habit", None)
    reward = attrs.get("reward", None)

    if instance:
        if linked_habit is None:
            linked_habit = instance.linked_habit
        if reward is None:
            reward = instance.reward
        if tag_pleasant_habit is None:
            tag_pleasant_habit = instance.tag_pleasant_habit

    if tag_pleasant_habit:
        if linked_habit or reward:
            raise ValidationError("Приятная привычка не должна ссылаться на другие привычки или иметь вознаграждение")
    else:
        if linked_habit:
            if not linked_habit.tag_pleasant_habit:
                raise ValidationError("Полезная привычка не может являться привычкой-вознаграждением")


def validate_duration(attrs, instance=None):
    duration = attrs.get("duration", None)

    if instance:
        if duration is None:
            duration = instance.duration

    if duration > 120:
        raise ValidationError("Длительность привычки не должна превышать 120 с.")


def validate_frequency(attrs, instance=None):
    frequency = attrs.get("frequency", None)

    if instance:
        if frequency is None:
            frequency = instance.frequency

    if frequency:
        if frequency > 7:
            raise ValidationError("Привычка должна выполняться хотя бы раз в неделю.")
    else:
        raise ValidationError("Задайте периодичность (поле frequency)")
