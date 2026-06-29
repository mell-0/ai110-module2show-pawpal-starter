import streamlit as st
from pawpal_system import Scheduler, Task, Pet, Owner, DailyPlan, Priority

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# Session state acts as the in-memory vault for the app.
# Streamlit reruns the entire script on every interaction, so objects must be
# stored here to persist across reruns. Each category uses a dict keyed by ID
# so we can look up, add, or iterate without knowing IDs in advance.
if "owners" not in st.session_state:
    st.session_state.owners = {}   # { owner_id: Owner }
if "pets" not in st.session_state:
    st.session_state.pets = {}     # { pet_id: Pet }
if "tasks" not in st.session_state:
    st.session_state.tasks = {}    # { task_id: Task }

st.divider()

# -------------------------------------------------------------------------
# ADD OWNER
# Creates an Owner instance and stores it in the vault.
# IDs are auto-generated as o1, o2, ... based on current count.
# -------------------------------------------------------------------------
st.subheader("Add Owner")

col1, col2, col3 = st.columns(3)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    time_available = st.number_input("Available time (mins)", min_value=1, max_value=480, value=60)
with col3:
    preferred_start = st.text_input("Preferred start time (HH:MM)", value="08:00")

if st.button("Add owner"):
    owner_id = f"o{len(st.session_state.owners) + 1}"
    if owner_id not in st.session_state.owners:
        st.session_state.owners[owner_id] = Owner(
            id=owner_id,
            name=owner_name,
            time_available_minutes=int(time_available),
            preferred_start_time=preferred_start,
        )
        st.success(f"Owner '{owner_name}' added (ID: {owner_id})")

if st.session_state.owners:
    st.write("Current owners:")
    st.table([
        {"id": o.id, "name": o.name, "available_mins": o.time_available_minutes, "start_time": o.preferred_start_time}
        for o in st.session_state.owners.values()
    ])

st.divider()

# -------------------------------------------------------------------------
# ADD PET
# Creates a Pet instance, assigns it to an owner via owner.add_pet(),
# and also stores it in the flat pets vault for easy cross-section lookup.
# Blocked until at least one owner exists.
# -------------------------------------------------------------------------
st.subheader("Add Pet")

if not st.session_state.owners:
    st.info("Add an owner first before adding a pet.")
else:
    # Build a name → id mapping so the selectbox can show names while we store by id
    owner_options = {o.name: oid for oid, o in st.session_state.owners.items()}

    col1, col2, col3 = st.columns(3)
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi")
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "other"])
    with col3:
        selected_owner_name = st.selectbox("Assign to owner", list(owner_options.keys()))

    if st.button("Add pet"):
        pet_id = f"p{len(st.session_state.pets) + 1}"
        owner_id = owner_options[selected_owner_name]
        owner = st.session_state.owners[owner_id]

        new_pet = Pet(id=pet_id, name=pet_name, species=species)
        owner.add_pet(new_pet)                          # links pet to owner
        st.session_state.pets[pet_id] = new_pet         # also store in flat vault
        st.success(f"Pet '{pet_name}' added to {owner.name} (ID: {pet_id})")

    if st.session_state.pets:
        st.write("Current pets:")
        # Reverse-lookup: walk each owner's pet list to map pet_id → owner name
        pet_owner = {
            p.id: o.name
            for o in st.session_state.owners.values()
            for p in o.pets
        }
        st.table([
            {"id": p.id, "name": p.name, "species": p.species, "owner": pet_owner.get(p.id, "unassigned")}
            for p in st.session_state.pets.values()
        ])

st.divider()

# -------------------------------------------------------------------------
# ADD TASK
# Creates a Task instance, assigns it to a pet via pet.add_task(),
# and stores it in the flat tasks vault.
# Priority string from the UI is converted to the Priority enum before storage.
# Blocked until at least one pet exists.
# -------------------------------------------------------------------------
st.subheader("Add Task")

