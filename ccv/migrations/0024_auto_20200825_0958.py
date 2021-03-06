# Generated by Django 3.0.7 on 2020-08-25 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ccv', '0023_auto_20200708_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicworkexperience',
            name='employment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='academic_work_experience', to='ccv.Employment'),
        ),
        migrations.AlterField(
            model_name='areaofresearch',
            name='academic_work_experience',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='academic_work_experience_aor', to='ccv.AcademicWorkExperience'),
        ),
        migrations.AlterField(
            model_name='areaofresearch',
            name='credential',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='credential_aor', to='ccv.Credential'),
        ),
        migrations.AlterField(
            model_name='areaofresearch',
            name='degree',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='degree_aor', to='ccv.Degree'),
        ),
        migrations.AlterField(
            model_name='areaofresearch',
            name='non_academic_work_experience',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='non_academic_work_experience_aor', to='ccv.NonAcademicWorkExperience'),
        ),
        migrations.AlterField(
            model_name='areaofresearch',
            name='recognition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recognition_aor', to='ccv.Recognition'),
        ),
        migrations.AlterField(
            model_name='areaofresearch',
            name='research_funding_assessment_activity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assessment_activity_aor', to='ccv.ResearchFundingApplicationAssessmentActivity'),
        ),
        migrations.AlterField(
            model_name='areaofresearch',
            name='research_funding_history',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='funding_history_aor', to='ccv.ResearchFundingHistory'),
        ),
        migrations.AlterField(
            model_name='areaofresearch',
            name='user_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_aor', to='ccv.UserProfile'),
        ),
        migrations.AlterField(
            model_name='employment',
            name='ccv',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employment', to='ccv.CanadianCommonCv'),
        ),
        migrations.AlterField(
            model_name='identification',
            name='ccv',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='identification', to='ccv.CanadianCommonCv'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='ccv',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to='ccv.CanadianCommonCv'),
        ),
    ]
