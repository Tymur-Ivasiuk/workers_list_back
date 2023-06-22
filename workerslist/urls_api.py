from django.urls import path, include
from rest_framework import routers

from workerslist.views import *


router = routers.SimpleRouter()
router.register(r'worker', WorkerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    # path('workers/', WorkersAPIView.as_view()),
    # path('workers/<int:pk>/', WorkerDetailAPIView.as_view()),
]