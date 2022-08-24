from django.contrib.postgres.search import SearchVector
from django.contrib import messages
from django.shortcuts import render
from .forms import LoginForm, RegistrationForm, PlaylistForm
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from .models import *
from django.db.models import Count, Avg, Sum, F
from django.core.mail import send_mail
from django.views.generic import DetailView, View, ListView
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import MusicProductSerializer, CategorySerializer
from django.shortcuts import redirect
from .utils import account_activation_token
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import generics
from .mixins import *


def is_valid_search(param):
    return param != '' and param is not None


class MainPageView(View):

    def get(self, request, *args, **kwargs):
        """ Sort by (for category page) """

        order_date = request.GET.get('order-by-date')
        order_date_descending = request.GET.get('order-by-date-descending')
        order_name = request.GET.get('order-by-name')
        order_name_descending = request.GET.get('order-by-name-descending')
        if order_name:
            category = Category.objects.all().order_by('name')
        elif order_name_descending:
            category = Category.objects.all().order_by('-name')
        elif order_date:
            category = Category.objects.all().order_by('date')
        elif order_date_descending:
            category = Category.objects.all().order_by('-date')
        else:
            category = Category.objects.all().order_by('pk')

        context = {
            'category_html': category,
            'order_name_html': order_name,
            'order_name_descending_html': order_name_descending,
            'order_date_html': order_date,
            'order_date_descending_html': order_date_descending,

        }
        return render(request, 'core/index.html', context)


class CategoryBasePageView(View):

    def get(self, request, slug, *args, **kwargs):
        """ Base category, output tracks """

        all_music = MusicProduct.objects.filter(category__slug=slug)
        name_category = Category.objects.filter(slug=slug)

        context = {
            'all_music_html': all_music,
            'name_category_html': name_category,
        }
        return render(request, 'core/base_category.html', context)


class GenreView(View):

    def get(self, request, *args, **kwargs):
        """ Output all genres, for genre page """

        genre = Genre.objects.all().order_by('name')

        context = {
            'genre_html': genre,
        }
        return render(request, 'core/genre.html', context)


class GenreBasePageView(View):

    def get(self, request, slug, *args, **kwargs):
        """ Base genre, output tracks """

        all_music = MusicProduct.objects.filter(genre__slug=slug)
        name_genre = Genre.objects.filter(slug=slug)

        context = {
            'all_music_html': all_music,
            'name_genre_html': name_genre,

        }
        return render(request, 'core/base_genre.html', context)


class AddTrackToPlaylistGenreView(View):

    def get(self, request, *args, **kwargs):

        track_slug = kwargs.get('slug')
        track = MusicProduct.objects.get(slug=track_slug)
        playlist_name = kwargs.get('name')
        user = Customer.objects.get(user=request.user)
        get_song = request.GET.get('add_playlist')
        playlist = Playlist.objects.get(user=user, name=playlist_name)

        if get_song:
            track_playlist, created = PlaylistTrack.objects.get_or_create(
                user=user, playlist=playlist, track=track

            )

            if created:
                playlist.track.add(track_playlist)
                return HttpResponseRedirect(f'/add_track_in_playlist/')

            if not created:
                playlist.track.remove(track_playlist)
                track_playlist.delete()
                return HttpResponseRedirect(f'/add_track_in_playlist/')


class AddTrackToPlaylistView(View):

    def get(self, request, *args, **kwargs):
        """ Add to track in user-created playlist """

        track_slug = kwargs.get('slug')
        track = MusicProduct.objects.get(slug=track_slug)
        user = Customer.objects.get(user=request.user)
        get_song = request.GET.get('add_song')
        playlist = Playlist.objects.get(name=get_song)
        if get_song:
            track_playlist, created = PlaylistTrack.objects.get_or_create(
                user=user, playlist=playlist, track=track

            )
            if created:
                playlist.track.add(track_playlist)
                messages.add_message(request, messages.INFO, "Audio add successfully")
            else:
                messages.add_message(request, messages.INFO, "This audio has already been added")

            return HttpResponseRedirect(f'/{track.slug}/')


class MusicProductView(View):

    def get(self, request, *args, **kwargs):
        """ Track main page """

        slug = kwargs.get('slug')
        song = MusicProduct.objects.filter(slug=slug)
        track = MusicProduct.objects.get(slug=slug)
        track_id = request.POST.get('track_id')

        if request.user.is_authenticated:
            """ Like view """
            like = Like.objects.filter(user=request.user, track_id__slug=slug)
            like_count = Like.objects.filter(track_id__slug=slug).count()
            """ Add to track in playlist view """
            user = Customer.objects.get(user=request.user)
            playlist = Playlist.objects.filter(user=user)
            playlist_track = PlaylistTrack.objects.filter(user=user, track=track)
        else:
            """ Like view (not authenticated) """
            like = Like.objects.none()
            like_count = Like.objects.none()
            """ Add to track in playlist view (not authenticated)"""
            playlist = Playlist.objects.none()
            playlist_track = PlaylistTrack.objects.none()

        context = {
            'songs_html': song,
            'playlist_html': playlist,
            'like_html': like,
            'track_id_html': track_id,
            'like_count_html': like_count,
            'track_html': track,
            'playlist_track': playlist_track,
        }
        return render(request, 'core/base_song.html', context)


def like_view(request):
    if request.method == "POST":
        """ Like """

        get_like = request.POST.get('like')
        track_id = request.POST.get('track_id')
        song = MusicProduct.objects.get(id=track_id)

        if get_like:
            like, created = Like.objects.get_or_create(user=request.user,
                                                       track_id=int(request.POST.get("track_id")))
            if created:
                music_product = MusicProduct.objects.get(id=track_id)
                music_product.all_like.add(like)
                music_product.save()
            if not created:
                like.delete()
            return HttpResponseRedirect(f'/{song.slug}/')


