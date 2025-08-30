from django.shortcuts import render
from api_services.const_response import return_response
from api_services.status_messages import StatusResponse as Res
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from permissions import IsActiveUser


# user operation
class UserOperation(APIView):
    permission_classes = [IsAuthenticated, IsActiveUser]

    def get(self, request):
        return return_response(Res.SUCCESS, status.HTTP_200_OK, f"Hello, {request.user.email}!",
                               data={"email": request.user.email, "id": request.user.id})
