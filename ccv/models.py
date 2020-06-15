# -*- coding: utf-8 -*-

import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from djangoyearlessdate.models import YearlessDateField

from .constants.db_constants import DEFAULT_COLUMN_LENGTH, NAME_LENGTH_MAX
from .utils import parse_integer

# TODO: Indexing the fields which will be used as filters in searching the CCVs


class Base(models.Model):
    """Abstract class """
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Organization(Base):
    name = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    subdivision = models.CharField(max_length=50, null=True, blank=True)


class OtherOrganization(Base):
    type = models.CharField(max_length=20, null=True, blank=True,
                            help_text="The type of organization, only if Other Organization is entered")
    name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                            help_text="The organization's name, only if not in Organization list")


class CanadianCommonCv(Base):
    """Master table which links all entities like Identification, Education, Employment, Contribution, etc."""

    _id = models.UUIDField(max_length=40, db_index=True, editable=False, default=uuid.uuid4)
    slug = models.SlugField(help_text="Short label to be used in URL")


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

    ccv = models.OneToOneField(CanadianCommonCv, on_delete=models.CASCADE)


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
    peer_review = models.BooleanField(null=True, blank=True)

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


class Education(Base):
    """Collection of information records that, in combination, represent the full and up-to-date history of the
    person's education """

    ccv = models.OneToOneField(CanadianCommonCv, on_delete=models.CASCADE)


class Degree(Base):
    """Academic title conferred by universities and colleges as an indication of the completion of a course of study"""

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

    type = models.CharField(max_length=30, choices=TYPE_CHOICES, null=True, blank=True,
                            help_text="The designation of the person's degree")
    name = models.CharField(max_length=NAME_LENGTH_MAX, null=True, blank=True,
                            help_text="The name of the person's degree program")
    specialization = models.CharField(max_length=100, null=True, blank=True, help_text="person's major course of study")
    thesis_title = models.CharField(max_length=500, null=True, blank=True,
                                    help_text="title of the person’s thesis project")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=True,
                              help_text="Indicates whether or not the person's degree is completed")
    start_date = models.DateField(null=True, blank=True, help_text="The date the person's study began")
    end_date = models.DateField(null=True, blank=True, help_text="The date the person's study was completed")
    expected_date = models.DateField(null=True, blank=True,
                                     help_text="If the person's study is not complete, the date completion is expected")
    phd_without_masters = models.BooleanField(default=False, null=True, blank=True,
                                              help_text="If doctorate degree, did the person transfer "
                                                        "directly to this degree without completing a Masters?")

    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, null=True, blank=True,
                                        help_text="The institution that conferred the degree.")
    other_organization = models.OneToOneField(OtherOrganization, on_delete=models.CASCADE, null=True, blank=True, )

    education = models.ForeignKey(Education, on_delete=models.CASCADE)


class Supervisor(Base):
    """The persons responsible for mentoring, advising and guiding the student academically throughout this degree
    program """

    name = models.CharField(max_length=NAME_LENGTH_MAX, null=True)
    start_date = models.DateField(null=True, blank=True, help_text="The date when the supervision started")
    end_date = models.DateField(null=True, blank=True, help_text="The date when the supervision ended")

    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)


class Credential(Base):
    """A designation earned to assure qualification to perform a job or task such as a certification,
    an accreditation, a designation, etc. """

    title = models.CharField(max_length=250, null=True, blank=True,
                             help_text="The name or title of the designation earned")
    effective_date = models.DateField(null=True, blank=True, help_text="The date the designation was received")
    end_date = models.DateField(null=True, blank=True, help_text="The date the designation expires, if applicable")
    description = models.CharField(max_length=1000, null=True, blank=True,
                                   help_text="A description of the person's designation")

    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, null=True, blank=True,
                                        help_text="The organization that conferred this credential")
    other_organization = models.OneToOneField(OtherOrganization, on_delete=models.CASCADE, null=True, blank=True)

    education = models.ForeignKey(Education, on_delete=models.CASCADE)


class Recognition(Base):
    """Recognitions are any acknowledgments, appreciations and monetary rewards that were obtained and which were not"""
    TYPE_CHOICES = (
        ('Citation', 'Citation'),
        ('Distinction', 'Distinction'),
        ('Honor', 'Honor'),
        ('Prize / Award', 'Prize / Award')
    )

    type = models.CharField(max_length=20, choices=TYPE_CHOICES, null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True, help_text="The name or title of the recognition")
    effective_date = models.DateField(null=True, blank=True, help_text="The date when the recognition was awarded")
    end_date = models.DateField(null=True, blank=True, help_text="The date when this recognition expires")
    amount = models.IntegerField(null=True, blank=True, help_text="The amount that was awarded for this recognition")
    amount_in_canadian_dollar = models.IntegerField(null=True, blank=True, help_text="Amount in CAN $")
    description = models.CharField(max_length=1000, null=True, blank=True,
                                   help_text="A description of the recognition obtained")
    currency = models.CharField(max_length=50, null=True, blank=True,
                                help_text="The currency in which the money was awarded")

    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, null=True, blank=True,
                                        help_text="The organization that gave the recognition")
    other_organization = models.OneToOneField(OtherOrganization, on_delete=models.CASCADE, null=True, blank=True)

    ccv = models.ForeignKey(CanadianCommonCv, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.amount = parse_integer(self.amount)
        # TODO: Add amount conversion logic in CAN $
        super().save(*args, **kwargs)


class UserProfile(Base):
    """A summary of the person's research career, interests, experience and specialization"""
    RESEARCHER_STATUS_CHOICES = (
        ('Doctoral Student', 'Doctoral Student'),
        ('Master\'s Student', 'Master\'s Student'),
        ('Post-doctoral Student', 'Post-doctoral Student'),
        ('Researcher', 'Researcher')
    )
    researcher_status = models.CharField(max_length=30, choices=RESEARCHER_STATUS_CHOICES, null=True, blank=True,
                                         help_text="research status")
    career_start_date = models.DateField(null=True, blank=True, help_text="When did you start your research career")
    engaged_in_clinical_research = models.BooleanField(default=False, help_text="if you are involved in clinical "
                                                                                "research activities (with drugs)")
    key_theory = models.CharField(max_length=500, null=True, blank=True, help_text="The key theories and "
                                                                                   "methodologies used in research")
    research_interest = models.CharField(max_length=1000, null=True, blank=True)
    experience_summary = models.CharField(max_length=1000, null=True, blank=True,
                                          help_text="summary of research experience")
    # country = ArrayField(models.CharField(max_length=DEFAULT_COLUMN_LENGTH), null=True, blank=True, default=list)

    ccv = models.OneToOneField(CanadianCommonCv, on_delete=models.CASCADE)


class ResearchSpecializationKeyword(Base):
    """Keywords that best correspond to the person's expertise in research, creation, instrumentation and techniques"""

    order = models.IntegerField(null=True, blank=True,
                                help_text="This field is used to order the entries. A value of 1 will show up at top.")
    keyword = models.CharField(max_length=50, null=True, blank=True)

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.order = parse_integer(self.order)
        super().save(*args, **kwargs)


class ResearchCentre(Base):
    """The research centres where most of the person's research is done."""

    name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    country = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    subdivision = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class TechnologicalApplication(Base):
    """The anticipated technological, industrial, social, cultural, organizational, educational, artistic and other
    applications of the person's research work """

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


class DisciplineTrainedIn(Base):
    """The discipline is a field of knowledge which is taught at the university level and where it is
    institutionalized as a unit, like a department or a faculty. In this section select values that describe your
    expertise and experience related to your disciplinary training """

    FIELDS_CHOICES = (
        ('Applied Sciences', 'Applied Sciences'),
        ('Arts and Literature Studies', 'Arts and Literature Studies'),
        ('Education', 'Education'), ('Engineering', 'Engineering'),
        ('Humanities', 'Humanities'), ('Management', 'Management'),
        ('Mathematical Sciences', 'Mathematical Sciences'),
        ('Medical Sciences', 'Medical Sciences'),
        ('Natural Sciences', 'Natural Sciences'),
        ('Nursing', 'Nursing'),
        ('Physical Education and Rehabilitation', 'Physical Education and Rehabilitation'),
        ('Social Sciences', 'Social Sciences'),
        ('Writing and Fine Arts', 'Writing and Fine Arts')
    )
    SECTOR_CHOICES = (
        ('Arts and literature', 'Arts and literature'),
        ('Health Sciences', 'Health Sciences'),
        ('Human and social sciences', 'Human and social sciences'),
        ('Natural Sciences and Engineering', 'Natural Sciences and Engineering')
    )

    discipline = models.CharField(max_length=50, null=True, blank=True)
    sector = models.CharField(max_length=50, null=True, blank=True, choices=SECTOR_CHOICES)
    fields = models.CharField(max_length=50, null=True, blank=True, choices=FIELDS_CHOICES)

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class TemporalPeriod(Base):
    """Indicate and rank the historical periods covered by your research interests, with #1 the most relevant."""

    YEAR_PERIOD_CHOICES = (
        ('AD', 'AD'),
        ('BC', 'BC')
    )

    from_year = models.IntegerField(null=True, blank=True,
                                    help_text="The starting year of the temporal period")
    from_year_period = models.CharField(max_length=2, null=True, blank=True, choices=YEAR_PERIOD_CHOICES,
                                        help_text="The period of the starting year")
    to_year = models.IntegerField(null=True, blank=True,
                                  help_text="The end year of the temporal period")
    to_year_period = models.CharField(max_length=2, null=True, blank=True, choices=YEAR_PERIOD_CHOICES,
                                      help_text="The period of the ending year")

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class GeographicalRegion(Base):
    """Indicate and rank the geographical regions covered by your research interests, with #1 the most relevant."""
    REGION_CHOICES = (
        ('Africa', 'Africa'),
        ('Antarctic and Arctic', 'Antarctic and Arctic'),
        ('Asia', 'Asia'),
        ('Atlantic Provinces', 'Atlantic Provinces'),
        ('Caribbean', 'Caribbean'),
        ('Central Africa', 'Central Africa'),
        ('Central America', 'Central America'),
        ('Central Asia', 'Central Asia'),
        ('Central Canada', 'Central Canada'),
        ('East Asia', 'East Asia'),
        ('Eastern Africa', 'Eastern Africa'),
        ('Eastern Europe', 'Eastern Europe'),
        ('Europe', 'Europe'),
        ('Former Soviet Union', 'Former Soviet Union'),
        ('International', 'International'),
        ('Melanesia', 'Melanesia'),
        ('Micronesia', 'Micronesia'),
        ('Near and Middle East', 'Near and Middle East'),
        ('North America', 'North America'),
        ('Northern Africa', 'Northern Africa'),
        ('Northern Canada', 'Northern Canada'),
        ('Not subject to geographical classification', 'Not subject to geographical classification'),
        ('Oceania', 'Oceania'),
        ('Polynesia', 'Polynesia'),
        ('Scandinavia', 'Scandinavia'),
        ('South America', 'South America'),
        ('South Asia', 'South Asia'),
        ('Southeast Asia', 'Southeast Asia'),
        ('Southern Africa', 'Southern Africa'),
        ('Southwest Asia', 'Southwest Asia'),
        ('Western Africa', 'Western Africa'),
        ('Western Canada', 'Western Canada'),
        ('Western Europe', 'Western Europe')
    )

    region = models.CharField(max_length=50, null=True, blank=True, choices=REGION_CHOICES)

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class Employment(Base):
    """Collection of information records that, in combination, represent the full and up-to-date history of the
    person's employment """

    ccv = models.OneToOneField(CanadianCommonCv, on_delete=models.CASCADE)


class AcademicWorkExperience(Base):
    """Employment in an academic environment"""

    POSITION_TYPE_CHOICES = (
        ('Adjunct', 'Adjunct'),
        ('Consultation', 'Consultation'),
        ('Sessional', 'Sessional'),
        ('Term', 'Term'),
        ('Visiting Professorship', 'Visiting Professorship')
    )
    POSITION_STATUS_CHOICES = (
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time')
    )
    ACADEMIC_RANK_CHOICES = (
        ('Assistant Professor', 'Assistant Professor'),
        ('Associate Professor', 'Associate Professor'),
        ('Emeritus', 'Emeritus'),
        ('Lecturer', 'Lecturer'),
        ('Professor', 'Professor')
    )
    TENURE_STATUS_CHOICES = (
        ('Non Tenure Track', 'Non Tenure Track'),
        ('Tenure', 'Tenure'),
        ('Tenure Track', 'Tenure Track')
    )

    position_type = models.CharField(max_length=30, null=True, blank=True, choices=POSITION_TYPE_CHOICES,
                                     help_text="The nature of the person's position")
    position_title = models.CharField(max_length=250, null=True, blank=True,
                                      help_text="The person's position at the institution")
    position_status = models.CharField(max_length=20, null=True, blank=True, choices=POSITION_STATUS_CHOICES,
                                       help_text="The status of the position with regard to tenure")
    academic_rank = models.CharField(max_length=20, null=True, blank=True, choices=ACADEMIC_RANK_CHOICES,
                                     help_text="The rank of the faculty member in the academic institution")
    start_date = models.DateField(null=True, blank=True, help_text="The date the person started this position")
    end_date = models.DateField(null=True, blank=True, help_text="Date the person did not occupy this position anymore")
    work_description = models.CharField(max_length=1000, null=True, blank=True,
                                        help_text="Description of the duties for this position")
    department = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                  help_text="The department within the given institution")
    campus = models.CharField(max_length=100, null=True, blank=True,
                              help_text="The location of the relevant campus of the institution")
    tenure_status = models.CharField(max_length=20, null=True, blank=True, choices=TENURE_STATUS_CHOICES,
                                     help_text="The status of the position with regard to tenure")
    tenure_start_date = models.DateField(null=True, blank=True,
                                         help_text="The date that the person achieved tenure within the named position")
    tenure_end_date = models.DateField(null=True, blank=True, help_text="The date when the tenure stopped, "
                                                                        "if applicable")

    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, null=True, blank=True)
    other_organization = models.OneToOneField(OtherOrganization, on_delete=models.CASCADE, null=True, blank=True, )

    employment = models.ForeignKey(Employment, on_delete=models.CASCADE)


