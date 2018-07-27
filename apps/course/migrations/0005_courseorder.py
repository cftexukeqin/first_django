# Generated by Django 2.0.5 on 2018-07-26 23:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0004_auto_20180725_1743'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseOrder',
            fields=[
                ('uid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('amount', models.FloatField(default=0)),
                ('status', models.SmallIntegerField(default=1)),
                ('istype', models.SmallIntegerField(default=1)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='course.Course')),
            ],
            options={
                'ordering': ['-create_time'],
            },
        ),
    ]
