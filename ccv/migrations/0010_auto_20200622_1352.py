# Generated by Django 3.0.7 on 2020-06-22 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccv', '0009_mostsignificantcontribution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='othermembership',
            name='role',
            field=models.CharField(blank=True, help_text="The person's role in this activity", max_length=50, null=True),
        ),
    ]