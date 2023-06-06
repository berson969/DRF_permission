from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from advertisements.filters import AdvertisementFilter

from advertisements.models import Advertisement, Favorite
from advertisements.permissions import IsOwnerOrIsStaffOrReadOnly # , IsNotOwner,
from advertisements.serializers import AdvertisementSerializer, FavoriteAdvertisementSerializer

from rest_framework.decorators import action

    
class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""

        # if self.request == action:
        #     return [IsAuthenticated(), IsNotOwner()]
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrIsStaffOrReadOnly()]
        return []

    # def get_queryset(self):
    #     queryset = Advertisement.objects.all()
    #     queryset = self.annotate_qs_is_favorite_field(queryset)
    #     return queryset
    
    @action(detail=False)
    def favorites(self, request):
        queryset = Favorite.objects.filter(user=request.user)
        serializer = FavoriteAdvertisementSerializer(queryset, many=True)
        return Response({request.user.username: serializer.data})
    
    @action(methods=['post'], detail=True)
    def add_favorite(self, request, pk=None):
        queryset = Advertisement.objects.filter(id=pk)
        if queryset:
            validated_data = {'favorite': queryset, 'user': request.user}
            serializer = FavoriteAdvertisementSerializer(data=validated_data)
            serializer.validate(data=validated_data)
            serializer.create(validated_data)
            return Response('The Advertisement added to Favorites ', status=status.HTTP_201_CREATED)
        return Response('The Advertisement missing in database', status=status.HTTP_204_NO_CONTENT)

    @action(methods=['delete'], detail=True)
    def delete_favorite(self, request, pk=None):
        queryset = Advertisement.objects.filter(id=pk)
        if queryset:
            validated_data = {'favorite': queryset, 'user': request.user}
            serializer = FavoriteAdvertisementSerializer(data=validated_data)
            serializer.validate(data=validated_data)
            serializer.delete(validated_data)
            return Response('The Advertisement deleted to Favorites ', status=status.HTTP_201_CREATED)
        return Response('The Advertisement missing in database', status=status.HTTP_204_NO_CONTENT)




# from django.contrib.contenttypes.models import ContentType
# from django.db.models import Exists, OuterRef

# class ManageFavorite:
#     @action(
#       detail=True, 
#       methods=['get'], 
#       url_path='favorite', 
#     #   permission_classes=[ IsNotOwner()]
#     )
#     def favorite(self, request, pk):
#         instance = self.get_object()
#         content_type = ContentType.objects.get_for_model(instance)
#         favorite_obj, created = Favorite.objects.get_or_create(
#             user=request.user, content_type=content_type, object_id=instance.id
#         )

#         if created:
#             return Response(
#                 {'message': 'Контент добавлен в избранное'},
#                 status=status.HTTP_201_CREATED
#             )
#         else:
#             favorite_obj.delete()
#             return Response(
#                 {'message': 'Контент удален из избранного'},
#                 status=status.HTTP_200_OK
#             )

#     def annotate_qs_is_favorite_field(self, queryset):
#         if self.request.user.is_authenticated:
#             is_favorite_subquery = Favorite.objects.filter(
#                 object_id=OuterRef('pk'), 
#                 user=self.request.user, 
#                 content_type=ContentType.objects.get_for_model(queryset.model)
#             )
#             queryset = queryset.annotate(is_favorite=Exists(is_favorite_subquery))
#         return queryset


#     @action(
#         detail=False,
#         methods=['get'],
#         url_path='favorites',
#         # permission_classes=[IsAuthenticated, ]
#     )
#     def favorites(self, request):
#         queryset = self.get_queryset().filter(is_favorite=True)
#         serializer_class = self.get_serializer_class()
#         serializer = serializer_class(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
