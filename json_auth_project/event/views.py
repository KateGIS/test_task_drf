from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from . import filters
from .filters import EventFilter
from .models import Event, Tag
from .serializers import EventSerializerDetail, EventSerializer, TagSerializer, EventSerializerUpdate


class TagList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class EventList(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    # filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EventFilter

    permission_classes = [IsAuthenticatedOrReadOnly, ]


class EventCreate(generics.CreateAPIView):
    serializer_class = EventSerializerDetail
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return super(EventCreate, self).post(request, *args, **kwargs)


class EventDetail(generics.RetrieveUpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializerDetail

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PUT':
            serializer_class = EventSerializerUpdate
        return serializer_class

    def delete(self, request, pk):
        event = Event.objects.get(pk=pk)
        if event.owner.email == request.user.email:
            event.delete()
