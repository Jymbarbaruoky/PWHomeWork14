from datetime import datetime, timedelta
from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel, ContactResponse


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    The get_contacts function returns a list of contacts for the user.

    :param skip: int: Skip the first n contacts in the database
    :param limit: int: Limit the number of contacts returned
    :param user: User: Get the user id from the database
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    The get_contact function takes in a contact_id and user, and returns the contact with that id.
        Args:
            contact_id (int): The id of the desired Contact object.
            user (User): The User object associated with this Contact.

    :param contact_id: int: Get the contact with a specific id
    :param user: User: Get the user's id from the database
    :param db: Session: Pass the database session to the function
    :return: The contact with the given id for the given user
    :doc-author: Trelent
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactModel: Get the data from the request body
    :param user: User: Get the user id from the token
    :param db: Session: Access the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = Contact(firstname=body.firstname, lastname=body.lastname, email=body.email, phone=body.phone,
                      birthday=body.birthday, description=body.description, user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            user (User): The user who owns the contacts list.
            db (Session): A connection to our database, used for querying and deleting data.

    :param contact_id: int: Identify the contact to be removed
    :param user: User: Get the user's id from the database
    :param db: Session: Pass the database session to the function
    :return: The contact that was removed
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactResponse, user: User, db: Session) -> Contact | None:
    """
    The update_contact function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactResponse): The updated information for the specified contact.

    :param contact_id: int: Identify the contact that is being updated
    :param body: ContactResponse: Pass the data from the request body to the function
    :param user: User: Get the user id from the token
    :param db: Session: Access the database
    :return: The contact object, if it exists
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.firstname = body.firstname
        contact.lastname = body.lastname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
    return contact


async def querys_contacts(firstname: str, lastname: str, email: str, user: User, db: Session) -> List[Contact]:
    """
    The querys_contacts function takes in a firstname, lastname, email and user object.
    It then queries the database for contacts that match any of these parameters.
    The function returns a list of all matching contacts.

    :param firstname: str: Filter the contacts by firstname
    :param lastname: str: Filter the contacts by lastname
    :param email: str: Filter the contacts by email
    :param user: User: Get the user_id of the logged in user
    :param db: Session: Access the database
    :return: A list of contacts that match the query parameters
    :doc-author: Trelent
    """
    contact_with_firstname = db.query(Contact).filter(
        and_(Contact.firstname == firstname, Contact.user_id == user.id)).all()
    contact_with_lastname = db.query(Contact).filter(
        and_(Contact.lastname == lastname, Contact.user_id == user.id)).all()
    contact_with_email = db.query(Contact).filter(and_(Contact.email == email, Contact.user_id == user.id)).all()
    result = []
    result.extend(contact_with_firstname)
    result.extend(contact_with_lastname)
    result.extend(contact_with_email)
    return result


async def birthdays(user: User, db: Session) -> List[Contact]:
    """
    The birthdays function returns a list of contacts whose birthdays are within the next 7 days.
        Args:
            user (User): The User object for which to retrieve contacts.
            db (Session): A database session object used to query the database.

    :param user: User: Get the user_id from the database
    :param db: Session: Access the database
    :return: A list of contacts whose birthdays are within the next 7 days
    :doc-author: Trelent
    """
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    result = []
    delta = timedelta(days=7)
    delta_date = datetime.now() + delta
    for contact in contacts:
        birthday_date = datetime(year=datetime.now().year, month=contact.birthday.month, day=contact.birthday.day)
        birthday_date_next_year = datetime(year=datetime.now().year + 1, month=contact.birthday.month,
                                           day=contact.birthday.day)
        if datetime.now() < birthday_date <= delta_date or datetime.now() < birthday_date_next_year <= delta_date:
            result.append(contact)
    return result
