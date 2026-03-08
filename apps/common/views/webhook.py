from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core import load_env
from apps.common.models import WebhookEvent
from  drf_spectacular.utils import extend_schema
from apps.common.utils import verify_hmac_signature
import json
import logging
import os
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.types import OpenApiTypes


logger = logging.getLogger(__name__)


class PaymentWebhookView(APIView):

    @extend_schema(
        tags=['payment-webhook'],
        parameters=[
            OpenApiParameter(
                name='X-Signature',
                location=OpenApiParameter.HEADER,
                type=OpenApiTypes.STR
            )
        ]
    )
    def post(self, request, *args, **kwargs):

        received_signature = request.headers.get('X-Signature', '')
        payload_bytes = request.body

        secret = load_env.WEBHOOK_SECRET

        if not verify_hmac_signature(payload_bytes, received_signature, secret):
            logger.warning("Invalid webhook signature")
            return Response({"detail": "Invalid signature"}, status=status.HTTP_403_FORBIDDEN)

        try:
            payload = json.loads(payload_bytes)
        except json.JSONDecodeError:
            return Response({"detail": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)

        event_id = payload.get('event_id')
        if not event_id:
            return Response({"detail": "event_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        if WebhookEvent.objects.filter(event_id=event_id).exists():
            logger.info(f"Duplicate webhook received: {event_id}")
            return Response({"detail": "Duplicate event"}, status=status.HTTP_400_BAD_REQUEST)

        WebhookEvent.objects.create(event_id=event_id, payload=payload)
        logger.info(f"Webhook processed successfully: {event_id}")

        return Response({"detail": "Webhook received"}, status=status.HTTP_200_OK)