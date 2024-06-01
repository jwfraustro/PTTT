# coding: utf-8

import importlib
import pkgutil
from datetime import datetime
from uuid import uuid4

import openapi_server.impl
from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)
from fastapi.responses import RedirectResponse
from openapi_server.cache.uws_cache import UWSCache
from openapi_server.models.error_summary import ErrorSummary
from openapi_server.models.execution_phase import ExecutionPhase
from openapi_server.models.job_summary import JobSummary
from openapi_server.models.jobs import Jobs
from openapi_server.models.parameters import Parameters
from openapi_server.models.post_create_job_request import PostCreateJobRequest
from openapi_server.models.post_update_job_destruction_request import PostUpdateJobDestructionRequest
from openapi_server.models.post_update_job_execution_duration_request import PostUpdateJobExecutionDurationRequest
from openapi_server.models.post_update_job_parameters_request import PostUpdateJobParametersRequest
from openapi_server.models.post_update_job_phase_request import PostUpdateJobPhaseRequest
from openapi_server.models.post_update_job_request import PostUpdateJobRequest
from openapi_server.models.results import Results

router = APIRouter()
job_cache = UWSCache()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/uws/",
    responses={
        200: {"model": Jobs, "description": "Any response containing the UWS job list"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["default"],
    summary="Returns the list of UWS jobs",
    response_model_by_alias=True,
)
def get_job_list(
    phase: ExecutionPhase = Query(None, description="Execution phase of the job to filter for", alias="PHASE"),
    after: str = Query(None, description="Return jobs submitted after this date", alias="AFTER"),
    last: int = Query(None, description="Return only the last N jobs", alias="LAST", ge=1),
) -> Jobs:
    # Get list of jobs
    jobs = job_cache.get_job_list()
    return jobs.to_dict()


@router.get(
    "/uws/{job_id}/results",
    responses={
        200: {"model": Results, "description": "Success"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["default"],
    summary="Returns the job results",
    response_model_by_alias=True,
)
def get_job_results(
    job_id: str = Path(..., description="Job ID"),
) -> Results:
    ...


@router.get(
    "/uws/{job_id}/error",
    responses={
        200: {"model": ErrorSummary, "description": "Success"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["default"],
    summary="Returns the job error summary",
    response_model_by_alias=True,
)
def get_job_error_summary(
    job_id: str = Path(..., description="Job ID"),
) -> ErrorSummary:
    ...


@router.get(
    "/uws/{job_id}/phase",
    responses={
        200: {"model": ExecutionPhase, "description": "Success"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["default"],
    summary="Returns the job phase",
    response_model_by_alias=True,
)
def get_job_phase(
    job_id: str = Path(..., description="Job ID"),
) -> ExecutionPhase:
    ...


@router.get(
    "/uws/{job_id}/executionduration",
    responses={
        200: {"model": int, "description": "Success"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["default"],
    summary="Returns the job execution duration",
    response_model_by_alias=True,
)
def get_job_execution_duration(
    job_id: str = Path(..., description="Job ID"),
) -> int:
    ...


@router.get(
    "/uws/{job_id}/destruction",
    responses={
        200: {"model": datetime, "description": "Success"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["default"],
    summary="Returns the job destruction time",
    response_model_by_alias=True,
)
def get_job_destruction(
    job_id: str = Path(..., description="Job ID"),
) -> datetime:
    ...


@router.get(
    "/uws/{job_id}/quote",
    responses={
        200: {"model": datetime, "description": "Success"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["default"],
    summary="Returns the job quote",
    response_model_by_alias=True,
)
def get_job_quote(
    job_id: str = Path(..., description="Job ID"),
) -> datetime:
    ...


@router.get(
    "/uws/{job_id}/parameters",
    responses={
        200: {"model": Parameters, "description": "Success"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["default"],
    summary="Returns the job parameters",
    response_model_by_alias=True,
)
def get_job_parameters(
    job_id: str = Path(..., description="Job ID"),
) -> Parameters:
    ...


@router.post(
    "/uws/{job_id}/parameters",
    responses={
        200: {"model": JobSummary, "description": "Success"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["default"],
    summary="Update job parameters",
    response_model_by_alias=True,
)
def post_update_job_parameters(
    job_id: str = Path(..., description="Job ID"),
    post_update_job_parameters_request: PostUpdateJobParametersRequest = Body(
        None, description="Destruction time to update"
    ),
) -> JobSummary:
    ...


@router.get(
    "/uws/{job_id}/owner",
    responses={
        200: {"model": str, "description": "Success"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["default"],
    summary="Returns the job owner",
    response_model_by_alias=True,
)
def get_job_owner(
    job_id: str = Path(..., description="Job ID"),
) -> str:
    ...


@router.get(
    "/uws/{job_id}",
    responses={
        200: {"model": JobSummary, "description": "Any response containing the job summary"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["default"],
    summary="Returns the job summary",
    response_model_by_alias=True,
)
def get_job_summary(
    job_id: str = Path(..., description="Job ID"),
    phase: str = Query(None, description="Phase of the job to poll for", alias="PHASE"),
    wait: int = Query(None, description="Maximum time to wait for the job to change phases.", alias="WAIT", ge=-1),
) -> JobSummary:
    try:
        job = job_cache.get_job(job_id)
        return job.to_dict()
    except Exception as e:
        return {"error": str(e)}


@router.post(
    "/uws/{job_id}",
    responses={
        200: {
            "model": datetime,
            "description": "Success (when updating a job.) When updating the destruction time, the response is the new destruction time.",
        },
        303: {"model": Jobs, "description": "Any response containing the UWS job list"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["default"],
    summary="Update job parameters",
    response_model_by_alias=True,
)
def post_update_job(
    job_id: str = Path(..., description="Job ID"),
    post_update_job_request: PostUpdateJobRequest = Body(None, description="Parameters to update"),
) -> datetime:
    ...


@router.post(
    "/uws/{job_id}/phase",
    responses={
        303: {"model": JobSummary, "description": "Any response containing the job summary"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["default"],
    summary="Updates the job phase",
    response_model_by_alias=True,
)
def post_update_job_phase(
    job_id: str = Path(..., description="Job ID"),
    post_update_job_phase_request: PostUpdateJobPhaseRequest = Body(None, description="Phase to update"),
) -> None:
    ...


@router.post(
    "/uws/{job_id}/destruction",
    responses={
        303: {"model": datetime, "description": "Success"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["default"],
    summary="Updates the job destruction time",
    response_model_by_alias=True,
)
def post_update_job_destruction(
    job_id: str = Path(..., description="Job ID"),
    post_update_job_destruction_request: PostUpdateJobDestructionRequest = Body(
        None, description="Destruction time to update"
    ),
) -> None:
    ...


@router.post(
    "/uws/{job_id}/executionduration",
    responses={
        303: {"model": JobSummary, "description": "Any response containing the job summary"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["default"],
    summary="Updates the job execution duration",
    response_model_by_alias=True,
)
def post_update_job_execution_duration(
    job_id: str = Path(..., description="Job ID"),
    post_update_job_execution_duration_request: PostUpdateJobExecutionDurationRequest = Body(
        None, description="Execution duration to update"
    ),
) -> None:
    ...


@router.post(
    "/uws/",
    responses={
        303: {"model": JobSummary, "description": "Any response containing the job summary"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["default"],
    summary="Submits a job",
    response_model_by_alias=True,
)
def post_create_job(
    post_create_job_request: PostCreateJobRequest = Body(None, description="Job parameters"),
) -> None:
    job_id = str(uuid4())
    job = JobSummary(
        job_id=job_id,
        phase=ExecutionPhase.PENDING,
        owner="anonymous",
        destruction=datetime.now().isoformat(),
        creation_time=datetime.now().isoformat(),
        execution_duration=0,
    )
    job_cache.add_job(job_id, job)
    return get_job_summary(job_id)


@router.delete(
    "/uws/{job_id}",
    responses={
        200: {"model": Jobs, "description": "Any response containing the UWS job list"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["default"],
    summary="Deletes the job",
    response_model_by_alias=True,
)
def delete_job(
    job_id: str = Path(..., description="Job ID"),
) -> Jobs:
    ...
