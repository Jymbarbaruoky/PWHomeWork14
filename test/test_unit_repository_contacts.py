from datetime import datetime, date, timedelta
import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel, ContactResponse
from src.repository.contacts import (
    get_contacts,
    get_contact,
    create_contact,
    remove_contact,
    update_contact,
    querys_contacts,
    birthdays,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        bd = datetime(year=2000, month=1, day=1)
        body = ContactModel(firstname="testfn", lastname="testln", email="tester@mail.ua", phone="1234567890",
                            birthday=bd, description="testd")
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.firstname, body.firstname)
        self.assertEqual(result.lastname, body.lastname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.description, body.description)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        bd = datetime(year=2000, month=1, day=1)
        body = ContactModel(firstname="testfn", lastname="testln", email="tester@mail.ua", phone="1234567890",
                            birthday=bd, description="testd", done=True)
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        bd = datetime(year=2000, month=1, day=1)
        body = ContactModel(firstname="testfn", lastname="testln", email="tester@mail.ua", phone="1234567890",
                             birthday=bd, description="testd")
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_birthdays(self):
        contact1 = Contact(id=1, firstname='Contact 1', birthday=date.today() + timedelta(days=1), user_id=self.user.id)
        contact2 = Contact(id=2, firstname='Contact 2', birthday=date.today() + timedelta(days=3), user_id=self.user.id)
        contact3 = Contact(id=3, firstname='Contact 3', birthday=date.today() + timedelta(days=6), user_id=self.user.id)
        contact4 = Contact(id=4, firstname='Contact 4', birthday=date.today() + timedelta(days=10), user_id=self.user.id)
        self.session.query().filter().all.return_value = [contact1, contact2, contact3, contact4]
        result = await birthdays(self.user, self.session)
        self.assertEqual(len(result), 3)
        self.assertIn(contact1, result)
        self.assertIn(contact2, result)
        self.assertIn(contact3, result)
        self.assertNotIn(contact4, result)


if __name__ == '__main__':
    unittest.main()
