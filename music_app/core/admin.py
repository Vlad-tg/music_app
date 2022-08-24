from django.contrib import admin
from .models import *
from .forms import *


class CategoryAdmin(admin.ModelAdmin):
    change_form_template = "core/admin_templates/admin_template_category.html"
    ordering = ['name']
    fieldsets = (
        (None, {
            'fields': (('name', 'slug'), 'image', 'description', 'date')
        }),
        ('Chose color for background', {
            'fields': ('color',)
        }),
    )
    search_fields = ["name"]


class MusicProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'author', 'file', 'status_track', 'data_added')
    # list_display_links = ('author', )
    # radio_fields = {"track_category": admin.VERTICAL}  --------- foringkey
    autocomplete_fields = ['category']
    # prepopulated_fields = {"slug": ("title",)}
    list_editable = ('status_track',)
    list_filter = ('author', 'status_track', 'data_added')

    fields = [('title', 'slug'), 'file', 'track_url', 'duration_track', 'all_like',
              # 'view_track_url',
              'author',
              'image',
              'description',
              'status_track',
              'category',
              'genre',
              'format',
              'size_file',
              'bitrate']
    date_hierarchy = 'data_added'
    filter_horizontal = ('genre',)
    list_per_page = 5
    search_fields = ['author']
    # formfield_overrides = {
    #     models.TextField: {'widget': RichTextEditorWidget},
    # }
    # forms = MusicProduct
    # readonly_fields = ['view_track_url']
    #
    # def view_track_url(self, obj):
    #     return obj.title
    #
    # view_track_url.empty_value_display = '???'

    # inlines = [MusicProductAllGenreInline]
    # fieldsets = (
    #     (None, {
    #         'fields': (('title', 'slug'), 'author')
    #     }),
    #     ('Url file', {
    #         'classes': ('collapse',),
    #         'fields': ('file', 'track_url')
    #     }),
    # )


admin.site.register(PlaylistTrack)
admin.site.register(Playlist)
admin.site.register(Like)
admin.site.register(Customer)
admin.site.register(MusicProduct, MusicProductAdmin)
admin.site.register(Genre)
admin.site.register(Category, CategoryAdmin)
