from rest_framework.routers import DefaultRouter

from habits import views
from habits.apps import HabitsConfig

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r"my_habits", views.HabitViewSet, basename="my_habits")
router.register(r"public_habits", views.PublicHabitViewSet, basename="public_habits")

urlpatterns = [] + router.urls