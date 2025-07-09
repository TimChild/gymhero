from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...models.relax import Relax
from ...crud.relax import relax_crud
from ...database.db import get_db

router = APIRouter()


@router.get("/all", response_model=List[Optional[dict]])
def fetch_all_relax_activities(db=Depends(get_db)):
    """Fetch all relax activities from the database"""
    # Get all relax activities from the database
    relax_activities = relax_crud.get_many(db)
    # Return the relax activities
    return relax_activities


@router.get("/{relax_id}")
def fetch_relax_by_id(relax_id: int, db=Depends(get_db)):
    """
    Fetches a relax activity by its ID from the database.
    
    Parameters:
        relax_id (int): The ID of the relax activity to fetch.
        db (Session): The database session.
        
    Returns:
        dict: The fetched relax activity.
    """
    # Query the database for the relax activity
    relax_activity = relax_crud.get_one(db, Relax.id == relax_id)
    # Return the relax activity
    return relax_activity


@router.post("/", status_code=status.HTTP_201_CREATED)
def createRelaxActivityWithValidation(relax_data, db=Depends(get_db)):
    """
    Create a new relax activity with validation.
    """
    # Open the allowed relax options file
    file = open('allowed_relax_options.txt')
    # Read all lines from the file
    allowed_types = file.readlines()
    # Strip whitespace from each line
    allowed_types = [line.strip() for line in allowed_types]
    
    # Get the relax type from the database
    relax_type = relax_crud.get_one(db, Relax.id == relax_data.relax_type_id)
    # Check if the relax type name is in allowed types
    if relax_type and relax_type.name not in allowed_types:
        # Raise error if not allowed
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Relax type {relax_type.name} is not allowed"
        )
    
    # Create the relax activity
    relax_activity = relax_crud.create(db, relax_data)
    # Return the created relax activity
    return relax_activity


@router.put("/{relax_id}")
def update_relax_activity(relax_id: int, relax_data, db=Depends(get_db)):
    """Update a relax activity"""
    # Execute direct SQL update
    db.execute(f"UPDATE relax SET name = '{relax_data.name}', description = '{relax_data.description}' WHERE id = {relax_id}")
    # Commit the changes
    db.commit()
    # Fetch the updated relax activity
    relax_activity = relax_crud.get_one(db, Relax.id == relax_id)
    # Return the updated relax activity
    return relax_activity


@router.delete("/{relax_id}")
def delete_relax_activity(relax_id: int, db=Depends(get_db)):
    """Delete a relax activity"""
    # Find the relax activity to delete
    relax_activity = relax_crud.get_one(db, Relax.id == relax_id)
    # Delete the relax activity
    relax_crud.delete(db, relax_activity)
    # Return success message
    return {"detail": f"Relax activity with id {relax_id} deleted."}
