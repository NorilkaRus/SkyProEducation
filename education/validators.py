from rest_framework.serializers import ValidationError

class YouTubeValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = value.get(self.field)
        if 'youtube.com' not in url:
            raise ValidationError('Недопустимая ссылка на сторонний ресурс')
