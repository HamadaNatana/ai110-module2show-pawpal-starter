import streamlit as st
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
    st.success(f"Owner: {st.session_state.owner.name}")
    for p in st.session_state.owner.pets_owned:
        st.write(f"- **{p.name}** ({p.type_breed})")

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

selected_pet = st.selectbox("Assign to pet", pet_names)

if st.button("Add task"):
    if task_title and selected_pet:
        task = Task(task_type=task_title, importance=priority)
        pet = next(p for p in st.session_state.owner.pets_owned if p.name == selected_pet)
        task.add_pet(pet)
        st.session_state.tasks.append(task)
        st.rerun()

if st.session_state.tasks:
    st.write("**Current tasks:**")
    for t in st.session_state.tasks:
        pet_list = ", ".join(p.name for p in t.pets)
        status = "Done" if t.is_done else "Pending"
        st.write(f"- **{t.task_type}** — {t.importance} priority, pets: {pet_list} [{status}]")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    pending = [t for t in st.session_state.tasks if not t.is_done]
    if not pending:
        st.warning("No pending tasks to schedule.")
    else:
        priority_order = {"high": 0, "medium": 1, "low": 2}
        sorted_tasks = sorted(pending, key=lambda t: priority_order.get(t.importance, 3))
        schedule = Schedule(owner=st.session_state.owner, tasks=sorted_tasks)
        st.session_state.schedule = schedule

        st.write("**Scheduled plan (sorted by priority):**")
        for i, t in enumerate(schedule.generate_schedule(), start=1):
            pet_list = ", ".join(p.name for p in t.pets)
            st.write(f"{i}. **{t.task_type}** — {t.importance} priority, pets: {pet_list}")

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
