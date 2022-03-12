from rest_framework.decorators import api_view
from user_app.api.serializers import RegisterationSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from user_app import models
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

#authorization_param = openapi.Parameter('username',in_= openapi.IN_QUERY, description="username", type=openapi.TYPE_STRING)
#token_param='Authorization :Token '+str(Token.objects.get(user=accountname).key)

@swagger_auto_schema(methods=['post'], responses={'200':'Logout Successfull'})
@api_view(['POST',])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)



response_schema_dict = {
    "201": openapi.Response(
        description="Registeration Response",
        examples={
            "application/json": {
                "201_key1": "201_value_1",
                "201_key2": "201_value_2",
                "201_key3": "201_value_3",
                "201_key4": "201_value_4",
            }
        }
    )
}

@swagger_auto_schema(methods=['post'], request_body=RegisterationSerializer,responses=response_schema_dict)
@api_view(['POST',])
def registeration_view(request):
    if request.method == 'POST':
        serializer=RegisterationSerializer(data=request.data)
        
        data={}
        
        if serializer.is_valid():
            account=serializer.save()
            data['username']=account.username
            data['email']=account.email
            
            token=Token.objects.get(user=account).key
            data['token']=token
            data['response']="Registeration Successful!"
            
            
        else:    
            raise serializer.errors
        
        return Response(data,status=status.HTTP_201_CREATED)
        
        
        
