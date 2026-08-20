"""
contact_manager.py
Defines ContactManager: handles storage, CRUD operations, search,
grouping, duplicate detection, and JSON persistence for Contact objects.
"""

import json
import os
from contact import Contact, ValidationError


class DuplicateContactError(Exception):
    """Raised when a contact with the same phone or email already exists."""
    pass


class ContactNotFoundError(Exception):
    """Raised when a lookup for a contact by name/index fails."""
    pass


class ContactManager:
    def __init__(self, data_file="contacts.json"):
        self.data_file = data_file
        self.contacts = []
        self.load()

    # ---------- Persistence ----------

    def load(self):
        """Load contacts from the JSON file, if it exists."""
        if not os.path.exists(self.data_file):
            self.contacts = []
            return
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                raw = json.load(f)
            self.contacts = [Contact.from_dict(item) for item in raw]
        except (json.JSONDecodeError, OSError) as e:
            print(f"[Warning] Could not load '{self.data_file}': {e}. Starting with an empty list.")
            self.contacts = []
        except ValidationError as e:
            print(f"[Warning] Corrupt contact data skipped: {e}")

    def save(self):
        """Persist contacts to the JSON file."""
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump([c.to_dict() for c in self.contacts], f, indent=2)
        except OSError as e:
            print(f"[Error] Could not save contacts: {e}")

    # ---------- Duplicate detection ----------

    def _find_duplicate(self, phone, email, exclude_index=None):
        for i, c in enumerate(self.contacts):
            if i == exclude_index:
                continue
            if c.phone == phone:
                return c
            if email and c.email and c.email.lower() == email.lower():
                return c
        return None

    # ---------- CRUD ----------

    def add_contact(self, name, phone, email="", group="General"):
        new_contact = Contact(name, phone, email, group)  # raises ValidationError if invalid
        duplicate = self._find_duplicate(new_contact.phone, new_contact.email)
        if duplicate:
            raise DuplicateContactError(
                f"Duplicate contact detected: '{duplicate.name}' already uses this phone/email."
            )
        self.contacts.append(new_contact)
        self.save()
        return new_contact

    def list_contacts(self, sort_by="name"):
        key_map = {
            "name": lambda c: c.name.lower(),
            "group": lambda c: c.group.lower(),
        }
        key_func = key_map.get(sort_by, key_map["name"])
        return sorted(self.contacts, key=key_func)

    def get_by_index(self, index):
        if index < 0 or index >= len(self.contacts):
            raise ContactNotFoundError(f"No contact at position {index + 1}.")
        return self.contacts[index]

    def update_contact(self, index, name=None, phone=None, email=None, group=None):
        contact = self.get_by_index(index)

        # Validate potential duplicate before committing changes
        check_phone = phone.strip().replace(" ", "").replace("-", "") if phone else contact.phone
        check_email = email.strip() if email else contact.email
        duplicate = self._find_duplicate(check_phone, check_email, exclude_index=index)
        if duplicate:
            raise DuplicateContactError(
                f"Update blocked: '{duplicate.name}' already uses this phone/email."
            )

        contact.update(name=name, phone=phone, email=email, group=group)
        self.save()
        return contact

    def delete_contact(self, index):
        contact = self.get_by_index(index)
        self.contacts.pop(index)
        self.save()
        return contact

    # ---------- Search & filter ----------

    def search(self, query):
        return [c for c in self.contacts if c.matches(query)]

    def filter_by_group(self, group):
        return [c for c in self.contacts if c.group.lower() == group.lower()]

    def list_groups(self):
        return sorted(set(c.group for c in self.contacts))

    def count(self):
        return len(self.contacts)
