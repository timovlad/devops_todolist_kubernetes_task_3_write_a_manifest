from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, request, status, APIView
from api.serializers import TodoListSerializer, TodoSerializer, UserSerializer
from lists.models import Todo, TodoList
from django.http import HttpResponse
import time

class IsCreatorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `creator` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # If the object doesn't have a creator (i.e. anon) allow all methods.
        if not obj.creator:
            return True

        # Instance must have an attribute named `creator`.
        return obj.creator == request.user


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class TodoListViewSet(viewsets.ModelViewSet):

    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
    permission_classes = (IsCreatorOrReadOnly,)

    def perform_create(self, serializer):
        user = self.request.user
        creator = user if user.is_authenticated else None
        serializer.save(creator=creator)

class TodoViewSet(viewsets.ModelViewSet):

    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = (IsCreatorOrReadOnly,)

    def perform_create(self, serializer):
        user = self.request.user
        creator = user if user.is_authenticated else None
        serializer.save(creator=creator)
        
class ReadyView(APIView):
    """
    View that returns a 200 OK response with a delay of 5 seconds.
    """
    def get(self, request) -> HttpResponse:
        time.sleep(60)
        return HttpResponse("OK", status=200)


class HealthView(APIView):
    """
    Health check view that returns a 200 OK response.
    """
    def get(self, request) -> HttpResponse:
        return HttpResponse("OK", status=200)
    