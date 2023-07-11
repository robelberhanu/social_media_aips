from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..import models, schemas, oauth2
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db



####################################################### POSTS ########################################################

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)
# Get posts path
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts



# send posts to server
@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    print(user_id)
    new_post =  models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# get single post
@router.get("/{id}", response_model= schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
  
    post = db.query(models.Post).filter(models.Post.id == id).first() # will fine the first post with specified ID only. 
    if not post:
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                           detail= f'post with id : {id} not found')
    return post

# Delete post Endpoint
@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
   
    post = db.query(models.Post).filter(models.Post.id == id)
    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update Posts
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


#########################################################End Posts #########################################################

