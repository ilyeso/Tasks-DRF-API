from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class TaskPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = TaskPagination
    permission_classes = [AllowAny]
    

    # def create(self, request, *args, **kwargs):
        
    #     serializer = self.get_serializer(data = request.data)
    #     serializer.is_valid(raise_exception = True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial',False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data = request.data, partial= partial)
    #     serializer.is_valid(raise_exception = True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)
    
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def public_tasks(self, request):
        tasks = Task.objects.filter(type= 'public')
        page = self.paginate_queryset(tasks)

        if page is not None:
            serializer = self.get_serializer(page, many = True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(tasks, many = True)
        return Response(serializer.data)
    

    @action(detail= False, methods=['get'])
    def user_tasks(self, request):
        user_id = request.query_params.get('user_id')

        if not user_id:
            return Response( {'error': 'user_id param is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        tasks = Task.objects.filter(affected_to__id = user_id).order_by('-priority')
        page = self.paginate_queryset(tasks)
        if page is not None:
            serializer = self.get_serializer(page, many = True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(tasks, many = True)
        return Response(serializer.data)