# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Window',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(help_text=b'Url friendly title. Leaving it in blank will be autogenerated, but if defined must be unique.', unique=True)),
                ('description', models.CharField(max_length=256, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]