from django.core.exceptions import ValidationError


def validated_message_content(content):
    if content is None or content == "" or content.isspace():
        raise ValidationError(
            'Content is empty or invalid',
            code='invalid',
            params={'content':content}
        )