if not st.session_state.pets:
    st.info("Add a pet first before adding tasks.")
else:
    pet_options = {p.name: pid for pid, p in st.session_state.pets.items()}

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task description", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority_str = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        selected_pet_name = st.selectbox("Assign to pet", list(pet_options.keys()))

    if st.button("Add task"):
        task_id = f"t{len(st.session_state.tasks) + 1}"
        pet_id = pet_options[selected_pet_name]
        pet = st.session_state.pets[pet_id]

        # Convert UI string to Priority enum so the Scheduler can compare values
        priority_map = {"low": Priority.LOW, "medium": Priority.MEDIUM, "high": Priority.HIGH}
        new_task = Task(
            id=task_id,
            description=task_title,
            duration_minutes=int(duration),
            priority=priority_map[priority_str],
        )
        pet.add_task(new_task)                          # links task to pet
        st.session_state.tasks[task_id] = new_task      # also store in flat vault
        st.success(f"Task '{task_title}' added to {pet.name} (ID: {task_id})")

    if st.session_state.tasks:
        st.write("Current tasks:")
        # task_pet: maps task_id → Pet by walking each pet's task list
        task_pet = {
            t.id: p
            for p in st.session_state.pets.values()
            for t in p.get_tasks()
        }
        # pet_owner: maps pet_id → owner name by walking each owner's pet list
        pet_owner = {
            p.id: o.name
            for o in st.session_state.owners.values()
            for p in o.pets
        }
        st.table([
            {
                "id": t.id,
                "description": t.description,
                "duration_mins": t.duration_minutes,
                "priority": t.priority.name.lower(),
                "pet": task_pet[t.id].name if t.id in task_pet else "unassigned",
                # chain task → pet → owner to resolve the owner column
                "owner": pet_owner.get(task_pet[t.id].id, "unassigned") if t.id in task_pet else "unassigned",
            }
            for t in st.session_state.tasks.values()
        ])

st.divider()

# -------------------------------------------------------------------------
# GENERATE SCHEDULE
# Enforces strict ownership: the pet dropdown only shows pets that belong
# to the selected owner (pulled from owner.pets, not the global vault).
# Passes the owner and pet to Scheduler.generate_plan(), then displays
# the resulting DailyPlan as a timed table.
# -------------------------------------------------------------------------
st.subheader("Generate Schedule")

if not st.session_state.owners or not st.session_state.pets:
    st.info("Add at least one owner and one pet to generate a schedule.")
else:
    owner_options = {o.name: oid for oid, o in st.session_state.owners.items()}

    sched_owner_name = st.selectbox("Owner", list(owner_options.keys()), key="sched_owner")
    owner = st.session_state.owners[owner_options[sched_owner_name]]

    # Only show pets this owner actually owns (strict ownership)
    owned_pets = {p.name: p.id for p in owner.pets}
    if not owned_pets:
        st.info(f"{owner.name} has no pets. Add a pet and assign it to this owner first.")
        st.stop()

    sched_pet_name = st.selectbox("Pet", list(owned_pets.keys()), key="sched_pet")

    if st.button("Generate schedule"):
        pet = st.session_state.pets[owned_pets[sched_pet_name]]

        if not pet.get_tasks():
            st.warning(f"{pet.name} has no tasks. Add tasks to this pet first.")
        else:
            # scheduler = Scheduler()
            plan = Scheduler.generate_plan(owner=owner, pet=pet)

            st.success(plan.get_summary())

            # Build a timed table by advancing a clock for each task in the plan
            import datetime
            current_time = datetime.datetime.strptime(owner.preferred_start_time, "%H:%M")
            rows = []
            for task in plan.tasks:
                rows.append({
                    "time": current_time.strftime("%H:%M"),
                    "task": task.description,
                    "duration_mins": task.duration_minutes,
                    "priority": task.priority.name.lower(),
                })
                current_time += datetime.timedelta(minutes=task.duration_minutes)

            st.table(rows)
