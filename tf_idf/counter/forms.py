from django.core.validators import FileExtensionValidator
from django.forms import Form, FileField, CharField


class UploadTextFile(Form):
    name = CharField()
    file = FileField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=['txt', 'doc', 'docx']
            )
        ]
    )
