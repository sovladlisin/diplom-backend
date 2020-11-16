from django.db import models
from db_file_storage.model_utils import delete_file, delete_file_if_needed
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

# Test model


class File(models.Model):
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)


# Отмеченный элемент (Любой класс)
class TaggedItem(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Relation(models.Model):
    name = models.CharField(max_length=300, default='')

# Связь между любыми таблицами


class Link(models.Model):
    relation = models.ForeignKey(Relation, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        TaggedItem, on_delete=models.CASCADE, related_name="first_item")
    child = models.ForeignKey(
        TaggedItem, on_delete=models.CASCADE, related_name="second_item")

    def __str__(self):
        return self.relation.__str__()

    class Meta:
        unique_together = ("parent", "child", "relation")


class Place(models.Model):
    name = models.CharField(max_length=300, default="Не указано")
    location = models.CharField(max_length=300, default="Не указано")

    tag = GenericRelation(TaggedItem, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self._state.adding:
            pk = self.pk  # pk will be None like objects if self is new instance
            super().save(*args, **kwargs)
            TaggedItem(content_object=self).save()
        else:
            pk = self.pk  # pk will be None like objects if self is new instance
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ResourceType(models.Model):
    name = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=300, default="Не указано")
    surname = models.CharField(max_length=300, default="Не указано")
    patronymic = models.CharField(max_length=300, default="Не указано")
    initials = models.CharField(max_length=300, default="Не указано")
    date_of_birth = models.CharField(max_length=300, default="Не указано")
    date_of_death = models.CharField(max_length=300, default="Не указано")
    place_of_birth = models.ForeignKey(
        Place, blank=True, null=True, related_name='place_of_birth', on_delete=models.PROTECT)
    picture = models.CharField(max_length=300, default="Не указано")

    tag = GenericRelation(TaggedItem, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self._state.adding:
            pk = self.pk  # pk will be None like objects if self is new instance
            super().save(*args, **kwargs)
            TaggedItem(content_object=self).save()
        else:
            pk = self.pk  # pk will be None like objects if self is new instance
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name + self.surname + self.patronymic


class Corpus(models.Model):
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='corpus_parent', on_delete=models.PROTECT)
    name = models.CharField(max_length=300, default="Не указано")
    language = models.CharField(max_length=300, default="Не указано")
    dialect = models.CharField(max_length=300, default="Не указано")
    extras = models.CharField(max_length=300, default="Не указано")

    tag = GenericRelation(TaggedItem, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self._state.adding:
            pk = self.pk  # pk will be None like objects if self is new instance
            super().save(*args, **kwargs)
            TaggedItem(content_object=self).save()
        else:
            pk = self.pk  # pk will be None like objects if self is new instance
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Resource(models.Model):
    corpus = models.ForeignKey(
        Corpus, blank=True, null=True, related_name='corpus', on_delete=models.CASCADE)
    name = models.CharField(max_length=300, default="Не указано")
    resource_type = models.ForeignKey(
        ResourceType, blank=True, null=True, related_name='resource_type', on_delete=models.PROTECT)
    language = models.CharField(max_length=300, default="Не указано")
    dialect = models.CharField(max_length=300, default="Не указано")
    speech = models.CharField(max_length=300, default="Не указано")
    theme = models.CharField(max_length=300, default="Не указано")
    time_of_recording = models.CharField(max_length=300, default="Не указано")

    place_of_recording = models.ForeignKey(
        Place, blank=True, null=True, related_name='resource_place_of_recording', on_delete=models.PROTECT)

    author = models.ForeignKey(
        Author, blank=True, null=True, related_name='resource_author', on_delete=models.PROTECT)
    collector = models.ForeignKey(
        Author, blank=True, null=True, related_name='resource_collector', on_delete=models.PROTECT)
    decryptor = models.ForeignKey(
        Author, blank=True, null=True, related_name='resource_decryptor', on_delete=models.PROTECT)
    translator = models.ForeignKey(
        Author, blank=True, null=True, related_name='resource_translator', on_delete=models.PROTECT)
    translation_redactor = models.ForeignKey(
        Author, blank=True, null=True, related_name='resource_translation_redactor', on_delete=models.PROTECT)
    origin_redactor = models.ForeignKey(
        Author, blank=True, null=True, related_name='resource_origin_redactor', on_delete=models.PROTECT)
    commentator = models.ForeignKey(
        Author, blank=True, null=True, related_name='resource_commentator', on_delete=models.PROTECT)

    published = models.CharField(max_length=300, default="Не указано")
    variants = models.CharField(max_length=300, default="Не указано")
    areal = models.CharField(max_length=300, default="Не указано")
    extras = models.CharField(max_length=300, default="Не указано")

    link = models.FileField(
        upload_to='backend.File/bytes/filename/mimetype', blank=True, null=True)

    tag = GenericRelation(TaggedItem, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self._state.adding:
            pk = self.pk  # pk will be None like objects if self is new instance
            delete_file_if_needed(self, 'link')
            super(Resource, self).save(*args, **kwargs)
            TaggedItem(content_object=self).save()
        else:
            pk = self.pk  # pk will be None like objects if self is new instance
            delete_file_if_needed(self, 'link')
            super(Resource, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(Resource, self).delete(*args, **kwargs)
        delete_file(self, 'link')

    def __str__(self):
        return self.name


class CorpusPlaces(models.Model):
    corpus = models.ForeignKey(
        Corpus, blank=True, null=True,  on_delete=models.CASCADE)
    place = models.ForeignKey(
        Place, blank=True, null=True,  on_delete=models.CASCADE)

    def __str__(self):
        return self.corpus.name + self.place.name


class CorpusAuthors(models.Model):
    corpus = models.ForeignKey(
        Corpus, blank=True, null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(
        Author, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.corpus.name + self.author.name


class TextToText(models.Model):
    original = models.ForeignKey(
        Resource, blank=True, null=True, related_name='original', on_delete=models.CASCADE)
    translated = models.ForeignKey(
        Resource, blank=True, null=True, related_name='translated', on_delete=models.CASCADE)

    def __str__(self):
        return self.original.name + '->' + self.translated.name


class Class(models.Model):
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='class_parent', on_delete=models.CASCADE)
    corpus = models.ForeignKey(
        Corpus, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, default="Не указано")

    tag = GenericRelation(TaggedItem, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self._state.adding:
            pk = self.pk  # pk will be None like objects if self is new instance
            super().save(*args, **kwargs)
            TaggedItem(content_object=self).save()
        else:
            pk = self.pk  # pk will be None like objects if self is new instance
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Object(models.Model):
    parent_class = models.ForeignKey(
        Class, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, default="Не указано")

    tag = GenericRelation(TaggedItem, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self._state.adding:
            pk = self.pk  # pk will be None like objects if self is new instance
            super().save(*args, **kwargs)
            TaggedItem(content_object=self).save()
        else:
            pk = self.pk  # pk will be None like objects if self is new instance
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ClassAttribute(models.Model):
    related_class = models.ForeignKey(
        Class, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, default='')


class ObjectAttributeValue(models.Model):
    related_attribute = models.ForeignKey(
        ClassAttribute, blank=True, null=True, on_delete=models.CASCADE)
    related_object = models.ForeignKey(
        Object, blank=True, null=True, on_delete=models.CASCADE)
    value = models.CharField(max_length=3000, default='')


class Markup(models.Model):
    name = models.CharField(max_length=100, default="Не указано")
    text = models.ForeignKey(
        Resource, blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Entity(models.Model):
    obj = models.ForeignKey(
        Object, blank=True, null=True, related_name='object', on_delete=models.CASCADE)

    position_start = models.IntegerField(default=0)
    position_end = models.IntegerField(default=0)
    markup = models.ForeignKey(
        Markup, blank=True, null=True, related_name='markup', on_delete=models.CASCADE)

    def __str__(self):
        return self.position_start.__str__() + self.position_end + self.markup.name