class NonAcademicWorkExperience(Base):
    """Employment in a non-academic environment"""

    POSITION_STATUS_CHOICES = (
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time')
    )

    position_title = models.CharField(max_length=250, null=True, blank=True,
                                      help_text="The position of the person with the employer")
    position_status = models.CharField(max_length=10, null=True, blank=True, choices=POSITION_STATUS_CHOICES,
                                       help_text="The nature of the person's position")
    start_date = models.DateField(null=True, blank=True, help_text="The date the position started")
    end_date = models.DateField(null=True, blank=True, help_text="The date the position ended")
    work_description = models.CharField(max_length=1000, null=True, blank=True,
                                        help_text="The responsibilities and duties associated with this position")
    unit_division = models.CharField(max_length=100, null=True, blank=True,
                                     help_text="The department within the given company or organization")

    organization = models.OneToOneField(Organization, null=True, blank=True, on_delete=models.CASCADE,
                                        help_text="The name of the organization where the person worked")
    other_organization = models.OneToOneField(OtherOrganization, on_delete=models.CASCADE)
    employment = models.ForeignKey(Employment, on_delete=models.CASCADE)


class Affiliation(Base):
    """Organizations with which the person is affiliated. These can be work or non-work related."""

    position_title = models.CharField(max_length=250, null=True, blank=True,
                                      help_text="The name or title of the position")
    department = models.CharField(max_length=100, null=True, blank=True,
                                  help_text="The department within the given organization")
    activity_description = models.CharField(max_length=1000, null=True, blank=True,
                                            help_text="A description of the person's activities with this organization")
    start_date = models.DateField(null=True, blank=True,
                                  help_text="The date when the persone became affiliated with this organization")
    end_date = models.DateField(null=True, blank=True,
                                help_text="The date when the person's affiliation with this organization ended")

    organization = models.OneToOneField(Organization, null=True, blank=True, on_delete=models.CASCADE,
                                        help_text="The organization with which the person is affiliated.")
    other_organization = models.OneToOneField(OtherOrganization, null=True, blank=True, on_delete=models.CASCADE)

    employment = models.ForeignKey(Employment, on_delete=models.CASCADE)


class LeavesOfAbsence(Base):
    """Gaps in the employment history"""

    LEAVE_TYPE_CHOICES = (
        ('Administrative', 'Administrative'),
        ('Bereavement', 'Bereavement'),
        ('Medical', 'Medical'),
        ('Other Circumstances', 'Other Circumstances'),
        ('Parental', 'Parental'),
        ('Sabbatical', 'Sabbatical'),
        ('Special', 'Special'),
        ('Study', 'Study'),
        ('Unpaid', 'Unpaid')
    )

    leave_type = models.CharField(max_length=50, choices=LEAVE_TYPE_CHOICES, null=True, blank=True,
                                  help_text="The nature of the leave of absence")
    start_date = models.DateField(null=True, blank=True, help_text="The date the leave started")
    end_date = models.DateField(null=True, blank=True, help_text="The date the leave ended, if applicable")

    absence_description = models.CharField(max_length=1000, null=True, blank=True,
                                           help_text="description of the leave of absence")

    organization = models.OneToOneField(Organization, null=True, blank=True, on_delete=models.CASCADE)
    other_organization = models.OneToOneField(OtherOrganization, null=True, blank=True, on_delete=models.CASCADE)
    employment = models.ForeignKey(Employment, on_delete=models.CASCADE)


class ResearchFundingHistory(Base):
    """Collection of information records that, in combination, represent the full and up-to-date history of research
    funding received and/or applied to by the person from any source. """

    FUNDING_TYPE_CHOICES = (
        ('Contract', 'Contract'),
        ('Fellowship', 'Fellowship'),
        ('Grant', 'Grant'),
        ('Research Chair', 'Research Chair'),
        ('Scholarship', 'Scholarship')
    )
    GRANT_TYPE_CHOICES = (
        ('Equipment', 'Equipment'),
        ('Establishment', 'Establishment'),
        ('Infrastructure', 'Infrastructure'),
        ('Operating', 'Operating'), ('Workshop', 'Workshop')
    )

    PROJECT_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No')
    )

    FUNDING_STATUS_CHOICES = (
        ('Awarded', 'Awarded'),
        ('Completed', 'Completed'),
        ('Declined', 'Declined'),
        ('Under Review', 'Under Review')
    )

    FUNDING_ROLE_CHOICES = (
        ('Co-applicant', 'Co-applicant'),
        ('Co-investigator', 'Co-investigator'),
        ('Co-knowledge User', 'Co-knowledge User'),
        ('Collaborator', 'Collaborator'),
        ('Decision Maker', 'Decision Maker'),
        ('Policy Maker', 'Policy Maker'),
        ('Principal Applicant', 'Principal Applicant'),
        ('Principal Investigator', 'Principal Investigator'),
        ('Principal Knowledge User', 'Principal Knowledge User')
    )

    funding_type = models.CharField(max_length=20, null=True, blank=True, choices=FUNDING_TYPE_CHOICES,
                                    help_text="The nature of the funding received")
    start_date = models.DateField(null=True, blank=True,
                                  help_text="The date when the funding for this project started.")
    end_date = models.DateField(null=True, blank=True, help_text="The date when the funding for this project ended.")

    funding_title = models.CharField(max_length=250, null=True, blank=True,
                                     help_text="The nature of the grant received")
    grant_type = models.CharField(max_length=20, choices=GRANT_TYPE_CHOICES, null=True, blank=True)
    project_description = models.CharField(
        max_length=1000, null=True, blank=True, help_text="description of project for which funding was received")
    clinical_research_project = models.CharField(max_length=5, null=True, blank=True, choices=PROJECT_CHOICES)

    funding_status = models.CharField(
        max_length=30, choices=FUNDING_STATUS_CHOICES, null=True,
        blank=True, help_text="current status of the funding of the overall project.")

    funding_role = models.CharField(max_length=30, choices=FUNDING_ROLE_CHOICES, blank=True, null=True,
                                    help_text="Person's role in this research, as defined by the funding organization")
    research_uptake = models.CharField(max_length=1000, null=True, blank=True,
                                       help_text="strategies used to promote the uptake of your research findings.")

    ccv = models.OneToOneField(CanadianCommonCv, on_delete=models.CASCADE)


class ResearchUptakeHolder(Base):
    """The groups or individuals which uptake your research findings"""

    STAKEHOLDER_CHOICES = (
        ('Academic Personnel', 'Academic Personnel'),
        ('Charity Organizations', 'Charity Organizations'),
        ('Elders', 'Elders'),
        ('General Public', 'General Public'),
        ('Government Personnel', 'Government Personnel'),
        ('Healthcare Personnel', 'Healthcare Personnel'),
        ('Industrial Association/Producer Group', 'Industrial Association/Producer Group'),
        ('Industrial Consortium', 'Industrial Consortium'),
        ('Industry/Business (>500 employees)', 'Industry/Business (>500 employees)'),
        ('Industry/Business-Medium (100 to 500 employees)', 'Industry/Business-Medium (100 to 500 employees)'),
        ('Industry/Business-Small (<100 employees)', 'Industry/Business-Small (<100 employees)'),
        ('Patients', 'Patients'), ('Policy Maker/Regulator', 'Policy Maker/Regulator'),
        ('Private Not-for-Profit Organization', 'Private Not-for-Profit Organization'),
        ('The Media', 'The Media'),
        ('Utility', 'Utility')
    )

    stakeholder = models.CharField(max_length=50, choices=STAKEHOLDER_CHOICES, blank=True, null=True,
                                   help_text="The group or individual which uptake research findings")

    research_funding_history = models.ForeignKey(ResearchFundingHistory, on_delete=models.CASCADE)


class ResearchSetting(Base):
    """The locations where the research was done. For example a canadian funded project might be composed of several
    teams working in different countries. """

    SETTING_TYPE_CHOICES = (
        ('Both', 'Both'),
        ('Rural', 'Rural'),
        ('Urban', 'Urban'),

    )
    country = models.CharField(max_length=50, null=True, blank=True, help_text="The place where the research was done")
    subdivision = models.CharField(max_length=50, null=True, blank=True, help_text="Division where research was done")
    setting_type = models.CharField(max_length=10, null=True, blank=True,
                                    help_text="The type of environment where the research was conducted")
    research_funding_history = models.ForeignKey(ResearchFundingHistory, on_delete=models.CASCADE)


