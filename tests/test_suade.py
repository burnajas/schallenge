import os
import tempfile

import pytest

from suade_challenge import create_app


@pytest.fixture
def app():
    """Usually would initialise test database here, build tables from test schema then populate from preconfigured
     database fixtures (files holding SQL inserts).
     But we know one exists from Docker initialisation.
     """
    app = create_app({
        'TESTING': True,
    })

    app.config['TESTING'] = True

    yield app


@pytest.fixture
def client(app):
    """"""
    return app.test_client()


def test_success_status(client):
    """Test that service is up and returns a status 200."""
    req = client.get('/')
    assert req.status_code == 200


def test_pdf_returned(client):
    """Test that PDF document returned from request"""
    req = client.get('/reports/1/pdf')
    assert req.status_code == 200
    assert req.content_type == 'application/pdf'


def test_xml_returned(client):
    """Test that PDF document returned from request"""
    req = client.get('/reports/1/xml')
    assert req.status_code == 200
    assert req.content_type == 'text/xml'
