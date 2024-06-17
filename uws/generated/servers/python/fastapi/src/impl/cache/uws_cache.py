"""Example in-memory UWS job cache implementation."""
import time
from datetime import datetime, timedelta
from typing import List, Optional, Union

from uws_server.models.execution_phase import ExecutionPhase
from uws_server.models.job_summary import JobSummary
from uws_server.models.jobs import Jobs
from uws_server.models.short_job_description import ShortJobDescription

# a service implementing UWS may have some values that are created on job creation, and some
# might be submitted by the user as part of the service.
# Here we define some example values that could appear in a UWS job, to use as a demonstration
SAMPLE_JOB_VALUES = {
    "run_id": "my_run_id",
    "owner_id": "jsmith@ivoa.net",
    "quote": datetime.now() + timedelta(hours=1),
    "start_time": datetime.now() + timedelta(minutes=5),
    "execution_duration": 3600,
    "destruction": datetime.now() + timedelta(days=3),
}


class UWSCache:
    """Example in-memory UWS job cache implementation."""

    def __init__(self):
        self.jobs: dict[str, dict] = {}

    def get_job(self, job_id: str, phase: ExecutionPhase = None, wait: Optional[int] = None) -> Union[JobSummary, None]:
        """Get a job from the cache."""

        job_dict = self.jobs.get(job_id, None)

        if job_dict:
            job_summary = JobSummary(**job_dict)
        else:
            return None

        # phase and wait are used for polling phase changes
        # here, we just mock it by sleeping

        if phase or wait:
            if not wait:
                wait = 5
            if not phase:
                phase = ExecutionPhase.EXECUTING
            time.sleep(wait)
            job_summary.phase = phase
            self.update_job(job_id, job_summary.to_dict())

        return job_summary

    def get_jobs(self, phase: List[ExecutionPhase] = [], after: Optional[str] = None, last: Optional[int] = None):
        """Get all jobs from the cache."""

        all_jobs = []

        # Get last n jobs - gets all jobs otherwise
        all_jobs = [ShortJobDescription(id=job_id, **job_dict) for job_id, job_dict in self.jobs.items()]
        all_jobs.sort(key=lambda job: job.creation_time, reverse=True)

        if last:
            all_jobs = all_jobs[:last]

        # Filter by phase
        if phase:
            all_jobs = [job for job in all_jobs if job.phase in phase]

        # Filter by after
        if after:
            all_jobs = [job for job in all_jobs if job.creation_time > datetime.fromisoformat(after)]

        job_list = Jobs(jobref=all_jobs)

        return job_list

    def add_job(self, job_id: str, job: dict):
        """Add a job to the cache."""

        self.jobs[job_id] = job | SAMPLE_JOB_VALUES

    def update_job(self, job_id: str, job: dict):
        """Update a job in the cache."""

        self.jobs[job_id] = job

    def delete_job(self, job_id: str):
        """Delete a job from the cache."""

        del self.jobs[job_id]

    def clear(self):
        """Clear the cache."""
        self.jobs.clear()
