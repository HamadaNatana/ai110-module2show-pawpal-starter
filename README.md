# PawPal+ (Module 2 Project)

## Main Features

### Smart Scheduling
Tasks are sorted by time and can be filtered by priority (high, medium, low). The generated schedule displays start/end times and duration for each task in a clean table view.

### Recurring Tasks
Tasks can be set to repeat on a **daily**, **weekly**, or **monthly** basis. When marked complete, they automatically reschedule to their next occurrence — including handling year boundaries (December to January).

### Conflict Detection
The scheduler checks for overlapping tasks assigned to the same pet and surfaces clear warnings. No crashes, no silent failures — just actionable alerts before you execute your plan.

### Task Management
Add, view, and complete tasks through an intuitive UI. Each task tracks its type, priority, assigned pet, scheduled date/time, duration, and recurrence pattern.

### Owner & Pet Profiles
Create owner profiles and register pets (dog, cat, or other) to assign tasks to specific animals.

📸 Demo
#### Creation
<a href="/imgs/user.png" target="_blank"><img src='/imgs/user.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

#### Task
<a href="/imgs/tasks.png" target="_blank"><img src='/imgs/tasks.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

#### Schedule
<a href="/imgs/schedule.png" target="_blank"><img src='/imgs/schedule.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>
---

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Smarter Scheduling

Your scheduler includes these intelligent features:

**1. Recurring Tasks**
- Tasks can be marked as `daily`, `weekly`, or `monthly`
- When completed, recurring tasks automatically reset to their next occurrence
- Handles edge cases like year boundaries (Dec → Jan for monthly tasks)

**2. Conflict Detection**
- Each task has a `duration_minutes` field (default: 30 min)
- The scheduler detects when two tasks overlap in time for the same pet
- Conflicts are surfaced as warnings in the schedule, without crashing the app
- Useful for catching scheduling mistakes before executing the plan

**3. Real-Time Scheduling**
- Tasks can specify their exact time and duration
- Schedule generation shows task start/end times (e.g., `Walk (09:00–09:30)`)
- UI allows users to set task duration and recurrence when creating tasks

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
