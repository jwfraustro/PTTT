from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from fastapi.responses import JSONResponse
from uws_server.apis.uws_api_base import BaseUWSApi
from uws_server.models.error_summary import ErrorSummary
from uws_server.models.execution_phase import ExecutionPhase
from uws_server.models.job_summary import JobSummary
from uws_server.models.jobs import Jobs
from uws_server.models.parameters import Parameters
from uws_server.models.post_update_job_destruction_request import PostUpdateJobDestructionRequest
from uws_server.models.post_update_job_execution_duration_request import PostUpdateJobExecutionDurationRequest
from uws_server.models.post_update_job_parameters_request import PostUpdateJobParametersRequest
from uws_server.models.post_update_job_phase_request import PostUpdateJobPhaseRequest
from uws_server.models.post_update_job_request import PostUpdateJobRequest
from uws_server.models.results import Results

from impl.cache.uws_cache import UWSCache

job_cache = UWSCache()


class UWSAPIImpl(BaseUWSApi):
    def get_job_list(
        self, phase: List[ExecutionPhase] = [], after: Optional[str] = None, last: Optional[int] = None
    ) -> Jobs:
        return job_cache.get_jobs(phase, after, last)

    def delete_job(
        self,
        job_id: str,
    ) -> Jobs:
        if not job_cache.get_job(job_id):
            return JSONResponse(status_code=404, content={"message": "Job not found"})

        job_cache.delete_job(job_id)

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
        return job_cache.get_job(job_id, phase, wait)

    def post_create_job(
        self,
        parameters: Parameters,
    ) -> None:
        job_id = str(uuid4())
        job = JobSummary(
            job_id=job_id,
            creationTime=datetime.now().isoformat(),
            phase=ExecutionPhase.PENDING,
            parameters=parameters,
        )
        job_cache.add_job(job_id, job.to_dict())
        return self.get_job_summary(job_id, None, None)

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
