from tasks.models import Manage
from .serializers import ManageSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer

class ManageListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Return only the tasks for the authenticated user
        manages = Manage.objects.filter(user=request.user)
        serializer = ManageSerializer(manages, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Create a new task with the authenticated user as the owner
        serializer = ManageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            # Ensure that the task belongs to the authenticated user
            return Manage.objects.get(pk=pk, user=self.request.user)
        except Manage.DoesNotExist:
            return None

    def get(self, request, pk):
        manage = self.get_object(pk)
        if manage is not None:
            serializer = ManageSerializer(manage)
            return Response(serializer.data)
        return Response({"error": "Task not found or you don't have permission."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        manage = self.get_object(pk)
        if manage is not None:
            serializer = ManageSerializer(manage, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Task not found or you don't have permission."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        manage = self.get_object(pk)
        if manage is not None:
            manage.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Task not found or you don't have permission."}, status=status.HTTP_404_NOT_FOUND)


class ManageStatusFilterView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, status):
        if status.lower() not in ['completed', 'pending']:
            return Response({"error": "Invalid status. Use 'completed' or 'pending'."},
                            status=status.HTTP_400_BAD_REQUEST)

        status_bool = status.lower() == 'completed'  # Convert status to boolean
        # Filter tasks by status and user
        manages = Manage.objects.filter(status=status_bool, user=request.user)
        serializer = ManageSerializer(manages, many=True)
        return Response(serializer.data)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully.",
                "user": {
                    "username": user.username,
                    "email": user.email
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.filter(username=username).first()
        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(password):
            return Response({"error": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_200_OK)




class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Only logged-in users should be able to log out

    def post(self, request):
        try:
            # Expect refresh token to be passed in the request body
            refresh_token = request.data.get("refresh")

            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response({"error": "Invalid token or token already blacklisted."}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # Get the authenticated user
        serializer = UserSerializer(user)  # Use the same serializer
        return Response(serializer.data, status=status.HTTP_200_OK)