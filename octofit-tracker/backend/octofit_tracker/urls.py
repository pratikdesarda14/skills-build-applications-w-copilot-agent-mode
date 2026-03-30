"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, TeamViewSet, ActivityViewSet, WorkoutViewSet, LeaderboardViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.reverse import reverse
import os

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'workouts', WorkoutViewSet)
router.register(r'leaderboard', LeaderboardViewSet)


# Helper to build full API URLs using $CODESPACE_NAME if available
def build_full_url(request, name, format=None):
    url = reverse(name, request=request, format=format)
    codespace_name = os.environ.get('CODESPACE_NAME')
    if codespace_name:
        # Use https and codespace public URL, avoid certificate issues by not verifying in client
        return f'https://{codespace_name}-8000.app.github.dev' + url
    # Fallback to request.build_absolute_uri (localhost)
    return request.build_absolute_uri(url)

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': build_full_url(request, 'user-list', format),
        'teams': build_full_url(request, 'team-list', format),
        'activities': build_full_url(request, 'activity-list', format),
        'workouts': build_full_url(request, 'workout-list', format),
        'leaderboard': build_full_url(request, 'leaderboard-list', format),
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', api_root, name='api-root'),
]
