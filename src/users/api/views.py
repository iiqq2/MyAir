from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from core.factories.rep_factory import RepositoryFactory
from users.api.serializers import UserRequestSerializer, UserResponseSerializer
from users.models import BaseUserPagination
from users.schemas import SelfCreateViewSchema, SelfUpdateViewSchema, SelfViewSchema

@extend_schema(tags=['Users'])
class SelfListView(ListAPIView):

    repository = RepositoryFactory.create('user')
    queryset = repository.get_all()

    serializer_class = UserResponseSerializer
    pagination_class = BaseUserPagination

@extend_schema(tags=['Users'])
class SelfView(GenericAPIView):
    serializer_class = UserRequestSerializer
    
    @extend_schema(
        parameters=SelfViewSchema()
    )
    def get(self, request, id):
        repository = RepositoryFactory.create('user')
        serializer = repository.get(id)
        return Response(data=serializer, status=status.HTTP_200_OK)
@extend_schema(tags=['Users'])
class SelfCreateView(GenericAPIView):
    serializer_class = UserRequestSerializer
    
    @extend_schema(
        request=SelfCreateViewSchema()
    )
    def post(self, request):
        repository = RepositoryFactory.create('user')
        serializer = repository.post(request)
        if serializer:
            return Response(data=serializer, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Users'])
class SelfUpdateDeleteView(GenericAPIView):
    serializer_class = UserRequestSerializer

    @extend_schema(
        parameters=SelfViewSchema(),
        request=SelfUpdateViewSchema()
    )
    def patch(self, request, id):
        repository = RepositoryFactory.create('user')
        serializer = repository.update(request, id)
        return Response(serializer, status=status.HTTP_200_OK)
    
    @extend_schema(
        parameters=SelfViewSchema()
    )
    def delete(self, request, id):
        repository = RepositoryFactory.create('user')
        serializer = repository.delete(id)
        return Response(serializer, status=status.HTTP_200_OK)
