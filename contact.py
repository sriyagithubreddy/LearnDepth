"""
contact.py
Defines the Contact class: a single contact record with validation.
"""

import re


class ValidationError(Exception):
    """Raised when contact field data fails validation."""
    pass


class Contact:
    """Represents a single contact entry."""

    PHONE_PATTERN = re.compile(r"^\+?\d{7,15}$")
    EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def __init__(self, name, phone, email="", group="General"):
        self.name = self._validate_name(name)
        self.phone = self._validate_phone(phone)
        self.email = self._validate_email(email) if email else ""
        self.group = group.strip() if group and group.strip() else "General"

    @staticmethod
    def _validate_name(name):
        if not name or not name.strip():
            raise ValidationError("Name cannot be empty.")
        if len(name.strip()) < 2:
            raise ValidationError("Name must be at least 2 characters long.")
        return name.strip()

    @classmethod
    def _validate_phone(cls, phone):
        if not phone or not phone.strip():
            raise ValidationError("Phone number cannot be empty.")
        cleaned = phone.strip().replace(" ", "").replace("-", "")
        if not cls.PHONE_PATTERN.match(cleaned):
            raise ValidationError(
                f"Invalid phone number: '{phone}'. Use 7-15 digits, optional leading +."
            )
        return cleaned

    @classmethod
    def _validate_email(cls, email):
        cleaned = email.strip()
        if not cls.EMAIL_PATTERN.match(cleaned):
            raise ValidationError(f"Invalid email address: '{email}'.")
        return cleaned

    def update(self, name=None, phone=None, email=None, group=None):
        """Update fields selectively, re-validating any that are provided."""
        if name is not None:
            self.name = self._validate_name(name)
        if phone is not None:
            self.phone = self._validate_phone(phone)
        if email is not None:
            self.email = self._validate_email(email) if email else ""
        if group is not None:
            self.group = group.strip() if group.strip() else "General"

    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "group": self.group,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name", ""),
            phone=data.get("phone", ""),
            email=data.get("email", ""),
            group=data.get("group", "General"),
        )

    def matches(self, query):
        """Case-insensitive search across name, phone, email, group."""
        query = query.lower().strip()
        return (
            query in self.name.lower()
            or query in self.phone.lower()
            or query in self.email.lower()
            or query in self.group.lower()
        )

    def __str__(self):
        email_part = self.email if self.email else "-"
        return f"{self.name:<20} | {self.phone:<15} | {email_part:<25} | {self.group}"
