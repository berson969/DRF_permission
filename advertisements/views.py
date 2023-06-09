from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .filters import AdvertisementFilter

from .models import Advertisement, Favorite
from .permissions import IsOwnerOrIsStaffOrReadOnly # , IsNotOwner,
from .serializers import AdvertisementSerializer, FavoriteAdvertisementSerializer

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

        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrIsStaffOrReadOnly()]
        return []

    def get_queryset(self, *args, **kwargs):
        return Advertisement.objects.all()

    @action(detail=False)
    def favorites(self, request):
        queryset = Favorite.objects.filter(user=request.user)
        serializer = FavoriteAdvertisementSerializer(queryset, many=True)
        return Response({request.user.username: serializer.data})
    
    @action(methods=['post'], detail=True)
    def add_favorite(self, request, pk=None):
        queryset = Advertisement.objects.filter(id=pk).first()
        if queryset:
            validated_data = {'favorite': queryset, 'user': request.user}
            serializer = FavoriteAdvertisementSerializer(data=validated_data)
            serializer.validate(data=validated_data)
            # serializer.is_valid(raise_exception=True)
            serializer.create(validated_data)
            # serializer.save()
            return Response('The Advertisement added to Favorites', status=status.HTTP_201_CREATED)
        return Response('The Advertisement missing in database', status=status.HTTP_204_NO_CONTENT)

    @action(methods=['delete'], detail=True)
    def delete_favorite(self, request, pk=None):
        queryset = Favorite.objects.filter(favorite=pk, user=request.user)
        if queryset:
            Favorite.delete(Favorite.objects.get(favorite=pk, user=request.user))
            return Response('The Advertisement deleted from Favorites', status=status.HTTP_204_NO_CONTENT)
        return Response('The Advertisement missing in database', status=status.HTTP_204_NO_CONTENT)