class FundingSource(Base):
    """A research project may receive funding from one or more organizations. List all of them here."""

    BOOLEAN_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No')
    )

    organization = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                    help_text="Organization that provided funding for this project")
    other_organization = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                          help_text="The funding organization's name, only if not in the above column")
    program_name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                    help_text="The funding organization's name, only if not in the above list")
    reference_no = models.CharField(max_length=20, null=True, blank=True,
                                    help_text="organization's funding reference number, if applicable")
    total_funding_in_canadian_dollar = models.IntegerField(null=True, blank=True,
                                                           help_text="total amount applied for or received from this "
                                                                     "organization in CAN $")
    total_funding = models.IntegerField(null=True, blank=True,
                                        help_text="total amount applied for or received from this organization")
    total_funding_currency = models.CharField(max_length=20, blank=True, null=True,
                                              help_text="The currency in which the money was awarded")
    funding_received = models.IntegerField(null=True, blank=True,
                                           help_text="From the total funding received from this organization for this "
                                                     "project")
    funding_received_in_canadian_dollar = models.IntegerField(null=True, blank=True,
                                                              help_text="total amount applied for or received from this"
                                                                        " organization in CAN $")
    funding_received_currency = models.CharField(max_length=20, blank=True, null=True,
                                                 help_text="The currency in which the money was awarded")
    start_date = models.DateField(null=True, blank=True,
                                  help_text="date when the funding from this organization, for this project, started")
    end_date = models.DateField(null=True, blank=True,
                                help_text="date when the funding from this organization, for this project, ended")
    renewable = models.CharField(max_length=5, null=True, blank=True, choices=BOOLEAN_CHOICES,
                                 help_text="Indicate if the funding received from this organization is renewable")
    competitive = models.CharField(max_length=5, null=True, blank=True, choices=BOOLEAN_CHOICES,
                                   help_text="Indicate if the funding received from this organization is renewable")

    research_funding_history = models.ForeignKey(ResearchFundingHistory, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # TODO: Add amount conversion logic in CAN $
        super().save(*args, **kwargs)


class FundingByYear(Base):
    """Breakdown of the total funding received from one or more organizations for this project, by year."""
    start_date = models.DateField(null=True, blank=True,
                                  help_text="Breakdown of the total funding received from one or more organizations "
                                            "for this project, by year.")
    end_date = models.DateField(null=True, blank=True,
                                help_text="Breakdown of the total funding received from one or more organizations for "
                                          "this project, by year.")
    total_funding_in_canadian_dollar = models.IntegerField(null=True, blank=True,
                                                           help_text="The total amount that was received for this "
                                                                     "period for this project in CAN $")
    total_funding = models.IntegerField(null=True, blank=True,
                                        help_text="The total amount that was received for this period for this project")
    total_funding_currency = models.CharField(max_length=20, blank=True, null=True,
                                              help_text="The currency in which the money was awarded")
    funding_received = models.IntegerField(null=True, blank=True,
                                           help_text="The amount that you received for this period for this project")
    funding_received_in_canadian_dollar = models.IntegerField(null=True, blank=True,
                                                              help_text="The amount that you received for this period "
                                                                        "for this project CAN $")
    funding_received_currency = models.CharField(max_length=20, blank=True, null=True,
                                                 help_text="The currency in which the money was awarded")

    time_commitment = models.IntegerField(null=True, blank=True, help_text="approximate percentage of regular working "
                                                                           "hours over this time period that were spent"
                                                                           " on this project")
    research_funding_history = models.ForeignKey(ResearchFundingHistory, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # TODO: Add amount conversion logic in CAN $
        super().save(*args, **kwargs)


class OtherInvestigator(Base):
    """The names and roles of other investigators who have participated in this research project"""
    ROLE_CHOICES = (
        ('Co-applicant', 'Co-applicant'),
        ('Co-investigator', 'Co-investigator'),
        ('Co-knowledge User', 'Co-knowledge User'),
        ('Collaborator', 'Collaborator'),
        ('Decision Maker', 'Decision Maker'),
        ('Policy Maker', 'Policy Maker'),
        ('Principal Applicant', 'Principal Applicant'),
        ('Principal Investigator', 'Principal Investigator'),
        ('Principal Knowledge User', 'Principal Knowledge User')
    )

    name = models.CharField(max_length=NAME_LENGTH_MAX, null=True, blank=True,
                            help_text="Name of the investigator who has participated in this research project. Family "
                                      "name followed by a comma and by the the first name, without any punctuation")
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, null=True, blank=True,
                            help_text="The role of this investigator")

    research_funding_history = models.ForeignKey(ResearchFundingHistory, on_delete=models.CASCADE)


class Membership(Base):
    """Services contributed as part of a group elected or appointed to perform such services but not directly related
    to the person's research activities. """

    ccv = models.OneToOneField(CanadianCommonCv, on_delete=models.CASCADE)


class CommitteeMembership(Base):
    ROLE_CHOICES = (
        ('Chair', 'Chair'),
        ('Co-chair', 'Co-chair'),
        ('Committee Member', 'Committee Member'),
        ('Ex-Officio', 'Ex-Officio'),
        ('Group Chair', 'Group Chair')
    )

    role = models.CharField(max_length=20, null=True, blank=True, choices=ROLE_CHOICES,
                            help_text="The person's role in this activity")
    name = models.CharField(max_length=250, null=True, blank=True, help_text="The name of the committee")
    start_date = models.DateField(null=True, blank=True, help_text="The date on which membership began")
    description = models.CharField(max_length=1000, null=True, blank=True,
                                   help_text="Description of services contributed by the person as part of a committee")
    end_date = models.DateField(null=True, blank=True, help_text="The date on which membership ended, if applicable")

    organization = models.OneToOneField(Organization, null=True, blank=True, on_delete=models.CASCADE,
                                        help_text="The name of the organisation of which the person is a member")
    other_organization = models.OneToOneField(OtherOrganization, null=True, blank=True, on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)


class OtherMembership(Base):
    """Services contributed as part of a scholarly society or other organization to perform services not directly
    related to the person's research activities """

    role = models.CharField(max_length=20, null=True, blank=True, help_text="The person's role in this activity")
    name = models.CharField(max_length=250, null=True, blank=True, help_text="The name of the committee")
    start_date = models.DateField(null=True, blank=True, help_text="The date on which membership began")
    description = models.CharField(max_length=1000, null=True, blank=True,
                                   help_text="Description of services contributed by the person as part of a committee")
    end_date = models.DateField(null=True, blank=True, help_text="The date on which membership ended, if applicable")

    organization = models.OneToOneField(Organization, null=True, blank=True, on_delete=models.CASCADE,
                                        help_text="The name of the organisation of which the person is a member")
    other_organization = models.OneToOneField(OtherOrganization, null=True, blank=True, on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)

########################################################################################################################


class Activity(Base):
    """Services that the person contributed to"""

    ccv = models.OneToOneField(CanadianCommonCv, on_delete=models.CASCADE)


class ActivityAbstract(Base):
    """Contains the common fields to be inherited in the respective table"""

    ACTIVITY_TYPE_CHOICES = (
        ('Teaching Activity', 'Teaching Activity'),
        ('Supervisory Activity', 'Supervisory Activity'),
        ('Administrative Activity', 'Administrative Activity'),
        ('Advisory Activity', 'Advisory Activity'),
        ('Assessment And Review Activity', 'Assessment And Review Activity'),
        ('Participation Activity', 'Participation Activity'),
        ('Other Activity', 'Other Activity'),
    )

    start_date = models.DateField(null=True, blank=True, help_text="The date the person began this activity.")
    end_date = models.DateField(null=True, blank=True, help_text="The date the person finished this activity.")

    class Meta:
        abstract = True


class TeachingActivity(Base):
    """Services contributed in the form of teaching activities at academic institutions with which the person is
    currently, or has in the past been, affiliated. """

    activity = models.OneToOneField(Activity, on_delete=models.CASCADE)


class CourseTaught(ActivityAbstract):
    """Services contributed in the form of courses taught at academic institutions with which the person is
    currently, or has in the past been, affiliated. """

    ACADEMIC_SESSION_CHOICES = (
        ('Fall', 'Fall'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Winter', 'Winter')
    )
    LEVEL_CHOICES = (
        ('College', 'College'),
        ('Graduate', 'Graduate'),
        ('Post Graduate', 'Post Graduate'),
        ('Undergraduate', 'Undergraduate')
    )
    BOOLEAN_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No')
    )

    role = models.CharField(max_length=100, null=True, blank=True,
                            help_text="The role of the person in this activity")
    department = models.CharField(max_length=100, null=True, blank=True,
                                  help_text="The department within the given institution")
    academic_session = models.CharField(max_length=20, null=True, blank=True, choices=ACADEMIC_SESSION_CHOICES,
                                        help_text="The academic session in which this course was taught")
    code = models.CharField(max_length=25, null=True, blank=True, help_text="The institution's course code")
    title = models.TextField(max_length=250, null=True, blank=True, help_text="The course title")
    topic = models.CharField(max_length=100, null=True, blank=True, help_text="The topic of the course")
    level = models.CharField(max_length=20, null=True, blank=True, choices=LEVEL_CHOICES)
    section = models.TextField(max_length=250, null=True, blank=True,
                               help_text="The area of study in which the course falls.")
    students_count = models.IntegerField(null=True, blank=True,
                                         help_text="The number of students who attend this course during a session")
    credits_count = models.IntegerField(null=True, blank=True, help_text="Institution’s credit value for the course")
    lecture_hours_per_week = models.IntegerField(null=True, blank=True, help_text="The number of hours of lecture the "
                                                                                  "person contributed per week")
    tutorial_hours_per_week = models.IntegerField(null=True, blank=True, help_text="The number of hours of tutorial "
                                                                                   "the person contributed per week.")
    lab_hours_per_week = models.IntegerField(null=True, blank=True,
                                             help_text="The number of hours of laboratory instruction the person "
                                                       "contributed per week.")
    guest_lecture = models.CharField(max_length=5, null=True, blank=True, choices=BOOLEAN_CHOICES,
                                     help_text="Indicate whether you were a guest lecturer for this course")

    organization = models.OneToOneField(Organization, null=True, blank=True, on_delete=models.CASCADE,
                                        help_text="The organization where the course was taught ")
    other_organization = models.OneToOneField(OtherOrganization, null=True, blank=True, on_delete=models.CASCADE)
    teaching_activity = models.ForeignKey(TeachingActivity, on_delete=models.CASCADE)


class CoInstructor(Base):
    """The names of the instructors who assisted in teaching the course"""

    family_name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                   help_text="The family name of the instructor")
    first_name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                  help_text="The first name of the instructor")

    course_taught = models.ForeignKey(CourseTaught, on_delete=models.CASCADE)


class CourseDevelopment(Base):
    """Contributions in the development of courses/modules for training or teaching purposes."""

    teaching_activity = models.ForeignKey(TeachingActivity, on_delete=models.CASCADE)


class ProgramDevelopment(Base):
    """"""


