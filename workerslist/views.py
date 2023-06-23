from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from workerslist.forms import *
from .models import *
from .serializers import WorkerSerializer


# class RegisterUser(CreateView):
#     template_name = 'shop/register.html'
#     success_url = reverse_lazy('login')
#     form_class = RegisterUserForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Register'
#         return context
#
#     def post(self, request, *args, **kwargs):
#         form = RegisterUserForm(self.request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#         else:
#             return render(request, self.template_name, {'form': form})


# class LoginUser(LoginView):
#     form_class = LoginUserForm
#     template_name = 'shop/login.html'
#
#     def dispatch(self, request, *args, **kwargs):
#         if self.request.user.is_authenticated:
#             return redirect('home')
#         return super(LoginUser, self).dispatch(request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Login'
#         return context
#
#     def get_success_url(self):
#         return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 10000

class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    pagination_class = LargeResultsSetPagination
    # permission_classes = (IsAuthenticated, )

    @action(methods=['get'], detail=False)
    def general(self, request, pk=None):
        worker = Worker.objects.filter(warden=None)
        serializer = self.get_serializer(worker, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def subordinate(self, request, pk=None):
        worker = Worker.objects.get(pk=pk)
        subordinates = worker.worker_set.all()
        serializer = self.get_serializer(subordinates, many=True)
        return Response(serializer.data)

    # recursion
    def recursion_find_nodes(self, instance):
        id_list = [instance.id, ]
        if instance.warden:
            id_list.extend(self.recursion_find_nodes(instance.warden))
        return id_list

    @action(methods=['get'], detail=True)
    def getnodesids(self, request, pk=None):
        worker = Worker.objects.get(pk=pk)
        node_ids = self.recursion_find_nodes(worker)[::-1]
        return Response(node_ids)

