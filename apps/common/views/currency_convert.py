from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.core.cache import cache
import requests
import os
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from core import load_env


class CurrencyConvertAPIView(APIView):

    authentication_classes = ()
    permission_classes = ()

    @extend_schema(
        tags=['currency-convert'],
        parameters=[
            OpenApiParameter(
                name='to_currency',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=True
            ),
            OpenApiParameter(
                name='from_currency',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=True
            ),
            OpenApiParameter(
                name='amount',
                type=OpenApiTypes.FLOAT,
                location=OpenApiParameter.QUERY,
                required=True
            )
        ]
    )
    def get(self, request):

        try:

            to_currency = request.query_params.get('to_currency')
            from_currency = request.query_params.get('from_currency')
            amount = float(request.query_params.get('amount', 0))

            if not to_currency or not from_currency or not amount:
                raise ValidationError({
                    "error": "from_currency, to_currency and amount query params are required"
                })
            
            cache_key = f"rate_{from_currency}_{to_currency}"

            rate = cache.get(cache_key)

            if rate is None:

                BASE_URL = load_env.EXCHANGE_RATE_BASE_URL
                API_KEY = load_env.EXCHANGE_RATE_API_KEY

                url = f"{BASE_URL}/{API_KEY}/latest/{from_currency}"

                response = requests.get(url)

                data = response.json()

                if response.status_code != status.HTTP_200_OK:
                    return Response({
                        "success": False,
                        "error": data
                    },  status=response.status_code)

                rate = data['conversion_rates'][to_currency]

                cache.set(cache_key, rate)

            convert_amount = round(rate * amount, 2)

            return Response({
                "success": True,
                "data": {
                    "convert_amount": convert_amount,
                    "from_currency": from_currency,
                    "to_currency": to_currency,
                }
            })

        except Exception as err:
            return Response({
                "success": False,
                "error": str(err)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)