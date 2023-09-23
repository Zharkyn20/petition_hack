from django.contrib import admin
from django.utils.safestring import mark_safe

from common.img_tag import image_tag
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

    def passport_front_tag(self, obj):
        return image_tag(obj)

    passport_front_tag.short_description = "Паспорт (лицевая сторона)"

    def passport_back_tag(self, obj):
        return image_tag(obj.passport_back)

    passport_back_tag.short_description = "Паспорт (обратная сторона)"

    def passport_selfie_tag(self, obj):
        return image_tag(obj.passport_selfie)

    passport_selfie_tag.short_description = "Селфи с паспортом"

    readonly_fields = ("passport_front_tag", "passport_back_tag", "passport_selfie_tag")

    class Meta:
        model = UserPassportVerificationImages
        fields = '__all__'
