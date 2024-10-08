from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Rating
from .serializers import RatingSerializer


class RatingsView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        # GETの場合は認証不要
        if (self.request.method == 'GET'):
            return []
        # それ以外は認証を要件とする
        return [IsAuthenticated()]
