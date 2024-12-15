from rest_framework import serializers
from apps.users.models import User, EmailVerify
from apps.users.validations import custom_validate_token


class EmailTokenCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerify
        fields = ['code', 'url']
        extra_kwargs = {
            "code": {
                "error_messages": {"required": "Пожалуйста, заполните поле кода.", "blank": "Пожалуйста, напишите ваш код."}},
            "url": {
                "error_messages": {"required": "Пожалуйста, заполните поле URL.", "blank": "Пожалуйста, напишите ваш URL."}},
        }

    def create(self, validated_data):
        url = self.context.get('url')
        token = EmailVerify.objects.get(url=url)
        user = token.user
        user.email_confirmed = True
        user.is_active = True
        user.save()
        token.delete()
        return user

    def validate(self, data):
        url = self.context.get('url')
        custom_validate_token(data, url)
        return data
