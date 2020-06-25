# Generated by Django 3.0.7 on 2020-06-25 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccv', '0019_auto_20200625_0840'),
    ]

    operations = [
        migrations.AddField(
            model_name='disciplinetrainedin',
            name='order',
            field=models.IntegerField(blank=True, help_text='This field is used to order the entries. A value of 1 will show up at top.', null=True),
        ),
        migrations.AddField(
            model_name='geographicalregion',
            name='order',
            field=models.IntegerField(blank=True, help_text='This field is used to order the entries. A value of 1 will show up at top.', null=True),
        ),
        migrations.AddField(
            model_name='researchcentre',
            name='order',
            field=models.IntegerField(blank=True, help_text='This field is used to order the entries. A value of 1 will show up at top.', null=True),
        ),
        migrations.AddField(
            model_name='technologicalapplication',
            name='order',
            field=models.IntegerField(blank=True, help_text='This field is used to order the entries. A value of 1 will show up at top.', null=True),
        ),
        migrations.AddField(
            model_name='temporalperiod',
            name='order',
            field=models.IntegerField(blank=True, help_text='This field is used to order the entries. A value of 1 will show up at top.', null=True),
        ),
    ]