class CoDeveloper(Base):
    """The names of persons who participated in the development of the course"""

    family_name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                   help_text="Family name of person who participated in the development of the course")
    first_name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                  help_text="First name of person who participated in the development of the course")

    course_development = models.ForeignKey(CourseDevelopment, on_delete=models.CASCADE, null=True, blank=True)

    # program_development = models.ForeignKey(CourseDevelopment, on_delete=models.CASCADE, null=True, blank=True)


class SupervisoryActivity(Base):
    """Services contributed in instances of overseeing the productivity and progress of students and employees"""

    activity = models.OneToOneField(Activity, on_delete=models.CASCADE)


class StudentSupervision(Base):
    """Contribution to the productivity and progress, usually for academic credit, of directly supervised students,
    postdocs or research associates. """

    ROLE_CHOICES = (
        ('Academic Advisor', 'Academic Advisor'),
        ('Co-Supervisor', 'Co-Supervisor'),
        ('Principal Supervisor', 'Principal Supervisor')
    )
    RESIDENCY_STATUS_CHOICES = (
        ('Canadian Citizen', 'Canadian Citizen'),
        ('Not Applicable', 'Not Applicable'),
        ('Permanent Resident', 'Permanent Resident'),
        ('Refugee', 'Refugee'),
        ('Student Work Permit', 'Student Work Permit'),
        ('Study Permit', 'Study Permit'),
        ('Visitor Visa', 'Visitor Visa'),
        ('Work Permit', 'Work Permit')
    )
    DEGREE_TYPE_CHOICES = (
        ('Bachelor’s', 'Bachelor’s'),
        ('Bachelor’s Equivalent', 'Bachelor’s Equivalent'),
        ('Bachelor’s Honours', 'Bachelor’s Honours'),
        ('Master’s Equivalent', 'Master’s Equivalent'),
        ('Master’s non-Thesis', 'Master’s non-Thesis'),
        ('Master’s Thesis', 'Master’s Thesis'),
        ('Doctorate', 'Doctorate'),
        ('Doctorate Equivalent', 'Doctorate Equivalent'),
        ('Post-doctorate', 'Post-doctorate'),
        ('Certificate', 'Certificate'),
        ('Diploma', 'Diploma'),
        ('Habilitation', 'Habilitation'),
        ('Research Associate', 'Research Associate'),
        ('Technician', 'Technician')
    )
    DEGREE_STATUS_CHOICES = (
        ('All But Degree', 'All But Degree'),
        ('Completed', 'Completed'),
        ('In Progress', 'In Progress'),
        ('Withdrawn', 'Withdrawn')
    )


class StudentCountryOfCitizenShip(Base):
    """The countries of citizenship of the student"""

    country_name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                    help_text="Country of citizenship of the student")

    student_supervision = models.ForeignKey(StudentSupervision, on_delete=models.CASCADE)


class StudentRecognition(Base):
    """Recognitions obtained by the student. Recognitions are any acknowledgments, appreciations and monetary rewards
    that were obtained and which were not directly related to your research funding. """

    TYPE_CHOICES = (
        ('Citation', 'Citation'),
        ('Distinction', 'Distinction'),
        ('Honor', 'Honor'),
        ('Prize / Award', 'Prize / Award')
    )

    type = models.CharField(max_length=20, null=True, blank=True, help_text="")
    name = models.CharField(max_length=250, null=True, blank=True, help_text="The name or title of the recognition")
    year_started = models.CharField(max_length=4, null=True, blank=True,
                                    help_text="The year when the recognition was awarded or took effect")
    year_completed = models.CharField(max_length=4, null=True, blank=True,
                                      help_text="The year when this recognition expires")
    amount = models.IntegerField(null=True, blank=True, help_text="The amount that was awarded for this recognition")
    currency = models.CharField(max_length=10, null=True, blank=True,
                                help_text="The currency in which the money was awarded")

    organisation = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                    help_text="The organization that gave the recognition")
    other_organization = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                          help_text="If someone cannot find the org from the list")

    student_supervision = models.ForeignKey(StudentSupervision, on_delete=models.CASCADE)





class AdministrativeActivity(Base):
    """"""


class AdvisoryActivity(Base):
    """"""


class AssessmentAndReviewActivity(Base):
    """Services contributed to examine something, formulate a judgement, and provide a statement of that judgement."""

    activity = models.OneToOneField(Activity, on_delete=models.CASCADE)


class JournalReviewActivity(ActivityAbstract):
    """Services contributed to examine a journal, formulate a judgement, and a statement of that judgement"""

    REVIEW_TYPE_CHOICES = (
        ('Blind', 'Blind'),
        ('Double Blind', 'Double Blind'),
        ('Open', 'Open')
    )

    role = models.CharField(max_length=100, null=True, blank=True, help_text="The person's role in this activity")
    review_type = models.CharField(max_length=20, null=True, blank=True, choices=REVIEW_TYPE_CHOICES,
                                   help_text="The nature of the review conducted")
    journal = models.CharField(max_length=200, null=True, blank=True, help_text="The name of the journal")
    press = models.CharField(max_length=250, null=True, blank=True, help_text="The name of the press")
    works_reviewed_count = models.IntegerField(null=True, blank=True, default=0,
                                               help_text="Indicate how many works were reviewed")

    assessment_review_activity = models.ForeignKey(AssessmentAndReviewActivity, on_delete=models.CASCADE)


class ConferenceReviewActivity(ActivityAbstract):
    """Services contributed, in conjunction with a scheduled conference, to examine something, formulate a judgement,
        and a statement of that judgement """

    REVIEW_TYPE_CHOICES = (
        ('Blind', 'Blind'),
        ('Double Blind', 'Double Blind'),
        ('Open', 'Open')
    )

    role = models.CharField(max_length=100, null=True, blank=True, help_text="The person's role in this activity")
    review_type = models.CharField(max_length=20, null=True, blank=True, choices=REVIEW_TYPE_CHOICES,
                                   help_text="The nature of the review conducted")
    conference = models.CharField(max_length=250, null=True, blank=True, help_text="The name of the conference")
    conference_host = models.CharField(max_length=250, null=True, blank=True, help_text="The organization hosting the "
                                                                                        "conference")
    works_referred_count = models.IntegerField(null=True, blank=True, default=0,
                                               help_text="Indicate how many works were reviewed")

    assessment_review_activity = models.ForeignKey(AssessmentAndReviewActivity, on_delete=models.CASCADE)


class GraduationExaminationActivity(ActivityAbstract):
    """Services contributed, in conjunction with the awarding of a graduate degree, to examine the proposal,
    formulate a judgement, and a statement of that judgement """

    ROLE_CHOICES = (
        ('Candidacy Committee Chair', 'Candidacy Committee Chair'),
        ('Candidacy Committee Member', 'Candidacy Committee Member'),
        ('Capping Project Evaluator', 'Capping Project Evaluator'),
        ('Chair', 'Chair'),
        ('Committee Member', 'Committee Member'),
        ('Examiner', 'Examiner'),
        ("Master's Oral Exam Chair", "Master's Oral Exam Chair"),
        ("Master's Oral Exam Member", "Master's Oral Exam Member"),
        ("Master's Proposal Defense Chair", "Master's Proposal Defense Chair"),
        ("Master's Proposal Defense Member", "Master's Proposal Defense Member"),
        ('PhD Comprehensive Exam Committee Member', 'PhD Comprehensive Exam Committee Member'),
        ('PhD External Examiner', 'PhD External Examiner'),
        ('PhD External Reader', 'PhD External Reader'),
        ('PhD Oral Exam Chair', 'PhD Oral Exam Chair'),
        ('PhD Oral Exam Member', 'PhD Oral Exam Member'),
        ('Thesis Defense Chair', 'Thesis Defense Chair'),
        ('Thesis Defense Examiner', 'Thesis Defense Examiner')
    )

    role = models.CharField(max_length=50, null=True, blank=True, choices=ROLE_CHOICES,
                            help_text="The person's role in this activity")
    department = models.CharField(max_length=100, null=True, blank=True,
                                  help_text="The department within the given institution")
    student_name = models.CharField(max_length=100, null=True, blank=True,
                                    help_text="The family and first name of the student")
    organization = models.OneToOneField(Organization, null=True, blank=True, on_delete=models.CASCADE,
                                        help_text="The institution for which the examination was conducted.")
    other_organization = models.OneToOneField(OtherOrganization, null=True, blank=True, on_delete=models.CASCADE)

    assessment_review_activity = models.ForeignKey(AssessmentAndReviewActivity, on_delete=models.CASCADE)


class ResearchFundingApplicationAssessmentActivity(ActivityAbstract):
    """Services contributed, in conjunction with the assessment of a research funding application, to examine the
    application, formulate a judgement, and a statement of that judgement. """

    REVIEWER_ROLE_CHOICES = (
        ('Chair', 'Chair'),
        ('Committee Member', 'Committee Member'),
        ('External Reviewer', 'External Reviewer'),
        ('Scientific Officer', 'Scientific Officer')
    )
    ASSESSMENT_TYPE_CHOICES = (
        ('Funder', 'Funder'),
        ('Organization', 'Organization')
    )
    REVIEWER_TYPE_CHOICES = (
        ('Academic Reviewer', 'Academic Reviewer'),
        ('Industry', 'Industry'),
        ('Knowledge User', 'Knowledge User'),
        ('Non-academic Reviewer', 'Non-academic Reviewer')
    )

    funding_reviewer_role = models.CharField(max_length=20, null=True, blank=True, choices=REVIEWER_ROLE_CHOICES,
                                             help_text="The person's role in this activity")
    assessment_type = models.CharField(max_length=20, null=True, blank=True, choices=ASSESSMENT_TYPE_CHOICES,
                                       help_text="The nature of the assessment. Indicate whether the assessment was "
                                                 "done for a Funding Organization (Funder) or another organization ("
                                                 "Institution)")
    reviewer_type = models.CharField(max_length=30, null=True, blank=True, choices=REVIEWER_TYPE_CHOICES,
                                     help_text="The nature of the reviewer")
    committee_name = models.CharField(max_length=250, null=True, blank=True,
                                      help_text="The committee name for the funding assessment")
    funding_organization = models.CharField(max_length=NAME_LENGTH_MAX, null=True, blank=True,
                                            help_text="The name of the organization which provided the grant or "
                                                      "scholarship")
    applications_assessed_count = models.IntegerField(null=True, blank=True,
                                                      help_text="The number of applications that the person assessed")
    organization = models.OneToOneField(Organization, null=True, blank=True, on_delete=models.CASCADE,
                                        help_text="The organization for which the assessment was made")
    other_organization = models.OneToOneField(OtherOrganization, null=True, blank=True, on_delete=models.CASCADE)

    assessment_review_activity = models.ForeignKey(AssessmentAndReviewActivity, on_delete=models.CASCADE)


