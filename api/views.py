from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
# Create your views here.
from rest_framework import generics, viewsets, permissions

from rest_framework.response import Response

from incling.models import *


from knox.models import AuthToken

from .serializers import *


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': 'task/list', 'tile/list'
        'Detail View': 'task/detail/<str:pk>/', 'tile/detail/<str:pk>/'
        'Create': 'task/create', 'tile/create'
        'Update': 'task/update/<str:pk>/', 'tile/update/<str:pk>/'
        'Delete': 'tile/delete/<str:pk>/',
    }

    return Response(api_urls)

# API to allow registeration for new users


class RegistrationAPI(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user,
                                   context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


# Login API

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]})


# Get User API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# Allowing users to creating instances of tasks

@api_view(['POST'])
def TaskCreateAPI(request):
    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

# API to allow lists of Tasks to be displayed


@api_view(['GET'])
def TaskListAPI(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True
                                )
    return Response(serializer.data)

# API to allow to update the tasks
@api_view(['POST'])
def TaskUpdateAPI(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(instance=task, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def TaskDetailAPI(request, pk):
    tasks = Task.objects.get(id=pk)
    serializer = TaskSerializer(tasks, many=False)
    return Response(serializer.data)

# API to allow users to delete the instances from the task model


@api_view(['DELETE'])
def TaskDeleteAPI(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()

    return Response("Task deleted")

# API to allow creating API for tile instances in relation to tasks
@api_view(['POST'])
def TileCreateAPI(request):
    serializer = TileSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

# API to allow lists of Tasks to be displayed


@api_view(['GET'])
def TileListAPI(request):
    tile = Tile.objects.all()
    serializer = TileSerializer(tile, many=True)

    return Response(serializer.data)

# API to allow to update the tile instances


@api_view(['GET'])
def TileUpdateAPI(request, pk):
    tile = Tile.objects.get(id=pk)
    serializer = TileSerializer(instance=tile, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def TileDetailAPI(request, pk):
    tile = Tile.objects.get(id=pk)
    serializer = TileSerializer(tile, many=False)
    return Response(serializer.data)


# API to allow users to delete the instances from the task model

@api_view(['DELETE'])
def TileDeleteAPI(request, pk):
    tile = Tile.objects.get(id=pk)
    tile.delete()

    return Response("Tile deleted")
