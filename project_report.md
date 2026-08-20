# Project Report — Contact Management System

## 1. Problem Understanding
The task required a console-based contact book supporting create, read,
update, delete, grouping, search, and duplicate detection, with data
surviving across program runs. Beyond basic CRUD, the assignment
required demonstrating validation, exception handling, and clean code
organization rather than just "making it work."

## 2. Proposed Approach
The problem naturally splits into two responsibilities: representing a
single contact (including its own validation rules) and managing the
collection of contacts (storage, search, duplicate checking). This
suggested two classes:

- `Contact` — owns its own field validation (name, phone, email) so
  invalid data can never exist in a valid `Contact` object.
- `ContactManager` — owns the list of contacts, JSON persistence, and
  all collection-level operations (add/update/delete/search/filter/
  duplicate-check).

`main.py` stays a thin CLI layer that only handles menu display and
input prompts, calling into the two classes above. This separation
keeps each file focused and easy to test independently of the CLI.

## 3. Implementation
- **Validation** is centralized in `Contact` using regular expressions
  for phone (7–15 digits, optional leading `+`) and email (basic
  `local@domain.tld` pattern). Both add and update paths reuse the same
  validation, so there's only one source of truth for "what is a valid
  contact."
- **Duplicate detection** checks both phone and email against all
  existing contacts (excluding the contact being edited, during
  updates) before committing any change.
- **Persistence** uses JSON via the standard `json` module. Contacts
  serialize to/from plain dictionaries (`to_dict`/`from_dict`), keeping
  the storage format simple and human-readable.
- **Exception handling** uses custom exception classes
  (`ValidationError`, `DuplicateContactError`, `ContactNotFoundError`)
  rather than generic exceptions, so the CLI layer can catch and
  message each failure mode distinctly.
- **Search** is a simple case-insensitive substring match across all
  fields, implemented as a `matches()` method on `Contact` — keeping
  the matching logic next to the data it operates on.

## 4. Important Technical Decisions
- Chose JSON over CSV for persistence since contacts are naturally
  key-value records and JSON preserves types and optional fields
  (empty email) more cleanly.
- Made duplicate detection block on *either* phone or email match
  rather than requiring both, since either one being duplicated
  usually indicates the same real-world contact.
- Kept the CLI intentionally simple (numbered menu, sequential
  prompts) rather than adding a command-parsing layer, since the
  assignment rewards clarity and correctness over interface complexity.

## 5. Testing Performed
Nine targeted test cases were run (see `test_cases.md`), covering: valid
add, duplicate phone rejection, invalid phone, invalid email, empty
name, case-insensitive search, out-of-range delete, persistence across
a fresh `ContactManager` instance (simulating a program restart), and
duplicate rejection during update. All 9 passed. The full CLI menu was
also walked manually end-to-end (add → view → search → filter → list
groups → exit) to confirm the user-facing flow works without crashing.

## 6. Challenges Encountered
- Deciding how strict phone/email validation should be without
  rejecting legitimate real-world formats (e.g., allowing an optional
  `+` prefix for country codes, allowing spaces/dashes to be stripped
  before validation).
- Ensuring the duplicate check during an *update* correctly excludes
  the contact being edited from the comparison — otherwise a contact
  would always appear to duplicate itself.

## 7. Solutions Implemented
- Used a permissive-but-bounded regex (7–15 digits) for phone numbers
  and stripped common formatting characters (spaces, dashes) before
  validating, balancing strictness with usability.
- Added an `exclude_index` parameter to the internal duplicate-check
  method, used only during updates, so a contact never conflicts with
  itself.

## 8. Future Scope
- Add CSV import/export for bulk contact management.
- Support multiple phone numbers or emails per contact.
- Add a lightweight GUI (Tkinter) as an alternative to the CLI.
- Add fuzzy name-matching to catch duplicates with typos, not just
  exact phone/email matches.