class PromotionTenureAssessmentActivity(ActivityAbstract):
    """Services contributed, in conjunction with the consideration of an application for promotion/tenure,
    to examine something, formulate a judgement, and a statement of that judgement. """

    role = models.CharField(max_length=NAME_LENGTH_MAX, null=True, blank=True,
                            help_text="The person's role in this activity")
    department = models.CharField(max_length=NAME_LENGTH_MAX, null=True, blank=True,
                                  help_text="The department within the given organization")
    assessments_count = models.IntegerField(null=True, blank=True,
                                            help_text="The number of applications which were assessed by "
                                                      "the person")
    description = models.CharField(max_length=1000, null=True, blank=True,
                                   help_text="Description of the services contributed by the person, in conjunction "
                                             "with the consideration of an application for promotion/tenure, "
                                             "to examine something, formulate a judgement, and a statement of that "
                                             "judgement.")
    organization = models.OneToOneField(Organization, null=True, blank=True, on_delete=models.CASCADE,
                                        help_text="The organization for which the assessment was made")
    other_organization = models.OneToOneField(OtherOrganization, null=True, blank=True, on_delete=models.CASCADE)

    assessment_review_activity = models.ForeignKey(AssessmentAndReviewActivity, on_delete=models.CASCADE)


class OrganizationalReviewActivity(ActivityAbstract):
    """Services contributed, in conjunction with the assessment of an institution, to examine something, formulate a
    judgement, and a statement of that judgement. """

    role = models.CharField(max_length=NAME_LENGTH_MAX, null=True, blank=True,
                            help_text="The person's role in this activity")
    description = models.CharField(max_length=1000, null=True, blank=True,
                                   help_text="Description of the services contributed by the person, in conjunction "
                                             "with the consideration of an application for promotion/tenure, "
                                             "to examine something, formulate a judgement, and a statement of that "
                                             "judgement.")
    organization = models.OneToOneField(Organization, null=True, blank=True, on_delete=models.CASCADE,
                                        help_text="The organization for which the assessment was made")
    other_organization = models.OneToOneField(OtherOrganization, null=True, blank=True, on_delete=models.CASCADE)

    assessment_review_activity = models.ForeignKey(AssessmentAndReviewActivity, on_delete=models.CASCADE)


class ParticipationActivity(Base):
    """Services contributed in participating in an activity"""

    activity = models.OneToOneField(Activity, on_delete=models.CASCADE)


class EventActivity(ActivityAbstract):
    """Services contributed in taking part in an event"""

    TYPE_CHOICES = (
        ('Association', 'Association'),
        ('Club', 'Club'),
        ('Conference', 'Conference'),
        ('Course', 'Course'),
        ('Seminar', 'Seminar'),
        ('Workshop', 'Workshop')
    )

    role = models.CharField(max_length=100, null=True, blank=True, help_text="The role of the person in this activity")
    type = models.CharField(max_length=20, null=True, blank=True, choices=TYPE_CHOICES,
                            help_text="The nature of the event")
    name = models.CharField(max_length=250, null=True, blank=True, help_text="The title or name of the event")
    event_start_date = models.DateField(null=True, blank=True, help_text="The date the event started")
    event_end_date = models.DateField(null=True, blank=True, help_text="The date the event ended")
    description = models.CharField(max_length=1000, null=True, blank=True,
                                   help_text="Description of the services the person contributed in taking part in an "
                                             "event")

    participation_activity = models.ForeignKey(ParticipationActivity, on_delete=models.CASCADE)


class CommunityAndVolunteerActivity(ActivityAbstract):
    """Services contributed, unpaid, on behalf of one’s locality, social, religious, occupational, or other group
    sharing common characteristics or interests, but not directly related to the person's research activities """

    role = models.CharField(max_length=100, null=True, blank=True, help_text="The role of the person in this activity")
    description = models.CharField(max_length=1000, null=True, blank=True,
                                   help_text="Description of the unpaid services")

    organization = models.OneToOneField(Organization, null=True, blank=True, on_delete=models.CASCADE,
                                        help_text="The name of the organization for which the service was undertaken")
    other_organization = models.OneToOneField(OtherOrganization, null=True, blank=True, on_delete=models.CASCADE)
    participation_activity = models.ForeignKey(ParticipationActivity, on_delete=models.CASCADE)


class KnowledgeTranslation(ActivityAbstract):
    """Contribution to knowledge and technology translation"""

    role = models.CharField(max_length=100, null=True, blank=True, help_text="The person's role in this activity")
    knowledge_translation_activity_type = models.CharField(max_length=50, null=True, blank=True,
                                                           help_text="")
    group_or_organization_serviced = models.CharField(max_length=100, null=True, blank=True,
                                                      help_text="")
    # evidence_of_uptake = models.CharField(max_length=1000, ?he)
    reference_or_citation = models.CharField(max_length=1000, null=True, blank=True,
                                             help_text="Provide references, citations or websites demonstrating the "
                                                       "uptake of your research findings")
    activity_description = models.CharField(max_length=1000, null=True, blank=True,
                                            help_text="Description of services the person contributed to knowledge "
                                                      "translation")


class InternationalCollaborationActivity(ActivityAbstract):
    """International Collaborations can be described as situations where the applicant worked with others outside of
    Canada on administrative, professional, research, or knowledge translation projects. These activities should be
    relevant to the application the researcher is submitting with this CV"""

    role = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                            help_text="The role of the person in this activity")
    location = models.CharField(max_length=30, null=True, blank=True,
                                help_text="The principal country with which the person collaborated")  # c
    description = models.TextField(max_length=1000, null=True, blank=True)

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

########################################################################################################################


class Contribution(Base):
    """The things you have done as part of your career"""

    ccv = models.OneToOneField(CanadianCommonCv, on_delete=models.CASCADE)


class ContributionFundingSource(Base):
    """Funding Source Model for Contribution Entity"""

    organisation = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                    help_text="Main funding org name who has funded this contribution")
    other_organization = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                          help_text="If someone cannot find the org from the list")
    reference_number = models.CharField(max_length=20, null=True, blank=True,
                                        help_text="reference number for the funds received")


class ContributionAbstract(Base):

    funding_source = models.ManyToManyField(FundingSource, related_name="%(app_label)s_%(class)s_related",
                                            related_query_name="%(app_label)s_%(class)ss")

    class Meta:
        abstract = True


class Presentation(ContributionAbstract):
    """Contributions of presentations to groups of people not delivered as part of a formal course of study"""

    MAIN_AUDIENCE_CHOICES = (
        ('Decision Maker', 'Decision Maker'),
        ('General Public', 'General Public'),
        ('Knowledge User', 'Knowledge User'),
        ('Researcher', 'Researcher')
    )

    title = models.CharField(max_length=250, null=True, blank=True, help_text="The title of the presentation")
    event_name = models.CharField(max_length=250, null=True, blank=True,
                                  help_text="The name of the event in which the person gave the presentation")
    location = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                help_text="The country where the conference took place")  #
    city = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                            help_text="The city where the conference took place")
    main_audience = models.CharField(max_length=20, null=True, blank=True, choices=MAIN_AUDIENCE_CHOICES,
                                     help_text="The nature of the audience")
    is_invited = models.BooleanField(null=True, blank=True,
                                     help_text="Indicate whether the person was invited to present this information")
    is_keynote = models.BooleanField(null=True, blank=True,
                                     help_text="Indicate whether the person gave the keynote address at this event")
    is_competitive = models.BooleanField(null=True, blank=True,
                                         help_text="Indicate if participation in this event was competitive")
    presentation_year = models.CharField(max_length=4, null=True, blank=True,
                                         help_text="The year the presentation was given")
    description = models.CharField(max_length=1000, null=True, blank=True,
                                   help_text="Concise description of this contribution and its value to the area of "
                                             "research for which you are applying for funding")
    url = models.URLField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                          help_text="The name of an associated website, if applicable")
    co_presenters = models.CharField(max_length=200, null=True, blank=True,
                                     help_text="The names of other persons presenting this topic, if applicable")

    contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE)


class InterviewAndMediumRelation(ContributionAbstract):
    """Services contributed in the form of interview(s) with the person with a member of the broadcast (TV or radio)
    media. """

    topic = models.CharField(max_length=250, null=True, blank=True, help_text="The subject of the interview")
    interviewer = models.CharField(max_length=100, null=True, blank=True, help_text="The interviewers' names")
    description = models.CharField(max_length=1000, null=True, blank=True,
                                   help_text="description of this contribution and its value to the area of research")
    url = models.URLField(max_length=100, null=True, blank=True,
                          help_text="The name of an associated website, if applicable")

    class Meta:
        abstract = True


class BroadcastInterview(InterviewAndMediumRelation):
    """Services contributed in the form of interview(s) with the person with a member of the broadcast (TV or radio)
    media. """

    program = models.CharField(max_length=250, null=True, blank=True, help_text="")
    network = models.CharField(max_length=250, null=True, blank=True, help_text="")
    first_broadcast_date = models.DateField(null=True, blank=True,
                                            help_text="The date on which the interview was first aired")
    end_date = models.DateField(null=True, blank=True,
                                help_text="The date on which the broadcast of the interview ended")

    contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE)


class TextInterview(InterviewAndMediumRelation):
    """Services contributed in the form of interview(s) with the person with a member of the print or online media"""

    forum = models.CharField(max_length=250, null=True, blank=True,
                             help_text="The name of the forum for which the interview was conducted")
    publication_date = models.DateField(null=True, blank=True,
                                        help_text="The date on which the interview was first published")

    contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE)


class Publication(Base):
    """Collection of information records that, in combination, represent a full and up-to-date history of research or
    scholarly published outputs resulting from, or related to, the person's research activities """

    contribution = models.OneToOneField(Contribution, on_delete=models.CASCADE)


class PublicationAbstract(ContributionAbstract):
    """"""

    CONTRIBUTION_PERCENTAGE_CHOICES = (
        ('0-10', '0-10'),
        ('11-20', '11-20'),
        ('21-30', '21-30'),
        ('31-40', '31-40'),
        ('41-50', '41-50'),
        ('51-60', '51-60'),
        ('61-70', '61-70'),
        ('71-80', '71-80'),
        ('81-90', '81-90'),
        ('91-100', '91-100')
    )
    ROLE_CHOICES = (
        ('Co-Author', 'Co-Author'),
        ('Co-Editor', 'Co-Editor'),
        ('First Listed Author', 'First Listed Author'),
        ('First Listed Editor', 'First Listed Editor'),
        ('Last Author', 'Last Author')
    )

    title = models.CharField(max_length=250, null=True, blank=True)
    contribution_value = models.CharField(max_length=1000, null=True, blank=True, help_text="")
    url = models.URLField(max_length=500, null=True, blank=True, help_text="")
    role = models.CharField(max_length=30, null=True, blank=True, choices=ROLE_CHOICES,
                            help_text="The nature of the person's role")
    contributors_count = models.IntegerField(null=True, blank=True, help_text="The number of contributors")
    contribution_percentage = models.CharField(max_length=10, null=True, blank=True,
                                               choices=CONTRIBUTION_PERCENTAGE_CHOICES,
                                               help_text="approximate percentage (%) of work you contributed towards "
                                                         "this publication")
    doi = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                           help_text="digital object identifier (DOI) for this publication")
    description_of_role = models.CharField(max_length=1000, null=True, blank=True,
                                           help_text="brief description of your contribution role towards this publication")

    class Meta:
        abstract = True


class AuthorEditor(models.Model):
    """Contains author & editor fields to be inherited wherever necessary"""

    authors = models.CharField(max_length=1000, null=True, blank=True,
                               help_text="The names of other authors")
    editors = models.CharField(max_length=200, null=True, blank=True, help_text="The names of the editors")

    class Meta:
        abstract = True


