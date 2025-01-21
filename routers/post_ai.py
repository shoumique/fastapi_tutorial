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
