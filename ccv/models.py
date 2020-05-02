# -*- coding: utf-8 -*-

from django.db import models
from .constants.db_constants import DEFAULT_COLUMN_LENGTH, NAME_LENGTH_MAX
from .utils import normalize_string
from django.contrib.postgres.fields import ArrayField
from djangoyearlessdate.models import YearlessDateField


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

    class Meta:
        db_table = "organization"


class OtherOrganization(Base):
    type = models.CharField(max_length=20, null=True, blank=True,
                            help_text="The type of organization, only if Other Organization is entered")
    name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                            help_text="The organization's name, only if not in Organization list")

    class Meta:
        db_table = "other_organization"


class PersonalInformation(Base):
    """Information about the person that facilitates identification, including name, date of birth, and sex"""

    class Meta:
        db_table = "personal_information"


class Identification(Base):
    """Collections of information records that, in combination, present an overall personal identification of person."""
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
    date_of_birth = YearlessDateField()
    sex = models.CharField(max_length=20, choices=SEX_CHOICES, null=True, blank=True)
    designated_group = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, choices=DESIGNATED_GROUP_CHOICES, null=True,
                                        blank=True, help_text="Group designated by the Employment Equity Act of Canada")
    correspondence_language = models.CharField(max_length=10, choices=CORRESPONDENCE_LANGUAGE_CHOICES)
    canadian_residency_status = models.CharField(max_length=DEFAULT_COLUMN_LENGTH,
                                                 choices=CANADIAN_RESIDENCY_STATUS_CHOICES, null=True, blank=True)
    permanent_residency = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, choices=PERMANENT_RESIDENCY_CHOICES,
                                           null=True, blank=True)
    permanent_residency_start_date = models.DateField(null=True, blank=True)

    personal_information = models.OneToOneField(PersonalInformation, on_delete=models.CASCADE)

    class Meta:
        db_table = "identification"


