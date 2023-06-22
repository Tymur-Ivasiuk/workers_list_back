from rest_framework import serializers

from .models import *


class WorkerSerializer(serializers.ModelSerializer):
    haveChildren = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    def get_haveChildren(self, obj):
        return bool(obj.worker_set.all().exists())

    def get_children(self, obj):
        return []

    class Meta:
        model = Worker
        fields = "__all__"
