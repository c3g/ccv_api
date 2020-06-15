# Generated by Django 3.0.5 on 2020-06-14 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ccv', '0005_auto_20200614_0844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='areaofresearch',
            name='academic_work_experience',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ccv.AcademicWorkExperience'),
        ),
        migrations.AlterField(
            model_name='areaofresearch',
            name='non_academic_work_experience',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ccv.NonAcademicWorkExperience'),
        ),
        migrations.AlterField(
            model_name='areaofresearch',
            name='research_funding_assessment_activity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ccv.ResearchFundingApplicationAssessmentActivity'),
        ),
        migrations.AlterField(
            model_name='areaofresearch',
            name='research_funding_history',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ccv.ResearchFundingHistory'),
        ),
        migrations.AlterField(
            model_name='areaofresearch',
            name='user_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ccv.UserProfile'),
        ),
        migrations.AlterField(
            model_name='fieldofapplication',
            name='academic_work_experience',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ccv.AcademicWorkExperience'),
        ),
        migrations.AlterField(
            model_name='fieldofapplication',
            name='non_academic_work_experience',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ccv.NonAcademicWorkExperience'),
        ),
        migrations.AlterField(
            model_name='fieldofapplication',
            name='research_funding_assessment_activity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ccv.ResearchFundingApplicationAssessmentActivity'),
        ),
        migrations.AlterField(
            model_name='fieldofapplication',
            name='research_funding_history',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ccv.ResearchFundingHistory'),
        ),
        migrations.AlterField(
            model_name='fieldofapplication',
            name='user_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ccv.UserProfile'),
        ),
        migrations.AlterField(
            model_name='researchdiscipline',
            name='academic_work_experience',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ccv.AcademicWorkExperience'),
        ),
        migrations.AlterField(
            model_name='researchdiscipline',
            name='non_academic_work_experience',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ccv.NonAcademicWorkExperience'),
        ),
        migrations.AlterField(
            model_name='researchdiscipline',
            name='research_funding_assessment_activity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ccv.ResearchFundingApplicationAssessmentActivity'),
        ),
        migrations.AlterField(
            model_name='researchdiscipline',
            name='research_funding_history',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ccv.ResearchFundingHistory'),
        ),
        migrations.AlterField(
            model_name='researchdiscipline',
            name='user_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ccv.UserProfile'),
        ),
    ]