class PublicationStaticAbstract(PublicationAbstract):
    """"""
    STATUS_CHOICES = (
        ('Accepted', 'Accepted'),
        ('In Press', 'In Press'),
        ('Published', 'Published'),
        ('Revision Requested', 'Revision Requested'),
        ('Submitted', 'Submitted')
    )

    publishing_status = models.CharField(max_length=30, choices=STATUS_CHOICES, null=True, blank=True,
                                         help_text="The status of the article with regard to publication")
    year = models.CharField(max_length=4, null=True, blank=True, help_text="The year relative to the Publishing Status")
    publisher = models.CharField(max_length=100, null=True, blank=True, help_text="The name of the publisher")
    publication_location = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                            help_text="The place where it was published")


class Journal(PublicationAbstract, AuthorEditor):
    """"Journal Article & Journal Type has been combined to one entity Journal because it contains all common fields."""

    TYPE_CHOICES = (
        ('Issue', 'Issue'),
        ('Article', 'Article')
    )

    journal = models.CharField(max_length=200, null=True, blank=True,
                               help_text="The name of the journal in which the article is published, or to be published")
    volume = models.CharField(max_length=20, null=True, blank=True, help_text="The volume number of the journal")
    issue = models.CharField(max_length=10, null=True, blank=True, help_text="The volume number of the journal")
    page_range = models.CharField(max_length=20, null=True, blank=True,
                                  help_text="The page range with a dash ('-') as separator (e.g. 234-256)")
    publisher = models.CharField(max_length=100, null=True, blank=True, help_text="The name of the publisher")
    publication_location = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                            help_text="The country where it was published")
    is_refereed = models.BooleanField(null=True, blank=True, help_text="Indicate if the journal is refereed")
    is_open_access = models.BooleanField(null=True, blank=True, help_text="Indicate if the journal is open access")
    is_synthesis = models.BooleanField(null=True, blank=True,
                                       help_text="contextualization and integration of research findings of "
                                                 "individual research within the larger body of knowledge on topic")
    journal_type = models.CharField(max_length=10, choices=TYPE_CHOICES,
                                    help_text="This field is to indicate journal type")

    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)


class Book(PublicationStaticAbstract, AuthorEditor):
    """Books written by a single author or collaboratively based on research or scholarly findings generally derived
    from peer reviewed funding """
###
    publication_city = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                        help_text="City where the publication was published")
    is_refereed = models.BooleanField(null=True, blank=True, help_text="Indicate if the project was refereed")

    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)


class BookChapter(PublicationStaticAbstract, AuthorEditor):
    """Texts written by a single author or collaboratively based on research or scholarly findings and expertise in a
    field """

    book_title = models.CharField(max_length=250, null=True, blank=True, help_text="The title of the book")
    publication_city = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                        help_text="City where the publication was published")
    is_refereed = models.BooleanField(null=True, blank=True, help_text="Indicate if the project was refereed")

    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)


class BookReview(PublicationAbstract):
    """Critical review of works of fiction or non-fiction highlighting the contributions to an art,
    field or discipline """
###
    review_year = models.CharField(max_length=4, null=True, blank=True, help_text="The year the review was published")
    reviewed_title = models.CharField(max_length=250, null=True, blank=True,
                                      help_text="The title of the book that was reviewed")
    reviewed_edition = models.CharField(max_length=50, null=True, blank=True,
                                        help_text="The edition of the book that was reviewed")
    reviewed_volume = models.CharField(max_length=20, null=True, blank=True,
                                       help_text="The publication Year of the book that was reviewed")
    reviewed_publication_year = models.CharField(max_length=4, null=True, blank=True,
                                                 help_text="The publication Year of the book that was reviewed")
    reviewed_author = models.CharField(max_length=1000, null=True, blank=True)

    is_refereed = models.BooleanField(null=True, blank=True, help_text="Indicate if the project was refereed")

    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)


class Translation(PublicationStaticAbstract):
    """Translations of books and articles that identify modifications to the original edition, such as a new or
    revised preface. """
###
    published_in = models.CharField(max_length=100, null=True, blank=True,
                                    help_text="The publication in which the translation was published")
    publication_city = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                        help_text="City where the publication was published")

    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)


class ThesisDissertation(PublicationAbstract):
    """Treatise advancing an original point of view resulting from research."""

    DEGREE_TYPE_CHOICES = (
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

    supervisor = models.CharField(max_length=100, null=True, blank=True,
                                  help_text="The family and first name of the supervisor")
    completion_year = models.CharField(max_length=4, null=True, blank=True,
                                       help_text="The year the dissertation was completed")
    degree_type = models.CharField(null=True, blank=True, max_length=30, choices=DEGREE_TYPE_CHOICES,
                                   help_text="The designation of the person's degree")
    pages_count = models.IntegerField(null=True, blank=True, help_text="Number of pages of the dissertation")

    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, null=True, blank=True,
                                       help_text="The name of the institution that consigned the report")
    other_organization = models.OneToOneField(OtherOrganization, on_delete=models.CASCADE, null=True, blank=True)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)


class SupervisedStudentPublication(PublicationStaticAbstract):
    """Articles on research findings published jointly with or supervised by the thesis advisor. The findings relate
    to research undertaken by the student or the supervisor’s program of research. """
###
    student = models.CharField(max_length=100, null=True, blank=True, help_text="name of student who was supervised")
    published_in = models.CharField(max_length=100, null=True, blank=True,
                                    help_text="Name of the journal in which article is published, or to be published")
    student_contribution = models.IntegerField(null=True, blank=True,
                                               help_text="Indicate the approximate contribution of the student "
                                                         "towards this publication")

    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)


class Litigation(PublicationAbstract):
    """The act or process of contesting at law"""

    person_acted_for = models.CharField(max_length=100, null=True, blank=True,
                                        help_text="The name of the person the person represented/acted for")
    court = models.CharField(max_length=250, null=True, blank=True, help_text="The court in which the case was heard")
    location = models.CharField(max_length=50, null=True, blank=True,
                                help_text="The location of the court in which the case was heard")
    year_started = models.CharField(max_length=4, null=True, blank=True,
                                    help_text="The year the case started")
    end_year = models.CharField(max_length=4, null=True, blank=True, help_text="The year the case ended")
    key_legal_issues = models.CharField(max_length=1000, null=True, blank=True,
                                        help_text="A description of the key issues in the case")

    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)


class NewspaperArticle(PublicationStaticAbstract, AuthorEditor):
    """Articles in a daily, weekly or monthly publication reporting on news and social issues aimed at the public.
    May entail critical analysis based on expertise in the field. """

###
    newspaper = models.CharField(max_length=250, null=True, blank=True,
                                 help_text="The name of the newspaper in which it was published")

    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)


class EncyclopediaEntry(PublicationStaticAbstract, AuthorEditor):
    """Authored entries in a reference work or a compendium focusing on a particular domain or on all branches of
    knowledge. """
####
    name = models.CharField(max_length=250, null=True, blank=True, help_text="")
    publication_city = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                        help_text="City where the publication was published")

    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)


class MagazineEntry(PublicationStaticAbstract, AuthorEditor):
    """Articles in thematic publications published at fixed intervals"""
###
    name = models.CharField(max_length=250, null=True, blank=True,
                            help_text="The name of the magazine in which it was published")

    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)


class DictionaryEntry(PublicationAbstract, AuthorEditor):
    """Entries of new words, new meanings of existing words, changes in spelling and hyphenation over a longer period
    of time, and grammatical changes. """

    name = models.CharField(max_length=250, null=True, blank=True, help_text="")
    edition = models.CharField(max_length=50, null=True, blank=True, help_text="The edition in which it was published")
    volume = models.CharField(max_length=20, null=True, blank=True, help_text="The volume in which it was published")
    volumes_count = models.IntegerField(null=True, blank=True,
                                        help_text="The total number of volumes contained in the dictionary")
    page_range = models.IntegerField(null=True, blank=True,
                                     help_text="The page range with a dash ('-') as separator (e.g. 234-256)")
    year = models.CharField(max_length=4, null=True, blank=True, help_text="The year relative to the Publishing Status")
    publisher = models.CharField(max_length=100, null=True, blank=True, help_text="")
    location = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                help_text="The country of the publication")
    city = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True, help_text="")

    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)


class Report(PublicationAbstract, AuthorEditor):
    """Reports disseminating the outcomes and deliverables of a research contract. May entail a contribution to
    public policy. """

    year_submitted = models.CharField(max_length=4, null=True, blank=True,
                                      help_text="The year the report was submitted to the institution")
    pages_count = models.IntegerField(null=True, blank=True, help_text="The number of pages in the document")
    is_synthesis = models.BooleanField(null=True, blank=True,
                                       help_text="contextualization and integration of research findings of individual research studies within the larger body of knowledge on the topic")

    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, null=True, blank=True,
                                        help_text="The name of the institution that consigned the report")
    other_organization = models.OneToOneField(OtherOrganization, on_delete=models.CASCADE, null=True, blank=True)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)


class WorkingPaper(PublicationAbstract, AuthorEditor):
    """Preliminary versions of articles that have not undergone review but that may be shared for comment."""

    year_completed = models.CharField(max_length=4, null=True, blank=True, help_text="The year the paper was completed")
    pages_count = models.IntegerField(null=True, blank=True, help_text="The number of pages in the document")

    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)


class Manual(PublicationStaticAbstract, AuthorEditor):
    """Course and assignment materials produced for teaching purposes"""

    published_in = models.CharField(max_length=100, null=True, blank=True,
                                    help_text="The publication in which the manual was published")
    edition = models.CharField(max_length=50, null=True, blank=True, help_text="The edition in which it was published")
    volume = models.CharField(max_length=20, null=True, blank=True, help_text="The volume in which it was published")
    volumes_count = models.IntegerField(null=True, blank=True,
                                        help_text="The total number of volumes contained in the manual")
    pages_count = models.IntegerField(null=True, blank=True, help_text="The total number of pages in the manual")

    publication_city = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                        help_text="City where the publication was published")

    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)


class OnlineResource(PublicationStaticAbstract, AuthorEditor):
    """Information accessible only on the web via traditional technical methods (ie hyperlinks)"""

    year_posted = models.CharField(max_length=4, null=True, blank=True, help_text="The year that it was posted online")

    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)


class Test(PublicationAbstract, AuthorEditor):
    """Assessments that include tests designed for general university selection, selection into specific courses or
    other evaluation purposes """

    year_released = models.CharField(max_length=4, null=True, blank=True,
                                     help_text="The year the guideline was first released")

    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)


class ClinicalCareGuideline(PublicationAbstract):
    """Clinical Care Guidelines are documents based on clinical evidence, designed to support the decision-making
    process in patient care. Use this section to capture any Clinical Care Guidelines that you developed or
    co-authored. """

    year_released = models.CharField(max_length=4, null=True, blank=True,
                                     help_text="The year the guideline was first released")
    contributors = models.CharField(max_length=200, null=True, blank=True,
                                    help_text="The names of the other contributors")

    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)


