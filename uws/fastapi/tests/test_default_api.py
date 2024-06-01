# coding: utf-8

import openapi_server
from fastapi.testclient import TestClient
from openapi_server.models.error_summary import ErrorSummary  # noqa: F401
from openapi_server.models.execution_phase import ExecutionPhase  # noqa: F401
from openapi_server.models.job_summary import JobSummary  # noqa: F401
from openapi_server.models.jobs import Jobs  # noqa: F401
from openapi_server.models.parameters import Parameters  # noqa: F401
from openapi_server.models.post_create_job_request import (  # noqa: F401
    PostCreateJobRequest,
)
from openapi_server.models.post_update_job_destruction_request import (  # noqa: F401
    PostUpdateJobDestructionRequest,
)
from openapi_server.models.post_update_job_execution_duration_request import (  # noqa: F401
    PostUpdateJobExecutionDurationRequest,
)
from openapi_server.models.post_update_job_parameters_request import (  # noqa: F401
    PostUpdateJobParametersRequest,
)
from openapi_server.models.post_update_job_phase_request import (  # noqa: F401
    PostUpdateJobPhaseRequest,
)
from openapi_server.models.post_update_job_request import (  # noqa: F401
    PostUpdateJobRequest,
)
from openapi_server.models.results import Results  # noqa: F401


def test_delete_job(client: TestClient):
    """Test case for delete_job

    Deletes the job
    """

    # uncomment below to make a request
    # response = client.request(
    #    "DELETE",
    #    "/{job-id}".format(job-id='job_id_example'),
    #    headers=headers,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_job_destruction(client: TestClient):
    """Test case for get_job_destruction

    Returns the job destruction time
    """

    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    "/{job-id}/destruction".format(job-id='job_id_example'),
    #    headers=headers,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_job_error_summary(client: TestClient):
    """Test case for get_job_error_summary

    Returns the job error summary
    """

    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    "/{job-id}/error".format(job-id='job_id_example'),
    #    headers=headers,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_job_execution_duration(client: TestClient):
    """Test case for get_job_execution_duration

    Returns the job execution duration
    """

    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    "/{job-id}/executionduration".format(job-id='job_id_example'),
    #    headers=headers,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_job_list(client: TestClient):
    """Test case for get_job_list

    Returns the list of UWS jobs
    """
    [("phase", openapi_server.ExecutionPhase()), ("after", "2013-10-20T19:20:30+01:00"), ("last", 56)]
    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    "/",
    #    headers=headers,
    #    params=params,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_job_owner(client: TestClient):
    """Test case for get_job_owner

    Returns the job owner
    """

    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    "/{job-id}/owner".format(job-id='job_id_example'),
    #    headers=headers,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_job_parameters(client: TestClient):
    """Test case for get_job_parameters

    Returns the job parameters
    """

    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    "/{job-id}/parameters".format(job-id='job_id_example'),
    #    headers=headers,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_job_phase(client: TestClient):
    """Test case for get_job_phase

    Returns the job phase
    """

    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    "/{job-id}/phase".format(job-id='job_id_example'),
    #    headers=headers,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_job_quote(client: TestClient):
    """Test case for get_job_quote

    Returns the job quote
    """

    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    "/{job-id}/quote".format(job-id='job_id_example'),
    #    headers=headers,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_job_results(client: TestClient):
    """Test case for get_job_results

    Returns the job results
    """

    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    "/{job-id}/results".format(job-id='job_id_example'),
    #    headers=headers,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_job_summary(client: TestClient):
    """Test case for get_job_summary

    Returns the job summary
    """
    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    "/{job-id}".format(job-id='job_id_example'),
    #    headers=headers,
    #    params=params,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_post_create_job(client: TestClient):
    """Test case for post_create_job

    Submits a job
    """
    openapi_server.PostCreateJobRequest()

    # uncomment below to make a request
    # response = client.request(
    #    "POST",
    #    "/",
    #    headers=headers,
    #    json=post_create_job_request,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_post_update_job(client: TestClient):
    """Test case for post_update_job

    Update job parameters
    """
    openapi_server.PostUpdateJobRequest()

    # uncomment below to make a request
    # response = client.request(
    #    "POST",
    #    "/{job-id}".format(job-id='job_id_example'),
    #    headers=headers,
    #    json=post_update_job_request,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_post_update_job_destruction(client: TestClient):
    """Test case for post_update_job_destruction

    Updates the job destruction time
    """
    openapi_server.PostUpdateJobDestructionRequest()

    # uncomment below to make a request
    # response = client.request(
    #    "POST",
    #    "/{job-id}/destruction".format(job-id='job_id_example'),
    #    headers=headers,
    #    json=post_update_job_destruction_request,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_post_update_job_execution_duration(client: TestClient):
    """Test case for post_update_job_execution_duration

    Updates the job execution duration
    """
    openapi_server.PostUpdateJobExecutionDurationRequest()

    # uncomment below to make a request
    # response = client.request(
    #    "POST",
    #    "/{job-id}/executionduration".format(job-id='job_id_example'),
    #    headers=headers,
    #    json=post_update_job_execution_duration_request,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_post_update_job_parameters(client: TestClient):
    """Test case for post_update_job_parameters

    Update job parameters
    """
    openapi_server.PostUpdateJobParametersRequest()

    # uncomment below to make a request
    # response = client.request(
    #    "POST",
    #    "/{job-id}/parameters".format(job-id='job_id_example'),
    #    headers=headers,
    #    json=post_update_job_parameters_request,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_post_update_job_phase(client: TestClient):
    """Test case for post_update_job_phase

    Updates the job phase
    """
    openapi_server.PostUpdateJobPhaseRequest()

    # uncomment below to make a request
    # response = client.request(
    #    "POST",
    #    "/{job-id}/phase".format(job-id='job_id_example'),
    #    headers=headers,
    #    json=post_update_job_phase_request,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