class CountryOfCitizenship(Base):
    name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                            help_text="List all countries that the person is a citizen of")

    identification = models.ForeignKey(Identification, on_delete=models.CASCADE)

    class Meta:
        db_table = "country_of_citizenship"


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

    personal_information = models.ForeignKey(PersonalInformation, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "language_skill"


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

    personal_information = models.ForeignKey(PersonalInformation, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "address"


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

    personal_information = models.ForeignKey(PersonalInformation, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "telephone"


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

    personal_information = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)

    class Meta:
        db_table = "email"


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
    url = models.CharField(max_length=100, null=True, blank=True, help_text="The person's web address")

    personal_information = models.ForeignKey(PersonalInformation, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "website"


class Education(Base):
    """Collection of information records that, in combination, represent the full and up-to-date history of the
    person's education """

    class Meta:
        db_table = "education"


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
    thesis_title = models.TextField(max_length=500, null=True, blank=True,
                                    help_text="itle of the person’s thesis project")
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
    other_organization = models.OneToOneField(OtherOrganization, on_delete=models.CASCADE, null=True, blank=True,)

    education = models.ForeignKey(Education, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "degree"


class Supervisor(Base):
    """The persons responsible for mentoring, advising and guiding the student academically throughout this degree
    program """

    name = models.CharField(max_length=NAME_LENGTH_MAX, null=True)
    start_date = models.DateField(null=True, blank=True, help_text="The date when the supervision started")
    end_date = models.DateField(null=True, blank=True, help_text="The date when the supervision ended")

    degree = models.ForeignKey(Degree, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "supervisor"


class Credential(Base):
    """A designation earned to assure qualification to perform a job or task such as a certification,
    an accreditation, a designation, etc. """

    title = models.TextField(max_length=250, null=True, blank=True,
                             help_text="The name or title of the designation earned")
    effective_date = models.DateField(null=True, blank=True, help_text="The date the designation was received")
    end_date = models.DateField(null=True, blank=True, help_text="The date the designation expires, if applicable")
    description = models.TextField(max_length=1000, null=True, blank=True,
                                   help_text="A description of the person's designation")

    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, null=True, blank=True,
                                        help_text="The organization that conferred this credential")
    other_organization = models.OneToOneField(OtherOrganization, on_delete=models.CASCADE, null=True, blank=True)

    education = models.ForeignKey(Education, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "credential"


class Recognition(Base):
    """Recognitions are any acknowledgments, appreciations and monetary rewards that were obtained and which were not"""
    TYPE_CHOICES = (
        ('Citation', 'Citation'),
        ('Distinction', 'Distinction'),
        ('Honor', 'Honor'),
        ('Prize / Award', 'Prize / Award')
    )

    type = models.CharField(max_length=20, choices=TYPE_CHOICES, null=True, blank=True)
    name = models.TextField(max_length=250, null=True, blank=True, help_text="The name or title of the recognition")
    effective_date = models.DateField(null=True, blank=True, help_text="The date when the recognition was awarded")
    end_date = models.DateField(null=True, blank=True, help_text="The date when this recognition expires")
    amount = models.IntegerField(null=True, blank=True, help_text="The amount that was awarded for this recognition")
    amount_in_canadian_dollar = models.IntegerField(null=True, blank=True, help_text="Amount in CAN $")
    currency = models.CharField(max_length=50, null=True, blank=True,
                                help_text="The currency in which the money was awarded")

    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, null=True, blank=True,
                                        help_text="The organization that gave the recognition")
    other_organization = models.OneToOneField(OtherOrganization, on_delete=models.CASCADE, null=True, blank=True,)

    def save(self, *args, **kwargs):
        # TODO: Add amount conversion logic in CAN $
        super().save(*args, **kwargs)

    class Meta:
        db_table = "recognition"


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
    key_theory = models.TextField(max_length=500, null=True, blank=True, help_text="The key theories and "
                                                                                   "methodologies used in research")
    research_interest = models.TextField(max_length=1000, null=True, blank=True)
    experience_summary = models.TextField(max_length=1000, null=True, blank=True,
                                          help_text="summary of research experience")
    country = ArrayField(models.CharField(max_length=DEFAULT_COLUMN_LENGTH), null=True, blank=True, default=list)

    class Meta:
        db_table = "user_profile"


class ResearchSpecializationKeyword(Base):
    """Keywords that best correspond to the person's expertise in research, creation, instrumentation and techniques"""

    keyword = models.CharField(max_length=50, null=True, blank=True)

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = "research_specialization_keyword"


class ResearchCentre(Base):
    """The research centres where most of the person's research is done."""

    name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    country = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    subdivision = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = "research_centre"


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

    class Meta:
        db_table = "technological_application"


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

    class Meta:
        db_table = "discipline_trained_in"


class TemporalPeriod(Base):
    """Indicate and rank the historical periods covered by your research interests, with #1 the most relevant."""

    YEAR_PERIOD_CHOICES = (
        ('AD', 'AD'),
        ('BC', 'BC')
    )

    from_year = models.IntegerField(max_length=4, null=True, blank=True,
                                    help_text="The starting year of the temporal period")
    from_year_period = models.CharField(max_length=2, null=True, blank=True, choices=YEAR_PERIOD_CHOICES,
                                        help_text="The period of the starting year")
    to_year = models.IntegerField(max_length=4, null=True, blank=True,
                                  help_text="The end year of the temporal period")
    to_year_period = models.CharField(max_length=2, null=True, blank=True, choices=YEAR_PERIOD_CHOICES,
                                      help_text="The period of the ending year")

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = "temporal_period"


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

    class Meta:
        db_table = "geographical_region"


class Employment(Base):
    """Collection of information records that, in combination, represent the full and up-to-date history of the
    person's employment """

    class Meta:
        db_table = "employment"


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
    position_title = models.TextField(max_length=250, null=True, blank=True,
                                      help_text="The person's position at the institution")
    position_status = models.CharField(max_length=20, null=True, blank=True, choices=POSITION_STATUS_CHOICES,
                                       help_text="The status of the position with regard to tenure")
    academic_rank = models.CharField(max_length=20, null=True, blank=True, choices=ACADEMIC_RANK_CHOICES,
                                     help_text="The rank of the faculty member in the academic institution")
    start_date = models.DateField(null=True, blank=True, help_text="The date the person started this position")
    end_date = models.DateField(null=True, blank=True, help_text="Date the person did not occupy this position anymore")
    work_description = models.TextField(max_length=1000, null=True, blank=True,
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
    other_organization = models.OneToOneField(OtherOrganization, on_delete=models.CASCADE, null=True, blank=True,)

    employment = models.ForeignKey(Employment, on_delete=models.CASCADE)

    class Meta:
        db_table = "academic_work_experience"


class NonAcademicWorkExperience(Base):
    """Employment in a non-academic environment"""

    POSITION_STATUS_CHOICES = (
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time')
    )

    position_title = models.TextField(max_length=250, null=True, blank=True,
                                      help_text="The position of the person with the employer")
    position_status = models.CharField(max_length=10, null=True, blank=True, choices=POSITION_STATUS_CHOICES,
                                       help_text="The nature of the person's position")
    start_date = models.DateField(null=True, blank=True, help_text="The date the position started")
    end_date = models.DateField(null=True, blank=True, help_text="The date the position ended")
    work_description = models.CharField(max_length=1000, null=True, blank=True,
                                        help_text="The responsibilities and duties associated with this position")
    unit_division = models.CharField(max_length=100, null=True, blank=True,
                                     help_text="The department within the given company or organization")

    organization = models.OneToOneField(Organization, null=True, blank=True, on_delete=models.DO_NOTHING,
                                        help_text="The name of the organization where the person worked")
    other_organization = models.OneToOneField(OtherOrganization, on_delete=models.DO_NOTHING)
    employment = models.ForeignKey(Employment, on_delete=models.CASCADE)

    class Meta:
        db_table = "non_academic_work_experience"


class Affiliation(Base):
    """Organizations with which the person is affiliated. These can be work or non-work related."""

    position_title = models.TextField(max_length=250, null=True, blank=True,
                                      help_text="The name or title of the position")
    department = models.CharField(max_length=100, null=True, blank=True,
                                  help_text="The department within the given organization")
    activity_description = models.CharField(max_length=1000, null=True, blank=True,
                                            help_text="A description of the person's activities with this organization")
    start_date = models.DateField(null=True, blank=True,
                                  help_text="The date when the persone became affiliated with this organization")
    end_date = models.DateField(null=True, blank=True,
                                help_text="The date when the person's affiliation with this organization ended")

    organization = models.OneToOneField(Organization, null=True, blank=True, on_delete=models.DO_NOTHING,
                                        help_text="The organization with which the person is affiliated.")
    other_organization = models.OneToOneField(OtherOrganization, null=True, blank=True, on_delete=models.DO_NOTHING)

    employment = models.ForeignKey(Employment, on_delete=models.CASCADE)

    class Meta:
        db_table = "affiliation"


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

    absence_description = models.TextField(max_length=1000, null=True, blank=True,
                                           help_text="description of the leave of absence")

    organization = models.OneToOneField(Organization, null=True, blank=True, on_delete=models.CASCADE)
    other_organization = models.OneToOneField(OtherOrganization, null=True, blank=True, on_delete=models.CASCADE)
    employment = models.ForeignKey(Employment, on_delete=models.CASCADE)

    class Meta:
        db_table = "leaves_of_absence"


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

    funding_title = models.TextField(max_length=250, null=True, blank=True,
                                     help_text="The nature of the grant received")
    grant_type = models.CharField(max_length=20, choices=GRANT_TYPE_CHOICES, null=True, blank=True)
    project_description = models.TextField(
        max_length=1000, null=True, blank=True, help_text="description of project for which funding was received")
    clinical_research_project = models.CharField(max_length=5, null=True, blank=True, choices=PROJECT_CHOICES)

    funding_status = models.CharField(
        max_length=30, choices=FUNDING_STATUS_CHOICES, null=True,
        blank=True, help_text="current status of the funding of the overall project.")

    funding_role = models.CharField(max_length=30, choices=FUNDING_ROLE_CHOICES, blank=True, null=True,
                                    help_text="Person's role in this research, as defined by the funding organization")
    research_uptake = models.TextField(max_length=1000, null=True, blank=True,
                                       help_text="strategies used to promote the uptake of your research findings.")

    class Meta:
        db_table = "research_funding_history"


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

    class Meta:
        db_table = "research_uptake_holder"


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

    class Meta:
        db_table = "research_setting"


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

    class Meta:
        db_table = "funding_source"


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

    class Meta:
        db_table = "funding_by_year"


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

    class Meta:
        db_table = "other_investigator"


class Membership(Base):
    """Services contributed as part of a group elected or appointed to perform such services but not directly related
    to the person's research activities. """

    class Meta:
        db_table = "membership"


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
    name = models.TextField(max_length=250, null=True, blank=True, help_text="The name of the committee")
    start_date = models.DateField(null=True, blank=True, help_text="The date on which membership began")
    description = models.TextField(max_length=1000, null=True, blank=True,
                                   help_text="Description of services contributed by the person as part of a committee")
    end_date = models.DateField(null=True, blank=True, help_text="The date on which membership ended, if applicable")

    organization = models.OneToOneField(Organization, null=True, blank=True, on_delete=models.DO_NOTHING,
                                        help_text="The name of the organisation of which the person is a member")
    other_organization = models.OneToOneField(OtherOrganization, null=True, blank=True, on_delete=models.DO_NOTHING)
    membership = models.ForeignKey(Membership, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "committee_membership"


class OtherMembership(Base):
    """Services contributed as part of a scholarly society or other organization to perform services not directly
    related to the person's research activities """

    role = models.CharField(max_length=20, null=True, blank=True, help_text="The person's role in this activity")
    name = models.TextField(max_length=250, null=True, blank=True, help_text="The name of the committee")
    start_date = models.DateField(null=True, blank=True, help_text="The date on which membership began")
    description = models.TextField(max_length=1000, null=True, blank=True,
                                   help_text="Description of services contributed by the person as part of a committee")
    end_date = models.DateField(null=True, blank=True, help_text="The date on which membership ended, if applicable")

    organization = models.OneToOneField(Organization, null=True, blank=True, on_delete=models.DO_NOTHING,
                                        help_text="The name of the organisation of which the person is a member")
    other_organization = models.OneToOneField(OtherOrganization, null=True, blank=True, on_delete=models.DO_NOTHING)
    membership = models.ForeignKey(Membership, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "other_membership"


class Activity(Base):
    """Services that the person contributed to"""

    class Meta:
        db_table = "activity"


class ResearchDiscipline(Base):
    """The research discipline is a field of knowledge which is taught at the university level and where it is
    institutionalized as a unit, like a department or a faculty. It can describe both the training of the researcher
    and the research projects. """

    discipline = models.CharField(max_length=50, null=True, blank=True)
    sector_of_discipline = models.CharField(max_length=50, null=True, blank=True)
    field = models.CharField(max_length=50, null=True, blank=True)

    degree = models.ForeignKey(Degree, null=True, blank=True, on_delete=models.CASCADE)
    credential = models.ForeignKey(Credential, null=True, blank=True, on_delete=models.CASCADE)
    recognition = models.ForeignKey(Recognition, null=True, blank=True, on_delete=models.CASCADE)
    research_funding_history = models.ForeignKey(ResearchFundingHistory, on_delete=models.CASCADE)
    academic_work_experience = models.ForeignKey(AcademicWorkExperience, on_delete=models.CASCADE)
    non_academic_work_experience = models.ForeignKey(NonAcademicWorkExperience, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = "research_discipline"


class AreaOfResearch(Base):
    """The area of research is the natural, technological or social phenomenon which attracts the attention and
    interests of the scientific community. The area of research is sometimes a specialty within a research discipline
    or the meeting ground of several research disciplines. """

    area = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    sector = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    field = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    subfield = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)

    degree = models.ForeignKey(Degree, null=True, blank=True, on_delete=models.CASCADE)
    credential = models.ForeignKey(Credential, null=True, blank=True, on_delete=models.CASCADE)
    recognition = models.ForeignKey(Recognition, null=True, blank=True, on_delete=models.CASCADE)
    research_funding_history = models.ForeignKey(ResearchFundingHistory, on_delete=models.CASCADE)
    academic_work_experience = models.ForeignKey(AcademicWorkExperience, on_delete=models.CASCADE)
    non_academic_work_experience = models.ForeignKey(NonAcademicWorkExperience, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = "area_of_research"


class FieldOfApplication(Base):
    """The field of application is the scientific, social, economic, cultural, or political area where the research
    can be applied, most of the time to help resolve a problem. """

    field = models.CharField(max_length=50, null=True, blank=True)
    subfield = models.CharField(max_length=50, null=True, blank=True)

    degree = models.ForeignKey(Degree, null=True, blank=True, on_delete=models.CASCADE)
    credential = models.ForeignKey(Credential, null=True, blank=True, on_delete=models.CASCADE)
    recognition = models.ForeignKey(Recognition, null=True, blank=True, on_delete=models.CASCADE)
    research_funding_history = models.ForeignKey(ResearchFundingHistory, on_delete=models.CASCADE)
    academic_work_experience = models.ForeignKey(AcademicWorkExperience, on_delete=models.CASCADE)
    non_academic_work_experience = models.ForeignKey(NonAcademicWorkExperience, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = "field_of_application"
