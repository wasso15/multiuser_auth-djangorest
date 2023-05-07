from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import FreelanceSignUpSerializer, ClientSignUpSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from .permissions import IsClientUser, IsFreelance
from rest_framework.permissions import IsAuthenticated


class FreelanceSignupView(generics.GenericAPIView):
    serializer_class=FreelanceSignUpSerializer
    def post(self, request, *args,**kwargs):
        serializer= self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
             "user":UserSerializer(user, context=self.get_serializer_context()).data,
             "token":Token.objects.get(user=user).key,
            "message":"account created successfull"
           })


class ClientSignupView(generics.GenericAPIView):
    serializer_class=ClientSignUpSerializer
    def post(self, request, *args,**kwargs):
        serializer= self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            "token":Token.objects.get(user=user).key,
            "message":"account created successfull"
           })

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer= self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid( raise_exception=True) 
        user=serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                'token':token.key,
                'user_id': user.pk,
                'is_client': user.is_client, 
            }
        )

class LogoutView(APIView):

    def post(self, request, format=None):
        request.auth.delete()

        return Response(status=status.HTTP_200_OK)
    

class CLientOnlyView(generics.RetrieveAPIView):

    permission_classes=[IsAuthenticated & IsClientUser]
    serializer_class=UserSerializer

    def get_object(self):
        return self.request.user
    
class FreelanceOnlyView(generics.RetrieveAPIView):

    permission_classes=[ IsAuthenticated & IsFreelance]
    serializer_class=UserSerializer

    def get_object(self):
        return self.request.user