# ado_tools.py (Partial example)

import json
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from google.adk.tools import FunctionTool
from pathlib import Path # <-- ADDED: For robust path handling

# --- Configuration ---
SYNTHETIC_DATA_FILE = "synthetic_data.json"

def _load_synthetic_data() -> Dict[str, Any]:
    """Loads the synthetic data from the JSON file."""
    
    # FIX: Construct the absolute path relative to the directory of this file (__file__).
    # This ensures the file is found regardless of where 'adk web' or 'adk run' is executed.
    file_path = Path(__file__).parent / SYNTHETIC_DATA_FILE
    
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Added clarity to the error message for debugging purposes
        print(f"Error: {SYNTHETIC_DATA_FILE} not found at {file_path}. Please create it.")
        return {}

# --- Structured Output Schemas (Pydantic) ---

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


### New method below
class TestResultsResponse(BaseModel):
    build_id: int
    pass_percent: float
    failing_tests_list: List[str]
    flaky_tests_flagged: List[str]

class SecurityFindingsResponse(BaseModel):
    vulnerabilities_by_severity: Dict[str, int]
    unresolved_count: int
    scan_url: str

class DeploymentHistoryResponse(BaseModel):
    last_successful_deployment_staging: str
    last_successful_deployment_prod: str
    release_approvals: Dict[str, str]

class PipelineInfo(BaseModel):
    id: int = Field(description="Unique integer ID of the pipeline.")
    name: str = Field(description="Human-readable name of the pipeline (e.g., 'CI-Build', 'Deployment-to-Prod').")
    is_active: bool = Field(description="True if the pipeline is currently enabled and runnable.")

class PipelineListResponse(BaseModel):
    project_name: str
    pipelines: List[PipelineInfo]
    count: int



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


# # --- Tool 1: Work Items ---
# @FunctionTool(function_model=WorkItemsResponse)
# def ado_query_work_items(project: str, wiql_or_filters: str) -> Dict[str, Any]:
#     """Queries Azure DevOps work items based on WIQL or simple filters (e.g., state, priority)."""
#     data = _load_synthetic_data()
#     # In a real tool, complex filtering logic would be applied here.
#     return {
#         "work_items": data.get("Work_Items", []),
#         "query_details": f"Simulated query for project '{project}' with filters: {wiql_or_filters}"
#     }


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


# --- Tool 2.1: Pipeline list ---
@FunctionTool
def ado_get_pipeline_list(project: str) -> PipelineListResponse:
    """
    Returns a list of all available CI/CD pipelines for the specified Azure DevOps project.
    Always returns a static list for 'MyWebappProject' for demonstration.
    """
    # In a real ADO tool, this would query the ADO API. 
    # Here, we return synthetic data specifically for the project "MyWebappProject".

    pipelines = [
        {"id": 42, "name": "Deployment-to-Prod", "is_active": True},
        {"id": 43, "name": "CI-Build-and-Test", "is_active": True},
        {"id": 44, "name": "Feature-Branch-Validation", "is_active": True},
        {"id": 45, "name": "Old-Release-Pipeline", "is_active": False}
    ]
    return PipelineListResponse(
        project_name=project,
        pipelines=pipelines,
        count=len(pipelines)
    )

    # if project.lower() == "mywebappproject":
    #     pipelines = [
    #         {"id": 42, "name": "Deployment-to-Prod", "is_active": True},
    #         {"id": 43, "name": "CI-Build-and-Test", "is_active": True},
    #         {"id": 44, "name": "Feature-Branch-Validation", "is_active": True},
    #         {"id": 45, "name": "Old-Release-Pipeline", "is_active": False}
    #     ]
    #     return PipelineListResponse(
    #         project_name=project,
    #         pipelines=pipelines,
    #         count=len(pipelines)
    #     )
    # else:
    #     return PipelineListResponse(
    #         project_name=project,
    #         pipelines=[],
    #         count=0
    #     )


# --- Tool 3: Test Results ---
@FunctionTool
def ado_get_test_results(project: str, build_id: int) -> TestResultsResponse:
    """Returns test pass percentage, failing test list, and flaky test flags for a given build."""
    data = _load_synthetic_data()
    # Simulate linking to the latest test results regardless of build_id for simplicity
    #return TestResultsResponse(data.get("Test_Results", {}))
    test_data = data.get("Test_Results", {})
    return TestResultsResponse(**test_data)

    
# --- Tool 4: vulnerability and their  severity---
@FunctionTool
def ado_get_security_findings(project: str) -> SecurityFindingsResponse:
    """Returns vulnerability counts by severity (critical/high/medium) and unresolved counts."""
    data = _load_synthetic_data()
    security_data = data.get("Security_Findings", {})
    return SecurityFindingsResponse(**security_data)

# --- Tool 5: Last successful deployment Status ---
@FunctionTool
def ado_get_deployment_history(project: str) -> DeploymentHistoryResponse:
    """Returns the last successful deployment timestamp for environments and release approvals."""
    data = _load_synthetic_data()
    history = data.get("Deployment_History", {})
    history["release_approvals"] = data.get("Release_Approvals", {})
    return DeploymentHistoryResponse(history)
