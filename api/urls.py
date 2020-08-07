from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoriesViewSet, CommentsViewSet, GenresViewSet,
                       ReviewsViewSet, TitlesViewSet, UsersViewSet, email_code,
                       get_token)

router_v1 = DefaultRouter()
router_v1.register('categories', CategoriesViewSet,
                   basename='categories')
router_v1.register('genres', GenresViewSet,
                   basename='genres')
router_v1.register('titles', TitlesViewSet,
                   basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)
router_v1.register('users', UsersViewSet,
                   basename='users')

v1_auth = [
    path('token/', get_token, name='token'),
    path('email/', email_code, name='email'),
]

urlpatterns = [
    path('v1/auth/', include(v1_auth)),
    path('v1/', include(router_v1.urls)),
]
