# Test Cases — Contact Management System

All tests below were executed against `ContactManager`/`Contact` directly
(unit-level) and confirmed again through the CLI (`main.py`). All 9 passed.

| # | Test Case | Input | Expected Result | Actual Result |
|---|-----------|-------|------------------|----------------|
| 1 | Add a valid contact | name="Ravi Kumar", phone="9876543210", email="ravi@example.com", group="Friends" | Contact added successfully | PASS — contact created and saved |
| 2 | Add duplicate phone number | phone="9876543210" (already used by Ravi Kumar) | `DuplicateContactError` raised, contact NOT added | PASS |
| 3 | Add contact with invalid phone | phone="abc123" | `ValidationError` raised: invalid phone format | PASS |
| 4 | Add contact with invalid email | email="notanemail" | `ValidationError` raised: invalid email format | PASS |
| 5 | Add contact with missing/empty name | name="" | `ValidationError` raised: name cannot be empty | PASS |
| 6 | Search by partial name (case-insensitive) | query="priya" | Returns exactly the matching contact | PASS |
| 7 | Delete contact at an out-of-range index | index=99 (only 2 contacts exist) | `ContactNotFoundError` raised, no crash | PASS |
| 8 | Persistence across restarts | Reload `ContactManager` after adding 2 contacts | New instance loads 2 contacts from `contacts.json` | PASS |
| 9 | Update triggers duplicate check | Update contact #2's phone to match contact #1's phone | `DuplicateContactError` raised, update blocked | PASS |

## Additional Manual CLI Verification
- Viewed all contacts sorted by name — correct alphabetical order confirmed.
- Filtered by group ("Work") — returned only contacts in that group.
- Listed groups — showed correct per-group counts.
- Ran the full menu loop from launch to Exit (option 8) — no crashes,
  clean exit message shown.

## How to Re-run the Automated Tests
The 9 core tests above can be reproduced by running the test script
logic shown in the project report, or by exercising each CLI menu
option manually with the inputs listed above.
