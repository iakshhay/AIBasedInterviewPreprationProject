from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import RegisterSerializer,LoginSerializer,UserSerializer

# Create your views here.
class RegistrationView(GenericAPIView):
    queryset=User.objects.all()
    serializer_class=RegisterSerializer

    def post(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                                "message":"User registered successfully",
                                "data":serializer.data
                            },
                            status=status.HTTP_201_CREATED)
        return Response({
                "message":"Registration failed",
                "errors":serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(GenericAPIView):
    serializer_class=LoginSerializer

    def post(self,request):
        serailizer = self.get_serializer(data=request.data)

        if serailizer.is_valid():
            user = serailizer.validated_data['user']

            refresh = RefreshToken.for_user(user)

            return Response({
                "message":"Login successfull",
                "data":{
                    "user":UserSerializer(user).data,
                    "access":str(refresh.access_token),
                    "refres":str(refresh)
                }
            },
            status=status.HTTP_200_OK)
        
        return Response(
            {
                "message":"Login failed",
                "errors": serailizer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class CurrentUserView(GenericAPIView):
    serializer_class=UserSerializer
    permission_classes=[IsAuthenticated]

    def get(self,request):
        user=request.user
        serializer=self.get_serializer(user)
        return Response({
            "message":"User details",
            "data":serializer.data
        },
        status=status.HTTP_200_OK)