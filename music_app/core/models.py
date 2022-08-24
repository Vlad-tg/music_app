from django.db import models
from datetime import date, datetime
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(verbose_name="Genre", max_length=255)
    slug = models.SlugField(verbose_name="Slug", allow_unicode=True, unique=True)
    image = models.ImageField(verbose_name='Imagine', upload_to=r'img_genre/', default='/img/default.jpg')
    description = models.TextField(verbose_name='Description genre', null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    """ Model category """

    name = models.CharField(verbose_name="Category", max_length=255)
    slug = models.SlugField(verbose_name="Slug", allow_unicode=True, unique=True)
    image = models.ImageField(verbose_name='Imagine', upload_to=r'img_category/', null=True, blank=True)
    description = models.TextField(verbose_name='Description category', null=True, blank=True)
    date = models.DateField(default=datetime.today, verbose_name="Date added")
    color = models.TextField(verbose_name='Color background', null=True, blank=True)

    def __str__(self):
        return self.name


class MusicProduct(models.Model):
    """ Model track """

    STATUS = (
        ('P', 'Posted'),
        ('NP', 'Not posted')
    )

    title = models.CharField(verbose_name='Title music', max_length=255)
    slug = models.SlugField(verbose_name="Slug", allow_unicode=True, unique=True)
    file = models.FileField(verbose_name='File', upload_to=r'tracks/')
    duration_track = models.CharField(verbose_name='Duration track', max_length=255, default='0:00')
    track_url = models.URLField(max_length=255, verbose_name='Url track', blank=True, null=True)
    author = models.CharField(verbose_name='Author', max_length=255)
    image = models.ImageField(verbose_name='Imagine', upload_to=r'img_tracks/')
    description = models.TextField(verbose_name='Track description', null=True, blank=True)
    status_track = models.CharField(verbose_name='Status track', choices=STATUS, max_length=255)
    data_added = models.DateField(auto_now_add=True, verbose_name="Date added")
    all_like = models.ManyToManyField('Like', verbose_name='All like')
    category = models.ManyToManyField(Category, verbose_name='Track category', db_column='all_category')
    genre = models.ManyToManyField(Genre, verbose_name='All genre', db_column='all_genre')
    format = models.CharField(verbose_name='Format', max_length=255, null=True, blank=True)
    size_file = models.CharField(verbose_name='Size file', max_length=255, null=True, blank=True)
    bitrate = models.CharField(verbose_name='Bitrate', max_length=255, null=True, blank=True)

    def __str__(self):
        return "Track: {} ({})".format(self.title, self.author)

    def get_absolute_url(self):
        return reverse('base_song', kwargs={'slug': self.slug})


class Customer(models.Model):
    """ Model customer(user) """

    MIN_RESOLUTION = (200, 200)
    MAX_RESOLUTION = (8000, 8000)
    MAX_IMAGE_SIZE = 3145728

    user = models.ForeignKey(User, verbose_name='Customer', on_delete=models.CASCADE)
    # icon = models.ImageField(verbose_name='Icon', default='owner.png', upload_to='icon/')
    # sequence = models.ImageField(verbose_name='Sequence', default='sequence.jpg', upload_to='sequence/')
    phone = models.CharField(max_length=20, verbose_name='Phone', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Address', null=True, blank=True)
    send_advertising = models.BooleanField(default=False, verbose_name='Consent to send advertising')
    all_playlist = models.ManyToManyField('Playlist', verbose_name='All playlists', blank=True)

    def __str__(self):
        return "Customer: {} {}".format(self.user.username, self.user.email)


class Like(models.Model):
    """ Model like """

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Customer')
    track = models.ForeignKey(MusicProduct, on_delete=models.CASCADE, verbose_name='Track')

    def __str__(self):
        return f"{self.user} - {self.track}"


class Playlist(models.Model):
    """ Model playlist(created by the user) """

    name = models.CharField(verbose_name='Name playlist', max_length=255)
    image = models.ImageField(verbose_name='Image for playlist', default='img_playlist/music_icon.svg',
                              upload_to=r'img_playlist/')
    user = models.ForeignKey('Customer', verbose_name='Customer', on_delete=models.CASCADE,
                             related_name='Customer website+')
    track = models.ManyToManyField('PlaylistTrack', verbose_name='Track', blank=True,
                                   related_name='Track name related+')
    date = models.DateField(default=datetime.today, verbose_name="Date create")
    color = models.TextField(verbose_name='Playlist background color', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.user.user.username}"

    def get_absolute_url(self):
        return reverse('base_playlist', kwargs={'name': self.name})


class PlaylistTrack(models.Model):
    """ Model track for playlist(created by the user) """

    user = models.ForeignKey(Customer, verbose_name='Customer', on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, verbose_name='Customer playlist', on_delete=models.CASCADE)
    track = models.ForeignKey(MusicProduct, verbose_name='Name track', on_delete=models.CASCADE)

    def __str__(self):
        return "Track: {} (for playlist ({}))".format(self.track.title, self.playlist.name)
