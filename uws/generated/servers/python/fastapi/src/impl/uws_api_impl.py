from typing import List
from uws_server.apis.uws_api_base import BaseUWSApi
from uws_server.models.execution_phase import ExecutionPhase
from uws_server.models.jobs import Jobs

class UWSAPIImpl(BaseUWSApi):

    def get_job_list(self, phase: List[ExecutionPhase], after: str, last: int) -> Jobs:
        return Jobs(jobref=[{"id":"example"}])
