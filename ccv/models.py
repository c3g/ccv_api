# -*- coding: utf-8 -*-

from django.db import models
from .constants.db_constants import DEFAULT_COLUMN_LENGTH, NAME_LENGTH_MAX
from .utils import normalize_string
from django.contrib.postgres.fields import ArrayField
from djangoyearlessdate.models import YearlessDateField


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class PersonalInformation(Base):
    pass


class Identification(Base):
    TITLE_CHOICES = (
        ('Dr.', 'Dr.'),
        ('Mr.', 'Mr.'),
        ('Mrs.', 'Mrs.'),
        ('Ms.', 'Ms.'),
        ('Professor', 'Professor'),
        ('Reverend', 'Reverend')
    )
    SEX_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('No Response', 'No Response')
    )
    DESIGNATED_GROUP_CHOICES = (
        ('Aboriginal', 'Aboriginal'),
        ('Disabled', 'Disabled'),
        ('Visible Minority', 'Visible Minority')
    )
    CORRESPONDENCE_LANGUAGE_CHOICES = (
        ('English', 'English'),
        ('French', 'French')
    )
    CANADIAN_RESIDENCY_STATUS_CHOICES = (
        ('Canadian Citizen', 'Canadian Citizen'),
        ('Not Applicable', 'Not Applicable'),
        ('Permanent Resident', 'Permanent Resident'),
        ('Refugee', 'Refugee'),
        ('Student Work Permit', 'Student Work Permit'),
        ('Study Permit', 'Study Permit'),
        ('Visitor Visa', 'Visitor Visa'),
        ('Work Permit', 'Work Permit')
    )
    PERMANENT_RESIDENCY_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No')
    )

    title = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, choices=TITLE_CHOICES)
    family_name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH)
    first_name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH)
    middle_name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH)
    previous_family_name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True)
    previous_first_name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True)
    date_of_birth = YearlessDateField()
    sex = models.CharField(max_length=20, choices=SEX_CHOICES, null=True)
    designated_group = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, choices=DESIGNATED_GROUP_CHOICES)
    correspondence_language = models.CharField(max_length=10, choices=CORRESPONDENCE_LANGUAGE_CHOICES)
    canadian_residency_status = models.CharField(max_length=DEFAULT_COLUMN_LENGTH,
                                                 choices=CANADIAN_RESIDENCY_STATUS_CHOICES)
    permanent_residency = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, choices=PERMANENT_RESIDENCY_CHOICES)
    permanent_residency_start_date = models.DateField()


class LanguageSkill(Base):
    language = models.CharField(max_length=10)
    can_read = models.BooleanField()
    can_write = models.BooleanField()
    can_speak = models.BooleanField()
    can_understand = models.BooleanField()
    peer_review = models.BooleanField()

    personal_information = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)


class Address(Base):
    ADDRESS_TYPE_CHOICES = (
        ('Courier', 'Courier'),
        ('Home', 'Home'),
        ('Mailing', 'Mailing'),
        ('Primary Affiliation', 'Primary Affiliation'),
        ('Temporary', 'Temporary')
    )
    type = models.CharField(max_length=20, choices=ADDRESS_TYPE_CHOICES)
    line_1 = models.CharField(max_length=DEFAULT_COLUMN_LENGTH)
    line_2 = models.CharField(max_length=DEFAULT_COLUMN_LENGTH)
    line_3 = models.CharField(max_length=DEFAULT_COLUMN_LENGTH)
    line_4 = models.CharField(max_length=DEFAULT_COLUMN_LENGTH)
    line_5 = models.CharField(max_length=DEFAULT_COLUMN_LENGTH)
    city = models.CharField(max_length=DEFAULT_COLUMN_LENGTH)
    # location
    postal = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()

    personal_information = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)


