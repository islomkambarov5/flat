from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import ApartmentFilter
from .serializers import *
from .models import Flat, Image, Comment


@permission_classes([IsAuthenticated])
class ApartmentCreateView(generics.CreateAPIView):
    serializer_class = FlatSerializer


@permission_classes([IsAuthenticated])
class MyApartmentsListView(generics.ListAPIView):
    serializer_class = FlatSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ApartmentFilter

    def get_queryset(self):
        queryset = Flat.objects.filter(status=True, user=self.request.user)
        return queryset.order_by('-created_at')


@permission_classes([IsAuthenticated])
class ApartmentUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = FlatSerializer

    def post(self, *args, **kwargs):
        flat = self.kwargs['pk']
        serializer = FlatSerializer(data=self.request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        if flat.user != self.request.user:
            return Response({
                'message': "That's not you flat"
            })
        flat.description = serializer.fields['description']
        flat.phone_number = serializer.fields['phone_number']
        flat.name = serializer.fields['name']
        flat.address = serializer.fields['address']
        flat.city = serializer.fields['city']
        flat.people = serializer.fields['people']
        flat.room_count = serializer.fields['room_count']
        flat.price_per_person = serializer.fields['price_per_person']
        flat.status = serializer.fields['status']
        flat.has_ac = serializer.fields['has_ac']
        flat.has_wifi = serializer.fields['has_wifi']
        flat.has_contract = serializer.fields['has_contract']
        flat.save()
        return Response({
            'data': 'flat info updated'
        })


class ApartmentListView(generics.ListAPIView):
    queryset = Flat.objects.filter(status=True)
    serializer_class = FlatSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ApartmentFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-created_at')


class ApartmentDetailView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        flat_id = self.kwargs['pk']
        return Comment.objects.filter(flat__id=flat_id)

    def get(self, request, *args, **kwargs):
        try:
            flat = get_object_or_404(Flat, id=self.kwargs['pk'])

            flat_serializer = FlatSerializer(data=self.request.data, context={'request': self.request})

            comments = self.get_queryset()
            comment_serializer = self.get_serializer(comments, many=True)

            response_data = {
                'flat': flat_serializer.data,
                'comments': comment_serializer.data
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, *args, **kwargs):
        try:
            flat = get_object_or_404(Flat, id=self.kwargs['pk'])

            serializer = CommentSerializer(data=self.request.data)
            serializer.flat = flat.id
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
