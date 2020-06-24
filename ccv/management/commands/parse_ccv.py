# -*- coding: utf-8 -*-

import datetime
import xml.etree.ElementTree as ET

from django.core.management.base import BaseCommand, CommandError

from ccv.models import CanadianCommonCv, Identification, CountryOfCitizenship, LanguageSkill, Address, Website, \
    Telephone, Email, Education, Degree, Supervisor, Credential, Recognition, ResearchCentre, UserProfile, \
    ResearchSpecializationKeyword, ResearchCentre, TechnologicalApplication, DisciplineTrainedIn, TemporalPeriod, \
    GeographicalRegion, Employment, AcademicWorkExperience, NonAcademicWorkExperience, Affiliation, LeavesOfAbsence, \
    ResearchFundingHistory, ResearchUptakeHolder, ResearchSetting, FundingSource, FundingByYear, OtherInvestigator, \
    Membership, CommitteeMembership, OtherMembership, ResearchDiscipline, FieldOfApplication, AreaOfResearch, \
    MostSignificantContribution, Organization, OtherOrganization, Contribution, Presentation, ConferencePublication, \
    ContributionFundingSource, BroadcastInterview, TextInterview, Publication, Journal, Book, BookReview, BookChapter, \
    Translation, ThesisDissertation, SupervisedStudentPublication, Litigation, NewspaperArticle, EncyclopediaEntry, \
    MagazineEntry, DictionaryEntry, Report, WorkingPaper, Manual, OnlineResource, Test, ClinicalCareGuideline

from ccv.utils import etree_to_dict, parse_integer


