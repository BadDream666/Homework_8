from django.core.exceptions import ValidationError
from rest_framework import serializers
from urllib.parse import urlparse


def validate_youtube_only(value):
    """
    Валидатор для проверки, что ссылка ведет только на youtube.com
    """
    if value:
        parsed_url = urlparse(value)
        # Проверяем, что домен - youtube.com или youtu.be
        allowed_domains = ['www.youtube.com', 'youtube.com', 'youtu.be']
        if parsed_url.netloc not in allowed_domains:
            raise ValidationError(
                "Разрешены только ссылки на youtube.com"
            )


class YouTubeValidator:
    """
    Класс-валидатор для проверки YouTube ссылок
    """
    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        field_value = attrs.get(self.field)
        if field_value:
            parsed_url = urlparse(field_value)
            allowed_domains = ['www.youtube.com', 'youtube.com', 'youtu.be']
            if parsed_url.netloc not in allowed_domains:
                raise serializers.ValidationError(
                    {self.field: "Разрешены только ссылки на youtube.com"}
                )
