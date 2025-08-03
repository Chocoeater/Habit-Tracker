from rest_framework.exceptions import ValidationError


def validate_mutually_exclusive_fields(attrs):
    """Валидация, что выбрано либо приятная привычка, либо вознаграждение"""

    linked_habit = attrs.get('linked_habit')
    reward = attrs.get('reward')

    if linked_habit and reward:
        raise ValidationError('Укажите либо вознаграждение, либо вознаграждающую привычку.')
    if not linked_habit and not reward:
        raise ValidationError('Должно быть указано либо вознаграждение, либо вознаграждающая привычка.')


def validate_pleasant_and_useful_habit(attrs):
    """Валидация, что приятная привычка не ссылается на полезную, приятную и не имеет вознаграждения,
     а полезная привычка ссылается только на приятную"""

    tag_pleasant_habit = attrs.get('tag_pleasant_habit')
    linked_habit = attrs.get('linked_habit')
    reward = attrs.get('reward')

    if tag_pleasant_habit:
        if linked_habit or reward:
            raise ValidationError('Приятная привычка не должна ссылаться на другие привычки или иметь вознаграждение')
    else:
        if linked_habit:
            if not linked_habit.tag_pleasant_habit:
                raise ValidationError('Полезная привычка не может являться привычкой-вознаграждением')

