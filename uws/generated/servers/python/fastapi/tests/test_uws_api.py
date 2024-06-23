# coding: utf-8

import time
from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from impl.uws_api_impl import simulate_error, simulate_results
from uws_server.main import app
from uws_server.models.error_summary import ErrorSummary  # noqa: F401
from uws_server.models.execution_phase import ExecutionPhase  # noqa: F401
from uws_server.models.job_summary import JobSummary  # noqa: F401
from uws_server.models.jobs import Jobs  # noqa: F401
from uws_server.models.parameters import Parameters  # noqa: F401
from uws_server.models.post_update_job_destruction_request import PostUpdateJobDestructionRequest  # noqa: F401
from uws_server.models.post_update_job_execution_duration_request import (
    PostUpdateJobExecutionDurationRequest,  # noqa: F401
)
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


def test_get_job_error_summary(client: TestClient):
    """Test case for get_job_error_summary

    Returns the job error summary
    """

    job_id = build_test_job(client)

    response = client.request(
        "GET",
        f"/uws/{job_id}/error",
    )

    assert response.status_code == 200
    assert response.text == ""

    simulate_error(job_id, error_message="Error message")

    response = client.request(
        "GET",
        f"/uws/{job_id}/error",
    )

    assert response.status_code == 200
    error_message = response.json()

    assert error_message["message"] == "Error message"
    assert error_message["type"] == "fatal"


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


def test_get_job_list_last(client: TestClient):
    """Test case for get_job_list

    Tests the "last" parameter, which should return the last N jobs
    """

    job_ids = []

    for _ in range(10):
        job_ids.append(build_test_job(client))

    # test "LAST" parameter
    response = client.request(
        "GET",
        "/uws",
        params={"LAST": 5},
    )

    assert response.status_code == 200
    job_list = response.json()

    assert job_list["jobref"] is not None
    assert len(job_list["jobref"]) == 5

    # assert the jobs are in the correct order
    desc_job_list = reversed(job_ids)
    for job_ref in job_list["jobref"]:
        assert job_ref["id"] == next(desc_job_list)


def test_get_job_list_after(client: TestClient):
    """Test case for get_job_list

    Tests the "after" parameter, which should return jobs created after a certain time
    """
    # create a job before the specified time
    build_test_job(client)

    after_time = datetime.now()

    # wait a bit
    time.sleep(2)

    # create a job after the specified time
    job_id_after = build_test_job(client)

    # test "AFTER" parameter
    response = client.request(
        "GET",
        "/uws",
        params={"AFTER": after_time.isoformat()},
    )

    assert response.status_code == 200
    job_list = response.json()

    assert job_list["jobref"] is not None
    assert len(job_list["jobref"]) == 1
    assert job_list["jobref"][0]["id"] == job_id_after


def test_get_job_list_phase(client: TestClient):
    """Test case for get_job_list

    Tests the "phase" parameter, which should return jobs in the specified phase
    """

    # create a job in a few phases
    pending_job = build_test_job(client)
    executing_job = build_test_job(client)
    aborted_job = build_test_job(client)
    archived_job = build_test_job(client)

    # map of job_id to phase
    update_phases = [
        {"job_id": executing_job, "phase": "RUN"},
        {"job_id": aborted_job, "phase": "ABORT"},
        {"job_id": archived_job, "phase": "ARCHIVE"},
    ]

    # update the phases
    for update_phase in update_phases:
        response = client.request(
            "POST",
            f"/uws/{update_phase['job_id']}",
            json={"phase": update_phase["phase"]},
            follow_redirects=False,
        )

        assert response.status_code == 303

    # test the standard job list
    response = client.request(
        "GET",
        "/uws",
    )

    assert response.status_code == 200
    job_list = response.json()

    assert job_list["jobref"] is not None

    # archived job should not be in the list
    assert len(job_list["jobref"]) == 3
    assert archived_job not in [job["id"] for job in job_list["jobref"]]

    # test "PHASE" parameter
    response = client.request(
        "GET",
        "/uws",
        params={"PHASE": "PENDING"},
    )

    assert response.status_code == 200
    job_list = response.json()

    assert job_list["jobref"] is not None
    assert len(job_list["jobref"]) == 1
    assert job_list["jobref"][0]["id"] == pending_job

    # test the other phases
    status_phases = [
        {"job_id": executing_job, "phase": "EXECUTING"},
        {"job_id": aborted_job, "phase": "ABORTED"},
        {"job_id": archived_job, "phase": "ARCHIVED"},
    ]

    for status_phase in status_phases:
        response = client.request(
            "GET",
            "/uws",
            params={"PHASE": status_phase["phase"]},
        )

        assert response.status_code == 200
        job_list = response.json()

        assert job_list["jobref"] is not None
        assert len(job_list["jobref"]) == 1
        assert job_list["jobref"][0]["id"] == status_phase["job_id"]

    # test multiple phases
    response = client.request(
        "GET",
        "/uws",
        params={"PHASE": [ExecutionPhase.PENDING.value, ExecutionPhase.EXECUTING.value]},
    )

    assert response.status_code == 200
    job_list = response.json()

    assert job_list["jobref"] is not None
    assert len(job_list["jobref"]) == 2
    assert pending_job in [job["id"] for job in job_list["jobref"]]
    assert executing_job in [job["id"] for job in job_list["jobref"]]

    # test archived job
    response = client.request(
        "GET",
        "/uws",
        params={"PHASE": ExecutionPhase.ARCHIVED.value},
    )

    assert response.status_code == 200
    job_list = response.json()

    assert job_list["jobref"] is not None
    assert len(job_list["jobref"]) == 1
    assert job_list["jobref"][0]["id"] == archived_job


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

    job_id = build_test_job(client)

    response = client.request(
        "GET",
        f"/uws/{job_id}/results",
    )

    assert response.status_code == 200
    assert response.text == ""

    simulate_results(job_id)

    response = client.request(
        "GET",
        f"/uws/{job_id}/results",
    )

    assert response.status_code == 200

    results = response.json()
    assert results["result"] is not None
    assert len(results["result"]) == 1
    assert results["result"][0]["id"] == "result1"


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

    # test DELETE
    job_id = build_test_job(client)

    response = client.request(
        "POST",
        f"/uws/{job_id}",
        json={"action": "DELETE"},
        follow_redirects=False,
    )

    assert response.status_code == 303

    response = client.request(
        "GET",
        f"/uws/{job_id}",
    )

    assert response.status_code == 404

    # test phase
    job_id = build_test_job(client)

    response = client.request(
        "POST",
        f"/uws/{job_id}",
        json={"phase": "RUN"},
        follow_redirects=False,
    )

    assert response.status_code == 303

    response = client.request(
        "GET",
        f"/uws/{job_id}/phase",
    )

    assert response.status_code == 200
    assert response.text == ExecutionPhase.EXECUTING.value

    # test destruction
    job_id = build_test_job(client)

    new_destruction = datetime.now() + timedelta(days=7)

    response = client.request(
        "POST",
        f"/uws/{job_id}",
        json={"destruction": new_destruction.isoformat()},
        follow_redirects=False,
    )

    assert response.status_code == 303

    response = client.request(
        "GET",
        f"/uws/{job_id}/destruction",
    )

    assert response.status_code == 200
    assert response.text is not None
    assert response.text == new_destruction.isoformat()


