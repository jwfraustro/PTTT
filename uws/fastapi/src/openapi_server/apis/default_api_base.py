# coding: utf-8

from datetime import datetime
from typing import ClassVar, Tuple  # noqa: F401

from openapi_server.models.error_summary import ErrorSummary
from openapi_server.models.execution_phase import ExecutionPhase
from openapi_server.models.job_summary import JobSummary
from openapi_server.models.jobs import Jobs
from openapi_server.models.parameters import Parameters
from openapi_server.models.post_create_job_request import PostCreateJobRequest
from openapi_server.models.post_update_job_destruction_request import (
    PostUpdateJobDestructionRequest,
)
from openapi_server.models.post_update_job_execution_duration_request import (
    PostUpdateJobExecutionDurationRequest,
)
from openapi_server.models.post_update_job_parameters_request import (
    PostUpdateJobParametersRequest,
)
from openapi_server.models.post_update_job_phase_request import (
    PostUpdateJobPhaseRequest,
)
from openapi_server.models.post_update_job_request import PostUpdateJobRequest
from openapi_server.models.results import Results


class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)
    def delete_job(
        self,
        job_id: str,
    ) -> Jobs:
        ...


    def get_job_destruction(
        self,
        job_id: str,
    ) -> datetime:
        ...


    def get_job_error_summary(
        self,
        job_id: str,
    ) -> ErrorSummary:
        ...


    def get_job_execution_duration(
        self,
        job_id: str,
    ) -> int:
        ...


    def get_job_list(
        self,
        phase: ExecutionPhase,
        after: str,
        last: int,
    ) -> Jobs:
        ...


    def get_job_owner(
        self,
        job_id: str,
    ) -> str:
        ...


    def get_job_parameters(
        self,
        job_id: str,
    ) -> Parameters:
        ...


    def get_job_phase(
        self,
        job_id: str,
    ) -> ExecutionPhase:
        ...


    def get_job_quote(
        self,
        job_id: str,
    ) -> datetime:
        ...


    def get_job_results(
        self,
        job_id: str,
    ) -> Results:
        ...


    def get_job_summary(
        self,
        job_id: str,
        phase: str,
        wait: int,
    ) -> JobSummary:
        ...


    def post_create_job(
        self,
        post_create_job_request: PostCreateJobRequest,
    ) -> None:
        ...


    def post_update_job(
        self,
        job_id: str,
        post_update_job_request: PostUpdateJobRequest,
    ) -> datetime:
        ...


    def post_update_job_destruction(
        self,
        job_id: str,
        post_update_job_destruction_request: PostUpdateJobDestructionRequest,
    ) -> None:
        ...


    def post_update_job_execution_duration(
        self,
        job_id: str,
        post_update_job_execution_duration_request: PostUpdateJobExecutionDurationRequest,
    ) -> None:
        ...


    def post_update_job_parameters(
        self,
        job_id: str,
        post_update_job_parameters_request: PostUpdateJobParametersRequest,
    ) -> JobSummary:
        ...


    def post_update_job_phase(
        self,
        job_id: str,
        post_update_job_phase_request: PostUpdateJobPhaseRequest,
    ) -> None:
        ...
