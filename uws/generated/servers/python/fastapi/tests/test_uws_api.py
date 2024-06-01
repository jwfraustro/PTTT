# coding: utf-8

from fastapi.testclient import TestClient


from uws_server.models.error_summary import ErrorSummary  # noqa: F401
from uws_server.models.execution_phase import ExecutionPhase  # noqa: F401
from uws_server.models.job_summary import JobSummary  # noqa: F401
from uws_server.models.jobs import Jobs  # noqa: F401
from uws_server.models.parameters import Parameters  # noqa: F401
from uws_server.models.post_create_job_request import PostCreateJobRequest  # noqa: F401
from uws_server.models.post_update_job_destruction_request import PostUpdateJobDestructionRequest  # noqa: F401
from uws_server.models.post_update_job_execution_duration_request import PostUpdateJobExecutionDurationRequest  # noqa: F401
from uws_server.models.post_update_job_parameters_request import PostUpdateJobParametersRequest  # noqa: F401
from uws_server.models.post_update_job_phase_request import PostUpdateJobPhaseRequest  # noqa: F401
from uws_server.models.post_update_job_request import PostUpdateJobRequest  # noqa: F401
from uws_server.models.results import Results  # noqa: F401


def test_delete_job(client: TestClient):
    """Test case for delete_job

    Deletes the job
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/{job_id}".format(job_id='job_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_job_destruction(client: TestClient):
    """Test case for get_job_destruction

    Returns the job destruction time
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{job_id}/destruction".format(job_id='job_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_job_error_summary(client: TestClient):
    """Test case for get_job_error_summary

    Returns the job error summary
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{job_id}/error".format(job_id='job_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_job_execution_duration(client: TestClient):
    """Test case for get_job_execution_duration

    Returns the job execution duration
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{job_id}/executionduration".format(job_id='job_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_job_list(client: TestClient):
    """Test case for get_job_list

    Returns the list of UWS jobs
    """
    params = [("phase", [uws_server.ExecutionPhase()]),     ("after", '2013-10-20T19:20:30+01:00'),     ("last", 56)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_job_owner(client: TestClient):
    """Test case for get_job_owner

    Returns the job owner
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{job_id}/owner".format(job_id='job_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_job_parameters(client: TestClient):
    """Test case for get_job_parameters

    Returns the job parameters
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{job_id}/parameters".format(job_id='job_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_job_phase(client: TestClient):
    """Test case for get_job_phase

    Returns the job phase
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{job_id}/phase".format(job_id='job_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_job_quote(client: TestClient):
    """Test case for get_job_quote

    Returns the job quote
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{job_id}/quote".format(job_id='job_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_job_results(client: TestClient):
    """Test case for get_job_results

    Returns the job results
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{job_id}/results".format(job_id='job_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_job_summary(client: TestClient):
    """Test case for get_job_summary

    Returns the job summary
    """
    params = [("phase", 'PENDING'),     ("wait", 56)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{job_id}".format(job_id='job_id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_post_create_job(client: TestClient):
    """Test case for post_create_job

    Submits a job
    """
    post_create_job_request = uws_server.PostCreateJobRequest()

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/",
    #    headers=headers,
    #    json=post_create_job_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_post_update_job(client: TestClient):
    """Test case for post_update_job

    Update job parameters
    """
    post_update_job_request = uws_server.PostUpdateJobRequest()

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/{job_id}".format(job_id='job_id_example'),
    #    headers=headers,
    #    json=post_update_job_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_post_update_job_destruction(client: TestClient):
    """Test case for post_update_job_destruction

    Updates the job destruction time
    """
    post_update_job_destruction_request = uws_server.PostUpdateJobDestructionRequest()

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/{job_id}/destruction".format(job_id='job_id_example'),
    #    headers=headers,
    #    json=post_update_job_destruction_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_post_update_job_execution_duration(client: TestClient):
    """Test case for post_update_job_execution_duration

    Updates the job execution duration
    """
    post_update_job_execution_duration_request = uws_server.PostUpdateJobExecutionDurationRequest()

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/{job_id}/executionduration".format(job_id='job_id_example'),
    #    headers=headers,
    #    json=post_update_job_execution_duration_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_post_update_job_parameters(client: TestClient):
    """Test case for post_update_job_parameters

    Update job parameters
    """
    post_update_job_parameters_request = uws_server.PostUpdateJobParametersRequest()

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/{job_id}/parameters".format(job_id='job_id_example'),
    #    headers=headers,
    #    json=post_update_job_parameters_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_post_update_job_phase(client: TestClient):
    """Test case for post_update_job_phase

    Updates the job phase
    """
    post_update_job_phase_request = uws_server.PostUpdateJobPhaseRequest()

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/{job_id}/phase".format(job_id='job_id_example'),
    #    headers=headers,
    #    json=post_update_job_phase_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

