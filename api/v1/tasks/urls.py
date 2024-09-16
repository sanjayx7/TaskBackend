from django.urls import path
from .views import ManageListCreateView, ManageDetailView, ManageStatusFilterView,RegisterView,LoginView,LogoutView,UserProfileView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('tasks/', ManageListCreateView.as_view(), name='manage-list-create'),
    path('tasks/<int:pk>/', ManageDetailView.as_view(), name='manage-detail'),
    path('tasks/status/<str:status>/', ManageStatusFilterView.as_view(), name='manage-status-filter'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
