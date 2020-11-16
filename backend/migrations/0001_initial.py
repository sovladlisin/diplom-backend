# Generated by Django 3.0.3 on 2020-11-09 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Не указано', max_length=300)),
                ('surname', models.CharField(default='Не указано', max_length=300)),
                ('patronymic', models.CharField(default='Не указано', max_length=300)),
                ('initials', models.CharField(default='Не указано', max_length=300)),
                ('date_of_birth', models.CharField(default='Не указано', max_length=300)),
                ('date_of_death', models.CharField(default='Не указано', max_length=300)),
                ('picture', models.CharField(default='Не указано', max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Не указано', max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Corpus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Не указано', max_length=300)),
                ('language', models.CharField(default='Не указано', max_length=300)),
                ('dialect', models.CharField(default='Не указано', max_length=300)),
                ('extras', models.CharField(default='Не указано', max_length=300)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='corpus_parent', to='backend.Corpus')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bytes', models.TextField()),
                ('filename', models.CharField(max_length=255)),
                ('mimetype', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Не указано', max_length=300)),
                ('parent_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.Class')),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Не указано', max_length=300)),
                ('location', models.CharField(default='Не указано', max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Не указано', max_length=300)),
                ('language', models.CharField(default='Не указано', max_length=300)),
                ('dialect', models.CharField(default='Не указано', max_length=300)),
                ('speech', models.CharField(default='Не указано', max_length=300)),
                ('theme', models.CharField(default='Не указано', max_length=300)),
                ('time_of_recording', models.CharField(default='Не указано', max_length=300)),
                ('published', models.CharField(default='Не указано', max_length=300)),
                ('variants', models.CharField(default='Не указано', max_length=300)),
                ('areal', models.CharField(default='Не указано', max_length=300)),
                ('extras', models.CharField(default='Не указано', max_length=300)),
                ('link', models.FileField(blank=True, null=True, upload_to='backend.File/bytes/filename/mimetype')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='resource_author', to='backend.Author')),
                ('collector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='resource_collector', to='backend.Author')),
                ('commentator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='resource_commentator', to='backend.Author')),
                ('corpus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='corpus', to='backend.Corpus')),
                ('decryptor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='resource_decryptor', to='backend.Author')),
                ('origin_redactor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='resource_origin_redactor', to='backend.Author')),
                ('place_of_recording', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='resource_place_of_recording', to='backend.Place')),
            ],
        ),
        migrations.CreateModel(
            name='ResourceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('salary', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TextToText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='original', to='backend.Resource')),
                ('translated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translated', to='backend.Resource')),
            ],
        ),
        migrations.AddField(
            model_name='resource',
            name='resource_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='resource_type', to='backend.ResourceType'),
        ),
        migrations.AddField(
            model_name='resource',
            name='translation_redactor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='resource_translation_redactor', to='backend.Author'),
        ),
        migrations.AddField(
            model_name='resource',
            name='translator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='resource_translator', to='backend.Author'),
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Не указано', max_length=300)),
                ('child', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relation_child', to='backend.Object')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relation_parent', to='backend.Object')),
            ],
        ),
        migrations.CreateModel(
            name='Markup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Не указано', max_length=100)),
                ('text', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='backend.Resource')),
            ],
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_start', models.IntegerField(default=0)),
                ('position_end', models.IntegerField(default=0)),
                ('markup', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='markup', to='backend.Markup')),
                ('obj', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='object', to='backend.Object')),
            ],
        ),
        migrations.CreateModel(
            name='CorpusPlaces',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corpus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.Corpus')),
                ('place', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.Place')),
            ],
        ),
        migrations.CreateModel(
            name='CorpusAuthors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.Author')),
                ('corpus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.Corpus')),
            ],
        ),
        migrations.AddField(
            model_name='class',
            name='corpus',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.Corpus'),
        ),
        migrations.AddField(
            model_name='class',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='class_parent', to='backend.Class'),
        ),
        migrations.AddField(
            model_name='author',
            name='place_of_birth',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='place_of_birth', to='backend.Place'),
        ),
    ]
