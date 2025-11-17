from .base import *

model = initialize_model()

# Master Orchestrator Agent
orchestrator_agent = Agent(
    name="orchestrator",
    model=model,
    instruction="""You are the Master Orchestrator for AIDE. Coordinate the multi-agent web development process."""
)

# Requirements Evolver Agent
requirements_evolver_agent = Agent(
    name="requirements_evolver",
    model=model,
    instruction="""You are the Requirements Evolver Agent. Conduct evolutionary Q&A to extract detailed project requirements."""
)

# Frontend Ensemble
ux_architect_agent = Agent(
    name="ux_architect",
    model=model,
    instruction="""You are the UX Architect Agent. Focus on USER FLOW and INFORMATION ARCHITECTURE."""
)

ui_designer_agent = Agent(
    name="ui_designer",
    model=model,
    instruction="""You are the UI Designer Agent. Focus on VISUAL DESIGN and LAYOUT."""
)

frontend_engineer_agent = Agent(
    name="frontend_engineer",
    model=model,
    instruction="""You are the Frontend Engineer Agent. Focus on TECHNICAL IMPLEMENTATION."""
)

# Backend Ensemble
data_architect_agent = Agent(
    name="data_architect",
    model=model,
    instruction="""You are the Data Architect Agent. Focus on DATA DESIGN and STORAGE."""
)

api_designer_agent = Agent(
    name="api_designer",
    model=model,
    instruction="""You are the API Designer Agent. Focus on SERVER LOGIC and ENDPOINTS."""
)

devops_agent = Agent(
    name="devops",
    model=model,
    instruction="""You are the DevOps Agent. Focus on DEPLOYMENT and INFRASTRUCTURE."""
)

# Quality Tier
validation_agent = Agent(
    name="validation",
    model=model,
    instruction="""You are the Validation Agent. Focus on REQUIREMENT CONSISTENCY."""
)

code_quality_agent = Agent(
    name="code_quality",
    model=model,
    instruction="""You are the Code Quality Agent. Focus on TECHNICAL EXCELLENCE."""
)

integration_agent = Agent(
    name="integration",
    model=model,
    instruction="""You are the Integration Agent. Focus on SYSTEM COHESION."""
)

# Agent Registry
agent_registry = {
    "requirements_evolver": requirements_evolver_agent,
    "ux_architect": ux_architect_agent,
    "ui_designer": ui_designer_agent,
    "frontend_engineer": frontend_engineer_agent,
    "data_architect": data_architect_agent,
    "api_designer": api_designer_agent,
    "devops": devops_agent,
    "validation": validation_agent,
    "code_quality": code_quality_agent,
    "integration": integration_agent
}

print("✅ All agents initialized successfully!")