class ConferencePublication(PublicationStaticAbstract, AuthorEditor):
    """Conference publications include Abstracts, Posters and Papers."""

    TYPE_CHOICES = (
        ('Abstract', 'Abstract'),
        ('Paper', 'Paper'),
        ('Poster', 'Poster')
    )

    type = models.CharField(max_length=10, null=True, blank=True, choices=TYPE_CHOICES,
                            help_text="The nature of the conference publication")
    name = models.CharField(max_length=250, null=True, blank=True,
                            help_text="The name of the conference for which the document was written")
    conference_location = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                           help_text="The country where the conference was held.")
    city = models.CharField(max_length=100, null=True, blank=True, help_text="The city where the conference was held")
    date = models.DateField(null=True, blank=True, help_text="The date the conference began")
    published_in = models.CharField(max_length=100, null=True, blank=True,
                                    help_text="The title of the proceedings publication")
    page_range = models.CharField(max_length=20, null=True, blank=True)
    is_refereed = models.BooleanField(null=True, blank=True, help_text="Indicate whether the document was refereed")
    is_invited = models.BooleanField(null=True, blank=True,
                                     help_text="Indicate whether the author was invited to present at the conference")

    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)

########################################################################################################################


class ArtisticContribution(Base):
    """Collection of information records that, in combination, represent a full and up-to-date history of artistic or
    performance outputs resulting from, or related to, the person's research or scholarly activities. Works may be
    produced alone or collaboratively as a creative practice that lead to production and dissemination. """

    contribution = models.OneToOneField(Contribution, on_delete=models.CASCADE)


class ArtisticContributionAbstract(ContributionAbstract):
    """It contains the fields which are common in Artistic Contribution fields."""

    title = models.CharField(max_length=250, null=True, blank=True)
    url = models.URLField(null=True, blank=True, help_text="The name of an associated website, if applicable")
    role = models.CharField(max_length=100, null=True, blank=True, help_text="The nature of the person's role")
    contributors_count = models.IntegerField(null=True, blank=True, help_text="The number of contributors")
    contributors = models.CharField(max_length=200, null=True, blank=True,
                                    help_text="The names of the other contributors")
    contribution_value = models.CharField(max_length=1000, null=True, blank=True, help_text="")

    class Meta:
        abstract = True


class ArtisticExhibition(ArtisticContributionAbstract):
    """Showings of works of art under the direction of a curator, an artist or as a graduation exhibition."""

    venue = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                             help_text="The venue where it was presented")
    first_performance_date = models.DateField(null=True, blank=True, help_text="The date the piece was first presented")

    artistic_contribution = models.ForeignKey(ArtisticContribution, on_delete=models.CASCADE)


class AudioRecording(ArtisticContributionAbstract):
    """Works such as classical or aboriginal music produced as a result of an artistic practice. May be produced and
    be commercially disseminated. """

    album_title = models.CharField(max_length=250, null=True, blank=True,
                                   help_text="The title of the album on which it is recorded")
    producer = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                help_text="The producer's name")
    distributor = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                   help_text="The name of the distributor of the album")
    release_date = models.DateField(null=True, blank=True, help_text="The date of initial release of the recording")

    artistic_contribution = models.ForeignKey(ArtisticContribution, on_delete=models.CASCADE)


class ExhibitionCatalogue(ArtisticContributionAbstract):
    """Publications for a temporary exhibition or installation at a gallery or alternative space. It documents the
    contents of an exhibition, providing a forum for critical dialogue between curators, artists and critics. It
    serves as a scholarly resource and is eligible for prestigious prizes. """

    gallery_publisher = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                         help_text="The name of the gallery or publisher for which the catalogue was created")
    publication_date = models.DateField(null=True, blank=True,
                                        help_text="The year and month the catalogue was published.")
    publication_location = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                            help_text="The place where the catalogue was published")
    publication_city = models.CharField(max_length=50, null=True, blank=True,
                                        help_text="City where the publication was published")
    pages_count = models.IntegerField(null=True, blank=True, help_text="The total number of pages")
    artists = models.CharField(max_length=250, null=True, blank=True,
                               help_text="The names of the artists presented in the catalogue")

    artistic_contribution = models.ForeignKey(ArtisticContribution, on_delete=models.CASCADE)


class MusicalCompilation(ArtisticContributionAbstract):
    """Original musical scores available in a format for dissemination"""

    instrumentation_tags = models.CharField(max_length=250, null=True, blank=True,
                                            help_text="The instrument(s) for which it is written")
    pages_count = models.IntegerField(null=True, blank=True, help_text="The total number of pages")
    duration = models.CharField(max_length=10, null=True, blank=True)
    publisher = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                 help_text="The publisher of the composition")
    publication_date = models.DateField(null=True, blank=True,
                                        help_text="The year and month the composition was published.")
    publication_location = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                            help_text="The place where the composition was published")

    artistic_contribution = models.ForeignKey(ArtisticContribution, on_delete=models.CASCADE)


class MusicalPerformance(ArtisticContributionAbstract):
    """Original musical scores available in a format for dissemination"""

    venue = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                             help_text="The venue where it was presented")
    first_performance_date = models.DateField(null=True, blank=True, help_text="The date the piece was first presented")

    artistic_contribution = models.ForeignKey(ArtisticContribution, on_delete=models.CASCADE)


class RadioAndTvProgram(ArtisticContributionAbstract):
    """Programming produced for and broadcast on radio or TV"""

    episode_title = models.CharField(max_length=250, null=True, blank=True,
                                     help_text="The title of the episode of the program")
    no_of_episodes = models.IntegerField(null=True, blank=True,
                                         help_text="The number of episodes for which the person took part")
    series_title = models.CharField(max_length=250, null=True, blank=True, help_text="The title of the series")
    publication_date = models.DateField(null=True, blank=True,
                                        help_text="The year and month the composition was published.")
    publication_location = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                            help_text="The place where the composition was published")

    artistic_contribution = models.ForeignKey(ArtisticContribution, on_delete=models.CASCADE)


class Broadcast(Base):
    """Broadcast details for the program"""

    date = models.DateField(null=True, blank=True, help_text="The date of broadcast of the program")
    network_name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                    help_text="The network on which the program was broadcasted")

    radio_and_tv_program = models.ForeignKey(RadioAndTvProgram, on_delete=models.CASCADE)


class Scripts(ArtisticContributionAbstract):
    """Written versions of a play, film, broadcast or other dramatic composition used in preparing for a performance
    and annotated with instructions for the performance """

    publication_date = models.DateField(null=True, blank=True, help_text="The date script was completed")
    authors = models.CharField(max_length=200, null=True, blank=True,
                               help_text="The names of other authors of the script")
    editors = models.CharField(max_length=200, null=True, blank=True, help_text="The names of the editors")

    artistic_contribution = models.ForeignKey(ArtisticContribution, on_delete=models.CASCADE)


class Fiction(ArtisticContributionAbstract):
    """Original literary texts"""

    appeared_in = models.CharField(max_length=100, null=True, blank=True,
                                   help_text="The name of the publication in which the work appeared")
    volume = models.CharField(max_length=20, null=True, blank=True, help_text="The volume number of the fiction")
    issue = models.CharField(max_length=10, null=True, blank=True, help_text="The volume number of the fiction")
    page_range = models.CharField(max_length=20, null=True, blank=True,
                                  help_text="The page range with a dash ('-') as separator (e.g. 234-256)")
    publication_date = models.DateField(null=True, blank=True, help_text="The date script was completed")
    publisher = models.CharField(max_length=100, null=True, blank=True, help_text="The name of the publisher")
    publication_location = models.CharField(max_length=50, null=True, blank=True,
                                            help_text="The country of publication")

    authors = models.CharField(max_length=200, null=True, blank=True,
                               help_text="The names of other authors of the function")
    editors = models.CharField(max_length=200, null=True, blank=True, help_text="The names of the editors")

    artistic_contribution = models.ForeignKey(ArtisticContribution, on_delete=models.CASCADE)


class TheatrePerformanceAndProduction(ArtisticContributionAbstract):
    """Creation, production, dissemination of plays by professional theatre artists and organizations. The artifacts,
    such costumes, props, sets and scripts, may be the object of a public exhibit. """

    producer = models.CharField(max_length=100, null=True, blank=True, help_text="The name of the producer of the work")
    venue = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                             help_text="The venue in which the exhibition was given")
    first_performance_date = models.DateField(null=True, blank=True,
                                              help_text="The date the work was first performed or exhibited")

    artistic_contribution = models.ForeignKey(ArtisticContribution, on_delete=models.CASCADE)


class VideoRecording(ArtisticContributionAbstract):
    """Works such as film, video, or new media developed as a result of an artistic practice. May serve for
    commercial purposes """

    director = models.CharField(max_length=100, null=True, blank=True, help_text="The name of the director")
    producer = models.CharField(max_length=100, null=True, blank=True, help_text="The name of the producer")
    distributor = models.CharField(max_length=100, null=True, blank=True, help_text="The name of the producer")
    release_date = models.DateField(null=True, blank=True, help_text="The date of initial release of the recording")

    artistic_contribution = models.ForeignKey(ArtisticContribution, on_delete=models.CASCADE)


class VisualArtwork(ArtisticContributionAbstract):
    """Works such as film, video, or new media developed as a result of an artistic practice. May serve for
    commercial purposes """

    publication_date = models.DateField(null=True, blank=True, help_text="Date that the work was published")

    artistic_contribution = models.ForeignKey(ArtisticContribution, on_delete=models.CASCADE)


class SoundDesign(ArtisticContributionAbstract):
    """Art and process of manipulating audio elements to achieve a desired effect. It is employed in a variety of
    disciplines including film, theatre, music recording, and live music performance. It involves the manipulation of
    previously composed audio or the creative composition of new audio. """

    writer = models.CharField(max_length=100, null=True, blank=True, help_text="The writer of the show")
    producer = models.CharField(max_length=100, null=True, blank=True, help_text="The producer of the show")
    venue = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                             help_text="The venue in which the exhibition was given")
    opening_date = models.DateField(null=True, blank=True, help_text="The date of the opening of the performance")


class SetDesign(ArtisticContributionAbstract):
    """Creations of theatrical, as well as film or television scenery (also known as stage design, scenic design or
    production design) """

    writer = models.CharField(max_length=100, null=True, blank=True, help_text="The writer of the show")
    producer = models.CharField(max_length=100, null=True, blank=True, help_text="The producer of the show")
    venue = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                             help_text="The venue in which the exhibition was given")
    opening_date = models.DateField(null=True, blank=True, help_text="The date of the opening of the performance")


class LightDesign(ArtisticContributionAbstract):
    """Work done within theatre or in relation to an art installation to design a production"""

    writer = models.CharField(max_length=100, blank=True, null=True, help_text="The writer of the show")
    producer = models.CharField(max_length=100, blank=True, null=True, help_text="The producer of the show")
    venue = models.CharField(max_length=100, blank=True, null=True, help_text="The venue in which the performance was "
                                                                              "given")
    opening_date = models.DateField(null=True, blank=True, help_text="The date of the opening of the performance")

    artistic_contribution = models.ForeignKey(ArtisticContribution, on_delete=models.CASCADE)


class Choreography(ArtisticContributionAbstract):
    """Dance compositions created for production and dissemination"""

    composer = models.CharField(max_length=100, null=True, blank=True,
                                help_text="The name of the composer of the music")
    company = models.CharField(max_length=250, null=True, blank=True,
                               help_text="The name of the performing dance company")
    premiere_date = models.DateField(null=True, blank=True, help_text="The date of the opening of the performance")
    media_release_date = models.DateField(null=True, blank=True,
                                          help_text="The date the performance was released to the media")
    principal_dancers = models.CharField(max_length=200, null=True, blank=True,
                                         help_text="The names of the principal dancers")

    artistic_contribution = models.ForeignKey(ArtisticContribution, on_delete=models.CASCADE)


