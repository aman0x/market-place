from rest_framework import serializers
from languageApp.models import Language


class languageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"
