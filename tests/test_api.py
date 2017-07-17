import pytest

import jobautomate.application


@pytest.fixture
def parameters():
    """Store the parameters for use with the Indeed API."""
    job_search = jobautomate.application.indeed_parameters('Financial Analyst', 'New York City')
    return job_search


@pytest.fixture
def application():
    """Link to a working job application."""
    return ('https://www.indeed.com/cmp/Indeed-Hire-Master-Account/jobs/Senior-API-Developer-6aeb0ad94f04299b?sjdu')


def fill(driver):
    """Open and fill an easily apply application."""
    jobautomate.application.open_application(driver, 'indeed-apply-button')
    jobautomate.application.switch_frames(driver, 'iframe[name$=modal-iframe]')
    jobautomate.application.fill_application(
        driver, 'Homer', 'Simpson', 'Chunkylover53@aol.com', 'resume.txt')


def test_indeed_api_parameters(parameters):
    """Test that the Indeed API returns the correct values."""
    assert isinstance(parameters, dict) is True
    assert 'Financial Analyst' in parameters.values()
    assert 'New York City' in parameters.values()


def test_retrieve_indeed_urls(selenium, parameters):
    """Test that the Indeed API returns 25 job application URLs."""
    response = jobautomate.application.access_indeed_api(parameters)
    job_urls = jobautomate.application.retrieve_indeed_urls(response)
    assert len(job_urls) == 25
    assert all('http://' in url for url in job_urls)


def test_false_api_key(parameters):
    """Test that an invalid API key returns an error."""
    assert jobautomate.application.access_indeed_api(
        parameters,
        123456789) == {'error': 'Invalid publisher number provided.'}


def test_open_application(selenium, application):
    """Test that an easily apply application opens properly."""
    selenium.get(application)
    jobautomate.application.open_application(selenium, 'indeed-apply-button')


def test_fill_application(selenium, application):
    """Test that an easily apply application can be filled."""
    selenium.get(application)
    fill(selenium)


def test_application_submission(selenium, application):
    """Test that all steps up to submitting the application are completed."""
    selenium.get(application)
    fill(selenium)
    jobautomate.application.submit_application(selenium, debug=True)