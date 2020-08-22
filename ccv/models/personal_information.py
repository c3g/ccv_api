from django.db import models
from .base import Base, CanadianCommonCv
from ..constants.db_constants import DEFAULT_COLUMN_LENGTH


class Identification(Base):
    """Information about the person that facilitates personal identification of person, including name,
    date of birth, and sex """

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
    family_name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, help_text="A person's surname")
    first_name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH)
    middle_name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    previous_family_name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    previous_first_name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    date_of_birth = models.CharField(max_length=5)
    sex = models.CharField(max_length=20, choices=SEX_CHOICES, null=True, blank=True)
    designated_group = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, choices=DESIGNATED_GROUP_CHOICES, null=True,
                                        blank=True, help_text="Group designated by the Employment Equity Act of Canada")
    correspondence_language = models.CharField(max_length=10, choices=CORRESPONDENCE_LANGUAGE_CHOICES)
    canadian_residency_status = models.CharField(max_length=DEFAULT_COLUMN_LENGTH,
                                                 choices=CANADIAN_RESIDENCY_STATUS_CHOICES, null=True, blank=True)
    permanent_residency = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, choices=PERMANENT_RESIDENCY_CHOICES,
                                           null=True, blank=True)
    permanent_residency_start_date = models.DateField(null=True, blank=True)

    ccv = models.OneToOneField(CanadianCommonCv, on_delete=models.CASCADE, related_name="identification")


class CountryOfCitizenship(Base):
    name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                            help_text="List all countries that the person is a citizen of")

    identification = models.ForeignKey(Identification, on_delete=models.CASCADE)


class LanguageSkill(Base):
    """List of languages in which the person has a level of competency along with an indication of competency level"""

    language = models.CharField(max_length=20, null=True, blank=True,
                                help_text="The language in which the person is indicating a competency.")
    can_read = models.BooleanField(default=False, null=True,
                                   help_text="The capacity of the person to comprehend the indicated language in "
                                             "written form.")
    can_write = models.BooleanField(default=False)
    can_speak = models.BooleanField(default=False)
    can_understand = models.BooleanField(default=False)
    peer_review = models.NullBooleanField(null=True, blank=True)

    personal_information = models.ForeignKey(Identification, on_delete=models.CASCADE)


class Address(Base):
    """Physical addresses with a known postal route location at which person can receive courier packages or mail."""

    ADDRESS_TYPE_CHOICES = (
        ('Courier', 'Courier'),
        ('Home', 'Home'),
        ('Mailing', 'Mailing'),
        ('Primary Affiliation', 'Primary Affiliation'),
        ('Temporary', 'Temporary')
    )

    type = models.CharField(max_length=20, choices=ADDRESS_TYPE_CHOICES, null=True, blank=True,
                            help_text="The nature and intended use of the given address")
    line_1 = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                              help_text="The exact location, number and street name for the given address")
    line_2 = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    line_3 = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    line_4 = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    line_5 = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    city = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                            help_text="The municipal component (city, town, etc.) of the given address")
    country = models.CharField(max_length=50, null=True, blank=True)
    subdivision = models.CharField(max_length=50, null=True, blank=True)
    postal = models.CharField(max_length=10, null=True, blank=True, help_text="The postal code of the given address")
    start_date = models.DateField(null=True, blank=True,
                                  help_text="If the given address is temporary, the date upon which it becomes active")
    end_date = models.DateField(null=True, blank=True,
                                help_text="If the given address is temporary, the date upon which it becomes inactive")

    personal_information = models.ForeignKey(Identification, on_delete=models.CASCADE)


class Telephone(Base):
    """Telephone and facsimile numbers at which the person can be contacted"""

    PHONE_TYPE_CHOICES = (
        ('Fax', 'Fax'),
        ('Home', 'Home'),
        ('Laboratory', 'Laboratory'),
        ('Mobile', 'Mobile'),
        ('Pager', 'Pager'),
        ('Temporary', 'Temporary'),
        ('Work', 'Work')
    )

    phone_type = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, choices=PHONE_TYPE_CHOICES, null=True, blank=True,
                                  help_text="The nature of the given phone number")
    country_code = models.CharField(max_length=5, null=True, blank=True,
                                    help_text="The country code with no space, bracket or dash, if located outside of "
                                              "North America e.g. 011")
    area_code = models.CharField(max_length=5, null=True, blank=True,
                                 help_text="The area code with no space, bracket or dash e.g. 613")
    number = models.CharField(max_length=12, null=True, blank=True,
                              help_text="The telephone number with no space, bracket or dash e.g. 1234567")
    extension = models.CharField(max_length=6, null=True, blank=True,
                                 help_text="The extension, if applicable, with no space, bracket or dash e.g. 5678")
    start_date = models.DateField(null=True, blank=True,
                                  help_text="If the given number is temporary, the date upon which it becomes active")
    end_date = models.DateField(null=True, blank=True,
                                help_text="If the given number is temporary, the date upon which it becomes inact")

    personal_information = models.ForeignKey(Identification, on_delete=models.CASCADE)


class Email(Base):
    """Electronic mail addresses at which the person can be contacted"""

    TYPE_CHOICES = (
        ('Personal', 'Personal'),
        ('Temporary', 'Temporary'),
        ('Work', 'Work'),
    )

    type = models.CharField(max_length=10, choices=TYPE_CHOICES, null=True, blank=True,
                            help_text="The nature of the given e-mail")
    address = models.CharField(max_length=100, null=True, blank=True, help_text="The person's e-mail address")
    start_date = models.DateField(null=True, blank=True,
                                  help_text="If the given e-mail is temporary, the date upon which it becomes active")
    end_date = models.DateField(null=True, blank=True,
                                help_text="If the given e-mail is temporary, the date upon which it becomes inactive")

    personal_information = models.ForeignKey(Identification, on_delete=models.CASCADE)


class Website(Base):
    """Web addresses at which the person maintains a presence in connection with research activities"""

    TYPE_CHOICES = (
        ('Blog', 'Blog'),
        ('Community', 'Community'),
        ('Corporate', 'Corporate'),
        ('Personal', 'Personal'),
        ('Social Media', 'Social Media')
    )

    type = models.CharField(max_length=20, choices=TYPE_CHOICES, null=True, blank=True,
                            help_text="The nature of the given web address")
    url = models.URLField(max_length=100, null=True, blank=True, help_text="The person's web address")

    personal_information = models.ForeignKey(Identification, on_delete=models.CASCADE)