def test_post_update_job_destruction(client: TestClient):
    """Test case for post_update_job_destruction

    Updates the job destruction time
    """

    job_id = build_test_job(client)

    response = client.request(
        "GET",
        f"/uws/{job_id}/destruction",
    )
    assert response.status_code == 200
    assert response.text is not None

    destruction = datetime.fromisoformat(response.text)
    # our example destruction is 3 days from now
    assert destruction > datetime.now() + timedelta(days=2)

    new_destruction = datetime.now() + timedelta(days=7)

    response = client.request(
        "POST",
        f"/uws/{job_id}/destruction",
        json={"destruction": new_destruction.isoformat()},
        follow_redirects=False,
    )

    assert response.status_code == 303

    response = client.request(
        "GET",
        f"/uws/{job_id}/destruction",
    )

    assert response.status_code == 200
    assert response.text == new_destruction.isoformat()


def test_post_update_job_execution_duration(client: TestClient):
    """Test case for post_update_job_execution_duration

    Updates the job execution duration
    """

    job_id = build_test_job(client)

    response = client.request(
        "GET",
        f"/uws/{job_id}/executionduration",
    )
    assert response.status_code == 200
    assert response.text == "3600"

    execution_duration = 999

    response = client.request(
        "POST",
        f"/uws/{job_id}/executionduration",
        json={"executionduration": execution_duration},
        follow_redirects=False,
    )

    assert response.status_code == 303

    response = client.request(
        "GET",
        f"/uws/{job_id}/executionduration",
    )

    assert response.status_code == 200
    assert response.text == str(execution_duration)


def test_post_update_job_parameters(client: TestClient):
    """Test case for post_update_job_parameters

    Update job parameters
    """

    job_id = build_test_job(client)

    test_params = {
        "parameter": [
            {"value": "BAD QUERY", "id": "QUERY", "is_post": True, "by_reference": False},
            {"value": "NEW_VALUE", "id": "NEW_PARAM", "is_post": True, "by_reference": False},
        ]
    }

    response = client.request(
        "POST",
        f"/uws/{job_id}/parameters",
        json=test_params,
        follow_redirects=False,
    )

    assert response.status_code == 303

    response = client.request(
        "GET",
        f"/uws/{job_id}/parameters",
    )

    assert response.status_code == 200

    parameters = response.json()

    assert parameters["parameter"] is not None
    for param in parameters["parameter"]:
        if param["id"] == "QUERY":
            assert param["value"] == "BAD QUERY"  # QUERY parameter should have been updated
        if param["id"] == "LANG":
            assert param["value"] == "ADQL"  # LANG should not
        if param["id"] == "NEW_PARAM":
            assert param["value"] == "NEW_VALUE"  # NEW_PARAM should now exist


def test_post_update_job_phase(client: TestClient):
    """Test case for post_update_job_phase

    Updates the job phase
    """

    job_id = build_test_job(client)

    new_phases = [
        ("RUN", ExecutionPhase.EXECUTING),
        ("ABORT", ExecutionPhase.ABORTED),
        ("SUSPEND", ExecutionPhase.SUSPENDED),
        ("ARCHIVE", ExecutionPhase.ARCHIVED),
    ]

    for phase_action, expected_phase in new_phases:
        response = client.request(
            "POST",
            f"/uws/{job_id}/phase",
            json={"phase": phase_action},
            follow_redirects=False,
        )

        assert response.status_code == 303

        response = client.request(
            "GET",
            f"/uws/{job_id}/phase",
        )

        assert response.status_code == 200
        assert response.text == expected_phase.value
