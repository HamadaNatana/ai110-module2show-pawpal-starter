import streamlit as st
import datetime
from pawpal_system import Owner, Pet, Task, Schedule

if "owner" not in st.session_state:
    st.session_state.owner = None
if "schedule" not in st.session_state:
    st.session_state.schedule = None
if "tasks" not in st.session_state:
    st.session_state.tasks = []

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
if st.button("Create owner and pet"):
    owner = Owner(name=owner_name)
    pet = Pet(name=pet_name, type_breed=species, owner=owner)
    owner.add_pet(pet)
    st.session_state.owner = owner

if st.session_state.owner:
    st.success(f"Owner: {st.session_state.owner.name} and pet: {st.session_state.owner.pets_owned[0].name} ({st.session_state.owner.pets_owned[0].type_breed}) created!")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if st.session_state.owner is None or not st.session_state.owner.pets_owned:
    st.info("Create an owner and pet above before adding tasks.")
    st.stop()

pet_names = [p.name for p in st.session_state.owner.pets_owned]

col1, col2 = st.columns(2)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

col3, col4 = st.columns(2)
with col3:
    duration = st.number_input("Duration (minutes)", min_value=5, max_value=480, value=30, step=5)
with col4:
    recurrence = st.selectbox("Recurrence", [None, "daily", "weekly", "monthly"])

col5, col6 = st.columns(2)
with col5:
    task_date = st.date_input("Scheduled date", value=datetime.date.today())
with col6:
    task_time = st.time_input("Scheduled time", value=datetime.time(9, 0))

selected_pet = st.selectbox("Assign to pet", pet_names)

if st.button("Add task"):
    if task_title and selected_pet:
        scheduled_dt = datetime.datetime.combine(task_date, task_time)
        task = Task(task_type=task_title, importance=priority, duration_minutes=duration, recurrence=recurrence, due_date=scheduled_dt)
        pet = next(p for p in st.session_state.owner.pets_owned if p.name == selected_pet)
        task.add_pet(pet)
        st.session_state.tasks.append(task)
        st.success(f"Task '{task_title}' added for {selected_pet}!")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

priority_filter = st.selectbox("Filter by priority", ["All", "high", "medium", "low"])

if st.button("Generate schedule"):
    pending = [t for t in st.session_state.tasks if not t.is_done]
    if not pending:
        st.warning("No pending tasks to schedule.")
    else:
        schedule = Schedule(owner=st.session_state.owner, tasks=list(pending))
        schedule.sort_by_time()

        if priority_filter != "All":
            schedule.filter_by_priority(priority_filter)

        st.session_state.schedule = schedule

        # Check for and display conflicts
        conflicts = schedule.detect_conflicts()
        if conflicts:
            for warning in schedule.get_conflict_warnings():
                st.warning(warning)
        else:
            st.success("✓ No scheduling conflicts detected!")

        scheduled_tasks = schedule.generate_schedule()
        if not scheduled_tasks:
            st.info(f"No {priority_filter} priority tasks found.")
        else:
            st.write("**Scheduled plan (sorted by time):**")
            table_data = []
            for t in scheduled_tasks:
                date_str = t.due_date.strftime("%Y-%m-%d")
                start_time = t.due_date.strftime("%H:%M")
                end_time = (t.due_date + datetime.timedelta(minutes=t.duration_minutes)).strftime("%H:%M")
                table_data.append({
                    "Task": t.task_type,
                    "Date": date_str,
                    "Start": start_time,
                    "End": end_time,
                    "Duration (min)": t.duration_minutes,
                    "Priority": t.importance.capitalize(),
                    "Pets": ", ".join(p.name for p in t.pets),
                    "Recurrence": t.recurrence if t.recurrence else "—",
                })
            st.table(table_data)

st.divider()

st.subheader("Mark Tasks Complete")

pending = [t for t in st.session_state.tasks if not t.is_done]
if pending:
    task_labels = [f"{t.task_type} ({t.importance}) — {', '.join(p.name for p in t.pets)}" for t in pending]
    selected_label = st.selectbox("Select a task to complete", task_labels)
    if st.button("Mark Done"):
        idx = task_labels.index(selected_label)
        pending[idx].mark_done()
        st.rerun()
else:
    st.info("No pending tasks.")
