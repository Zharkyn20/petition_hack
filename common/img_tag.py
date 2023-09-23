from pathlib import Path

from django.utils.safestring import mark_safe

from PIL import Image


def image_tag(obj):
    # return mark_safe(
    #     '<img src="{url}" width="{width}" height="{height}"/>'.format(
    #         url=obj.passport_front.url, width=250, height=250
    #     )
    # )
    # if obj.passport_front and Path(obj.passport_front.path).exists():
    #     img = Image.open(obj.passport_front.path)
    #     width, height = img.size
    #     if width > height:
    #         height = int(250 / width * height)
    #         width = 250
    #     else:
    #         width = 250
    #         height = 250
    #     print(width, height)
    #     img = img.resize((width, height), Image.ANTIALIAS)
    img = Image.open(obj.passport_front.path)
    width, height = img.size
    height = 250
    width = 250
    return '<img src="{url}" width="{width}" height="{height}"/>'.format(
            url=obj.url, width=width, height=height
        )
    # else:
    #     return "-"
