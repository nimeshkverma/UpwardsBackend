from rest_framework.views import APIView
from rest_framework import status, mixins, generics
from rest_framework.response import Response


from . import serializers
from loan import models

from common.v1.decorators import meta_data_response, catch_exception

import logging
LOGGER = logging.getLogger(__name__)


class LoanTypeList(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   generics.GenericAPIView):
    queryset = models.LoanType.active_objects.all()
    serializer_class = serializers.LoanTypeSerializer

    @catch_exception(LOGGER)
    @meta_data_response()
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @catch_exception(LOGGER)
    @meta_data_response()
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class LoanTypeDetail(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    queryset = models.LoanType.objects.all()
    serializer_class = serializers.LoanTypeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CostBreakupDetails(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    def get(self, requests):
        serializer = serializers.CostBreakupSerializer(
            data=requests.query_params)
        if serializer.is_valid():
            serializer.validate_foreign_keys()
            return Response(serializer.cost_breakup(), status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class RepaymentScheduleDetails(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    def get(self, requests):
        serializer = serializers.RepaymentScheduleSerializer(
            data=requests.query_params)
        if serializer.is_valid():
            serializer.validate_foreign_keys()
            return Response(serializer.repayment_schedule(), status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)