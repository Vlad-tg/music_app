from django.views.generic import DetailView, View, ListView
from .models import *


class PlaylistMixin(View):
    def dispatch(self, request, *args, **kwargs):
        name = kwargs.get('name')
        get_id_playlist = request.POST.get('playlist_id')
        user = Customer.objects.get(user=request.user)
        playlist = Playlist.objects.get(user=user)
        self.playlist = playlist
        return super().dispatch(request, *args, **kwargs)
