from django.contrib import admin


from .models import Petition, PetitionImage, PetitionVote, PetitionComment
from .models import PetitionTag


class PetitionImageInline(admin.TabularInline):
    model = PetitionImage


class PetitionVoteInline(admin.TabularInline):
    model = PetitionVote


@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    inlines = [PetitionImageInline, PetitionVoteInline]
    list_display = ['id', 'title', 'author']
    list_display_links = ['id', 'title', 'author']

    class Meta:
        model = Petition
        fields = '__all__'


@admin.register(PetitionTag)
class PetitionTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']

    class Meta:
        model = PetitionTag
        fields = '__all__'
