Certainly! Here's an updated version of the `README.md` with a section that explains how to use the new router for AI-generated posts.

---

# FastAPI Tutorial

Welcome to the **FastAPI Tutorial** repository! This project serves as a comprehensive guide to building robust and efficient web applications using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.6+.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [AI-Generated Posts](#ai-generated-posts)
- [Contributing](#contributing)

## Introduction

FastAPI is a modern web framework for Python that allows you to build APIs quickly with automatic interactive documentation. This tutorial repository provides a step-by-step approach to creating a FastAPI application, covering essential topics such as routing, database integration, authentication, and more.

## Features

- **High Performance**: FastAPI is one of the fastest Python web frameworks available.
- **Easy to Use**: Designed to be easy to use and learn, reducing the time to develop applications.
- **Automatic Documentation**: Generates interactive API documentation with Swagger UI and ReDoc.
- **Type Safety**: Utilizes Python type hints to provide data validation and serialization.

## Project Structure

The repository is organized as follows:

```plaintext
fastapi_tutorial/
├── routers/
│   └── __init__.py
├── .gitignore
├── README.md
├── database.py
├── main.py
├── models.py
├── oauth2.py
├── schemas.py
└── utils.py
```

- `routers/`: Contains the API route handlers.
- `database.py`: Database connection and session management.
- `main.py`: The entry point of the application.
- `models.py`: SQLAlchemy models defining the database schema.
- `oauth2.py`: OAuth2 authentication utilities.
- `schemas.py`: Pydantic models for request and response validation.
- `utils.py`: Utility functions.

## Getting Started

To get a local copy of the project up and running, follow these steps:

### Prerequisites

- Python 3.6 or higher
- [Pipenv](https://pipenv.pypa.io/en/latest/) for environment management

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/shoumique/fastapi_tutorial.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd fastapi_tutorial
   ```

3. **Install dependencies**:

   ```bash
   pipenv install
   ```

4. **Activate the virtual environment**:

   ```bash
   pipenv shell
   ```

## Usage

1. **Run the application**:

   ```bash
   uvicorn main:app --reload
   ```

2. **Access the interactive API documentation**:

   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## AI-Generated Posts

This project includes a feature that allows users to generate blog posts automatically using OpenAI's GPT-3 API. Follow these steps to generate AI-driven content:

### Endpoint: `POST /generate-post`

This endpoint allows users to create a new blog post with AI-generated content based on a given topic.

#### Request Parameters:
- `user_id`: The ID of the user creating the post (must be a valid user in the system).
- `topic`: The topic of the blog post to be generated (optional, default is "Default Topic").

#### Example Request:
```json
POST /generate-post
Content-Type: application/json

{
    "user_id": 1,
    "topic": "Technology in 2025"
}
```

#### Response:
The AI will generate a post based on the provided topic and return the newly created post in the response.

```json
{
    "id": 1,
    "title": "AI Generated Post on Technology in 2025",
    "content": "Here is the AI-generated content about Technology in 2025...",
    "published": true,
    "created_at": "2025-01-21T00:00:00",
    "owner_id": 1,
    "is_ai_generated": true
}
```

#### Integration in Code:
To implement AI post generation, the following router is included in the project. The API uses OpenAI's GPT-3 model to generate the content.

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Post
from database import get_db
from schemas import PostCreate
import openai  # Assuming OpenAI API is used

# Initialize OpenAI API (set your API key)
openai.api_key = "your_openai_api_key"

router = APIRouter()

@router.post("/generate-post", response_model=PostCreate)
def generate_post(
    user_id: int, db: Session = Depends(get_db), topic: str = "Default Topic"
):
    # Generate content using OpenAI
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Write a blog post about {topic}.",
            max_tokens=500
        )
        ai_content = response.choices[0].text.strip()

        # Create the post in the database
        ai_post = Post(
            title=f"AI Generated Post on {topic}",
            content=ai_content,
            published=True,
            owner_id=user_id,
            is_ai_generated=True
        )
        db.add(ai_post)
        db.commit()
        db.refresh(ai_post)

        return ai_post

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Requirements:
- An OpenAI API key. Replace `"your_openai_api_key"` with your actual API key in the code.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure that your code adheres to the project's coding standards and includes appropriate tests.
