from rest_framework import routers
from .api import TaggedItemViewSet, LinkViewSet, ObjectAttributeValueViewSet, ClassAttributeViewSet, RelationViewSet, MarkupViewSet, ClassViewSet, ObjectViewSet, CorpusViewSet, ResourceViewSet, ResourceTypeViewSet, AuthorViewSet, TextToTextViewSet, PlaceViewSet, CorpusPlacesViewSet, CorpusAuthorsViewSet, EntityViewSet
from .views import LoadCheck, getLinks, addLink, uploadFile, connectFileToResource
from django.urls import path
from django.conf.urls import url
router = routers.DefaultRouter()
router.register('api/corpus', CorpusViewSet, 'corpus')
router.register('api/resource', ResourceViewSet, 'resource')
router.register('api/resourceType', ResourceTypeViewSet, 'resourceType')
router.register('api/author', AuthorViewSet, 'author')
router.register('api/textToText', TextToTextViewSet, 'textToText')
router.register('api/place', PlaceViewSet, 'place')
router.register('api/corpusPlaces', CorpusPlacesViewSet, 'corpusPlaces')
router.register('api/corpusAuthors', CorpusAuthorsViewSet, 'corpusAuthors')
router.register('api/entity', EntityViewSet, 'entity')
router.register('api/class', ClassViewSet, 'class')
router.register('api/object', ObjectViewSet, 'object')
router.register('api/markup', MarkupViewSet, 'markup')
router.register('api/relation', RelationViewSet, 'relation')
router.register('api/link', LinkViewSet, 'link')
router.register('api/taggedItem', TaggedItemViewSet, 'taggedItem')
router.register('api/objectAttributeValue',
                ObjectAttributeValueViewSet, 'objectAttributeValue')
router.register('api/classAttributes',
                ClassAttributeViewSet, 'classAttributes')


urlpatterns = [path('loaderio-dad475efde7ab1a335f97bc6bf875046/',
                    LoadCheck, name='loadcheck'),
               path('api/getLinks',
                    getLinks, name='getLinks'),
               path('api/addLink',
                    addLink, name='addLink'),
               url(r'^api/connectFileToResource/(?P<pk>\d+)/$',
                   connectFileToResource, name='connectFileToResource'),
               ] + router.urls
