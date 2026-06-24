#!/usr/bin/env python3
"""Generate import-ready mock data for the Activity 5 multi-agent demo.

Produces two CSV files you import into n8n Data Tables:
  - mock-hr-employees.csv  -> Data Table "HR Employee Data"  (HR agent)
  - mock-it-tickets.csv    -> Data Table "IT Support Tickets" (IT agent)

The columns match what the index.html dashboard expects so the HR and IT
tabs render correctly after a "Sync from Database".
"""
import csv
import random

random.seed(42)  # deterministic output so re-running gives the same rows

# ----------------------------------------------------------------------------
# HR Employee Data  (columns: Name, Gender, Department, Role, Location, Food, Attending)
# ----------------------------------------------------------------------------
FIRST_F = ["Aisha", "Mei Ling", "Priya", "Sarah", "Hui Wen", "Nadia", "Grace",
           "Ananya", "Siti", "Rachel", "Ling", "Fatimah", "Joanne", "Divya",
           "Wei Ting", "Carmen", "Yuki", "Deepa"]
FIRST_M = ["Arjun", "Wei Jie", "Daniel", "Rahul", "Jun Hao", "Imran", "Marcus",
           "Vikram", "Hafiz", "Ethan", "Cheng", "Faisal", "Bryan", "Karthik",
           "Zhi Hao", "Diego", "Haruto", "Sanjay"]
LAST = ["Tan", "Lim", "Nair", "Wong", "Kumar", "Rahman", "Lee", "Sharma",
        "Abdullah", "Ng", "Goh", "Iqbal", "Chua", "Reddy", "Teo", "Garcia",
        "Sato", "Menon"]
DEPARTMENTS = ["Engineering", "Sales", "Marketing", "Finance", "Operations", "HR", "IT"]
ROLES = {
    "Engineering": ["Software Engineer", "Senior Engineer", "QA Engineer", "Engineering Manager"],
    "Sales": ["Account Executive", "Sales Manager", "Sales Rep"],
    "Marketing": ["Marketing Specialist", "Content Lead", "Marketing Manager"],
    "Finance": ["Accountant", "Financial Analyst", "Finance Manager"],
    "Operations": ["Operations Analyst", "Ops Coordinator", "Operations Manager"],
    "HR": ["HR Executive", "Recruiter", "HR Manager"],
    "IT": ["IT Support Engineer", "System Administrator", "IT Manager"],
}
LOCATIONS = ["Singapore", "Penang", "San Diego", "Hyderabad", "Shanghai"]
FOODS = ["No Preference", "Vegetarian", "Halal", "Vegan", "Seafood"]

def make_employees(n=36):
    rows = []
    for i in range(1, n + 1):
        gender = random.choice(["Female", "Male"])
        first = random.choice(FIRST_F if gender == "Female" else FIRST_M)
        name = f"{first} {random.choice(LAST)}"
        dept = random.choice(DEPARTMENTS)
        rows.append({
            "EmployeeID": f"E{1000 + i}",
            "Name": name,
            "Gender": gender,
            "Department": dept,
            "Role": random.choice(ROLES[dept]),
            "Location": random.choice(LOCATIONS),
            "Food": random.choice(FOODS),
            "Attending": random.choice(["Yes", "Yes", "Yes", "No"]),  # ~75% Yes
        })
    return rows

# ----------------------------------------------------------------------------
# IT Support Tickets
# (columns: TicketID, Requester, Department, Category, Priority, Status,
#           Assignee, Channel, CreatedDate, ResolvedDate)
# ----------------------------------------------------------------------------
CATEGORIES = ["Password Reset", "Account Lockout", "MFA", "VPN", "Wi-Fi / Network",
              "Email / Outlook", "Software Install", "Printer", "Hardware",
              "Access Request", "Phishing / Security"]
# Rough weighting so the charts look realistic (password/VPN/email dominate)
CATEGORY_WEIGHTS = [22, 10, 8, 14, 12, 13, 7, 5, 6, 7, 4]
PRIORITIES = ["P1", "P2", "P3"]
PRIORITY_WEIGHTS = [1, 4, 7]
STATUSES = ["Open", "In Progress", "Resolved", "Closed"]
STATUS_WEIGHTS = [3, 3, 8, 6]
ASSIGNEES = ["Marcus Lee", "Priya Nair", "Hafiz Abdullah", "Joanne Goh", "Unassigned"]
CHANNELS = ["Portal", "Email", "Phone", "Walk-in"]
CHANNEL_WEIGHTS = [10, 8, 4, 2]

def make_tickets(n=45):
    rows = []
    for i in range(1, n + 1):
        cat = random.choices(CATEGORIES, weights=CATEGORY_WEIGHTS)[0]
        status = random.choices(STATUSES, weights=STATUS_WEIGHTS)[0]
        prio = random.choices(PRIORITIES, weights=PRIORITY_WEIGHTS)[0]
        day = random.randint(1, 28)
        created = f"2026-05-{day:02d}"
        if status in ("Resolved", "Closed"):
            rday = min(day + random.randint(0, 4), 31)
            resolved = f"2026-05-{rday:02d}"
            assignee = random.choice([a for a in ASSIGNEES if a != "Unassigned"])
        else:
            resolved = ""
            assignee = random.choice(ASSIGNEES)
        rows.append({
            "TicketID": f"INC{2000 + i}",
            "Requester": f"E{1000 + random.randint(1, 36)}",
            "Department": random.choice(DEPARTMENTS),
            "Category": cat,
            "Priority": prio,
            "Status": status,
            "Assignee": assignee,
            "Channel": random.choices(CHANNELS, weights=CHANNEL_WEIGHTS)[0],
            "CreatedDate": created,
            "ResolvedDate": resolved,
        })
    return rows


def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"Saved {path} ({len(rows)} rows)")


if __name__ == "__main__":
    emp = make_employees()
    tix = make_tickets()
    write_csv("mock-hr-employees.csv", emp)
    write_csv("mock-it-tickets.csv", tix)
    # quick distribution sanity print
    from collections import Counter
    print("HR depts:", dict(Counter(e["Department"] for e in emp)))
    print("HR gender:", dict(Counter(e["Gender"] for e in emp)))
    print("IT status:", dict(Counter(t["Status"] for t in tix)))
    print("IT category:", dict(Counter(t["Category"] for t in tix)))
