from django.contrib import admin


from .models import Petition, PetitionImage, PetitionVote, PetitionComment


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


