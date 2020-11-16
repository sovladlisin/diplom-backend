from rest_framework import serializers
from backend.models import TaggedItem, Link, ObjectAttributeValue, ClassAttribute, Relation, Markup, Class, Object, Corpus, Resource, ResourceType, Author, TextToText, Place, CorpusPlaces, CorpusAuthors, TextToText, Entity


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'


class TaggedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaggedItem
        fields = '__all__'


class ObjectAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectAttributeValue
        fields = '__all__'


class ClassAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassAttribute
        fields = '__all__'


class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = '__all__'


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = '__all__'


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class CorpusPlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorpusPlaces
        fields = '__all__'


class CorpusAuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorpusAuthors
        fields = '__all__'


class TextToTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextToText
        fields = '__all__'


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = '__all__'


class CorpusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corpus
        fields = '__all__'


class ResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resource
        fields = '__all__'


class MarkupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Markup
        fields = '__all__'


class ResourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceType
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
