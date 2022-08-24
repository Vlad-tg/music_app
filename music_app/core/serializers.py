from rest_framework import serializers
from .models import MusicProduct
from .models import Category


class CategorySerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    slug = serializers.SlugField(allow_unicode=True)
    image = serializers.ImageField(max_length=None, allow_empty_file=False)
    description = serializers.CharField(style={'base_template': 'textarea.html'})
    color = serializers.CharField(style={'base_template': 'textarea.html'})

    def create(self, validated_data):

        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.name = validated_data.get('name', instance.name)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.color = validated_data.get('color', instance.color)
        instance.save()
        return instance


class CategoryMusicProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name']


class MusicProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = MusicProduct
        fields = "__all__"



