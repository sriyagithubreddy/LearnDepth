# Contact Management System

## Problem Statement
Build a personal contact book application supporting create, read, update
and delete (CRUD) operations, contact grouping, keyword search, and
duplicate-contact detection, with data persisted between runs.

## Objective
To design and implement a menu-driven, console-based Contact Management
System in Python that demonstrates core programming fundamentals: OOP,
data structures, input validation, exception handling, file-based
persistence, and search/filter logic — while remaining simple enough to
fully explain and defend.

## Features
- Add a contact with name, phone, email (optional) and group
- View all contacts, sortable by name or group
- Search contacts by any field (name, phone, email, group)
- Filter contacts by a specific group
- Update any field of an existing contact
- Delete a contact
- List all groups with per-group contact counts
- Duplicate detection: rejects a new/updated contact if its phone or
  email already belongs to another contact
- Input validation for name, phone number format, and email format
- Persistent storage to a local JSON file (`contacts.json`), reloaded
  automatically on startup
- Graceful error handling for invalid input, corrupt data files, and
  file I/O failures

## Technologies Used
- Python 3 (standard library only — no external dependencies)
- `json` module for persistence
- `re` module for validation
- Object-Oriented Programming (`Contact`, `ContactManager` classes)

## Installation / Setup Instructions
1. Ensure Python 3.7+ is installed (`python3 --version`).
2. No external packages are required — the project uses only the
   standard library, satisfying the zero-cost requirement.
3. Copy the project folder to your machine.

## How to Run the Project
```bash
cd contact_manager
python3 main.py
```
Follow the on-screen numbered menu (1–8) to perform operations.
Contacts are automatically saved to `contacts.json` in the same folder
after every add/update/delete, and reloaded automatically the next time
the program starts.

## Project Structure
```
contact_manager/
├── main.py              # CLI entry point and menu logic
├── contact.py           # Contact class + field validation
├── contact_manager.py   # ContactManager class: CRUD, search, persistence
├── contacts.json         # Data file (created/updated automatically)
├── README.md
└── test_cases.md
```

## Testing Details
The project was tested using an automated script exercising the
`ContactManager` and `Contact` classes directly (unit-style tests) as
well as manual CLI walkthroughs of every menu option. See
`test_cases.md` for the full list of test cases and results, covering
valid input, invalid input (bad phone/email/empty name), duplicate
detection on both add and update, out-of-range deletion, search
correctness, and persistence across program restarts.

## Screenshots
![Add Contact](screenshots/add_contact.png)
*Adding a new contact through the menu.*

![View and Search](screenshots/view_and_search.png)
*Viewing all contacts and searching by name.*

![Validation and Duplicate Errors](screenshots/validation_errors.png)
*Invalid phone rejected, then a duplicate contact rejected.*

![Groups and Exit](screenshots/list_groups_and_exit.png)
*Listing groups with counts, then exiting the program.*

## Limitations
- Single-user, local, console-only application (no GUI or network access)
- No contact photo or multi-phone-number support
- Duplicate detection is based on exact phone/email match only, not
  fuzzy name matching
- No authentication — the JSON file is not encrypted

## Future Improvements
- Add a simple GUI (e.g., Tkinter) as an alternative front-end
- Support multiple phone numbers/emails per contact
- Add CSV import/export
- Add fuzzy-matching duplicate detection based on name similarity
- Add undo/soft-delete functionality
