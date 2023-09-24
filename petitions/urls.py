from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PetitionViewSet, PetitionImageViewSet, PetitionCommentViewSet, PetitionVoteViewSet
from .views import PetitionTagViewSet

router = DefaultRouter()
router.register("petition", PetitionViewSet, basename="petition")
router.register("petition-image", PetitionImageViewSet, basename="petition-image")
router.register("petition-comment", PetitionCommentViewSet, basename="petition-comment")
router.register("petition-vote", PetitionVoteViewSet, basename="petition-vote")
router.register("petition-tag", PetitionTagViewSet, basename="petition-tag")

urlpatterns = [
    path("", include(router.urls)),
]
