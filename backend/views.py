from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
# Create your views here.
from .models import Author, CorpusAuthors, Corpus, ResourceTexts, ResourceType
from django.forms.models import model_to_dict
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Link, Relation, TaggedItem, Resource, File, ClassAttribute, Class
from django.db.models import Q
from django.apps import apps
from django.core.files.base import ContentFile
from docx import Document
import os
import datetime

from django.core.files.base import ContentFile, File


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
def changeComments(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        comments = data.get('comments', None)
        resource_pk = data.get('resource_pk', None)
        name = str(datetime.datetime.now().time())[:8]

        commentary = ContentFile(b'')
        for comment in comments:
            temp = comment['text'] + '\n'
            commentary.write(temp.encode('utf-8'))

        resource_texts = ResourceTexts.objects.get(resource__pk=resource_pk)
        resource_texts.commentary.save(
            'commentary_' + name + '.txt', commentary)
        return HttpResponse(status=200)
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
        result = model_to_dict(res)
        # result['link'] = 'http://localhost:8000'+res.link.url
        result['link'] = 'https://annotation-project-backend.herokuapp.com'+res.link.url
        return JsonResponse(result, safe=False)
    return HttpResponse(status=403)


@csrf_exempt
def uploadDocx(request, pk):
    if request.method == 'POST':
        file_d = request.FILES.get('attached_file', None)
        name = str(datetime.datetime.now().time())[:8]
        if file_d is None:
            return HttpResponse(status=200)
        docx_file = Document(file_d)
        tables = docx_file.tables
        info_table = tables[0]

        corpus = Corpus.objects.get(pk=pk)
        r_type = ResourceType.objects.all().filter(name='Текст').first()
        resource = Resource(
            corpus=corpus,
            resource_type=r_type,
            title=info_table.rows[0].cells[1].text if len(
                info_table.rows[0].cells[1].text) != 0 else 'Не указано',
            title_origin=info_table.rows[1].cells[1].text if len(
                info_table.rows[1].cells[1].text) != 0 else 'Не указано',
            language=info_table.rows[2].cells[1].text if len(
                info_table.rows[2].cells[1].text) != 0 else 'Не указано',
            dialect=info_table.rows[3].cells[1].text if len(
                info_table.rows[3].cells[1].text) != 0 else 'Не указано',
            speech=info_table.rows[4].cells[1].text if len(
                info_table.rows[4].cells[1].text) != 0 else 'Не указано',
            theme=info_table.rows[5].cells[1].text if len(
                info_table.rows[5].cells[1].text) != 0 else 'Не указано',
            time_of_recording=info_table.rows[6].cells[1].text if len(
                info_table.rows[6].cells[1].text) != 0 else 'Не указано',

            published=info_table.rows[15].cells[1].text if len(
                info_table.rows[15].cells[1].text) != 0 else 'Не указано',
            place_of_storage=info_table.rows[16].cells[1].text if len(
                info_table.rows[16].cells[1].text) != 0 else 'Не указано',
            variants=info_table.rows[17].cells[1].text if len(
                info_table.rows[17].cells[1].text) != 0 else 'Не указано',
            areal=info_table.rows[18].cells[1].text if len(
                info_table.rows[18].cells[1].text) != 0 else 'Не указано',
            extras=info_table.rows[19].cells[1].text if len(
                info_table.rows[19].cells[1].text) != 0 else 'Не указано'
        )

        main_table = tables[1]

        temp = ''
        original = ContentFile(b'')
        translation = ContentFile(b'')
        commentary = ContentFile(b'')

        for cell in main_table.columns[0].cells:
            temp = cell.text + '\n'
            original.write(temp.encode('utf-8'))

        for cell in main_table.columns[2].cells:
            temp = cell.text + '\n'
            translation.write(temp.encode('utf-8'))

        for cell in main_table.columns[3].cells:
            temp = cell.text + '\n'
            commentary.write(temp.encode('utf-8'))

        resource.save()
        resource_texts = ResourceTexts(resource=resource)
        resource_texts.save()

        resource_texts.original.save('original_' + name + '.txt', original)
        resource_texts.translation.save(
            'translation_' + name + '.txt', translation)
        resource_texts.commentary.save(
            'commentary_' + name + '.txt', commentary)

        return HttpResponse(status=200)
    # save()
    # for row in main_table.rows:
    #     Line(text_left=row.cells[0].text,
    #          text_right=row.cells[2].text, block=block, position=i).save()
    #     i = i + 1


@ csrf_exempt
def getClassAttributes(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        pk = data.get('pk', None)
        if pk is not None:
            result = classRecursion(pk, [])
            return JsonResponse({'related_class': pk, 'result': result}, safe=False)
        return HttpResponse(status=404)
    return HttpResponse(status=403)


def classRecursion(class_id, result):
    class_obj = Class.objects.get(pk=class_id)
    temp = ClassAttribute.objects.all().filter(related_class__pk=class_obj.pk)

    for line in temp:
        result.append(model_to_dict(line))

    if class_obj.parent is None:
        return result

    return classRecursion(class_obj.parent.pk, result)

    #    title = info_table.rows[0].cells[1].text
    #     title_origin = info_table.rows[1].cells[1].text
    #     language = info_table.rows[2].cells[1].text
    #     dialect = info_table.rows[3].cells[1].text
    #     speech = info_table.rows[4].cells[1].text
    #     theme = info_table.rows[5].cells[1].text
    #     time_of_recording = info_table.rows[6].cells[1].text
    #     place_of_recording = info_table.rows[7].cells[1].text

    #     author = info_table.rows[8].cells[1].text  # исполнитель
    #     collector = info_table.rows[9].cells[1].text
    #     decryptor = info_table.rows[10].cells[1].text
    #     translator = info_table.rows[11].cells[1].text
    #     translation_redactor = info_table.rows[12].cells[1].text
    #     origin_redactor = info_table.rows[13].cells[1].text
    #     commentator = info_table.rows[14].cells[1].text

    #     published = info_table.rows[15].cells[1].text
    #     place_of_storage = info_table.rows[16].cells[1].text
    #     variants = info_table.rows[17].cells[1].text
    #     areal = info_table.rows[18].cells[1].text
    #     extras = info_table.rows[19].cells[1].text
