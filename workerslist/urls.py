from django.urls import path
from .views import *

urlpatterns = [
    path('', WorkersList.as_view(), name='home'),

    #user
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
]