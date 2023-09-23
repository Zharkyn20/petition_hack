from django.contrib import admin


from .models import UserAccount, UserPassportVerificationImages


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'inn']
    list_display_links = ['id', 'full_name', 'inn']

    class Meta:
        model = UserAccount
        fields = '__all__'


@admin.register(UserPassportVerificationImages)
class UserPassportVerificationImagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'auth_status']
    list_display_links = ['id', 'user', 'auth_status']

    class Meta:
        model = UserPassportVerificationImages
        fields = '__all__'
