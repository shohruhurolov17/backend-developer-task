from celery import shared_task
from .models import FileProcessingTask
import time


@shared_task(bind=True)
def process_file(self, task_id):

    task = FileProcessingTask.objects.get(task_id=task_id)

    task.status = "processing"
    task.save()

    for i in range(1, 101):

        task.refresh_from_db()

        if task.status == "cancelled":
            return "cancelled"

        time.sleep(1)

        task.progress = i
        task.save()

        self.update_state(
            state="PROGRESS",
            meta={"progress": i}
        )

    task.status = "completed"
    task.save()

    return "done"