# Generated by Django 3.0.7 on 2020-06-23 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ccv', '0011_auto_20200623_0858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researchfundinghistory',
            name='ccv',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ccv.CanadianCommonCv'),
        ),
    ]
