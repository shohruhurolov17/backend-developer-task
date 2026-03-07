from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from apps.common.models import FileProcessingTask
from apps.common.tasks import process_file
from apps.common.serializers import FileProcessingTaskCreateSerializer, FileProcessingTaskSerializer
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema


@extend_schema(tags=['tasks'])
class FileProcessingTaskViewSet(ModelViewSet):

    authentication_classes = ()
    permission_classes = ()
    queryset = FileProcessingTask.objects.all()
    
    def get_serializer_class(self):
        
        if self.action == 'create':
            return FileProcessingTaskCreateSerializer
        return FileProcessingTaskSerializer

    def create(self, request):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            file = serializer.validated_data['file']

            task = FileProcessingTask.objects.create(file=file)

            process_file.delay(task.id)

            return Response({
                "data": {
                    "task_id": task.id
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "error": str(serializer.errors)
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=True, url_path='cancel')
    def cancel_task(self, request, pk=None):

        task = self.get_object()

        task.status = "cancelled"
        task.save()

        return Response({
            "data": {
                "message": "Task cancelled"
            }
        })
    
    @action(methods=['POST'], detail=True, url_path='restart')
    def restart_task(self, request, pk=None):

        task = self.get_object()

        task.status = "pending"
        task.progress = 0
        task.save()

        process_file.delay(task.id)

        return Response({
            "message": "Task restarted"
        })