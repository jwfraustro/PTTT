# coding: utf-8

from datetime import datetime

from fastapi.testclient import TestClient
from uws_server.main import app
from src.impl.uws_api_impl
from uws_server.models.error_summary import ErrorSummary  # noqa: F401
from uws_server.models.execution_phase import ExecutionPhase  # noqa: F401
from uws_server.models.job_summary import JobSummary  # noqa: F401
from uws_server.models.jobs import Jobs  # noqa: F401
from uws_server.models.parameters import Parameters  # noqa: F401
from uws_server.models.post_update_job_destruction_request import PostUpdateJobDestructionRequest  # noqa: F401
from uws_server.models.post_update_job_execution_duration_request import (
    PostUpdateJobExecutionDurationRequest,  # noqa: F401
)
from uws_server.models.post_update_job_parameters_request import PostUpdateJobParametersRequest  # noqa: F401
from uws_server.models.post_update_job_phase_request import PostUpdateJobPhaseRequest  # noqa: F401
from uws_server.models.post_update_job_request import PostUpdateJobRequest  # noqa: F401
from uws_server.models.results import Results  # noqa: F401

SIMPLE_PARAMETERS = {
    "parameter": [
        {"value": "SELECT * FROM TAP_SCHEMA.tables", "id": "QUERY", "is_post": True, "by_reference": False},
        {"value": "ADQL", "id": "LANG", "is_post": True, "by_reference": False},
    ]
}

client = TestClient(app)  # noqa: E501


def build_test_job(client: TestClient):
    response = client.request(
        "POST",
        "/uws",
        json=SIMPLE_PARAMETERS,
    )

    assert response.status_code == 200
    assert response.json()["jobId"] is not None

    return response.json()["jobId"]


def test_delete_job(client: TestClient):
    """Test case for delete_job

    Deletes the job
    """

    job_id = build_test_job(client)

    # make sure the job is in the job list
    response = client.request(
        "GET",
        "/uws",
    )
    assert response.status_code == 200
    assert job_id in response.text

    # delete the job
    response = client.request(
        "DELETE",
        f"/uws/{job_id}",
        follow_redirects=False,
    )

    # we should have been redirected to the job list
    assert response.status_code == 303
    assert response.headers["location"] == "/uws"

    # make sure the job is no longer in the job list
    response = client.request(
        "GET",
        "/uws",
    )
    assert response.status_code == 200
    assert job_id not in response.text


def test_get_job_destruction(client: TestClient):
    """Test case for get_job_destruction

    Returns the job destruction time
    """

    job_id = build_test_job(client)

    response = client.request(
        "GET",
        f"/uws/{job_id}/destruction",
    )

    assert response.status_code == 200
    assert response.text is not None
    assert isinstance(datetime.fromisoformat(response.text), datetime)

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_job_error_summary(client: TestClient):
    """Test case for get_job_error_summary

    Returns the job error summary
    """

    headers = {}
    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    f"/uws/{job_id}/error"),
    #    headers=headers,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_job_execution_duration(client: TestClient):
    """Test case for get_job_execution_duration

    Returns the job execution duration
    """

    job_id = build_test_job(client)

    response = client.request(
        "GET",
        f"/uws/{job_id}/executionduration",
    )

    assert response.status_code == 200
    assert response.text == "3600"


def test_get_job_list(client: TestClient):
    """Test case for get_job_list

    Returns the list of UWS jobs
    """

    job_ids = []

    for _ in range(10):
        job_ids.append(build_test_job(client))

    response = client.request(
        "GET",
        "/uws",
    )

    assert response.status_code == 200

    job_list = response.json()

    assert job_list["jobref"] is not None

    job_refs = job_list["jobref"]

    assert len(job_refs) == 10
    for job_ref in job_refs:
        assert job_ref["id"] in job_ids

    # TODO - test phase, after, last
    # params = [("phase", [ExecutionPhase()]), ("after", "2013-10-20T19:20:30+01:00"), ("last", 56)]
    # headers = {}


