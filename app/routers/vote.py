from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    #raise an exception if the user is trying to vote on a post that does not exist in the "posts" table in database
    verify_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not verify_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {vote.post_id} does not exist")

    #query vote table to see if current user has already voted on the specified post
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
    #vote dir of 1 indicates that the user intends to vote/like the post
    if (vote.dir == 1):
        
        #raise an exception if user has already voted on the post (user cannot vote on the same post multiple times)
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user with id: {current_user.id} has already voted on post with id: {vote.post_id}")
        
        #create new entry in vote table if user has not already voted on the post
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()

        return{"message": "successfully added vote"}
    
    else:

        #raise an exception if user is trying to remove a vote on a post that they have not voted on previously
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {current_user.id} has not voted on post with id: {vote.post_id}")
        
        #remove vote from post
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfuly removed vote"}
        