import re
from .serializers import CustomUserRegistrationSerializer, LoginSerializer, UserProfileSerializer, CustomUserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import CustomUser, UserProfile
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Subquery, OuterRef, Count
from rest_framework.pagination import PageNumberPagination


class CustomUserRegistrationView(CreateAPIView):
    serializer_class = CustomUserRegistrationSerializer

    def perform_create(self, serializer):
        serializer.save()


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class UserProfileView(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        data = self.request.query_params.dict()
        keyword = data.get("keyword", None)

        if keyword:
            search_fields = (
                "user__email", "first_name", "last_name"
        )
            query = self.get_query(keyword, search_fields)
            return self.queryset.filter(query).distinct()
        return self.queryset

    @staticmethod
    def get_query(query_string, search_fields):
        query = None
        terms = UserProfileView.normalize_query(query_string)
        for term in terms:
            or_query = None
            for field_name in search_fields:
                q = Q(**{"%s__icontains"% field_name: term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query & or_query

        return query

    @staticmethod
    def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
        return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]





