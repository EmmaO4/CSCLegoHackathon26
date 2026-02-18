
import streamlit as st
import json
import os

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def load_data(file):
    path = f"{DATA_DIR}/{file}"
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

def save_data(file, data):
    with open(f"{DATA_DIR}/{file}", "w") as f:
        json.dump(data, f, indent=2)

st.set_page_config(page_title="Warrior Hub", layout="centered")

st.title("🏹 Warrior Hub (Stan State)")

if "user" not in st.session_state:
    email = st.text_input("Stan State Email")
    if st.button("Login"):
        if email.endswith("@csustan.edu"):
            st.session_state.user = email
            st.success("Logged in!")
            st.rerun()
        else:
            st.error("Only @csustan.edu emails allowed")
    st.stop()

st.sidebar.write(f"Logged in as: {st.session_state.user}")
page = st.sidebar.radio("Menu", ["Study Hall", "Campus Life", "Discounts"])

if page == "Study Hall":
    st.header("📚 Study Hall")
    courses = load_data("courses.json")
    notes = load_data("notes.json")

    with st.form("add_course"):
        course = st.text_input("Course name (ex: CS 4440)")
        if st.form_submit_button("Add Course"):
            courses.append(course)
            save_data("courses.json", courses)
            st.success("Course added")
            st.rerun()

    for c in courses:
        st.write(f"• {c}")
        note = st.text_input(f"Add note for {c}", key=c)
        if st.button("Save Note", key=f"btn_{c}"):
            notes.append({"course": c, "note": note, "user": st.session_state.user})
            save_data("notes.json", notes)
            st.success("Note saved")

    st.subheader("All Notes")
    for n in notes:
        st.write(f"**{n['course']}** – {n['note']} ({n['user']})")

elif page == "Campus Life":
    st.header("📍 Campus Life")
    spots = load_data("campus_life.json")

    with st.form("add_spot"):
        place = st.text_input("Place")
        category = st.selectbox("Category", ["Study Spot", "Food", "Hangout"])
        if st.form_submit_button("Add"):
            spots.append({"place": place, "category": category, "user": st.session_state.user})
            save_data("campus_life.json", spots)
            st.success("Added!")
            st.rerun()

    for s in spots:
        st.write(f"• {s['place']} ({s['category']})")

elif page == "Discounts":
    st.header("💸 Local Discounts")
    discounts = load_data("discounts.json")

    with st.form("add_discount"):
        business = st.text_input("Business Name")
        deal = st.text_input("Discount Details")
        if st.form_submit_button("Submit"):
            discounts.append({"business": business, "deal": deal, "user": st.session_state.user})
            save_data("discounts.json", discounts)
            st.success("Submitted!")
            st.rerun()

    for d in discounts:
        st.write(f"**{d['business']}** – {d['deal']}")
