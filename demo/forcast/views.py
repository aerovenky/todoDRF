from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework import generics
import requests

@api_view(['POST'])
#@authentication_classes([TokenAuthentication])
#@permission_classes([IsAuthenticated])
def getForecast(request):
    '''
    POST gives weather forecast
    POST DATA
    latitude : <lable name>
    longitude : <lable name>
    '''
    lat = request.POST.get('latitude')
    lng = request.POST.get('longitude')
    if lat and lng:
        url = 'http://api.openweathermap.org/data/2.5/weather?lat='+lat+'&lon='+lng+'&appid=dae7e4d983aad96854c5ca63bc341e0d'
        res = requests.get(url)
        print res.json()
        print res.status_code
        return Response(res.json())
        if res.status_code == '200':
            return Response(res.json())
        else:
            return Response({'error':'something went wrong'}, status=400)
    else:
        return Response({'error':'latitude / longitude missing'},status=400)