class PlaylistView(View):

    def get(self, request, *args, **kwargs):
        """ Output playlist """

        form = PlaylistForm(request.POST, request.FILES)

        if request.user.is_authenticated:
            playlist = Playlist.objects.filter(user__user_id=request.user)
        else:
            playlist = Playlist.objects.none()

        context = {
            'playlist_html': playlist,
            'form': form,
        }
        return render(request, 'core/playlist.html', context)


def create_playlist(request):
    """ Create playlist """

    if request.method == 'POST':

        user = Customer.objects.get(user=request.user)
        form = PlaylistForm(request.POST, request.FILES)

        if form.is_valid():
            name = form.cleaned_data['name']
            color = form.cleaned_data['color']
            image = form.cleaned_data['image']
            playlist = Playlist.objects.create(name=name, user=user, color=color, image=image)
            playlist.save()

            if name:
                customer = Customer.objects.get(user=request.user)
                customer.all_playlist.add(playlist)
                customer.save()
            return HttpResponseRedirect(reverse('playlists'))

        context = {
            'form': form,

        }

        return render(request, 'core/playlist.html', context)


def delete_playlist(request, name):
    """ Delete playlist """

    if request.method == 'GET':
        user = Customer.objects.get(user=request.user)
        playlist = Playlist.objects.get(name=name, user=user)
        playlist.delete()
        return HttpResponseRedirect(reverse('playlists'))


def delete_track_in_playlist(request, name, *args, **kwargs):
    """ Delete track in playlist """

    if request.method == 'GET':
        get_track_id = request.GET.get('track_id')
        playlist = Playlist.objects.get(name=name)
        playlist_track = PlaylistTrack.objects.get(id=get_track_id)
        playlist.track.remove(playlist_track)
        playlist_track.delete()
        return HttpResponseRedirect(f'/playlist/{name}')


class BasePlaylistView(View):

    def get(self, request, name, *args, **kwargs):
        """ Output playlist """

        user = Customer.objects.get(user=request.user)
        playlist = Playlist.objects.filter(name=name, user=user).prefetch_related('track')
        get_playlist = Playlist.objects.get(name=name, user=user)
        first_track_playlist = PlaylistTrack.objects.filter(playlist=get_playlist, user=user).first()

        context = {
            'playlist_html': playlist,
            'first_track_playlist': first_track_playlist,

        }
        return render(request, 'core/base_playlist.html', context)


class SearchView(View):

    def get(self, request, *args, **kwargs):
        """ Search track in website by author and title """

        get_song = request.GET.get("search")
        song = MusicProduct.objects.annotate(
            search=SearchVector('author', 'title'),
        ).filter(search=get_song)

        context = {
            'song_html': song,
        }
        return render(request, 'core/search.html', context)


class LoginView(View):
    """ Login for website """

    def get(self, request, *args, **kwargs):

        form = LoginForm(request.POST or None)

        context = {
            'form': form,
        }

        return render(request, 'core/login.html', context)

    def post(self, request, *args, **kwargs):

        form = LoginForm(request.POST or None)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return HttpResponseRedirect('/')

        context = {
            'form': form,
        }

        return render(request, 'core/login.html', context)


class CreateAccountView(View):

    def get(self, request, *args, **kwargs):
        """ Registration for website """

        form = RegistrationForm(request.POST or None)

        context = {
            'form': form,
        }

        return render(request, 'core/create_account.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                send_advertising=form.cleaned_data['send_advertising']
            )
            # code = generate_code()
            # message = code
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            user.is_active = False
            user.save()

            """ Send verification cod """

            current_site = get_current_site(request)
            email_body = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }

            link = reverse('activate', kwargs={
                'uidb64': email_body['uid'], 'token': email_body['token']})

            email_subject = 'Activate your account'

            activate_url = 'http://' + current_site.domain + link
            email = EmailMessage(
                email_subject,
                'Hi ' + user.username + ', Please the link below to activate your account \n' + activate_url,
                settings.EMAIL_HOST_USER,
                [new_user.email],
            )
            email.send(fail_silently=False)
            return HttpResponseRedirect('/login/')

        context = {
            'form': form,
        }
        return render(request, 'core/create_account.html', context)


class VerificationView(View):
    def get(self, request, uidb64, token):
        """ Verification cod """

        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login' + '?message=' + 'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')


class AdView(View):
    """ Advertisement """

    def get(self, request, *args, **kwargs):
        context = {
        }

        return render(request, 'core/advertising/ad_for_send.html', context)


class FavoriteTrackView(View):
    """ Customer favorite tracks """

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            like_track = Like.objects.filter(user=request.user)
        else:
            like_track = Like.objects.none()

        context = {
            'like_track_html': like_track,
        }

        return render(request, 'core/favorite_tracks.html', context)


class ProductListView(viewsets.ModelViewSet):
    queryset = MusicProduct.objects.all()
    serializer_class = MusicProductSerializer


class CategorySerializerView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@api_view()
def music_product_list_serializer(request):
    if request.method == 'GET':
        audio = MusicProduct.objects.all()
        serializer_class = MusicProductSerializer(audio, many=True)
        return Response(serializer_class.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MusicProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class MusicProductAddSerializer(generics.CreateAPIView):
    serializer_class = MusicProductSerializer

    def perform_create(self, serializer):
        serializer.save()
