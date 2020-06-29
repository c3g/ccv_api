from django.db import models
from .base import Base, CanadianCommonCv, Organization, OtherOrganization
from ..constants.db_constants import NAME_LENGTH_MAX


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
