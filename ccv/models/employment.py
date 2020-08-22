from django.db import models
from .base import Base, CanadianCommonCv, Organization, OtherOrganization
from ..constants.db_constants import DEFAULT_COLUMN_LENGTH


class Employment(Base):
    """Collection of information records that, in combination, represent the full and up-to-date history of the
    person's employment """

    ccv = models.OneToOneField(CanadianCommonCv, on_delete=models.CASCADE, related_name='employment')


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

    employment = models.ForeignKey(Employment, on_delete=models.CASCADE, related_name='academic_work_experience')


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
    other_organization = models.OneToOneField(OtherOrganization, on_delete=models.CASCADE, null=True, blank=True)
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
