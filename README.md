# FastAPI Ranked Choice Voting (RCV)

A simple demonstration of Ranked Choice (Instant-Runoff) Voting using [FastAPI](https://fastapi.tiangolo.com/) for server-side logic and Jinja2 templates for HTML rendering. This project is pre-configured for **GitHub Codespaces**, complete with a `.devcontainer` directory for a Docker-based development environment.

---

## Table of Contents

1. [Features](#features)  
2. [Project Structure](#project-structure)  
3. [Getting Started in Codespaces](#getting-started-in-codespaces)  
4. [Local Development (Optional)](#local-development-optional)  
5. [Usage](#usage)  
6. [How it Works](#how-it-works)  
7. [Future Improvements](#future-improvements)  
8. [License](#license)

---

## Features

- **Instant-Runoff Voting Algorithm**  
  - Collects ballots with up to 3 ranked choices (easily extendable).  
  - Eliminates lowest-polling candidates in each round until a winner emerges.

- **FastAPI**  
  - Lightweight, high-performance, and modern Python framework.  
  - Async-ready if needed (though this example uses simple sync code).

- **Jinja2 Templating**  
  - Renders the Start, Vote, and Closed pages for a simple user interface.

- **Docker & Codespaces Integration**  
  - A `Dockerfile` to containerize the app.  
  - A `.devcontainer/devcontainer.json` for easy spin-up in GitHub Codespaces.

---

## Project Structure

```text
fastapi-rcv/
├── .devcontainer/
│   └── devcontainer.json
├── Dockerfile
├── main.py
├── requirements.txt
└── templates/
    ├── closed.html
    ├── start.html
    └── vote.html
