from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# Create your views here.
@api_view(['POST'])
def getAuthToken(request):
    '''
    FROM POST

    username : <username>

    password : <password>
    '''
    #username = request.body.get('username')
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username and password:

        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'Token': token.key})
        else:
            return Response({'error':'worng username or password'}, status=401)
    return Response({'error':'username / password missing'},status=400)
