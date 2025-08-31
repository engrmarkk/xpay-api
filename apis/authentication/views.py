from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import LoginSerializer, RegisterSerializer
from api_services.const_response import return_response
from api_services.status_messages import StatusResponse as Res
from rest_framework import status
from api_services.utils import get_serializer_errors, get_tokens_for_user
from api_services.logger import logger
from django.db import transaction


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                returned_data = serializer.validated_data
                print(returned_data, "returned_data")
                return return_response(
                    Res.SUCCESS,
                    status.HTTP_200_OK,
                    "Login successful",
                    **get_tokens_for_user(returned_data),
                )
            else:
                return return_response(
                    Res.FAILED,
                    status.HTTP_400_BAD_REQUEST,
                    get_serializer_errors(serializer),
                )
        except Exception as e:
            logger.exception(f"Error in LoginView: {e}")
            transaction.rollback()
            return return_response(
                Res.FAILED, status.HTTP_500_INTERNAL_SERVER_ERROR, "Network Error"
            )


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return return_response(
                    Res.SUCCESS,
                    status.HTTP_201_CREATED,
                    "User registered successfully",
                    **get_tokens_for_user(user),
                )
            else:
                return return_response(
                    Res.FAILED,
                    status.HTTP_400_BAD_REQUEST,
                    get_serializer_errors(serializer),
                )
        except Exception as e:
            logger.exception(f"Error in RegisterView: {e}")
            transaction.rollback()
            return return_response(
                Res.FAILED, status.HTTP_500_INTERNAL_SERVER_ERROR, "Network Error"
            )
