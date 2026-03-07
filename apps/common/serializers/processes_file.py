from rest_framework import serializers
from apps.common.models import FileProcessingTask


class FileProcessingTaskCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileProcessingTask
        fields = (
            "file",
        )

class FileProcessingTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileProcessingTask
        fields = (
            "id",
            "status",
            "file",
        )