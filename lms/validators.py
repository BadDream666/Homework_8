from rest_framework.serializers import ValidationError


class LinkValidator:
    def __init__(
        self, field
    ):  # field - данные с которыми будут сравниваться входящие данные от пользователя
        self.field = field

    def __call__(self, value):  # value - те данные которые приходят от пользователя
        link = dict(value).get(self.field)
        # если в передаваемых данных value есть значение 'youtube.com' с ключом 'link', то:
        if bool(dict(value).get("link")) and not bool("youtube.com" in link):
            raise ValidationError("Недопустимая ссылка")
