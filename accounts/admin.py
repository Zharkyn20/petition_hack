from django.contrib import admin


from .models import UserAccount


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'inn']
    list_display_links = ['id', 'full_name', 'inn']

    class Meta:
        model = UserAccount
        fields = '__all__'
