from django.db import models
from .base import Base, CanadianCommonCv, Organization, OtherOrganization
from ..constants.db_constants import DEFAULT_COLUMN_LENGTH


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

    def __str__(self):
        return f"{self.organisation} - {self.reference_number}"


class ContributionAbstract(Base):

    funding_source = models.ManyToManyField(ContributionFundingSource, related_name="%(app_label)s_%(class)s_related",
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


class InterviewAndMediaRelation(ContributionAbstract):
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


class BroadcastInterview(InterviewAndMediaRelation):
    """Services contributed in the form of interview(s) with the person with a member of the broadcast (TV or radio)
    media. """

    program = models.CharField(max_length=250, null=True, blank=True, help_text="")
    network = models.CharField(max_length=250, null=True, blank=True, help_text="")
    first_broadcast_date = models.DateField(null=True, blank=True,
                                            help_text="The date on which the interview was first aired")
    end_date = models.DateField(null=True, blank=True,
                                help_text="The date on which the broadcast of the interview ended")

    contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE)


class TextInterview(InterviewAndMediaRelation):
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
                                           help_text="brief description of contribution role towards this publication")

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

    STATUS_CHOICES = (
        ('Accepted', 'Accepted'),
        ('In Press', 'In Press'),
        ('Published', 'Published'),
        ('Revision Requested', 'Revision Requested'),
        ('Submitted', 'Submitted')
    )

    journal = models.CharField(max_length=200, null=True, blank=True,
                               help_text="Name of the journal in which the article is published, or to be published")
    volume = models.CharField(max_length=20, null=True, blank=True, help_text="The volume number of the journal")
    issue = models.CharField(max_length=10, null=True, blank=True, help_text="The volume number of the journal")
    page_range = models.CharField(max_length=20, null=True, blank=True,
                                  help_text="The page range with a dash ('-') as separator (e.g. 234-256)")
    publishing_status = models.CharField(max_length=30, choices=STATUS_CHOICES, null=True, blank=True,
                                         help_text="The status of the article with regard to journal")
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
                                       help_text="contextualization and integration of research findings of "
                                                 "individual research studies within the larger body of knowledge on "
                                                 "the topic")

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
                                         help_text="The name of the gallery or publisher for which the catalogue was "
                                                   "created")
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
    publisher = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                                 help_text="The publisher of the composition")
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

    artistic_contribution = models.ForeignKey(ArtisticContribution, on_delete=models.CASCADE)


class SetDesign(ArtisticContributionAbstract):
    """Creations of theatrical, as well as film or television scenery (also known as stage design, scenic design or
    production design) """

    writer = models.CharField(max_length=100, null=True, blank=True, help_text="The writer of the show")
    producer = models.CharField(max_length=100, null=True, blank=True, help_text="The producer of the show")
    venue = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                             help_text="The venue in which the exhibition was given")
    opening_date = models.DateField(null=True, blank=True, help_text="The date of the opening of the performance")

    artistic_contribution = models.ForeignKey(ArtisticContribution, on_delete=models.CASCADE)


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
                                  help_text="The page range with a dash ('-') as separator (e.g. 234-256), "
                                            "if applicable")
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
                                                        "value to and impact on the area of research for which you "
                                                        "are applying "
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
