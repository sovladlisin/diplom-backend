# Generated by Django 3.0.3 on 2020-11-15 08:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_auto_20201115_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='class_parent', to='backend.Class'),
        ),
    ]
