import sys
from io import StringIO

import pytest
from django.core import management
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ..models.base import CanadianCommonCv
from ..serializers import CanadianCommonCvSerializer

client = APIClient()


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

    def test_ccv_endpoint(self):
        """
        It tests the /ccv endpoint
        """
        # getting api response
        response = client.get('/ccv')

        # getting data from db
        ccvs = CanadianCommonCv.objects.all()
        ccv_serializer = CanadianCommonCvSerializer(ccvs, many=True)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'] == ccv_serializer.data
