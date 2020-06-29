from django.db import models

from .base import Base, CanadianCommonCv
from ..constants.db_constants import DEFAULT_COLUMN_LENGTH
from ..utils import parse_integer


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


class UserProfileAbstract(Base):
    """"""

    order = models.IntegerField(null=True, blank=True,
                                help_text="This field is used to order the entries. A value of 1 will show up at top.")

    class Meta:
        abstract = True


class ResearchSpecializationKeyword(UserProfileAbstract):
    """Keywords that best correspond to the person's expertise in research, creation, instrumentation and techniques"""

    keyword = models.CharField(max_length=50, null=True, blank=True)

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.order = parse_integer(self.order)
        super().save(*args, **kwargs)


class ResearchCentre(UserProfileAbstract):
    """The research centres where most of the person's research is done."""

    name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    country = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    subdivision = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class TechnologicalApplication(UserProfileAbstract):
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


class DisciplineTrainedIn(UserProfileAbstract):
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


class TemporalPeriod(UserProfileAbstract):
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


class GeographicalRegion(UserProfileAbstract):
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