def test_get_job_owner(client: TestClient):
    """Test case for get_job_owner

    Returns the job owner
    """

    job_id = build_test_job(client)

    response = client.request(
        "GET",
        f"/uws/{job_id}/owner",
    )

    assert response.status_code == 200
    assert response.text == "jsmith@ivoa.net"

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_job_parameters(client: TestClient):
    """Test case for get_job_parameters

    Returns the job parameters
    """

    job_id = build_test_job(client)

    response = client.request(
        "GET",
        f"/uws/{job_id}/parameters",
    )

    assert response.status_code == 200

    parameters = response.json()

    assert parameters["parameter"] is not None
    assert len(parameters["parameter"]) == 2
    for param in parameters["parameter"]:
        assert param["id"] in ["QUERY", "LANG"]
        assert param["value"] in ["SELECT * FROM TAP_SCHEMA.tables", "ADQL"]

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_job_phase(client: TestClient):
    """Test case for get_job_phase

    Returns the job phase
    """

    job_id = build_test_job(client)

    response = client.request(
        "GET",
        f"/uws/{job_id}/phase",
    )

    assert response.status_code == 200
    assert response.text == "PENDING"


def test_get_job_quote(client: TestClient):
    """Test case for get_job_quote

    Returns the job quote
    """

    job_id = build_test_job(client)

    response = client.request(
        "GET",
        f"/uws/{job_id}/quote",
    )

    assert response.status_code == 200
    assert response.text is not None
    assert isinstance(datetime.fromisoformat(response.text), datetime)


def test_get_job_results(client: TestClient):
    """Test case for get_job_results

    Returns the job results
    """

    headers = {}
    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    f"/uws/{job_id}/results",
    #    headers=headers,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_job_summary(client: TestClient):
    """Test case for get_job_summary

    Returns the job summary
    """

    job_id = build_test_job(client)

    response = client.request(
        "GET",
        f"/uws/{job_id}",
    )

    assert response.status_code == 200

    job_summary = response.json()

    assert job_summary["jobId"] == job_id
    assert job_summary["phase"] == "PENDING"
    assert job_summary["parameters"] is not None
    for param in job_summary["parameters"]["parameter"]:
        assert param["id"] in ["QUERY", "LANG"]
        assert param["value"] in ["SELECT * FROM TAP_SCHEMA.tables", "ADQL"]

    # TODO: test wait parameters
    params = [("phase", "PENDING"), ("wait", 56)]
    headers = {}
    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    f"/uws/{job_id}",
    #    headers=headers,
    #    params=params,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_post_create_job(client: TestClient):
    """Test case for post_create_job

    Submits a job
    """
    parameters = SIMPLE_PARAMETERS

    headers = {}
    # uncomment below to make a request
    response = client.request(
        "POST",
        "/uws",
        headers=headers,
        json=parameters,
    )

    assert response.status_code == 200

    job_summary = response.json()

    assert job_summary["jobId"] is not None
    assert job_summary["phase"] == "PENDING"
    assert job_summary["parameters"] is not None


def test_post_update_job(client: TestClient):
    """Test case for post_update_job

    Update job parameters
    """
    post_update_job_request = PostUpdateJobRequest()

    headers = {}
    # uncomment below to make a request
    # response = client.request(
    #    "POST",
    #    f"/uws/{job_id}",
    #    headers=headers,
    #    json=post_update_job_request,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_post_update_job_destruction(client: TestClient):
    """Test case for post_update_job_destruction

    Updates the job destruction time
    """
    post_update_job_destruction_request = PostUpdateJobDestructionRequest()

    headers = {}
    # uncomment below to make a request
    # response = client.request(
    #    "POST",
    #    f"/uws/{job_id}/destruction",
    #    headers=headers,
    #    json=post_update_job_destruction_request,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_post_update_job_execution_duration(client: TestClient):
    """Test case for post_update_job_execution_duration

    Updates the job execution duration
    """
    post_update_job_execution_duration_request = PostUpdateJobExecutionDurationRequest()

    headers = {}
    # uncomment below to make a request
    # response = client.request(
    #    "POST",
    #    f"/uws/{job_id}/executionduration",
    #    headers=headers,
    #    json=post_update_job_execution_duration_request,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_post_update_job_parameters(client: TestClient):
    """Test case for post_update_job_parameters

    Update job parameters
    """
    post_update_job_parameters_request = PostUpdateJobParametersRequest()

    headers = {}
    # uncomment below to make a request
    # response = client.request(
    #    "POST",
    #    f"/uws/{job_id}/parameters",
    #    headers=headers,
    #    json=post_update_job_parameters_request,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_post_update_job_phase(client: TestClient):
    """Test case for post_update_job_phase

    Updates the job phase
    """
    post_update_job_phase_request = PostUpdateJobPhaseRequest()

    headers = {}
    # uncomment below to make a request
    # response = client.request(
    #    "POST",
    #    f"/uws/{job_id}/phase",
    #    headers=headers,
    #    json=post_update_job_phase_request,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
