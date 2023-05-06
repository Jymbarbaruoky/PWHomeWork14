from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Path
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository import contacts as repository_contacts
from src.schemas import ContactResponse, ContactModel
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED,
             description='No more than 1 contact per minute',
             dependencies=[Depends(RateLimiter(seconds=60))])
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         _current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.
        The function takes a ContactModel object as input, and returns the newly created contact.

    :param body: ContactModel: Validate the request body
    :param db: Session: Pass the database session to the repository layer
    :param _current_user: User: Get the current user from the database
    :return: A contactmodel object
    :doc-author: Trelent
    """
    return await repository_contacts.create_contact(body, db)


@router.get("/", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
                        _current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_contacts function returns a list of contacts.

    :param skip: int: Skip the first n contacts in the database
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Pass the database session to the function
    :param _current_user: User: Get the user from the database
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(skip, limit, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                       _current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_contact function is used to retrieve a single contact from the database.
    It takes in an integer representing the ID of the contact, and returns a Contact object.

    :param contact_id: int: Specify the type of data that is expected in the url path
    :param db: Session: Pass the database connection to the repository layer
    :param _current_user: User: Get the current user
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         _current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        The function takes an id and a body as input, and returns the updated contact.
        If no contact is found with that id, it raises an HTTPException.

    :param body: ContactModel: Get the data from the request body
    :param contact_id: int: Specify the contact id that is being updated
    :param db: Session: Get the database session
    :param _current_user: User: Get the current user from the auth_service
    :return: The updated contact
    :doc-author: Trelent
    """
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                         _current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_contact function removes a contact from the database.

    :param contact_id: int: Specify the contact to be removed
    :param db: Session: Pass the database session to the function
    :param _current_user: User: Get the current user from the auth_service
    :return: The removed contact
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/query/", response_model=List[ContactResponse])
async def querys_contacts(firstname: str = '', lastname: str = '', email: str = '', db: Session = Depends(get_db),
                          _current_user: User = Depends(auth_service.get_current_user)):
    """
    The querys_contacts function is used to query the contacts table in the database.
        The function takes three parameters: firstname, lastname and email.
        If a parameter is not provided, it will be set to an empty string by default.

    :param firstname: str: Pass the firstname of the contact to be queried
    :param lastname: str: Search for a contact by lastname
    :param email: str: Query the database for a specific contact
    :param db: Session: Pass the database session to the repository layer
    :param _current_user: User: Get the current user logged in
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.querys_contacts(firstname, lastname, email, db)
    return contacts


@router.get("/birthdays/", response_model=List[ContactResponse])
async def birthdays(db: Session = Depends(get_db), _current_user: User = Depends(auth_service.get_current_user)):
    """
    The birthdays function returns a list of contacts with birthdays in the current month.

    :param db: Session: Get the database session
    :param _current_user: User: Get the current user,
    :return: A list of contacts that have birthdays today
    :doc-author: Trelent
    """
    contacts = await repository_contacts.birthdays(db)
    return contacts
