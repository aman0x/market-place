from rest_framework import serializers
from agencyApp.models import Agency


class AgencySerializers(serializers.ModelSerializer):
    class Meta:
        model=Agency
        fields="__all__"