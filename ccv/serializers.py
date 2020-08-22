from rest_framework.serializers import CharField, ModelSerializer

from .models.base import CanadianCommonCv
from .models.employment import AcademicWorkExperience, Employment
from .models.personal_information import Identification, Email, Website
from .models.recognitions import AreaOfResearch
from .models.user_profile import UserProfile


class AreaOfResearchSerializer(ModelSerializer):
    class Meta:
        model = AreaOfResearch
        fields = [
            'area',
            'sector',
            'field'
        ]


class WebsiteSerializer(ModelSerializer):
    class Meta:
        model = Website
        fields = ['url']


class EmailSerializer(ModelSerializer):
    class Meta:
        model = Email
        fields = ['address']


class IdentificationSerializer(ModelSerializer):
    email = EmailSerializer(many=True, read_only=True, source='email_set')
    website = WebsiteSerializer(many=True, read_only=True, source="website_set")

    class Meta:
        model = Identification
        fields = [
            'email',
            'title',
            'website',
            'family_name',
            'first_name',
            'middle_name',
            'previous_family_name',
            'previous_first_name'
        ]


class AcademicWorkExperienceSerializer(ModelSerializer):
    class Meta:
        model = AcademicWorkExperience
        fields = [
            'department',
            'position_title'
        ]


class EmploymentSerializer(ModelSerializer):
    academic_work_experience = AcademicWorkExperienceSerializer(many=True, read_only=True)

    class Meta:
        model = Employment
        fields = ['academic_work_experience']


class UserProfileSerializer(ModelSerializer):
    research_description = CharField(source='research_interest', read_only=True)
    research_interests = AreaOfResearchSerializer(many=True, read_only=True, source='user_aor')

    class Meta:
        model = UserProfile
        fields = [
            'research_description',
            'research_interests'
        ]


class CanadianCommonCvSerializer(ModelSerializer):
    identification = IdentificationSerializer(read_only=True)
    employment = EmploymentSerializer(read_only=True)
    user_profile = UserProfileSerializer(read_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['research_description'] = ret['user_profile']['research_description']
        ret['research_interests'] = ret['user_profile']['research_interests']
        ret.pop('user_profile')
        return ret

    class Meta:
        model = CanadianCommonCv
        fields = [
            'identification',
            'employment',
            'user_profile'
        ]
