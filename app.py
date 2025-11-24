import streamlit as st
import sqlite3
from datetime import datetime
DB_PATH = "todo_tasks.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_task(task):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO tasks(task, status, timestamp) VALUES (?, ?, ?)",
              (task, "Pending", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def update_task(task_id, new_task):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE tasks SET task=? WHERE id=?", (new_task, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

def toggle_status(task_id, current_status):
    new_status = "Completed" if current_status=="Pending" else "Pending"
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE tasks SET status=? WHERE id=?", (new_status, task_id))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM tasks ORDER BY timestamp DESC")
    tasks = c.fetchall()
    conn.close()
    return tasks

# -------------------------------
# INITIALIZE DATABASE
# -------------------------------
init_db()

# -------------------------------
# STREAMLIT UI
# -------------------------------
st.set_page_config(page_title="📝 My To-Do App", page_icon="📝", layout="wide")
st.title("📝 My To-Do App")
st.markdown("**A clean and fun task manager for your daily life!**")

# -------------------------------
# ADD TASK SECTION
# -------------------------------
st.subheader("➕ Add a Task")
task_input = st.text_input("Enter your task here:")
if st.button("Add Task"):
    if task_input.strip() != "":
        add_task(task_input.strip())
        st.success(f"Task '{task_input}' added successfully!")
    else:
        st.warning("Please enter a task before adding!")

# -------------------------------
# FILTER SECTION
# -------------------------------
st.subheader("📋 Tasks")
filter_option = st.radio("Filter tasks:", ["All", "Pending", "Completed"])

tasks = get_tasks()
if filter_option != "All":
    tasks = [t for t in tasks if t[2] == filter_option]

if tasks:
    for task in tasks:
        task_id, task_text, status, timestamp = task
        col1, col2, col3, col4 = st.columns([5,2,2,1])

        with col1:
            st.markdown(f"**{'✅' if status=='Completed' else '🔹'} {task_text}**")
        with col2:
            if st.button(f"Toggle ✅/🔹", key=f"toggle_{task_id}"):
                toggle_status(task_id, status)
                st.experimental_rerun()
        with col3:
            new_text = st.text_input(f"Edit", value=task_text, key=f"edit_{task_id}")
            if st.button("Save", key=f"save_{task_id}"):
                if new_text.strip() != "":
                    update_task(task_id, new_text.strip())
                    st.success("Task updated!")
                    st.experimental_rerun()
        with col4:
            if st.button("❌", key=f"delete_{task_id}"):
                delete_task(task_id)
                st.warning("Task deleted!")
                st.experimental_rerun()
else:
    st.info("No tasks found. Add one above!")

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown("Made with ❤️ in **Streamlit**")
