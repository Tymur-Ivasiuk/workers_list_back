from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from .models import *


def recursionGetParentIds(instance):
    try:
        id_list = [instance.id, ]
        if instance.warden:
            id_list.extend(recursionGetParentIds(instance.warden))
        return id_list
    except:
        return []

class ParentIdError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = u'Your parent can`t be your child'


class WorkerSerializer(serializers.ModelSerializer):
    haveChildren = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    def get_haveChildren(self, obj):
        return bool(obj.worker_set.all().exists())

    def get_children(self, obj):
        return []

    # redefine
    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        # add start
        if instance.id in recursionGetParentIds(instance.warden):
            raise ParentIdError()
        # add end
        instance.save()

        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance

    class Meta:
        model = Worker
        fields = "__all__"
