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

    def passport_front_preview(self, obj):
        return mark_safe('<img src="{url}" width="300"/>'.format(
            url=obj.passport_front.url
        ))

    def passport_selfie_preview(self, obj):
        return mark_safe('<img src="{url}" width="300"/>'.format(
            url=obj.passport_selfie.url
        ))

    readonly_fields = ("passport_front_preview", "passport_selfie_preview",)
    passport_front_preview.short_description = "Фото лицевой стороны паспорта"
    passport_selfie_preview.short_description = "Фото с паспортом"

    class Meta:
        model = UserPassportVerificationImages
        fields = '__all__'
