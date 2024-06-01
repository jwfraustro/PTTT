"""Basic in-memory example cache for UWS jobs."""

from uuid import uuid4

from openapi_server.models.job_summary import JobSummary
from openapi_server.models.jobs import Jobs
from openapi_server.models.short_job_description import ShortJobDescription


class BasicCache:
    def __init__(self):
        self._store = {}

    def add(self, value: object, key: str = None):
        if not key:
            key = str(uuid4())
        self._store[key] = value

    def get(self, key: str):
        return self._store.get(key)

    def get_all(self):
        return self._store

    def remove(self, key: str):
        if key in self._store:
            del self._store[key]

    def clear(self):
        self._store.clear()


class UWSCache(BasicCache):
    def __init__(self):
        super().__init__()

    def add_job(self, job_id: str, job: object):
        self.add(job, job_id)

    def get_job(self, job_id: str) -> JobSummary:
        return self.get(job_id)

    def remove_job(self, job_id: str):
        self.remove(job_id)

    def clear_jobs(self):
        self.clear()

    def get_job_list(self, phase: str = None, after: str = None, last: int = None):
        jobs: dict[str, JobSummary] = self.get_all()
        job_list = Jobs(jobref=[])

        for job_id, job in jobs.items():
            job_list.jobref.append(ShortJobDescription(**job.to_dict(), href=f"/jobs/{job_id}"))

        return job_list
