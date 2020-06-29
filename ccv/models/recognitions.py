from django.db import models

from .activity import ResearchFundingApplicationAssessmentActivity
from .base import Base, CanadianCommonCv, Organization, OtherOrganization
from .education import Credential, Degree
from .employment import AcademicWorkExperience, NonAcademicWorkExperience
from .user_profile import UserProfile
from ..constants.db_constants import DEFAULT_COLUMN_LENGTH, NAME_LENGTH_MAX
from ..utils import parse_integer


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

    ccv = models.ForeignKey(CanadianCommonCv, on_delete=models.CASCADE)


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

    organization = models.CharField(max_length=100, null=True, blank=True,
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

    role = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
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


class MostSignificantContribution(Base):
    """Information regarding your most significant contributions as they relate to the application"""

    title = models.CharField(max_length=250, null=True, blank=True,
                             help_text="A title, name, or short description of the contribution")
    contribution_date = models.DateField(null=True, blank=True,
                                         help_text="The key date associated with this contribution (e.g. publication "
                                                   "date, activity start date, etc.)")
    description = models.CharField(max_length=1000, null=True, blank=True,
                                   help_text="Provide a concise description of this contribution, its value to the "
                                             "area of research fr which u are applying for funding & potential impact")

    ccv = models.ForeignKey(CanadianCommonCv, on_delete=models.CASCADE)


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
