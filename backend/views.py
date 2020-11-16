from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
# Create your views here.
from .models import Author, CorpusAuthors
from django.forms.models import model_to_dict
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Link, Relation, TaggedItem, Resource, File
from django.db.models import Q
from django.apps import apps
from django.core.files.base import ContentFile


def LoadCheck(request):
    return HttpResponse("loaderio-dad475efde7ab1a335f97bc6bf875046")


@csrf_exempt
def getLinks(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        model_pk = data.get('model_pk', None)
        model_name = data.get('model_name', None)

        Model = apps.get_model(app_label="backend", model_name=model_name)
        item = Model.objects.get(pk=model_pk)

        result_slaves = {}
        result_masters = {}

        slaves = Link.objects.all().filter(Q(parent=item.tag.first()))
        masters = Link.objects.all().filter(Q(child=item.tag.first()))

        for slave in slaves:
            relation_name = slave.relation.name
            temp_model_pk = slave.child.object_id
            temp_model_name = slave.child.content_type.__str__().split(' | ')[
                1]

            if relation_name not in result_slaves:
                result_slaves[relation_name] = []

            temp = result_slaves[relation_name]
            temp.append({'model_pk': temp_model_pk,
                         'model_name': temp_model_name,
                         'link_pk': slave.pk})
            result_slaves[relation_name] = temp

        for master in masters:
            relation_name = master.relation.name
            temp_model_pk = master.parent.object_id
            temp_model_name = master.parent.content_type.__str__().split(' | ')[
                1]

            if relation_name not in result_masters:
                result_masters[relation_name] = []

            temp = result_masters[relation_name]
            temp.append({'model_pk': temp_model_pk,
                         'model_name': temp_model_name,
                         'link_pk': master.pk})
            result_masters[relation_name] = temp

        return JsonResponse({'model_pk': model_pk, 'model_name': model_name, 'parents': result_masters, 'children': result_slaves}, safe=False)
    return HttpResponse(status=403)


@csrf_exempt
def addLink(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        relation = data.get('relation', None)

        parent_model_pk = data.get('parent_model_pk', None)
        parent_model_name = data.get('parent_model_name', None)

        child_model_pk = data.get('child_model_pk', None)
        child_model_name = data.get('child_model_name', None)

        ModelParent = apps.get_model(
            app_label="backend", model_name=parent_model_name)
        parent = ModelParent.objects.get(pk=parent_model_pk)

        ModelChild = apps.get_model(
            app_label="backend", model_name=child_model_name)
        child = ModelChild.objects.get(pk=child_model_pk)

        relation = Relation.objects.get(pk=relation)
        link = Link(relation=relation, parent=parent.tag.first(),
                    child=child.tag.first())
        link.save()
        return JsonResponse({'pk': link.pk}, safe=False)
    return HttpResponse(status=403)


@csrf_exempt
def uploadFile(request):
    if request.method == 'POST':
        file_d = request.FILES['image']
        res = Resource()
        res.link.save(file_d.name,  ContentFile(file_d.read()))
        return HttpResponse(status=200)
    return HttpResponse(status=403)


@csrf_exempt
def connectFileToResource(request, pk):
    if request.method == 'POST':
        file_d = request.FILES.get('attached_file', None)
        if file_d is None:
            return HttpResponse(status=200)
        res = Resource.objects.get(pk=pk)
        res.link.save(file_d.name,  ContentFile(file_d.read()))
        return HttpResponse(status=200)
    return HttpResponse(status=403)
