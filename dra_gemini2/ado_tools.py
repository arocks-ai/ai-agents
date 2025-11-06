# ado_tools.py (Partial example)

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import json

# --- 1. Work Item Schema ---
class WorkItem(BaseModel):
    id: int = Field(description="Unique work item ID.")
    title: str
    type: str
    state: str = Field(description="e.g., 'New', 'Active', 'Resolved', 'Closed'")
    priority: int
    assignee: str
    tags: List[str]
    is_blocking: bool
    acceptance_criteria: str
    url: str

class WorkItemsResponse(BaseModel):
    work_items: List[WorkItem]
    query_details: str

# --- 2. Pipeline Status Schema ---
class PipelineRun(BaseModel):
    build_id: int
    status: str = Field(description="e.g., 'Succeeded', 'Failed', 'PartiallySucceeded'")
    duration_seconds: int
    failing_stages: List[str]
    artifacts: List[str]

class PipelineStatusResponse(BaseModel):
    pipeline_id: int
    pipeline_name: str
    last_n_runs: List[PipelineRun]

# ... Define TestResultsResponse, SecurityFindingsResponse, DeploymentHistoryResponse

# ado_tools.py (Tool functions example)

from google.adk.tools import FunctionTool

SYNTHETIC_DATA_FILE = "synthetic_data.json"

def _load_synthetic_data() -> Dict[str, Any]:
    with open(SYNTHETIC_DATA_FILE, 'r') as f:
        return json.load(f)

# --- Tool 1: Work Items ---
@FunctionTool
def ado_query_work_items(project: str, wiql_or_filters: str) -> WorkItemsResponse:
    """Queries Azure DevOps work items based on WIQL or simple filters like state or priority."""
    data = _load_synthetic_data()
    # In a real implementation, you'd execute the query/filters against the 'Work_Items' data.
    # For simulation, we return a subset of the data based on simple logic or the whole list.
    return WorkItemsResponse(
        work_items=data["Work_Items"],
        query_details=f"Simulated query for project {project} with filters: {wiql_or_filters}"
    )

# --- Tool 2: Pipeline Status ---
@FunctionTool
def ado_get_pipeline_status(project: str, pipeline_id: int) -> PipelineStatusResponse:
    """Returns the status and details for the last N runs of a specific pipeline."""
    data = _load_synthetic_data()
    # Find the pipeline data in the synthetic dataset and return
    pipeline_data = next((p for p in data["Pipelines"] if p["pipeline_id"] == pipeline_id), None)
    if pipeline_data:
        return PipelineStatusResponse(**pipeline_data)
    else:
        # Return a mock failure or empty response if not found
        return PipelineStatusResponse(pipeline_id=pipeline_id, pipeline_name="Not Found", last_n_runs=[])

# ... Define other tools: get_test_results, get_security_findings, etc.