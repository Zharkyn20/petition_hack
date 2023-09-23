from rest_framework import serializers

from .models import Petition, PetitionImage, PetitionComment, PetitionVote
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
    image = serializers.ImageField(required=True)


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


class PetitionSerializer(serializers.ModelSerializer):
    author = UserAccountSerializer(read_only=True)
    images = PetitionImageSerializer(many=True, read_only=True)
    agree = serializers.SerializerMethodField('get_agree')
    disagree = serializers.SerializerMethodField('get_disagree')

    class Meta:
        model = Petition
        fields = '__all__'

    def get_agree(self, obj):
        return obj.votes.filter(is_agree=True).count()

    def get_disagree(self, obj):
        return obj.votes.filter(is_agree=False).count()


class PetitionCreateSerializer(serializers.ModelSerializer):
    images = PetitionImageCreateSerializer(many=True, required=False)

    class Meta:
        model = Petition
        exclude = ("author",)
