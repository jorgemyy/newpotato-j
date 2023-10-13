# NewPOTATO: Human-in-the-Loop Open Information Extraction

## Overview
NewPotato is an MVP project aimed at implementing Open Information Extraction (OIE) principles with a Human-in-the-Loop (HITL) approach. The project consists of a backend API built with FastAPI, a frontend built with Streamlit, and a core package named `newpotato` that contains the core logic of the project.

## Features

- Text parsing with graphbrain
- HITL process for refining triplet extraction
- Knowledge graph visualization
- RESTful API for interaction
- Streamlit frontend for user interaction

## Installation

### Pre-requisites
- Python 3.11
- Docker

### Development
#### Backend
The backend functionalities are implemented as a REST API built with FastAPI. The code is located in the `api/` directory.

#### Frontend
The frontend is built using Streamlit and is located in the `frontend/` directory.

#### Core Package
The core functionalities are in the `newpotato` package.

#### Running Locally
To run the project locally for development:

1. Install the dependencies:
    ```bash
    pip install -e .
    ```
2. Start the FastAPI server:
    ```bash
    uvicorn api.main:app --reload
    ```
3. Start the Streamlit app:
    ```bash
    streamlit run frontend/app.py
    ```

#### Running with Docker
The devlopment environment can be also used from .devcontainer in VSCode. It can be found under the .devcontainer folder.

### Production
The production environment is built using Docker Compose. To run the project in production:
```bash
docker-compose -f deploy/docker-compose.yml up
```
