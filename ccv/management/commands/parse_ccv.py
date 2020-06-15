# -*- coding: utf-8 -*-

import json
import uuid
import datetime
import xml.etree.ElementTree as ET

from django.core.management.base import BaseCommand, CommandError

from ccv.models import CanadianCommonCv, Identification, CountryOfCitizenship, LanguageSkill, Address, Website, \
    Telephone, Email, Education, Degree, Supervisor, Credential, Recognition, ResearchCentre, UserProfile, \
    ResearchSpecializationKeyword, ResearchCentre, TechnologicalApplication, DisciplineTrainedIn, TemporalPeriod, \
    GeographicalRegion, Employment, AcademicWorkExperience, NonAcademicWorkExperience, Affiliation, LeavesOfAbsence, \
    ResearchFundingHistory, ResearchUptakeHolder, ResearchSetting, FundingSource, FundingByYear, OtherInvestigator, \
    Membership, CommitteeMembership, OtherMembership, ResearchDiscipline, FieldOfApplication, AreaOfResearch
from ccv.utils import etree_to_dict


class Command(BaseCommand):
    help = ''

    final_data = {}

    def add_arguments(self, parser):
        parser.add_argument('ccv_xml_filepath', type=str)

    def get_fields(self, fields: list) -> dict:
        """
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

    def get_response(self, sections: list) -> dict:
        """
        :param sections:
        :return:
        """

        response = {}
        for section in sections:
            if 'field' in section:
                if not isinstance(section.get('field'), list):
                    section['field'] = [section.get('field')]

                if section.get('label') in response:
                    response[section.get('label')].append(self.get_fields(section.get('field')))
                else:
                    response[section.get('label')] = [self.get_fields(section.get('field'))]

            if 'section' in section:
                if isinstance(section['section'], dict):
                    section['section'] = [section['section']]
                for _section in section["section"]:
                    if "field" in _section:
                        if not isinstance(_section.get('field'), list):
                            _section['field'] = [_section.get('field')]
                        if _section.get('label') in response[section.get('label')][0]:
                            response[section.get('label')][0][_section.get('label')].append(
                                self.get_fields(_section.get('field')))
                        else:
                            response[section.get('label')][0][_section.get('label')] = [
                                self.get_fields(_section.get('field'))]
        return response

    def parse_boolean(self, value):
        return True if value == "Yes" else False

    def parse_datetime(self, date, format):
        return datetime.datetime.strptime(date, format) if date else None

    def save_to_db(self):

        ccv = CanadianCommonCv(**{})
        ccv.save()
        self.stdout.write(f"{ccv.id}")

        # identification

        for i in self.final_data["Personal Information"]["Identification"]:
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
                ccv=ccv
            )
            self.identification.save()

        # country of citizenship

        # language skills

        for i in self.final_data["Personal Information"]["Language Skills"]:
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

        for i in self.final_data["Personal Information"]["Address"]:
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

        for i in self.final_data["Personal Information"]["Telephone"]:
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

        for i in self.final_data["Personal Information"]["Email"]:
            Email(
                type=i["Email Type"],
                address=i["Email Address"],
                start_date=self.parse_datetime(i["Email Start Date"], "%Y/%m"),
                end_date=self.parse_datetime(i["Email End Date"], "%Y/%m"),
                personal_information=self.identification
            ).save()

        # website
        for i in self.final_data["Personal Information"]["Website"]:
            Website(
                type=i["Website Type"],
                url=i["URL"],
                personal_information=self.identification
            ).save()

        # education
        self.education = Education(ccv=ccv)
        self.education.save()

        # degree

        for i in self.final_data["Education"]["Degrees"]:
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

        for credential in self.final_data["Education"]["Credentials"]:
            Credential(
                title=credential["Title"],
                effective_date=self.parse_datetime(credential["Effective Date"], "%Y/%m"),
                end_date=self.parse_datetime(credential["End Date"], "%Y/%m"),
                description=credential["Description"],
                education_id=self.education.id
            )

        # recognitions
        self.stdout.write(f"----------{self.final_data.get('Recognitions')}")

        self.final_data["Recognitions"] = [self.final_data.get("Recognitions")]

        for recognition in self.final_data.get("Recognitions", []):
            self.stdout.write(f"----------{recognition}")
            Recognition(
                type=recognition["Recognition Type"],
                name=recognition["Recognition Name"],
                effective_date=self.parse_datetime(recognition["Effective Date"], "%Y/%m"),
                end_date=self.parse_datetime(recognition["End Date"], "%Y/%m"),
                amount=recognition.get("Amount"),
                currency=recognition["Currency"],
                description=recognition["Description"],
                ccv=ccv
            ).save()

        user_profile = UserProfile(
            researcher_status=self.final_data["User Profile"]["Researcher Status"],
            career_start_date=self.parse_datetime(self.final_data["User Profile"]["Research Career Start Date"],
                                                  "%Y-%m-%d"),
            engaged_in_clinical_research=self.parse_boolean(
                self.final_data["User Profile"]["Engaged in Clinical Research?"]),
            key_theory=self.final_data["User Profile"]["Key Theory / Methodology"],
            research_interest=self.final_data["User Profile"]["Research Interests"],
            experience_summary=self.final_data["User Profile"]["Research Experience Summary"],
            # country=self.final_data["User Profile"][""],
            ccv=ccv
        )
        user_profile.save()

        for research_specialization_keyword in \
                self.final_data["User Profile"].get("Research Specialization Keywords", []):
            ResearchSpecializationKeyword(
                keyword=research_specialization_keyword["Research Specialization Keywords"],
                order=research_specialization_keyword["Order"],
                user_profile=user_profile
            ).save()

        for research_centre in self.final_data["User Profile"].get("Research Centres", []):

            research_centre = research_centre["Research Centre"]["Research Centre"]

            ResearchCentre(
                name=research_centre["Research Centre"],
                country=research_centre["Country"],
                subdivision=research_centre["Subdivision"],
                user_profile=user_profile
            ).save()

        for discipline in self.final_data["User Profile"]["Disciplines Trained In"]:

            DisciplineTrainedIn(
                # order=discipline["Order"]
                sector=discipline["Discipline Trained In"]["Research Discipline"]["Sector of Discipline"],
                fields=discipline["Discipline Trained In"]["Research Discipline"]["Field"],
                discipline=discipline["Discipline Trained In"]["Research Discipline"]["Discipline"],
                user_profile=user_profile
            ).save()

        for research_discipline in self.final_data["User Profile"]["Research Disciplines"]:

            ResearchDiscipline(
                order=research_discipline["Order"],
                field=research_discipline["Research Discipline"]["Research Discipline"]["Field"],
                sector_of_discipline=research_discipline["Research Discipline"]["Research Discipline"]["Sector of Discipline"],
                discipline=research_discipline["Research Discipline"]["Research Discipline"]["Discipline"],
                user_profile=user_profile
            ).save()

        for area in self.final_data["User Profile"]["Areas of Research"]:

            AreaOfResearch(
                order=area["Order"],
                sector=area["Area of Research"]["Area of Research"]["Sector of Research"],
                field=area["Area of Research"]["Area of Research"]["Field"],
                subfield=area["Area of Research"]["Area of Research"]["Subfield"],
                area=area["Area of Research"]["Area of Research"]["Area"],
                user_profile=user_profile
            ).save()

        for application in self.final_data["User Profile"]["Fields of Application"]:

            FieldOfApplication(
                order=application["Order"],
                field=application["Field of Application"]["Field of Application"]["Field of Application"],
                subfield=application["Field of Application"]["Field of Application"]["Subfield"],
                user_profile=user_profile
            ).save()

        # employment

        # for i in self.final_data["Education"][""]

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

        for i in data["section"]:
            try:
                if "section" in i:
                    if isinstance(i["section"], dict):
                        i['section'] = [i["section"]]
                    self.final_data[i["label"]] = self.get_response(i["section"])
                if "field" in i and "section" not in i:
                    if i["label"] in self.final_data:
                        self.final_data[i["label"]].append(self.get_fields(i["field"]))
                    else:
                        self.final_data[i["label"]] = [self.get_fields(i["field"])]
                if "field" in i and "section" in i:
                    extra_fields = self.get_fields(i["field"])
                    self.final_data[i['label']] = {**self.final_data[i['label']], **extra_fields}

            except Exception as e:
                import traceback
                print(traceback.print_exc())

        self.save_to_db()
