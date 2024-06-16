# coding: utf-8

from typing import Dict, List  # noqa: F401
from datetime import datetime
import importlib
import pkgutil

from uws_server.apis.uws_api_base import BaseUWSApi
import impl

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

from uws_server.models.extra_models import TokenModel  # noqa: F401
from uws_server.models.error_summary import ErrorSummary
from uws_server.models.execution_phase import ExecutionPhase
from uws_server.models.job_summary import JobSummary
from uws_server.models.jobs import Jobs
from uws_server.models.parameters import Parameters
from uws_server.models.post_update_job_destruction_request import PostUpdateJobDestructionRequest
from uws_server.models.post_update_job_execution_duration_request import PostUpdateJobExecutionDurationRequest
from uws_server.models.post_update_job_phase_request import PostUpdateJobPhaseRequest
from uws_server.models.post_update_job_request import PostUpdateJobRequest
from uws_server.models.results import Results


router = APIRouter()

ns_pkg = impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.delete(
    "/uws/{job_id}",
    responses={
        303: {"model": Jobs, "description": "Any response containing the UWS job list"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["UWS"],
    summary="Deletes the job",
    response_model_by_alias=True,
)
async def delete_job(
    job_id: str = Path(..., description="Job ID"),
) -> None:
    
    return BaseUWSApi.subclasses[0]().delete_job(job_id)


@router.get(
    "/uws/{job_id}/destruction",
    responses={
        200: {"model": datetime, "description": "Success"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["UWS"],
    summary="Returns the job destruction time",
    response_model_by_alias=True,
)
async def get_job_destruction(
    job_id: str = Path(..., description="Job ID"),
) -> datetime:
    
    return BaseUWSApi.subclasses[0]().get_job_destruction(job_id)


@router.get(
    "/uws/{job_id}/error",
    responses={
        200: {"model": ErrorSummary, "description": "Success"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["UWS"],
    summary="Returns the job error summary",
    response_model_by_alias=True,
)
async def get_job_error_summary(
    job_id: str = Path(..., description="Job ID"),
) -> ErrorSummary:
    
    return BaseUWSApi.subclasses[0]().get_job_error_summary(job_id)


@router.get(
    "/uws/{job_id}/executionduration",
    responses={
        200: {"model": int, "description": "Success"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["UWS"],
    summary="Returns the job execution duration",
    response_model_by_alias=True,
)
async def get_job_execution_duration(
    job_id: str = Path(..., description="Job ID"),
) -> int:
    
    return BaseUWSApi.subclasses[0]().get_job_execution_duration(job_id)


@router.get(
    "/uws/",
    responses={
        200: {"model": Jobs, "description": "Any response containing the UWS job list"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["UWS"],
    summary="Returns the list of UWS jobs",
    response_model_by_alias=True,
)
async def get_job_list(
    phase: List[ExecutionPhase] = Query(None, description="Execution phase of the job to filter for", alias="PHASE"),
    after: str = Query(None, description="Return jobs submitted after this date", alias="AFTER"),
    last: int = Query(None, description="Return only the last N jobs", alias="LAST", ge=1),
) -> Jobs:
    
    return BaseUWSApi.subclasses[0]().get_job_list(phase, after, last)


@router.get(
    "/uws/{job_id}/owner",
    responses={
        200: {"model": str, "description": "Success"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["UWS"],
    summary="Returns the job owner",
    response_model_by_alias=True,
)
async def get_job_owner(
    job_id: str = Path(..., description="Job ID"),
) -> str:
    
    return BaseUWSApi.subclasses[0]().get_job_owner(job_id)


@router.get(
    "/uws/{job_id}/parameters",
    responses={
        200: {"model": Parameters, "description": "Success"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["UWS"],
    summary="Returns the job parameters",
    response_model_by_alias=True,
)
async def get_job_parameters(
    job_id: str = Path(..., description="Job ID"),
) -> Parameters:
    
    return BaseUWSApi.subclasses[0]().get_job_parameters(job_id)


@router.get(
    "/uws/{job_id}/phase",
    responses={
        200: {"model": ExecutionPhase, "description": "Success"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["UWS"],
    summary="Returns the job phase",
    response_model_by_alias=True,
)
async def get_job_phase(
    job_id: str = Path(..., description="Job ID"),
) -> ExecutionPhase:
    
    return BaseUWSApi.subclasses[0]().get_job_phase(job_id)


@router.get(
    "/uws/{job_id}/quote",
    responses={
        200: {"model": datetime, "description": "Success"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["UWS"],
    summary="Returns the job quote",
    response_model_by_alias=True,
)
async def get_job_quote(
    job_id: str = Path(..., description="Job ID"),
) -> datetime:
    
    return BaseUWSApi.subclasses[0]().get_job_quote(job_id)


@router.get(
    "/uws/{job_id}/results",
    responses={
        200: {"model": Results, "description": "Success"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["UWS"],
    summary="Returns the job results",
    response_model_by_alias=True,
)
async def get_job_results(
    job_id: str = Path(..., description="Job ID"),
) -> Results:
    
    return BaseUWSApi.subclasses[0]().get_job_results(job_id)


@router.get(
    "/uws/{job_id}",
    responses={
        200: {"model": JobSummary, "description": "Any response containing the job summary"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["UWS"],
    summary="Returns the job summary",
    response_model_by_alias=True,
)
async def get_job_summary(
    job_id: str = Path(..., description="Job ID"),
    phase: str = Query(None, description="Phase of the job to poll for", alias="PHASE"),
    wait: int = Query(None, description="Maximum time to wait for the job to change phases.", alias="WAIT", ge=-1),
) -> JobSummary:
    
    return BaseUWSApi.subclasses[0]().get_job_summary(job_id, phase, wait)


@router.post(
    "/uws/",
    responses={
        303: {"model": JobSummary, "description": "Any response containing the job summary"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["UWS"],
    summary="Submits a job",
    response_model_by_alias=True,
)
async def post_create_job(
    parameters: Parameters = Body(None, description="Job parameters"),
) -> None:
    
    return BaseUWSApi.subclasses[0]().post_create_job(parameters)


@router.post(
    "/uws/{job_id}",
    responses={
        200: {"model": datetime, "description": "Success (when updating a job.) When updating the destruction time, the response is the new destruction time."},
        303: {"model": Jobs, "description": "Any response containing the UWS job list"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["UWS"],
    summary="Update job parameters",
    response_model_by_alias=True,
)
async def post_update_job(
    job_id: str = Path(..., description="Job ID"),
    post_update_job_request: PostUpdateJobRequest = Body(None, description="Parameters to update"),
) -> datetime:
    
    return BaseUWSApi.subclasses[0]().post_update_job(job_id, post_update_job_request)


@router.post(
    "/uws/{job_id}/destruction",
    responses={
        303: {"model": datetime, "description": "Success"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["UWS"],
    summary="Updates the job destruction time",
    response_model_by_alias=True,
)
async def post_update_job_destruction(
    job_id: str = Path(..., description="Job ID"),
    post_update_job_destruction_request: PostUpdateJobDestructionRequest = Body(None, description="Destruction time to update"),
) -> None:
    
    return BaseUWSApi.subclasses[0]().post_update_job_destruction(job_id, post_update_job_destruction_request)


@router.post(
    "/uws/{job_id}/executionduration",
    responses={
        303: {"model": JobSummary, "description": "Any response containing the job summary"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["UWS"],
    summary="Updates the job execution duration",
    response_model_by_alias=True,
)
async def post_update_job_execution_duration(
    job_id: str = Path(..., description="Job ID"),
    post_update_job_execution_duration_request: PostUpdateJobExecutionDurationRequest = Body(None, description="Execution duration to update"),
) -> None:
    
    return BaseUWSApi.subclasses[0]().post_update_job_execution_duration(job_id, post_update_job_execution_duration_request)


@router.post(
    "/uws/{job_id}/parameters",
    responses={
        303: {"model": JobSummary, "description": "Success"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["UWS"],
    summary="Update job parameters",
    response_model_by_alias=True,
)
async def post_update_job_parameters(
    job_id: str = Path(..., description="Job ID"),
    parameters: Parameters = Body(None, description="Parameters to update"),
) -> None:
    
    return BaseUWSApi.subclasses[0]().post_update_job_parameters(job_id, parameters)


@router.post(
    "/uws/{job_id}/phase",
    responses={
        303: {"model": JobSummary, "description": "Any response containing the job summary"},
        403: {"model": object, "description": "Forbidden"},
        404: {"model": object, "description": "Job not found"},
    },
    tags=["UWS"],
    summary="Updates the job phase",
    response_model_by_alias=True,
)
async def post_update_job_phase(
    job_id: str = Path(..., description="Job ID"),
    post_update_job_phase_request: PostUpdateJobPhaseRequest = Body(None, description="Phase to update"),
) -> None:
    
    return BaseUWSApi.subclasses[0]().post_update_job_phase(job_id, post_update_job_phase_request)
