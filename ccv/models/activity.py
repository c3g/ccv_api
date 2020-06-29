from django.db import models
from .base import Base, CanadianCommonCv, Organization, OtherOrganization
from ..constants.db_constants import DEFAULT_COLUMN_LENGTH, NAME_LENGTH_MAX


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
