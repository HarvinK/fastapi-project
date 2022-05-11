from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func #required for COUNT() function in query
from .. import models, oauth2, schemas, database


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

# get all posts
@router.get("/", response_model=List[schemas.PostOUT])
def get_posts(db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # SQLALCHEMY query retrieve all posts AND votes using LEFT OUTER join (SQLALCHEMY uses LEFT INNER join as default so we must set "isouter" parameter to True)
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # SQLALCHEMY query to obtain ONLY posts (with specified filters)
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # Query below will only return posts that are associated with the logged in user. Uncomment to implement.
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    return posts

# create post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# get single post (with specidied id)
@router.get("/{id}", response_model=schemas.PostOUT)
def get_post(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
   
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    
    # SQLALCHEMY query to get single post, and join the votes total for that post
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    # statement below can be used if intent is to restrict post access to the owner of the post
    # if post.owner_id != current_user.id:
        # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    return post

# delete single post (with specified id)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # defining query
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # find first post that matches the criteria, and store it in a variable
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    # delete post
    post_query.delete(synchronize_session=False)
    # commit changes to database
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# update single post (with specified id)
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # defining query
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # find first post that matches the criteria, and store it in a variable
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    # checks to see if post belongs to user
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()

    return post_query.first()