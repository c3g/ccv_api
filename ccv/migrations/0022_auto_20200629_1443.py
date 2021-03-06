# Generated by Django 3.0.7 on 2020-06-29 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccv', '0021_auto_20200625_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreview',
            name='description_of_role',
            field=models.CharField(blank=True, help_text='brief description of contribution role towards this publication', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='clinicalcareguideline',
            name='description_of_role',
            field=models.CharField(blank=True, help_text='brief description of contribution role towards this publication', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='dictionaryentry',
            name='description_of_role',
            field=models.CharField(blank=True, help_text='brief description of contribution role towards this publication', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='journal',
            name='description_of_role',
            field=models.CharField(blank=True, help_text='brief description of contribution role towards this publication', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='journal',
            name='journal',
            field=models.CharField(blank=True, help_text='Name of the journal in which the article is published, or to be published', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='litigation',
            name='description_of_role',
            field=models.CharField(blank=True, help_text='brief description of contribution role towards this publication', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='publicationstaticabstract',
            name='description_of_role',
            field=models.CharField(blank=True, help_text='brief description of contribution role towards this publication', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='description_of_role',
            field=models.CharField(blank=True, help_text='brief description of contribution role towards this publication', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='description_of_role',
            field=models.CharField(blank=True, help_text='brief description of contribution role towards this publication', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='thesisdissertation',
            name='description_of_role',
            field=models.CharField(blank=True, help_text='brief description of contribution role towards this publication', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='workingpaper',
            name='description_of_role',
            field=models.CharField(blank=True, help_text='brief description of contribution role towards this publication', max_length=1000, null=True),
        ),
    ]
