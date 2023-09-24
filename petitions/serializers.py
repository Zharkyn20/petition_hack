from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import Petition, PetitionImage, PetitionComment, PetitionVote, PetitionTag
from accounts.models import UserAccount


class UserAccountSerializer(serializers.ModelSerializer):

        class Meta:
            model = UserAccount
            fields = ("id", "full_name", "email")


class PetitionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetitionImage
        fields = '__all__'


class PetitionImageCreateSerializer(serializers.Serializer):
    image = Base64ImageField(required=True)


class PetitionCommentSerializer(serializers.ModelSerializer):
    author = UserAccountSerializer(read_only=True)

    class Meta:
        model = PetitionComment
        fields = '__all__'


class PetitionCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetitionComment
        exclude = ("author",)


class PetitionVoteSerializer(serializers.ModelSerializer):
    author = UserAccountSerializer(read_only=True)

    class Meta:
        model = PetitionVote
        fields = '__all__'


class PetitionVoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetitionVote
        exclude = ("author",)


class PetitionTagReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = PetitionTag
        fields = ("id", "name")


class PetitionSerializer(serializers.ModelSerializer):
    author = UserAccountSerializer(read_only=True)
    images = PetitionImageSerializer(many=True, read_only=True)
    agree = serializers.SerializerMethodField('get_agree')
    disagree = serializers.SerializerMethodField('get_disagree')
    tags = PetitionTagReadSerializer(many=True, read_only=True)
    vote_status = serializers.SerializerMethodField()

    class Meta:
        model = Petition
        fields = '__all__'

    def get_agree(self, obj):
        return obj.votes.filter(is_agree=True).count()

    def get_disagree(self, obj):
        return obj.votes.filter(is_agree=False).count()

    def get_vote_status(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return "no_vote"
        try:
            vote = PetitionVote.objects.get(petition=obj, author=user)
            return "agree" if vote.is_agree else "disagree"
        except PetitionVote.DoesNotExist:
            return "no_vote"


class PetitionCreateSerializer(serializers.ModelSerializer):
    images = serializers.ImageField(required=True)

    class Meta:
        model = Petition
        exclude = ("author",)

    def create(self, validated_data):
        images = validated_data.pop("images")

        petition = Petition.objects.create(**validated_data)
        PetitionImage.objects.create(petition=petition, image=images)

        existing_tags = list(PetitionTag.objects.values_list("name", flat=True))

        return petition


class PetitionTagSerializer(serializers.ModelSerializer):
    petitions = PetitionSerializer(many=True, read_only=True)

    class Meta:
        model = PetitionTag
        fields = '__all__'