class Telephone(Base):
    PHONE_TYPE_CHOICES = (
        ('Fax', 'Fax'),
        ('Home', 'Home'),
        ('Laboratory', 'Laboratory'),
        ('Mobile', 'Mobile'),
        ('Pager', 'Pager'),
        ('Temporary', 'Temporary'),
        ('Work', 'Work')
    )

    phone_type = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, choices=PHONE_TYPE_CHOICES)
    country_code = models.CharField(max_length=5, null=True)
    area_code = models.CharField(max_length=5, null=True)
    number = models.CharField(max_length=12, null=True)
    extension = models.CharField(max_length=6, null=True)
    start_date = models.DateField()  # only valid when phone type is temporary
    end_date = models.DateField()  # only valid when phone type is temporary
    personal_information = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)


class Email(Base):
    TYPE_CHOICES = (
        ('Personal', 'Personal'),
        ('Temporary', 'Temporary'),
        ('Work', 'Work'),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    address = models.CharField(max_length=100)
    start_date = models.DateField()  # only valid when email type is temporary
    end_date = models.DateField()  # only valid when email type is temporary

    personal_information = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)


class Website(Base):
    TYPE_CHOICES = (
        ('Blog', 'Blog'),
        ('Community', 'Community'),
        ('Corporate', 'Corporate'),
        ('Personal', 'Personal'),
        ('Social Media', 'Social Media')
    )

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    url = models.CharField(max_length=100, null=True)

    personal_information = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)


class Degree(Base):
    TYPE_CHOICES = (
        ('Bachelor\'s', 'Bachelor\'s'),
        ('Bachelor\'s Equivalent', 'Bachelor\'s Equivalent'),
        ('Bachelor\'s Honours', 'Bachelor\'s Honours'),
        ('Master\'s Equivalent', 'Master\'s Equivalent'),
        ('Master\'s non-Thesis', 'Master\'s non-Thesis'),
        ('Master\'s Thesis', 'Master\'s Thesis'),
        ('Doctorate', 'Doctorate'),
        ('Doctorate Equivalent', 'Doctorate Equivalent'),
        ('Post-doctorate', 'Post-doctorate'),
        ('Certificate', 'Certificate'),
        ('Diploma', 'Diploma'),
        ('Habilitation', 'Habilitation'),
        ('Research Associate', 'Research Associate')
    )
    STATUS_CHOICES = (
        ('All But Degree', 'All But Degree'),
        ('Completed', 'Completed'),
        ('In Progress', 'In Progress'),
        ('Withdrawn', 'Withdrawn')
    )

    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    name = models.CharField(max_length=NAME_LENGTH_MAX, null=True)
    specialization = models.CharField(max_length=100, null=True)
    thesis_title = models.TextField(max_length=500, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    expected_date = models.DateField()
    phd_without_masters = models.BooleanField(default=False)


class Supervisor(Base):
    name = models.CharField(max_length=NAME_LENGTH_MAX, null=True)
    start_date = models.DateField()
    end_date = models.DateField()


class UserProfile(Base):
    RESEARCHER_STATUS_CHOICES = (
        ('Doctoral Student', 'Doctoral Student'),
        ('Master\'s Student', 'Master\'s Student'),
        ('Post-doctoral Student', 'Post-doctoral Student'),
        ('Researcher', 'Researcher')
    )
    researcher_status = models.CharField(max_length=30, choices=RESEARCHER_STATUS_CHOICES)
    career_start_date = models.DateField()
    engaged_in_clinical_research = models.BooleanField(default=False)
    key_theory = models.TextField(max_length=500)
    research_interest = models.TextField(max_length=1000)
    experience_summary = models.TextField(max_length=1000)
    country = ArrayField(models.CharField(max_length=DEFAULT_COLUMN_LENGTH), null=True, blank=True, default=list)


class ResearchCentre(Base):
    name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    country = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    subdivision = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class TechnologicalApplication(Base):
    CATEGORY_CHOICES = (
        ('Agro-alimentary', 'Agro-alimentary'),
        ('Chemistry / Biochemistry', 'Chemistry / Biochemistry'),
        ('Medical materials and instrumentation', 'Medical materials and instrumentation'),
        ('Orthopaedic devices', 'Orthopaedic devices'),
        ('Pharmacy', 'Pharmacy')
    )

    subfield = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    category = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, choices=CATEGORY_CHOICES, null=True, blank=True)

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


