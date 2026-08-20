"""
main.py
Command-line interface for the Contact Management System.
"""

from contact import ValidationError
from contact_manager import ContactManager, DuplicateContactError, ContactNotFoundError

MENU = """
==================================================
        CONTACT MANAGEMENT SYSTEM
==================================================
1. Add Contact
2. View All Contacts
3. Search Contacts
4. Filter by Group
5. Update Contact
6. Delete Contact
7. List Groups
8. Exit
==================================================
"""


def print_contacts(contacts):
    if not contacts:
        print("No contacts found.")
        return
    print(f"{'NAME':<20} | {'PHONE':<15} | {'EMAIL':<25} | GROUP")
    print("-" * 75)
    for i, c in enumerate(contacts, start=1):
        print(f"{i}. {c}")


def prompt_nonempty(label):
    return input(f"{label}: ").strip()


def add_contact_flow(manager):
    print("\n-- Add Contact --")
    name = prompt_nonempty("Name")
    phone = prompt_nonempty("Phone")
    email = input("Email (optional): ").strip()
    group = input("Group (default: General): ").strip() or "General"
    try:
        contact = manager.add_contact(name, phone, email, group)
        print(f"[Success] Added: {contact.name}")
    except (ValidationError, DuplicateContactError) as e:
        print(f"[Error] {e}")


def view_all_flow(manager):
    print("\n-- All Contacts --")
    sort_choice = input("Sort by (name/group) [name]: ").strip().lower() or "name"
    contacts = manager.list_contacts(sort_by=sort_choice)
    print_contacts(contacts)


def search_flow(manager):
    print("\n-- Search Contacts --")
    query = prompt_nonempty("Search term (name/phone/email/group)")
    if not query:
        print("[Error] Search term cannot be empty.")
        return
    results = manager.search(query)
    print_contacts(results)


def filter_group_flow(manager):
    print("\n-- Filter by Group --")
    groups = manager.list_groups()
    if not groups:
        print("No groups exist yet.")
        return
    print("Available groups:", ", ".join(groups))
    group = prompt_nonempty("Group name")
    results = manager.filter_by_group(group)
    print_contacts(results)


def update_flow(manager):
    print("\n-- Update Contact --")
    view_all_flow(manager)
    try:
        idx = int(input("Enter contact number to update: ").strip()) - 1
    except ValueError:
        print("[Error] Please enter a valid number.")
        return

    print("Leave a field blank to keep it unchanged.")
    name = input("New Name: ").strip() or None
    phone = input("New Phone: ").strip() or None
    email = input("New Email: ").strip() or None
    group = input("New Group: ").strip() or None

    try:
        contact = manager.update_contact(idx, name=name, phone=phone, email=email, group=group)
        print(f"[Success] Updated: {contact.name}")
    except (ValidationError, DuplicateContactError, ContactNotFoundError) as e:
        print(f"[Error] {e}")


def delete_flow(manager):
    print("\n-- Delete Contact --")
    view_all_flow(manager)
    try:
        idx = int(input("Enter contact number to delete: ").strip()) - 1
    except ValueError:
        print("[Error] Please enter a valid number.")
        return

    try:
        contact = manager.delete_contact(idx)
        print(f"[Success] Deleted: {contact.name}")
    except ContactNotFoundError as e:
        print(f"[Error] {e}")


def list_groups_flow(manager):
    print("\n-- Groups --")
    groups = manager.list_groups()
    if not groups:
        print("No groups exist yet.")
        return
    for g in groups:
        count = len(manager.filter_by_group(g))
        print(f"- {g} ({count} contact{'s' if count != 1 else ''})")


def main():
    manager = ContactManager(data_file="contacts.json")
    print("Welcome to the Contact Management System.")
    print(f"Loaded {manager.count()} existing contact(s).")

    actions = {
        "1": add_contact_flow,
        "2": view_all_flow,
        "3": search_flow,
        "4": filter_group_flow,
        "5": update_flow,
        "6": delete_flow,
        "7": list_groups_flow,
    }

    while True:
        print(MENU)
        choice = input("Enter your choice (1-8): ").strip()
        if choice == "8":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action(manager)
        else:
            print("[Error] Invalid choice. Please select 1-8.")


if __name__ == "__main__":
    main()
