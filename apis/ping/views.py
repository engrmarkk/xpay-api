from django.shortcuts import render
from api_services.const_response import return_response
from api_services.status_messages import StatusResponse as Res
from rest_framework.decorators import api_view
from rest_framework import status


# Create your views here.
@api_view(["GET"])
def ping(request):
    return return_response(Res.SUCCESS, status.HTTP_200_OK, "Pong")
