from django.urls import path, include
from .views import *
from rest_framework import routers
from . import views
from django.contrib.auth.views import LogoutView

router = routers.DefaultRouter()
router.register(r'music', ProductListView)
router.register(r'category', CategorySerializerView)


urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('add-like/', views.like_view, name='add_like'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls)),
    path('api/music_list/', views.music_product_list_serializer, name='music_list'),
    path('api/music_list/create/', MusicProductAddSerializer.as_view(), name='music_create'),
    path('logout/', LogoutView.as_view(next_page="/"), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('create_account/', CreateAccountView.as_view(), name='create_account'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
    path('category/<slug>/', CategoryBasePageView.as_view(), name='base_category'),
    path('genre/', GenreView.as_view(), name='genre'),
    path('genre/<slug>/', GenreBasePageView.as_view(), name='base_genre'),
    path('playlists/', PlaylistView.as_view(), name='playlists'),
    path('create_playlist/', views.create_playlist, name='create_playlist'),
    path('delete_playlist/<name>/', views.delete_playlist, name='delete_playlist'),
    path('delete_track_in_playlist/<name>/', views.delete_track_in_playlist, name='delete_track_in_playlist'),
    path('add_track/<str:slug>/', AddTrackToPlaylistView.as_view(), name='add_track'),
    path('add_tracks/<str:slug>/', AddTrackToPlaylistGenreView.as_view(), name='genre_add_track'),
    path('favorite-track/', FavoriteTrackView.as_view(), name='favorite_track'),
    path('playlist/<name>/', BasePlaylistView.as_view(), name='base_playlist'),
    path('search/', SearchView.as_view(), name='search'),
    path('<slug>/', MusicProductView.as_view(), name='base_song'),
    path('ad/', AdView.as_view(), name='ad'),
]