class Command(BaseCommand):
    help = ''
    final_data = {}

    def add_arguments(self, parser):
        parser.add_argument('ccv_xml_filepath', type=str)

    def get_fields(self, fields: list) -> dict:
        """
        Function to resolve fields
        :param fields:
        :return:
        """
        all_fields = {}
        for field in fields:
            if 'lov' in field and 'text' in field.get('lov'):
                all_fields[field.get('label')] = field.get('lov').get('text')
            elif 'value' in field and 'text' in field.get('value'):
                all_fields[field.get('label')] = field.get('value').get('text')
            elif 'refTable' in field:
                all_fields[field.get('label')] = {
                    field.get('refTable').get('label'): {i['label']: i['value'] for i in
                                                         field['refTable']['linkedWith']}}
            else:
                all_fields[field.get('label')] = ''
        return all_fields

    def get_response(self, section: dict) -> dict:
        """
        Recursive function handle the nested structure
        :param section:
        :return:
        """

        label = section.get('label')
        if label is None:
            label = 'ccv'
        resp = {label: {}}

        if 'field' in section:
            if not isinstance(section.get('field'), list):
                section['field'] = [section.get('field')]
            resp[label] = self.get_fields(section['field'])

        if 'section' in section:
            if not isinstance(section.get('section'), list):
                section['section'] = [section.get('section')]

            for sec in section['section']:
                res = self.get_response(sec)
                if sec['label'] not in resp[label]:
                    resp[label][sec['label']] = []
                resp[label][sec['label']].append(res[sec['label']])

        return resp

    def parse_boolean(self, value: str) -> bool:
        """
        :param value:
        :return:
        """
        return True if value == "Yes" else False

    def parse_datetime(self, date, format: str):
        """
        :param date:
        :param format:
        :return:
        """
        return datetime.datetime.strptime(date, format) if date else None

    def save_organization(self, organization: dict):
        """
        :param organization:
        :return:
        """

        if not isinstance(organization, dict):
            return None

        organization_obj = Organization(
            country=organization.get("Country"),
            subdivision=organization.get("Subdivision"),
            type=organization.get("Organization Type"),
            name=organization.get("Organization")
        )
        organization_obj.save()

        return organization_obj

    def save_other_organization(self, type, name):

        if not type or not name:
            return None

        other_org_obj = OtherOrganization(
            type=type,
            name=name
        )
        other_org_obj.save()

        return other_org_obj

    def save_research_funding_history(self, research_histories: list) -> bool:
        """
        :param research_histories:
        :return:
        """

        if isinstance(research_histories, list) and len(research_histories) == 0:
            return False

        for research_history in research_histories:

            research_history_obj = ResearchFundingHistory(
                funding_type=research_history.get('Funding Type'),
                start_date=self.parse_datetime(research_history.get('Funding Start Date'), '%Y/%m'),
                end_date=self.parse_datetime(research_history.get('Funding End Date'), '%Y/%m'),
                funding_title=research_history.get('Funding Title'),
                grant_type=research_history.get('Grant Type'),
                project_description=research_history.get('Project Description'),
                clinical_research_project=research_history.get('Clinical Research Project?'),
                funding_status=research_history.get('Funding Status'),
                funding_role=research_history.get('Funding Role'),
                research_uptake=research_history.get('Research Uptake'),
                ccv=self.ccv
            )
            research_history_obj.save()

            for stakeholder in research_history.get('Research Uptake Stakeholders', []):

                ResearchUptakeHolder(
                    stakeholder=stakeholder.get('Stakeholder'),
                    research_funding_history=research_history_obj
                ).save()

            for research_setting in research_history.get('Research Settings', []):

                ResearchSetting(
                    country=research_setting.get('Location', {}).get('Country-Subdivision', {}).get('Country'),
                    subdivision=research_setting.get('Location', {}).get('Country-Subdivision', {}).get('Subdivision'),
                    setting_type=research_setting.get('Setting Type'),
                    research_funding_history=research_history_obj
                ).save()

            for funding_source in research_history.get('Funding Sources', []):

                FundingSource(
                    organization=funding_source.get('Funding Organization'),
                    other_organization=funding_source.get('Other Funding Organization'),
                    program_name=funding_source.get('Program Name'),
                    reference_no=funding_source.get('Funding Reference Number'),
                    total_funding=parse_integer(funding_source.get('Total Funding')),
                    total_funding_currency=funding_source.get('Currency of Total Funding"'),
                    funding_received=parse_integer(funding_source.get('Portion of Funding Received')),
                    funding_received_currency=funding_source.get('Currency of Portion of Funding Received'),
                    renewable=funding_source.get('Funding Renewable?'),
                    competitive=funding_source.get('Funding Competitive?'),
                    start_date=self.parse_datetime(funding_source.get('Funding Start Date'), '%Y/%m'),
                    end_date=self.parse_datetime(funding_source.get('Funding End Date'), '%Y/%m'),
                    research_funding_history=research_history_obj
                ).save()

            for funding_by_year in research_history.get('Funding by Year', []):

                FundingByYear(
                    start_date=self.parse_datetime(funding_by_year.get('Start Date'), '%Y/%m'),
                    end_date=self.parse_datetime(funding_by_year.get('End Date'), '%Y/%m'),
                    total_funding=parse_integer(funding_by_year.get('Total Funding')),
                    total_funding_currency=funding_by_year.get('Currency of Total Funding'),
                    funding_received=parse_integer(funding_by_year.get('Portion of Funding Received')),
                    funding_received_currency=funding_by_year.get('Currency of Portion of Funding Received'),
                    time_commitment=parse_integer(funding_by_year.get('Time Commitment')),
                    research_funding_history=research_history_obj
                ).save()

            for other_investigator in research_history.get('Other Investigators', []):

                OtherInvestigator(
                    name=other_investigator.get('Investigator Name'),
                    role=other_investigator.get('Role'),
                    research_funding_history=research_history_obj
                ).save()

    def save_memberships(self, memberships: list) -> bool:
        """
        :param memberships:
        :return:
        """

        if len(memberships) == 0:
            return False

        for membership in memberships:

            membership_obj = Membership(
                ccv=self.ccv
            )
            membership_obj.save()

            for committee_membership in membership.get("Committee Memberships", []):
                CommitteeMembership(
                    role=committee_membership.get('Role'),
                    name=committee_membership.get('Committee Name'),
                    start_date=self.parse_datetime(committee_membership.get('Membership Start Date'), "%Y/%m"),
                    end_date=self.parse_datetime(committee_membership.get('Membership End Date'), "%Y/%m"),
                    description=committee_membership.get('Description'),
                    membership_id=membership_obj.id
                ).save()

            for other_membership in membership.get("Other Memberships", []):
                OtherMembership(
                    role=other_membership.get('Role'),
                    start_date=self.parse_datetime(other_membership.get('Membership Start Date'), '%Y/%m'),
                    end_date=self.parse_datetime(other_membership.get('Membership End Date'), '%Y/%m'),
                    description=other_membership.get('Description'),
                    membership_id=membership_obj.id
                ).save()
        return True

    def save_most_significant_contribution(self, contributions: list) -> bool:
        """
        :param contributions:
        :return:
        """

        if isinstance(contributions, list) and len(contributions) == 0:
            return False

        for contribution in contributions:
            MostSignificantContribution(
                title=contribution.get('Title'),
                description=contribution.get('Description / Contribution Value/Impact'),
                contribution_date=self.parse_datetime(contribution.get("Contribution Date"), "%Y/%m"),
                ccv=self.ccv
            ).save()

        return True

    def save_area_of_research(self, areas: list) -> bool:
        pass

    def get_organization_obj(self, obj):

        if "Organization" in obj and \
                isinstance(obj['Organization'], dict):
            org_obj = self.save_organization(obj['Organization']['Organization'])
        else:
            org_obj = None

        return org_obj

    def save_funding_source(self, funding_sources: dict, ref_obj) -> bool:
        """
        :param funding_sources:
        :param ref_obj:
        :return:
        """

        if 'Funding Sources' not in funding_sources:
            return False

        for funding_source in funding_sources.get('Funding Sources', []):
            funding_source_obj = ContributionFundingSource(
                organisation=funding_source.get('Funding Organization'),
                other_organization=funding_source.get('Other Funding Organization'),
                reference_number=funding_source.get('Funding Reference Number')
            )
            funding_source_obj.save()
            ref_obj.funding_source.add(funding_source_obj)

        return True

    def save_contributions(self, contributions: list) -> bool:
        """
        :param contributions:
        :return:
        """

        if isinstance(contributions, list) and len(contributions) == 0:
            return False

        for contribution in contributions:

            contribution_obj = Contribution(
                ccv=self.ccv
            )
            contribution_obj.save()

            # presentation
            for presentation in contribution.get('Presentations', []):

                presentation_obj = Presentation(
                    title=presentation.get('Presentation Title'),
                    event_name=presentation.get('Conference / Event Name'),
                    location=presentation.get('Location'),
                    city=presentation.get('City'),
                    main_audience=presentation.get('Main Audience'),
                    is_invited=self.parse_boolean(presentation.get('Invited?')),
                    is_keynote=self.parse_boolean(presentation.get('Keynote?')),
                    is_competitive=self.parse_boolean(presentation.get('Competitive?')),
                    presentation_year=presentation.get('Presentation Year'),
                    description=presentation.get('Description / Contribution Value'),
                    co_presenters=presentation.get('Co-Presenters'),
                    url=presentation.get('URL'),
                    contribution=contribution_obj
                )
                presentation_obj.save()

                self.save_funding_source(presentation, presentation_obj)

            # Interview & Media Relations

            for interview_and_media_relation in contribution.get('Interviews and Media Relations', []):

                for broadcast_interview in interview_and_media_relation.get('Broadcast Interviews', []):

                    broadcast_obj = BroadcastInterview(
                        topic=broadcast_interview.get('Topic'),
                        interviewer=broadcast_interview.get('Interviewer'),
                        program=broadcast_interview.get('Program'),
                        network=broadcast_interview.get('Network'),
                        first_broadcast_date=self.parse_datetime(broadcast_interview.get('First Broadcast Date'),
                                                                 '%Y-%m-%d'),
                        end_date=self.parse_datetime(broadcast_interview.get('End Date'), '%Y-%m-%d'),
                        description=broadcast_interview.get('Description / Contribution Value'),
                        url=broadcast_interview.get('URL'),
                        contribution=contribution_obj
                    )
                    broadcast_obj.save()

                    self.save_funding_source(broadcast_interview, broadcast_obj)

                for text_interview in interview_and_media_relation.get('Text Interviews', []):

                    text_interview_obj = TextInterview(
                        topic=text_interview.get('Topic'),
                        interviewer=text_interview.get('Interviewer'),
                        forum=text_interview.get('Forum'),
                        publication_date=self.parse_datetime(text_interview.get('Publication Date'), '%Y-%m-%d'),
                        description=text_interview.get('Description / Contribution Value'),
                        url=text_interview.get('URL'),
                        contribution=contribution_obj
                    )
                    text_interview_obj.save()

                    self.save_funding_source(text_interview, text_interview_obj)

            # publications

            for publication in contribution.get('Publications', []):

                publication_obj = Publication(
                    contribution=contribution_obj
                )
                publication_obj.save()

                for journal_article in publication.get('Journal Articles', []):

                    journal_article_obj = Journal(
                        title=journal_article.get('Article Title'),
                        journal=journal_article.get('Journal'),
                        volume=journal_article.get('Volume'),
                        issue=journal_article.get('Issue'),
                        page_range=journal_article.get('Page Range'),
                        publishing_status=journal_article.get('Publishing Status'),
                        # year
                        publisher=journal_article.get('Publisher'),
                        publication_location=journal_article.get('Publication Location'),
                        contribution_value=journal_article.get('Description / Contribution Value'),
                        url=journal_article.get('URL'),
                        is_refereed=self.parse_boolean(journal_article.get('Refereed?')),
                        is_open_access=self.parse_boolean(journal_article.get('Open Access?')),
                        is_synthesis=self.parse_boolean(journal_article.get('Synthesis?')),
                        role=journal_article.get('Contribution Role'),
                        contributors_count=parse_integer(journal_article.get('Number of Contributors')),
                        authors=journal_article.get('Authors'),
                        editors=journal_article.get('Editors'),
                        doi=journal_article.get('DOI'),
                        contribution_percentage=journal_article.get('Contribution Percentage'),
                        description_of_role=journal_article.get('Description of Contribution Role'),
                        journal_type="Article",
                        publication=publication_obj
                    )
                    journal_article_obj.save()

                    self.save_funding_source(journal_article, journal_article_obj)

                for journal_issue in publication.get('Journal Issues', []):

                    journal_issue_obj = Journal(
                        title=journal_issue.get('Article Title'),
                        journal=journal_issue.get('Journal'),
                        volume=journal_issue.get('Volume'),
                        issue=journal_issue.get('Issue'),
                        page_range=journal_issue.get('Page Range'),
                        publishing_status=journal_issue.get('Publishing Status'),
                        # year
                        publisher=journal_issue.get('Publisher'),
                        publication_location=journal_issue.get('Publication Location'),
                        contribution_value=journal_issue.get('Description / Contribution Value'),
                        url=journal_issue.get('URL'),
                        is_refereed=self.parse_boolean(journal_issue.get('Refereed?')),
                        is_open_access=self.parse_boolean(journal_issue.get('Open Access?')),
                        role=journal_issue.get('Contribution Role'),
                        contributors_count=parse_integer(journal_issue.get('Number of Contributors')),
                        authors=journal_issue.get('Authors'),
                        editors=journal_issue.get('Editors'),
                        doi=journal_issue.get('DOI'),
                        contribution_percentage=journal_issue.get('Contribution Percentage'),
                        description_of_role=journal_issue.get('Description of Contribution Role'),
                        journal_type="Issue",
                        publication=publication_obj
                    )
                    journal_issue_obj.save()

                    self.save_funding_source(journal_issue, journal_issue_obj)

                for book in publication.get('Books', []):

                    book_obj = Book(
                        title=book.get('Book Title'),
                        # # #
                        publishing_status=book.get('Publishing Status'),
                        year=book.get('Year'),
                        publisher=book.get('Publisher'),
                        publication_location=book.get('Publication Location'),
                        publication_city=book.get('Publication City'),
                        contribution_value=book.get('Description / Contribution Value'),
                        url=book.get('URL'),
                        is_refereed=self.parse_boolean(book.get('Refereed?')),
                        role=book.get('Contribution Role'),
                        contributors_count=book.get('Number of Contributors'),
                        authors=book.get('Authors'),
                        editors=book.get('Editors'),
                        doi=book.get('DOI'),
                        contribution_percentage=book.get('Contribution Percentage'),
                        description_of_role=book.get('Description of Contribution Role'),
                        publication=publication_obj
                    )
                    book_obj.save()
                    self.save_funding_source(book, book_obj)

                # # # #

                for thesis in publication.get('Thesis/Dissertation', []):

                    org_obj = self.get_organization_obj(thesis)
                    thesis_obj = ThesisDissertation(
                        title=thesis.get('Dissertation Title'),
                        organization=org_obj,
                        #
                        supervisor=thesis.get('Supervisor'),
                        completion_year=thesis.get('Completion Year'),
                        degree_type=thesis.get('Degree Type'),
                        pages_count=thesis.get('Number of Pages'),
                        contribution_value=thesis.get('Description / Contribution Value'),
                        url=thesis.get('URL'),
                        doi=thesis.get('DOI'),
                        contribution_percentage=thesis.get('Contribution Percentage'),
                        description_of_role=thesis.get('Description of Contribution Role'),
                        publication=publication_obj
                    )
                    thesis_obj.save()

                    self.save_funding_source(thesis, thesis_obj)

                for student_publication in publication.get('Supervised Student Publications', []):

                    student_publication_obj = SupervisedStudentPublication(
                        student=student_publication.get('Student'),
                        title=student_publication.get('Publication Title'),
                        published_in=student_publication.get('Published In'),
                        # # #
                        publishing_status=student_publication.get('Publishing Status'),
                        year=student_publication.get('Year'),
                        publisher=student_publication.get('Publisher'),
                        publication_location=student_publication.get('Publication Location'),
                        student_contribution=parse_integer(student_publication.get('Student Contribution (%)')),
                        contribution_value=student_publication.get('Description / Contribution Value'),
                        url=student_publication.get('URL'),
                        doi=student_publication.get('DOI'),
                        contribution_percentage=student_publication.get('Contribution Percentage'),
                        description_of_role=student_publication.get('Description of Contribution Role'),
                        publication=publication_obj
                    )
                    student_publication_obj.save()

                    self.save_funding_source(student_publication, student_publication_obj)

                for litigation in publication.get('Litigations', []):

                    litigation_obj = Litigation(
                        title=litigation.get('Case Name'),
                        person_acted_for=litigation.get('Person Acted For'),
                        court=litigation.get('Court'),
                        location=litigation.get('Location'),
                        year_started=litigation.get('Year Started'),
                        end_year=litigation.get('End Year'),
                        key_legal_issues=litigation.get('Key Legal Issues'),
                        contribution_value=litigation.get('Description / Contribution Value'),
                        url=litigation.get('URL'),
                        doi=litigation.get('DOI'),
                        contribution_percentage=litigation.get('Contribution Percentage'),
                        description_of_role=litigation.get('Description of Contribution Role'),
                        publication=publication_obj
                    )
                    litigation_obj.save()

                    self.save_funding_source(litigation, litigation_obj)

                for article in publication.get('Newspaper Articles', []):

                    article_obj = NewspaperArticle(
                        title=article.get('Article Title'),
                        newspaper=article.get('Page Range'),
                        # # #
                        year=article.get('Publication Year'),
                        publication_location=article.get('Publication Location'),
                        #
                        contribution_value=article.get('Description / Contribution Value'),
                        url=article.get('URL'),
                        role=article.get('Contribution Role'),
                        contributors_count=article.get('Number of Contributors'),
                        authors=article.get('Authors'),
                        editors=article.get('Editors'),
                        doi=article.get('DOI'),
                        contribution_percentage=article.get('Contribution Percentage'),
                        description_of_role=article.get('Description of Contribution Role'),
                        publication=publication_obj
                    )
                    article_obj.save()

                    self.save_funding_source(article, article_obj)

                #

                for encyclopedia_entry in publication.get('Encyclopedia Entries', []):

                    encyclopedia_entry_obj = EncyclopediaEntry(
                        title=encyclopedia_entry.get('Entry Title'),
                        name=encyclopedia_entry.get('Encyclopedia Name'),
                        # # # #
                        publishing_status=encyclopedia_entry.get('Publishing Status'),
                        year=encyclopedia_entry.get('Year'),
                        publisher=encyclopedia_entry.get('Publisher'),
                        publication_location=encyclopedia_entry.get('Publication Location'),
                        publication_city=encyclopedia_entry.get('Publication City'),
                        contribution_value=encyclopedia_entry.get('Description / Contribution Value'),
                        url=encyclopedia_entry.get('URL'),
                        role=encyclopedia_entry.get('Contribution Role'),
                        contributors_count=encyclopedia_entry.get('Number of Contributors'),
                        authors=encyclopedia_entry.get('Authors'),
                        editors=encyclopedia_entry.get('Editors'),
                        doi=encyclopedia_entry.get('DOI'),
                        contribution_percentage=encyclopedia_entry.get('Contribution Percentage'),
                        description_of_role=encyclopedia_entry.get('Description of Contribution Role'),
                        publication=publication_obj
                    )
                    encyclopedia_entry_obj.save()

                    self.save_funding_source(encyclopedia_entry, encyclopedia_entry_obj)

                for magazine in publication.get('Magazine Entries', []):

                    magazine_obj = MagazineEntry(
                        title=magazine.get('Article Title'),
                        name=magazine.get('Magazine Name'),
                        # # #
                        publishing_status=magazine.get('Publishing Status'),
                        year=magazine.get('Year'),
                        publisher=magazine.get('Publisher'),
                        publication_location=magazine.get('Publication Location'),
                        contribution_value=magazine.get('Description / Contribution Value'),
                        url=magazine.get('URL'),
                        role=magazine.get('Contribution Role'),
                        contributors_count=magazine.get('Number of Contributors'),
                        authors=magazine.get('Authors'),
                        editors=magazine.get('Editors'),
                        doi=magazine.get('DOI'),
                        contribution_percentage=magazine.get('Contribution Percentage'),
                        description_of_role=magazine.get('Description of Contribution Role'),
                        publication=publication_obj
                    )
                    magazine_obj.save()

                    self.save_funding_source(magazine, magazine_obj)

                # for dictionary in publication.get('Dictionary Entries', []):
                #
                #     dictionary_obj= DictionaryEntry(
                #         title=dictionary.get('Entry Title'),
                #         name=dictionary.get('Magazine Name'),
                #         # # #
                #         publishing_status=dictionary.get('Publishing Status'),
                #         year=dictionary.get('Year'),
                #         publisher=dictionary.get('Publisher'),
                #         publication_location=dictionary.get('Publication Location'),
                #         contribution_value=dictionary.get('Description / Contribution Value'),
                #         url=dictionary.get('URL'),
                #         role=dictionary.get('Contribution Role'),
                #         contributors_count=dictionary.get('Number of Contributors'),
                #         authors=dictionary.get('Authors'),
                #         editors=dictionary.get('Editors'),
                #         doi=dictionary.get('DOI'),
                #         contribution_percentage=dictionary.get('Contribution Percentage'),
                #         description_of_role=dictionary.get('Description of Contribution Role'),
                #         publication=publication_obj
                #     )
                    # dictionary_obj.save()

                    # self.save_funding_source(dictionary, dictionary_obj)




        return True


    def save_employments(self, employments: list) -> bool:
        """
        :param employments:
        :return:
        """

        if isinstance(employments, list) and len(employments) == 0:
            return False

        for employment in employments:

            employment_obj = Employment(
                ccv=self.ccv
            )
            employment_obj.save()

            for academic_work_experience in employment.get('Academic Work Experience', []):

                org_obj = self.get_organization_obj(academic_work_experience)
                AcademicWorkExperience(
                    position_type=academic_work_experience.get('Position Type'),
                    position_title=academic_work_experience.get('Position Title'),
                    position_status=academic_work_experience.get('Position Status'),
                    academic_rank=academic_work_experience.get('Academic Rank'),
                    start_date=self.parse_datetime(academic_work_experience.get('Start Date'), "%Y/%m"),
                    end_date=self.parse_datetime(academic_work_experience.get('End Date'), '%Y/%m'),
                    work_description=academic_work_experience.get('Work Description'),
                    organization=org_obj,
                    department=academic_work_experience.get('department'),
                    campus=academic_work_experience.get('Faculty / School / Campus'),
                    tenure_status=academic_work_experience.get('Tenure Status'),
                    tenure_start_date=self.parse_datetime(academic_work_experience.get('Tenure Start Date'), "%Y/%M"),
                    tenure_end_date=self.parse_datetime(academic_work_experience.get('Tenure Start Date'), "%Y/%M"),
                    employment=employment_obj
                ).save()

            for non_academic_work_experience in employment.get('Non-academic Work Experience', []):
                org_obj = self.get_organization_obj(non_academic_work_experience)

                NonAcademicWorkExperience(
                    position_title=non_academic_work_experience.get('Position Title'),
                    position_status=non_academic_work_experience.get('Position Status'),
                    start_date=self.parse_datetime(non_academic_work_experience.get('Start Date'), "%Y/%m"),
                    end_date=self.parse_datetime(non_academic_work_experience.get('End Date'), "%Y/%m"),
                    work_description=non_academic_work_experience.get('Work Description'),
                    unit_division=non_academic_work_experience.get('Unit / Division'),
                    organization=org_obj,
                    employment=employment_obj
                ).save()

            for affiliation in employment.get('Affiliations', []):

                org_obj = self.get_organization_obj(affiliation)

                Affiliation(
                    position_title=affiliation.get('Position Title'),
                    organization=org_obj,
                    department=affiliation.get('Department'),
                    activity_description=affiliation.get('Activity Description'),
                    start_date=self.parse_datetime(affiliation.get('Start Date'), '%Y/%m'),
                    end_date=self.parse_datetime(affiliation.get('End Date'), '%Y/%m'),
                    employment=employment_obj
                ).save()

            for leaves_of_absence in employment.get('Leaves of Absence and Impact on Research', []):
                org_obj = self.get_organization_obj(leaves_of_absence)

                LeavesOfAbsence(
                    leave_type=leaves_of_absence.get('Leave Type'),
                    start_date=self.parse_datetime(leaves_of_absence.get('Start Date'), '%Y/%m'),
                    end_date=self.parse_datetime(leaves_of_absence.get('End Date'), '%Y/%m'),
                    organization=org_obj,
                    absence_description=leaves_of_absence.get('Absence and Impact Description'),
                    employment=employment_obj
                ).save()

        return True



    def save_to_db(self):

        self.ccv = CanadianCommonCv(**{})
        self.ccv.save()
        self.stdout.write(f"{self.ccv.id}")

        # identification

        for i in self.final_data["Personal Information"][0]["Identification"]:
            self.identification = Identification(
                title=i["Title"],
                family_name=i["Family Name"],
                first_name=i["First Name"],
                middle_name=i["Middle Name"],
                previous_family_name=i["Previous Family Name"],
                previous_first_name=i["Previous First Name"],
                date_of_birth=i["Date of Birth"],
                sex=i["Sex"],
                designated_group=i["Designated Group"],
                correspondence_language=i["Correspondence language"],
                canadian_residency_status=i["Canadian Residency Status"],
                permanent_residency=i["Applied for Permanent Residency?"],
                permanent_residency_start_date=self.parse_datetime(i["Permanent Residency Start Date"], ""),
                ccv=self.ccv
            )
            self.identification.save()

        # country of citizenship

        # language skills

        for i in self.final_data["Personal Information"][0]["Language Skills"]:
            LanguageSkill(
                language=i["Language"],
                can_read=self.parse_boolean(i["Read"]),
                can_speak=self.parse_boolean(i["Speak"]),
                can_write=self.parse_boolean(i["Write"]),
                can_understand=self.parse_boolean(i["Understand"]),
                peer_review=self.parse_boolean(i["Peer Review"]),
                personal_information=self.identification
            ).save()

        # address

        for i in self.final_data["Personal Information"][0]["Address"]:
            Address(
                type=i["Address Type"],
                line_1=i["Address - Line 1"],
                line_2=i["Line 2"],
                line_3=i["Line 3"],
                line_4=i["Line 4"],
                line_5=i["Line 5"],
                city=i["City"],
                country=i["Location"]["Country-Subdivision"]["Country"],
                subdivision=i["Location"]["Country-Subdivision"]["Subdivision"],
                postal=i["Postal / Zip Code"],
                start_date=self.parse_datetime(i["Address Start Date"], "%Y-%m-%d"),
                end_date=self.parse_datetime(i["Address End Date"], "%Y-%m-%d"),
                personal_information=self.identification
            ).save()

        # # telephone
        #

        for i in self.final_data["Personal Information"][0]["Telephone"]:
            Telephone(
                phone_type=i["Phone Type"],
                country_code=i["Country Code"],
                area_code=i["Area Code"],
                number=i["Telephone Number"],
                extension=i["Extension"],
                start_date=self.parse_datetime(i["Telephone Start Date"], "%Y-%m-%d"),
                end_date=self.parse_datetime(i["Telephone End Date"], "%Y-%m-%d"),
                personal_information=self.identification
            ).save()

        # email

        for i in self.final_data["Personal Information"][0]["Email"]:
            Email(
                type=i["Email Type"],
                address=i["Email Address"],
                start_date=self.parse_datetime(i["Email Start Date"], "%Y/%m"),
                end_date=self.parse_datetime(i["Email End Date"], "%Y/%m"),
                personal_information=self.identification
            ).save()

        # website
        for i in self.final_data["Personal Information"][0]["Website"]:
            Website(
                type=i["Website Type"],
                url=i["URL"],
                personal_information=self.identification
            ).save()

        # education

        self.education = Education(ccv=self.ccv)
        self.education.save()

        # degree

        for i in self.final_data["Education"][0]["Degrees"]:
            degree = Degree(
                type=i["Degree Type"],
                name=i["Degree Name"],
                specialization=i["Specialization"],
                thesis_title=i["Thesis Title"],
                status=i["Degree Status"],
                start_date=self.parse_datetime(i["Degree Start Date"], "%Y/%m"),
                end_date=self.parse_datetime(i["Degree Received Date"], "%Y/%m"),
                expected_date=self.parse_datetime(i["Degree Expected Date"], "%Y/%m"),
                phd_without_masters=self.parse_boolean(i["Transferred to PhD without completing Masters?"]),
                education_id=self.education.id
            )
            degree.save()

            for supervisor in i.get("Supervisors", []):
                Supervisor(
                    name=supervisor["Supervisor Name"],
                    start_date=self.parse_datetime(supervisor["Start Date"], "%Y/%m"),
                    end_date=self.parse_datetime(supervisor["End Date"], "%Y/%m"),
                    degree=degree
                ).save()

        for credential in self.final_data["Education"][0].get("Credentials", []):
            Credential(
                title=credential["Title"],
                effective_date=self.parse_datetime(credential["Effective Date"], "%Y/%m"),
                end_date=self.parse_datetime(credential["End Date"], "%Y/%m"),
                description=credential["Description"],
                education_id=self.education.id
            )

        # recognitions
        # self.stdout.write(f"----------{self.final_data.get('Recognitions')}")
        #
        # self.final_data["Recognitions"] = [self.final_data.get("Recognitions")]

        for recognition in self.final_data.get("Recognitions", []):
            # self.stdout.write(f"----------{recognition}")
            Recognition(
                type=recognition["Recognition Type"],
                name=recognition["Recognition Name"],
                effective_date=self.parse_datetime(recognition["Effective Date"], "%Y/%m"),
                end_date=self.parse_datetime(recognition["End Date"], "%Y/%m"),
                amount=recognition.get("Amount"),
                currency=recognition["Currency"],
                description=recognition["Description"],
                ccv=self.ccv
            ).save()

        user_profile = UserProfile(
            researcher_status=self.final_data["User Profile"][0]["Researcher Status"],
            career_start_date=self.parse_datetime(self.final_data["User Profile"][0]["Research Career Start Date"],
                                                  "%Y-%m-%d"),
            engaged_in_clinical_research=self.parse_boolean(
                self.final_data["User Profile"][0]["Engaged in Clinical Research?"]),
            key_theory=self.final_data["User Profile"][0]["Key Theory / Methodology"],
            research_interest=self.final_data["User Profile"][0]["Research Interests"],
            experience_summary=self.final_data["User Profile"][0]["Research Experience Summary"],
            # country=self.final_data["User Profile"][""],
            ccv=self.ccv
        )
        user_profile.save()

        for research_specialization_keyword in \
                self.final_data["User Profile"][0].get("Research Specialization Keywords", []):
            ResearchSpecializationKeyword(
                keyword=research_specialization_keyword["Research Specialization Keywords"],
                order=research_specialization_keyword["Order"],
                user_profile=user_profile
            ).save()

        for research_centre in self.final_data["User Profile"][0].get("Research Centres", []):
            research_centre = research_centre["Research Centre"]["Research Centre"]

            ResearchCentre(
                name=research_centre["Research Centre"],
                country=research_centre["Country"],
                subdivision=research_centre["Subdivision"],
                user_profile=user_profile
            ).save()

        for discipline in self.final_data["User Profile"][0]["Disciplines Trained In"]:
            DisciplineTrainedIn(
                # order=discipline["Order"]
                sector=discipline["Discipline Trained In"]["Research Discipline"]["Sector of Discipline"],
                fields=discipline["Discipline Trained In"]["Research Discipline"]["Field"],
                discipline=discipline["Discipline Trained In"]["Research Discipline"]["Discipline"],
                user_profile=user_profile
            ).save()

        for research_discipline in self.final_data["User Profile"][0]["Research Disciplines"]:
            ResearchDiscipline(
                order=research_discipline["Order"],
                field=research_discipline["Research Discipline"]["Research Discipline"]["Field"],
                sector_of_discipline=research_discipline["Research Discipline"]["Research Discipline"][
                    "Sector of Discipline"],
                discipline=research_discipline["Research Discipline"]["Research Discipline"]["Discipline"],
                user_profile=user_profile
            ).save()

        for area in self.final_data["User Profile"][0]["Areas of Research"]:
            AreaOfResearch(
                order=area["Order"],
                sector=area["Area of Research"]["Area of Research"]["Sector of Research"],
                field=area["Area of Research"]["Area of Research"]["Field"],
                subfield=area["Area of Research"]["Area of Research"]["Subfield"],
                area=area["Area of Research"]["Area of Research"]["Area"],
                user_profile=user_profile
            ).save()

        for application in self.final_data["User Profile"][0]["Fields of Application"]:
            FieldOfApplication(
                order=application["Order"],
                field=application["Field of Application"]["Field of Application"]["Field of Application"],
                subfield=application["Field of Application"]["Field of Application"]["Subfield"],
                user_profile=user_profile
            ).save()

        # employment

        # for i in self.final_data["Education"][""]

        if "Employment" in self.final_data and \
                isinstance(self.final_data["Employment"], list):
            self.save_employments(self.final_data['Employment'])

        if "Research Funding History" in self.final_data and \
                isinstance(self.final_data["Research Funding History"], list):
            self.save_research_funding_history(self.final_data['Research Funding History'])

        if "Most Significant Contributions" in self.final_data and \
                isinstance(self.final_data['Most Significant Contributions'], list):
            self.save_most_significant_contribution(self.final_data['Most Significant Contributions'])

        if "Memberships" in self.final_data and \
                isinstance(self.final_data['Memberships'], list):
            self.save_memberships(self.final_data['Memberships'])

        if "Contributions" in self.final_data and \
                isinstance(self.final_data['Contributions'], list):
            self.save_contributions(self.final_data['Contributions'])

    # def save_employment(self):

    def handle(self, *args, **options):

        if "ccv_xml_filepath" not in options:
            raise CommandError("XML file path is not provided")

        file_path = options.get("ccv_xml_filepath")

        try:
            with open(file_path, encoding="utf8") as xml_file:
                parsed_xml = ET.parse(xml_file)
        except (FileNotFoundError, IsADirectoryError):
            raise CommandError("File path doesn't exist. Provide a valid path")

        parsed_xml = etree_to_dict(parsed_xml.getroot())
        data = parsed_xml['{http://www.cihr-irsc.gc.ca/generic-cv/1.0.0}generic-cv']

        self.final_data = self.get_response(data)['ccv']

        self.save_to_db()
