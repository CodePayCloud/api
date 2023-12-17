from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse
from fastapi.openapi.models import Info, ExternalDocumentation
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from typing import Optional, List
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import uuid
from docker import DockerClient

client = DockerClient.from_env()

app = FastAPI(
    title="CodePay Cloud API",
    description="An API to get coders paid.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Pricing",
            "description": "Workspaces, Deployments, Projects.",
        }
    ],
    info=Info(
        title="CodePay Cloud API",
        version="1.0.0",
        description="An API to get coders paid.",
        terms_of_service="https://codepay.cloud/terms",
    ),
    external_docs=ExternalDocumentation(
        description="Find more information here",
        url="https://codepay.cloud",
    ),
)

origins = [
    "http://localhost:3000",  # React app
    "https://codepay.cloud",  # Production site
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return RedirectResponse(url='/docs')

@app.get("/deploy")
async def deploy():
    return {"deployment": "url"}

@app.get("/workspace/{name}")
async def workspace(name: str):
    container = client.containers.run(
        "codercom/code-server",  # Docker image for VS Code server
        detach=True,  # Run in detached mode
        ports={'8080/tcp': 8080},  # Map container's port 8080 to host's port 8080
        environment=["PASSWORD=yourpassword"],  # Set the password for the VS Code server
        name=name  # Name of the container
    )
    return {"workspace": f"http://localhost:8080"}

@app.get("/request")
async def request():
    return {"request": "request"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