class MajorPerformanceDate(Base):
    """The dates that subsequent performances were given"""

    date = models.DateField(null=True, blank=True, help_text="The date that performance was given")

    choreography = models.ForeignKey(Choreography, on_delete=models.CASCADE)


class MuseumExhibition(ArtisticContributionAbstract):
    """Exhibits under the guidance of a curator responsible for a collection"""

    venue = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                             help_text="The venue in which the exhibition was given")
    start_date = models.DateField(null=True, blank=True, help_text="The date of the opening of the exhibition")
    end_date = models.DateField(null=True, blank=True, help_text="The date of the closing of the exhibition")
    catalogue_title = models.CharField(max_length=250, null=True, blank=True,
                                       help_text="The title of the catalogue created for the exhibition")

    artistic_contribution = models.ForeignKey(ArtisticContribution, on_delete=models.CASCADE)


class PerformanceArt(ArtisticContributionAbstract):
    """Avant-garde or conceptual pieces of music, song, dance or theatre performed for an audience. It may be
    scripted or improvisational """

    venue = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                             help_text="The venue in which the performance was given")

    artistic_contribution = models.ForeignKey(ArtisticContribution, on_delete=models.CASCADE)


class PerformanceDate(Base):
    """The dates that major performances were given"""

    date = models.DateField(null=True, blank=True, help_text="The date of a major performance")

    performance_art = models.ForeignKey(PerformanceArt, on_delete=models.CASCADE)


class Poetry(ArtisticContributionAbstract):
    """Poetry collections and performances"""

    venue = models.CharField(max_length=250, null=True, blank=True,
                             help_text="The venue in which the performance or exhibition was given, if applicable")
    appeared_in = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                   help_text="The name of the publication in which the work appeared, if applicable")
    volume = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                              help_text="The volume, if applicable")
    issue = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                             help_text="The issue, if applicable")
    page_range = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                  help_text="The page range with a dash ('-') as separator (e.g. 234-256), if applicable")
    date = models.DateField(null=True, blank=True, help_text="The date of first presentation/production")
    publisher = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                 help_text="The name of the publisher, if applicable")
    country = models.CharField(max_length=50, null=True, blank=True,
                               help_text="The country of the publication/performance")
    authors = models.CharField(max_length=200, null=True, blank=True, help_text="")
    editors = models.CharField(max_length=200, null=True, blank=True, help_text="")

    artistic_contribution = models.ForeignKey(ArtisticContribution, on_delete=models.CASCADE)


class OtherArtisticContribution(ArtisticContributionAbstract):
    """Artistic or performance contributions that cannot be classified under the preceeding subsections which results
    from, or is related to, the person's """

    date = models.DateField(null=True, blank=True, help_text="The date of first presentation/production")
    venue = models.CharField(max_length=200, null=True, blank=True,
                             help_text="The venue in which the performance or exhibition was given, if applicable")

    artistic_contribution = models.ForeignKey(ArtisticContribution, on_delete=models.CASCADE)


class IntellectualProperty(Base):
    """Collection of information records that, in combination, represent a full and up-to-date history of the
    intellectual property owned by the person and resulting from, or related to, the person's research activities. """

    contribution = models.OneToOneField(Contribution, on_delete=models.CASCADE)


class IntellectualPropertyAbstract(ContributionAbstract):
    """It contains the fields which are common in Patent, License, Disclosure, RegisteredCopyright & Trademark"""

    title = models.CharField(max_length=250, null=True, blank=True, help_text="The name of the patent")
    filing_date = models.DateField(null=True, blank=True, help_text="The year patent was issued")
    date_issued = models.DateField(null=True, blank=True, help_text="The date the license was issued")
    end_date = models.DateField(null=True, blank=True, help_text="The date of expiry of the license")
    contribution_or_impact = models.CharField(max_length=1000, null=True, blank=True,
                                              help_text="Provide a concise description of this contribution and its "
                                                        "value to and impact on the area of research for which you are applying "
                                                        "for funding")
    url = models.URLField(max_length=100, null=True, blank=True,
                          help_text="The name of an associated website, if applicable")

    class Meta:
        abstract = True


class Patent(IntellectualPropertyAbstract):
    """A form of IP protection that defines the exclusive right by law for inventors and assignees to make use of and
    exploit their inventions, products or processes, for a limited period of time """

    STATUS_CHOICES = (
        ('Allowed', 'Allowed'),
        ('Expired', 'Expired'),
        ('Granted/Issued', 'Granted/Issued'),
        ('Lapsed', 'Lapsed'),
        ('Pending', 'Pending'),
        ('Withdrawn', 'Withdrawn')
    )

    number = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                              help_text="The number of the patent")
    location = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                help_text="The country in which the patent resides")
    status = models.CharField(max_length=20, null=True, blank=True, choices=STATUS_CHOICES,
                              help_text="Status of the patent")
    inventors = models.CharField(max_length=1000, null=True, blank=True, help_text="")

    intellectual_property = models.ForeignKey(IntellectualProperty, on_delete=models.CASCADE)


class License(IntellectualPropertyAbstract):
    """Signed agreements to exploit a piece of IP such as a process, product, data, or software"""

    STATUS_CHOICES = (
        ('Granted', 'Granted'),
        ('In Negotiation', 'In Negotiation')
    )

    status = models.CharField(max_length=20, null=True, blank=True, choices=STATUS_CHOICES,
                              help_text="The status of the license application")

    intellectual_property = models.ForeignKey(IntellectualProperty, on_delete=models.CASCADE)


class Disclosure(IntellectualPropertyAbstract):
    """Publications that establish inventions as prior art thereby preventing others from patenting the same
    invention or concept """

    STATUS_CHOICES = (
        ('Disclosed', 'Disclosed'),
        ('Protected', 'Protected')
    )

    status = models.CharField(max_length=20, null=True, blank=True, help_text="Status of the disclosure application")

    intellectual_property = models.ForeignKey(IntellectualProperty, on_delete=models.CASCADE)


class RegisteredCopyright(IntellectualPropertyAbstract):
    """Registered ownership of rights under a system of laws for promoting both the creation of and access to
    artistic, literary, musical, dramatic and other creative works """

    STATUS_CHOICES = (
        ('Expunged', 'Expunged'),
        ('First Fixation', 'First Fixation'),
        ('Registered', 'Registered')
    )

    status = models.CharField(max_length=20, null=True, blank=True, help_text="status of the copyright registration")

    intellectual_property = models.ForeignKey(IntellectualProperty, on_delete=models.CASCADE)


class Trademark(IntellectualPropertyAbstract):
    """Marks such as a name, word, phrase, logo, symbol, design, image of a product or service that indicates the
    source and provides the right to control the use of the identifier """

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Registered', 'Registered')
    )

    status = models.CharField(max_length=20, null=True, blank=True, help_text="Status of the trademark registration")

    intellectual_property = models.ForeignKey(IntellectualProperty, on_delete=models.CASCADE)


class ResearchDiscipline(Base):
    """The research discipline is a field of knowledge which is taught at the university level and where it is
    institutionalized as a unit, like a department or a faculty. It can describe both the training of the researcher
    and the research projects. """

    discipline = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    sector_of_discipline = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    field = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    order = models.IntegerField(null=True, blank=True,
                                help_text="This field is used to order the entries. A value of 1 will show up at top.")

    degree = models.ForeignKey(Degree, null=True, blank=True, on_delete=models.CASCADE)
    credential = models.ForeignKey(Credential, null=True, blank=True, on_delete=models.CASCADE)
    recognition = models.ForeignKey(Recognition, null=True, blank=True, on_delete=models.CASCADE)
    research_funding_history = models.ForeignKey(ResearchFundingHistory, null=True, blank=True,
                                                 on_delete=models.CASCADE)
    academic_work_experience = models.ForeignKey(AcademicWorkExperience, null=True, blank=True,
                                                 on_delete=models.CASCADE)
    non_academic_work_experience = models.ForeignKey(NonAcademicWorkExperience, null=True, blank=True,
                                                     on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, null=True, blank=True,
                                     on_delete=models.CASCADE)
    research_funding_assessment_activity = models.ForeignKey(ResearchFundingApplicationAssessmentActivity,
                                                             null=True, blank=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.order = parse_integer(self.order)
        super().save(*args, **kwargs)


class AreaOfResearch(Base):
    """The area of research is the natural, technological or social phenomenon which attracts the attention and
    interests of the scientific community. The area of research is sometimes a specialty within a research discipline
    or the meeting ground of several research disciplines. """

    area = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    sector = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    field = models.CharField(max_length=NAME_LENGTH_MAX, null=True, blank=True)
    subfield = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    order = models.IntegerField(null=True, blank=True,
                                help_text="This field is used to order the entries. A value of 1 will show up at top.")

    degree = models.ForeignKey(Degree, null=True, blank=True, on_delete=models.CASCADE)
    credential = models.ForeignKey(Credential, null=True, blank=True, on_delete=models.CASCADE)
    recognition = models.ForeignKey(Recognition, null=True, blank=True, on_delete=models.CASCADE)
    research_funding_history = models.ForeignKey(ResearchFundingHistory, null=True, blank=True,
                                                 on_delete=models.CASCADE)
    academic_work_experience = models.ForeignKey(AcademicWorkExperience, null=True, blank=True,
                                                 on_delete=models.CASCADE)
    non_academic_work_experience = models.ForeignKey(NonAcademicWorkExperience, null=True, blank=True,
                                                     on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, null=True, blank=True,
                                     on_delete=models.CASCADE)
    research_funding_assessment_activity = models.ForeignKey(ResearchFundingApplicationAssessmentActivity,
                                                             null=True, blank=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.order = parse_integer(self.order)
        super().save(*args, **kwargs)


class FieldOfApplication(Base):
    """The field of application is the scientific, social, economic, cultural, or political area where the research
    can be applied, most of the time to help resolve a problem. """

    field = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    subfield = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    order = models.IntegerField(null=True, blank=True,
                                help_text="This field is used to order the entries. A value of 1 will show up at top.")

    degree = models.ForeignKey(Degree, null=True, blank=True, on_delete=models.CASCADE)
    credential = models.ForeignKey(Credential, null=True, blank=True, on_delete=models.CASCADE)
    recognition = models.ForeignKey(Recognition, null=True, blank=True, on_delete=models.CASCADE)
    research_funding_history = models.ForeignKey(ResearchFundingHistory, null=True, blank=True,
                                                 on_delete=models.CASCADE)
    academic_work_experience = models.ForeignKey(AcademicWorkExperience, null=True, blank=True,
                                                 on_delete=models.CASCADE)
    non_academic_work_experience = models.ForeignKey(NonAcademicWorkExperience, null=True, blank=True,
                                                     on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, null=True, blank=True,
                                     on_delete=models.CASCADE)
    research_funding_assessment_activity = models.ForeignKey(ResearchFundingApplicationAssessmentActivity,
                                                             null=True, blank=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.order = parse_integer(self.order)
        super().save(*args, **kwargs)
