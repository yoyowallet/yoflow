from rest_framework import serializers

from example import models


class PostSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()

    class Meta:
        model = models.Post
        fields = ("name", "content", "state")

    def get_state(self, obj):
        return obj.get_state_display()
