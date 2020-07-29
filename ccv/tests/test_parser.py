import sys
from io import StringIO

import pytest
from django.core import management
from django.test import TestCase

from ..constants.test_constants import SAMPLE_TEST_CONSTANTS
from ..models.base import CanadianCommonCv
from ..models.personal_information import Identification
from ..models.education import Credential, Degree
from ..models.employment import Employment, AcademicWorkExperience, NonAcademicWorkExperience
from ..models.recognitions import Recognition, CommitteeMembership, Membership, MostSignificantContribution
from ..models.user_profile import UserProfile, ResearchCentre, DisciplineTrainedIn
from ..utils import normalize_date


@pytest.mark.django_db
class TestParser(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        It sets up the initial data for the models
        :return:
        """
        super(TestParser, cls).setUpTestData()
        db_id = cls.parse_ccv("sample_ccv/ccv_sample_3.xml")
        cls.id = db_id

    @staticmethod
    def parse_ccv(filepath: str) -> int:
        """
        it calls the parse_ccv django custom command which
        ingests the xml file to the database
        :param filepath: Filepath of the ccv xml file
        :return: id of the ingested ccv
        """

        output = StringIO()
        management.call_command('parse_ccv', filepath, stdout=output)
        sys.stderr.write(f'{output.getvalue()}')
        output = int(output.getvalue().strip())

        return output

    def test_valid_id(self) -> None:
        assert type(self.id) is int

    def test_id_exists(self) -> None:
        """
        Checks whether the id given by the parser exists in db
        """
        ccv_obj = CanadianCommonCv.objects.get(id=self.id)

        assert isinstance(ccv_obj, CanadianCommonCv)

    def test_personal_information(self) -> None:
        """
        It tests the personal information entity of the ccv
        """

        identification = Identification.objects.get(ccv__id=int(self.id))
        sample_data = SAMPLE_TEST_CONSTANTS['personal_information']

        assert isinstance(identification, Identification)
        assert identification.first_name == sample_data['first_name']
        assert identification.family_name == sample_data['family_name']
        assert identification.sex == sample_data['sex']
        assert identification.correspondence_language == sample_data['correspondence_language']
        assert identification.canadian_residency_status == sample_data['canadian_residency_status']
        assert identification.date_of_birth == sample_data['date_of_birth']

    def test_education(self) -> None:
        """
        It tests the education entity of the ccv
        """
        degrees = Degree.objects.filter(education__ccv__id=self.id).order_by('id')
        sample_data = SAMPLE_TEST_CONSTANTS['education']['degrees']

        for index, degree in enumerate(degrees):
            assert isinstance(degree, Degree)
            assert degree.name == sample_data[index]['name']
            assert degree.specialization == sample_data[index]['specialization']
            assert degree.status == sample_data[index]['status']
            assert normalize_date(degree.start_date, '%Y-%m-%d') == sample_data[index]['start_date']
            assert normalize_date(degree.end_date, '%Y-%m-%d') == sample_data[index]['end_date']
            assert degree.phd_without_masters == sample_data[index]['phd_without_masters']

        credentials = Credential.objects.filter(education__ccv__id=self.id).order_by('id')
        sample_data = SAMPLE_TEST_CONSTANTS['education']['credentials']

        for index, credential in enumerate(credentials):
            assert isinstance(credential, Credential)
            assert credential.title == sample_data[index]['title']
            assert normalize_date(credential.effective_date, '%Y-%m-%d') == sample_data[index]['effective_date']
            assert credential.description == sample_data[index]['description']

    def test_recognitions(self) -> None:
        """
        :It tests the recognitions entity of the ccv:
        """

        recognitions = Recognition.objects.filter(ccv_id=self.id).order_by('id')
        sample_data = SAMPLE_TEST_CONSTANTS['recognitions']

        for index, recognition in enumerate(recognitions):
            assert isinstance(recognition, Recognition)
            assert recognition.type == sample_data[index]['type']
            assert recognition.name == sample_data[index]['name']
            assert normalize_date(recognition.effective_date, '%Y-%m-%d') == sample_data[index]['effective_date']
            assert normalize_date(recognition.end_date, '%Y-%m-%d') == sample_data[index]['end_date']
            assert recognition.description == sample_data[index]['description']
            assert recognition.currency == sample_data[index]['currency']

    def test_memberships(self) -> None:
        """
        It tests the memberships entity of the ccv
        """

        membership = Membership.objects.get(ccv__id=self.id)
        assert isinstance(membership, Membership)

        memberships = CommitteeMembership.objects.filter(membership__ccv__id=self.id).order_by('id')
        sample_data = SAMPLE_TEST_CONSTANTS['memberships']['committee']
        for index, membership in enumerate(memberships):
            assert isinstance(membership, CommitteeMembership)
            assert membership.role == sample_data[index]['role']
            assert membership.name == sample_data[index]['name']
            assert normalize_date(membership.start_date, '%Y-%m-%d') == sample_data[index]['start_date']
            assert normalize_date(membership.end_date, '%Y-%m-%d') == sample_data[index]['end_date']
            assert membership.description == sample_data[index]['description']

    def test_most_significant_contribution(self) -> None:
        """
        It tests the most significant contributions entity of the ccv
        """

        msc = MostSignificantContribution.objects.filter(ccv__id=self.id).order_by('id')
        sample_data = SAMPLE_TEST_CONSTANTS['most_significant_contribution']

        for index, m in enumerate(msc):
            assert isinstance(m, MostSignificantContribution)
            assert m.title == sample_data[index]['title']
            assert normalize_date(m.contribution_date, '%Y-%m-%d') == sample_data[index]['contribution_date']

    def test_user_profile(self) -> None:
        """
        It tests the user profile entity of the ccv
        """

        user_profile = UserProfile.objects.get(ccv__id=self.id)
        sample_data = SAMPLE_TEST_CONSTANTS['user_profile']
        assert isinstance(user_profile, UserProfile)
        assert user_profile.researcher_status == sample_data['researcher_status']
        assert normalize_date(user_profile.career_start_date, '%Y-%m-%d') == sample_data['career_start_date']
        assert user_profile.engaged_in_clinical_research == sample_data['engaged_in_clinical_research']
        assert user_profile.key_theory == sample_data['key_theory']
        assert user_profile.research_interest == sample_data['research_interest']
        assert user_profile.experience_summary == sample_data['experience_summary']

        research_centres = ResearchCentre.objects.filter(user_profile__ccv__id=self.id).order_by('id')
        sample_data = SAMPLE_TEST_CONSTANTS['user_profile']['research_centre']
        for index, research_centre in enumerate(research_centres):
            assert isinstance(research_centre, ResearchCentre)
            assert research_centre.order == sample_data[index]['order']
            assert research_centre.name == sample_data[index]['name']
            assert research_centre.country == sample_data[index]['country']
            assert research_centre.subdivision == sample_data[index]['subdivision']

        disciplines_trained = DisciplineTrainedIn.objects.filter(user_profile__ccv__id=self.id).order_by('id')
        sample_data = SAMPLE_TEST_CONSTANTS['user_profile']['disciplines_trained']
        for index, discipline_trained in enumerate(disciplines_trained):
            assert isinstance(discipline_trained, DisciplineTrainedIn)
            assert discipline_trained.order == sample_data[index]['order']
            assert discipline_trained.discipline == sample_data[index]['discipline']
            assert discipline_trained.sector == sample_data[index]['sector']
            assert discipline_trained.fields == sample_data[index]['fields']

    def test_employment(self) -> None:
        """
        It tests the user employment entity of the ccv
        """
        employment = Employment.objects.get(ccv_id=self.id)
        assert isinstance(employment, Employment)

        academic_work_experiences = AcademicWorkExperience.objects.filter(employment__ccv__id=self.id).order_by('id')
        sample_data = SAMPLE_TEST_CONSTANTS['employment']['academic_work_experiences']
        for index, academic_work_experience in enumerate(academic_work_experiences):
            assert isinstance(academic_work_experience, AcademicWorkExperience)
            assert academic_work_experience.position_type == sample_data[index]['position_type']
            assert academic_work_experience.position_title == sample_data[index]['position_title']
            assert academic_work_experience.position_status == sample_data[index]['position_status']
            assert academic_work_experience.academic_rank == sample_data[index]['academic_rank']
            assert normalize_date(academic_work_experience.start_date, '%Y-%m-%d') == \
                sample_data[index]['start_date']
            assert normalize_date(academic_work_experience.end_date, '%Y-%m-%d') == sample_data[index]['end_date']
            assert academic_work_experience.work_description == sample_data[index]['work_description']
            assert academic_work_experience.department == sample_data[index]['department']
            assert academic_work_experience.campus == sample_data[index]['campus']
            assert academic_work_experience.tenure_status == sample_data[index]['tenure_status']
            assert normalize_date(academic_work_experience.tenure_start_date, '%Y-%m-%d') == \
                sample_data[index]['tenure_start_date']
            assert normalize_date(academic_work_experience.tenure_end_date, '%Y-%m-%d') == \
                sample_data[index]['tenure_end_date']

        non_academic_work_experiences = NonAcademicWorkExperience.objects.filter(
            employment__ccv__id=self.id).order_by('id')
        sample_data = SAMPLE_TEST_CONSTANTS['employment']['non_academic_work_experiences']
        for index, non_academic_work_experience in enumerate(non_academic_work_experiences):
            assert isinstance(non_academic_work_experience, NonAcademicWorkExperience)
            assert non_academic_work_experience.position_title == sample_data[index]['position_title']
            assert non_academic_work_experience.position_status == sample_data[index]['position_status']
            assert normalize_date(non_academic_work_experience.start_date, '%Y-%m-%d') == \
                sample_data[index]['start_date']
            assert normalize_date(non_academic_work_experience.end_date, '%Y-%m-%d') == sample_data[index]['end_date']
            assert non_academic_work_experience.work_description == sample_data[index]['work_description']
            assert non_academic_work_experience.unit_division == sample_data[index]['unit_division']
