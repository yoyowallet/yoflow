from rest_framework import serializers
from example import models


class ParentSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()

    class Meta:
        model = models.Parent
        fields = ('name', 'state')

    def get_state(self, obj):
        return obj.get_state_display()


class ChildSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField(source='custom_state_field')
    parent = ParentSerializer()

    class Meta:
        model = models.Child
        fields = ('name', 'state', 'parent')

    def get_state(self, obj):
        return obj.get_custom_state_field_display()
