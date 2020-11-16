# Generated by Django 3.0.3 on 2020-11-15 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('backend', '0004_auto_20201114_1237'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TaggedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.RemoveField(
            model_name='classrelation',
            name='child',
        ),
        migrations.RemoveField(
            model_name='classrelation',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='classrelation',
            name='relation',
        ),
        migrations.RemoveField(
            model_name='objectrelation',
            name='child',
        ),
        migrations.RemoveField(
            model_name='objectrelation',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='objectrelation',
            name='relation',
        ),
        migrations.DeleteModel(
            name='Test',
        ),
        migrations.DeleteModel(
            name='ClassRelation',
        ),
        migrations.DeleteModel(
            name='ObjectRelation',
        ),
        migrations.AddField(
            model_name='link',
            name='first_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first_item', to='backend.TaggedItem'),
        ),
        migrations.AddField(
            model_name='link',
            name='relation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Relation'),
        ),
        migrations.AddField(
            model_name='link',
            name='second_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='second_item', to='backend.TaggedItem'),
        ),
        migrations.AlterUniqueTogether(
            name='link',
            unique_together={('first_item', 'second_item', 'relation')},
        ),
    ]