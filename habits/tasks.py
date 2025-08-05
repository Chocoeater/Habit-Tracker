from celery import shared_task
from users.telegram_bot import send_telegram_notification

from celery import shared_task
from django.contrib.auth import get_user_model
from users.telegram_bot import send_telegram_notification

User = get_user_model()


@shared_task
def send_daily_habits():
    users = User.objects.filter(telegram_id__isnull=False)  # Только у кого есть telegram_id

    for user in users:
        habits = user.habits.filter(tag_pleasant_habit=False)  # Все привычки пользователя

        if not habits:
            continue  # Пропускаем, если привычек нет

        # Формируем сообщение
        message = "📅 Ваши привычки на сегодня:\n\n"
        for i, habit in enumerate(habits, start=1):
            if habit.reward:
                prize = habit.reward
            else:
                prize = habit.linked_habit
            message += (
                f"{i}. [{habit.time_to_do.strftime('%H:%M')}] "
                f"{habit.action} ({habit.place}, {habit.duration} сек)\n"
                f"Награда: {prize}"
            )

        # Отправляем в Telegram
        send_telegram_notification(
            telegram_id=user.telegram_id,
            message=message
        )