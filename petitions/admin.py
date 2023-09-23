from django.contrib import admin


from .models import Petition, PetitionImage, PetitionVote, PetitionComment


class PetitionImageInline(admin.TabularInline):
    model = PetitionImage


@admin.register(Petition)
class UserAccountAdmin(admin.ModelAdmin):
    inlines = [PetitionImageInline]
    list_display = ['id', 'title', 'author']
    list_display_links = ['id', 'title', 'author']

    class Meta:
        model = Petition
        fields = '__all__'
