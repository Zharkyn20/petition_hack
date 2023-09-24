import django_filters
from django.http import HttpRequest
from rest_framework import viewsets, status
from rest_framework.response import Response
from petitions import serializers

from .models import Petition, PetitionImage, PetitionComment, PetitionVote, PetitionTag


class PetitionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PetitionCreateSerializer
    queryset = Petition.objects.all()
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
    )
    filterset_fields = (
        'tags'
    )

    def perform_create(self, serializer):
        user = self.request.user

        serializer.save(
            author=user
        )

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return serializers.PetitionSerializer
        return super().get_serializer_class()

    def create(self, request: HttpRequest) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PetitionImageViewSet(viewsets.ModelViewSet):
    queryset = PetitionImage.objects.all()
    serializer_class = serializers.PetitionImageSerializer


class PetitionCommentViewSet(viewsets.ModelViewSet):
    queryset = PetitionComment.objects.all()
    serializer_class = serializers.PetitionCommentCreateSerializer

    def perform_create(self, serializer):
        user = self.request.user

        serializer.save(
            author=user
        )

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return serializers.PetitionCommentSerializer
        return super().get_serializer_class()


class PetitionVoteViewSet(viewsets.ModelViewSet):
    queryset = PetitionVote.objects.all()
    serializer_class = serializers.PetitionVoteCreateSerializer

    def perform_create(self, serializer):
        user = self.request.user

        serializer.save(
            author=user
        )

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return serializers.PetitionVoteSerializer
        return super().get_serializer_class()


class PetitionTagViewSet(viewsets.ModelViewSet):
    queryset = PetitionTag.objects.all()
    serializer_class = serializers.PetitionTagSerializer
