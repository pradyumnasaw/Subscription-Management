import streamlit as st
import pandas as pd
from database import add_member, update_member, update_status, get_all_members, search_members, get_payment_history, get_upcoming_renewals, export_data

# Initialize session state for page navigation if not already set
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_to_new_member():
    st.session_state.page = "new_member_details"

def go_to_update():
    st.session_state.page = "update"

def go_to_home():
    st.session_state.page = "home"

def go_to_manage_membership():
    st.session_state.page = "activate_deactivate_mem"

def go_to_view_members():
    st.session_state.page = "view_members"

def go_to_search_members():
    st.session_state.page = "search_members"

def go_to_payment_tracking():
    st.session_state.page = "payment_tracking"

def go_to_upcoming_renewals():
    st.session_state.page = "upcoming_renewals"

def go_to_download_reports():
    st.session_state.page = "download_reports"

def register_btn(name, number, email, membership_type, start_date, end_date):
    if name and number and email and membership_type and start_date and end_date:
        mem_info = {
            "name": name,
            "mobile": number,
            "email": email,
            "mem_type": membership_type,
            "start_date": start_date,
            "end_date": end_date
        }
        add_member(mem_info)
        st.success("Registration Successful!")
        st.session_state.page = "home"
    else:
        st.error("All fields are required!")

def update_details_btn(id, number, email, membership_type):
    if id and number and email and membership_type:
        update_info = {
            "id": id,
            "mobile": number,
            "email": email,
            "mem_type": membership_type
        }
        update_member(update_info)
        st.success("Details updated successfully!")
        st.session_state.page = "home"
    else:
        st.error("All fields are required!")

def act_deact_btn(id, act_deact):
    if id and act_deact:
        update_status_info = {
            "id": id,
            "act_deact": act_deact 
        }
        update_status(update_status_info)
        st.success("Membership status updated successfully!")
        st.session_state.page = 'home'
    else:
        st.error("All fields are required!")

def show_page(page):
    if page == "home":
        st.write("# Membership Management and Subscriptions")
        st.button("Register New Member", on_click=go_to_new_member)
        st.button("Update Details", on_click=go_to_update)
        st.button("Manage Membership", on_click=go_to_manage_membership)
        st.button("View Members List", on_click=go_to_view_members)
        st.button("Search Members", on_click=go_to_search_members)
        st.button("Payment Tracking", on_click=go_to_payment_tracking)
        st.button("Upcoming Renewals", on_click=go_to_upcoming_renewals)
        st.button("Download Reports", on_click=go_to_download_reports)

    elif page == "new_member_details":
        st.title("New Member Registration")
        name = st.text_input("Enter your full name")
        col1, col2 = st.columns(2)
        with col1:
            number = st.text_input("Enter mobile no.")
        with col2:
            email = st.text_input("Enter your email")
        membership_type = st.selectbox("Membership Type", ["Monthly", "Quarterly", "Yearly"], index=0)
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date")
        with col2:
            end_date = st.date_input("End Date")
        col1, col2 = st.columns(2)
        with col1:
            st.button("Home", on_click=go_to_home)
        with col2:
            st.button("Submit", on_click=register_btn, args=(name, number, email, membership_type, start_date, end_date))

    elif page == "update":
        st.title("Update your details")
        id = st.text_input("Enter Member ID")
        col1, col2 = st.columns(2)
        with col1:
            number = st.text_input("Enter mobile no.")
        with col2:
            email = st.text_input("Enter your email")
        membership_type = st.selectbox("Membership Type", ["Monthly", "Quarterly", "Yearly"], index=0)
        col1, col2 = st.columns(2)
        with col1:
            st.button("Home", on_click=go_to_home)
        with col2:
            st.button("Update", on_click=update_details_btn, args=(id, number, email, membership_type))

    elif page == "activate_deactivate_mem":
        st.title("Activate/Deactivate Membership")
        id = st.text_input("Enter Member ID")
        act_deact = st.selectbox("Activate/Deactivate", ["Activate", "Deactivate"], index=0)
        col1, col2 = st.columns(2)
        with col1:
            st.button("Home", on_click=go_to_home)
        with col2:
            st.button("Update", on_click=act_deact_btn, args=(id, act_deact))

    elif page == "view_members":
        st.title("View Members List")
        members = get_all_members()
        df = pd.DataFrame(members)
        st.dataframe(df)
        st.button("Home", on_click=go_to_home)

    elif page == "search_members":
        st.title("Search Members")
        search_by = st.selectbox("Search by", ["Name", "Email", "Membership Type"], index=0)
        search_value = st.text_input(f"Enter {search_by}")
        if st.button("Search"):
            results = search_members(search_by, search_value)
            df = pd.DataFrame(results)
            st.dataframe(df)
        st.button("Home", on_click=go_to_home)

    elif page == "payment_tracking":
        st.title("Payment Tracking")
        member_id = st.text_input("Enter Member ID")
        if st.button("View Payment History"):
            payments = get_payment_history(member_id)
            df = pd.DataFrame(payments)
            st.dataframe(df)
        st.button("Home", on_click=go_to_home)

    elif page == "upcoming_renewals":
        st.title("Upcoming Renewals")
        renewals = get_upcoming_renewals()
        df = pd.DataFrame(renewals)
        st.dataframe(df)
        st.button("Home", on_click=go_to_home)

    elif page == "download_reports":
        st.title("Download Reports")
        if st.button("Download CSV"):
            data = export_data()
            df = pd.DataFrame(data)
            csv = df.to_csv(index=False)
            st.download_button(label="Download CSV", data=csv, file_name="members_report.csv", mime="text/csv")
        st.button("Home", on_click=go_to_home)

show_page(st.session_state.page)