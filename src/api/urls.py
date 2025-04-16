from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"todolists", views.TodoListViewSet)
router.register(r"todos", views.TodoViewSet)

app_name = "api"
urlpatterns = [
    path("ready/", views.ReadyView.as_view(), name="ready"),
    path("health/", views.HealthView.as_view(), name="health"),
    path("", include(router.urls)),
    
]
