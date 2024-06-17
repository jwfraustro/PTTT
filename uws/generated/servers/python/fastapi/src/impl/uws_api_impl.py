from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from fastapi.responses import JSONResponse, PlainTextResponse, RedirectResponse
from uws_server.apis.uws_api_base import BaseUWSApi
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

        return RedirectResponse(url="/uws", status_code=303)

    def get_job_destruction(
        self,
        job_id: str,
    ) -> datetime:
        job = job_cache.get_job(job_id)
        if not job:
            return JSONResponse(status_code=404, content={"message": "Job not found"})

        if not job.destruction:
            return PlainTextResponse("")
        return PlainTextResponse(content=job.destruction.isoformat())  # pylint:disable=no-member

    def get_job_error_summary(
        self,
        job_id: str,
    ) -> ErrorSummary:
        job = job_cache.get_job(job_id)
        if not job:
            return JSONResponse(status_code=404, content={"message": "Job not found"})
        if not job.error_summary:
            return PlainTextResponse("")
        return job.error_summary

    def get_job_execution_duration(
        self,
        job_id: str,
    ) -> int:
        job = job_cache.get_job(job_id)
        if not job:
            return JSONResponse(status_code=404, content={"message": "Job not found"})
        return PlainTextResponse(content=str(job.execution_duration))

    def get_job_owner(
        self,
        job_id: str,
    ) -> str:
        job = job_cache.get_job(job_id)
        if not job:
            return JSONResponse(status_code=404, content={"message": "Job not found"})
        return PlainTextResponse(content=job.owner_id)

    def get_job_parameters(
        self,
        job_id: str,
    ) -> Parameters:
        job = job_cache.get_job(job_id)
        if not job:
            return JSONResponse(status_code=404, content={"message": "Job not found"})
        return job.parameters

    def get_job_phase(
        self,
        job_id: str,
    ) -> ExecutionPhase:
        job = job_cache.get_job(job_id)
        if not job:
            return JSONResponse(status_code=404, content={"message": "Job not found"})
        return PlainTextResponse(content=job.phase.value)

    def get_job_quote(
        self,
        job_id: str,
    ) -> datetime:
        job = job_cache.get_job(job_id)
        if not job:
            return JSONResponse(status_code=404, content={"message": "Job not found"})
        if not job.quote:
            return PlainTextResponse("")
        return PlainTextResponse(content=job.quote.isoformat())  # pylint:disable=no-member

    def get_job_results(
        self,
        job_id: str,
    ) -> Results:
        job = job_cache.get_job(job_id)
        if not job:
            return JSONResponse(status_code=404, content={"message": "Job not found"})
        if not job.results:
            return PlainTextResponse("")
        return job.results

    def get_job_summary(
        self,
        job_id: str,
        phase: str,
        wait: int,
    ) -> JobSummary:
        job = job_cache.get_job(job_id)
        if not job:
            return JSONResponse(status_code=404, content={"message": "Job not found"})

        return job

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
        job = job_cache.get_job(job_id)
        if not job:
            return JSONResponse(status_code=404, content={"message": "Job not found"})

        phase, destruction, action = (
            post_update_job_request.phase,
            post_update_job_request.destruction,
            post_update_job_request.action,
        )

        # update action first
        # if action is DELETE, there's no need to update phase or destruction
        if action:
            return self.delete_job(job_id)
        if destruction:
            resp = self.post_update_job_destruction(job_id, destruction)
            if resp.status_code != 303:
                return resp
        if phase:
            return self.post_update_job_phase(job_id, phase)

        return RedirectResponse(f"/uws/{job_id}", status_code=303)

    def post_update_job_destruction(
        self,
        job_id: str,
        post_update_job_destruction_request: PostUpdateJobDestructionRequest,
    ) -> None:
        job = job_cache.get_job(job_id)
        if not job:
            return JSONResponse(status_code=404, content={"message": "Job not found"})

        if isinstance(post_update_job_destruction_request, PostUpdateJobDestructionRequest):
            job.destruction = post_update_job_destruction_request.destruction
        else:
            job.destruction = post_update_job_destruction_request

        job_cache.update_job(job_id, job.to_dict())

        return RedirectResponse(f"/uws/{job_id}", status_code=303)

    def post_update_job_execution_duration(
        self,
        job_id: str,
        post_update_job_execution_duration_request: PostUpdateJobExecutionDurationRequest,
    ) -> None:
        job = job_cache.get_job(job_id)
        if not job:
            return JSONResponse(status_code=404, content={"message": "Job not found"})

        job.execution_duration = post_update_job_execution_duration_request.executionduration

        job_cache.update_job(job_id, job.to_dict())

        return RedirectResponse(f"/uws/{job_id}", status_code=303)

    def post_update_job_parameters(
        self,
        job_id: str,
        parameters: Parameters,
    ) -> JobSummary:
        job = job_cache.get_job(job_id)
        if not job:
            return JSONResponse(status_code=404, content={"message": "Job not found"})

        # get the job's current parameters and update them
        curr_params = job.parameters.parameter
        for new_param in parameters.parameter:
            for i, curr_param in enumerate(curr_params):
                if curr_param.id == new_param.id:
                    curr_params[i] = new_param
                    break
            else:
                curr_params.append(new_param)

        job.parameters.parameter = curr_params

        job_cache.update_job(job_id, job.to_dict())

        return RedirectResponse(f"/uws/{job_id}", status_code=303)

    def post_update_job_phase(
        self,
        job_id: str,
        post_update_job_phase_request: PostUpdateJobPhaseRequest,
    ) -> None:
        job = job_cache.get_job(job_id)
        if not job:
            return JSONResponse(status_code=404, content={"message": "Job not found"})

        if isinstance(post_update_job_phase_request, PostUpdateJobPhaseRequest):
            phase = post_update_job_phase_request.phase
        else:
            phase = post_update_job_phase_request

        if phase == "RUN":
            job.phase = ExecutionPhase.EXECUTING
        elif phase == "ABORT":
            job.phase = ExecutionPhase.ABORTED
        elif phase == "SUSPEND":
            job.phase = ExecutionPhase.SUSPENDED
        elif phase == "ARCHIVE":
            job.phase = ExecutionPhase.ARCHIVED

        job_cache.update_job(job_id, job.to_dict())

        return RedirectResponse(f"/uws/{job_id}", status_code=303)


def simulate_error(job_id: str, error_message: str):
    """Simulate an error"""
    job = job_cache.get_job(job_id)
    if not job:
        return JSONResponse(status_code=404, content={"message": "Job not found"})
    job.error_summary = ErrorSummary(message=error_message, type="fatal", hasDetail=False)
    job.phase = ExecutionPhase.ERROR
    job_cache.update_job(job_id, job.to_dict())


def simulate_results(job_id: str):
    """Simulate results"""
    job = job_cache.get_job(job_id)
    if not job:
        return JSONResponse(status_code=404, content={"message": "Job not found"})
    results = Results()
    results.result = [{"id": "result1", "type": "table", "href": "http://example.com/result1"}]
    job.results = results
    job.phase = ExecutionPhase.COMPLETED
    job_cache.update_job(job_id, job.to_dict())
    return job.results
