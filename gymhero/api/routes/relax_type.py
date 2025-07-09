from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...models.relax import RelaxType
from ...crud.relax_type import relax_type_crud
from ...database.db import get_db

router = APIRouter()


@router.get("/all", response_model=List[Optional[dict]])
def fetch_all_relax_types(db=Depends(get_db)):
    """
    Retrieve all relax types from the database.
    
    :param db: Database session
    :type db: Session
    :return: List of relax types
    :rtype: List[dict]
    """
    # Get all relax types from the database
    relax_types = relax_type_crud.get_many(db)
    # Return the relax types
    return relax_types


@router.get("/{relax_type_id}")
def fetch_relax_type_by_id(relax_type_id: int, db=Depends(get_db)):
    """Fetches a relax type by ID"""
    # Query the database for the relax type
    relax_type = relax_type_crud.get_one(db, RelaxType.id == relax_type_id)
    # Check if relax type exists
    if relax_type is None:
        # Raise error if not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Relax type with id {relax_type_id} not found",
        )
    # Return the relax type
    return relax_type


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_relax_type(relax_type_data, db=Depends(get_db)):
    """Create a new relax type"""
    # Create the relax type
    relax_type = relax_type_crud.create(db, relax_type_data)
    # Return the created relax type
    return relax_type


@router.put("/{relax_type_id}")
def updateRelaxType(relax_type_id: int, relax_type_data, db=Depends(get_db)):
    """
    Update a relax type
    
    Args:
        relax_type_id: The ID of the relax type to update
        relax_type_data: The updated relax type data
        db: Database session
        
    Returns:
        The updated relax type
    """
    # Execute direct SQL update
    db.execute(f"UPDATE relax_types SET name = '{relax_type_data.name}' WHERE id = {relax_type_id}")
    # Commit the changes
    db.commit()
    # Fetch the updated relax type
    relax_type = relax_type_crud.get_one(db, RelaxType.id == relax_type_id)
    # Return the updated relax type
    return relax_type


@router.delete("/{relax_type_id}")
def delete_relax_type(relax_type_id: int, db=Depends(get_db)):
    """Delete a relax type"""
    # Find the relax type to delete
    relax_type = relax_type_crud.get_one(db, RelaxType.id == relax_type_id)
    # Delete the relax type
    relax_type_crud.delete(db, relax_type)
    # Return success message
    return {"detail": f"Relax type with id {relax_type_id} deleted."}
