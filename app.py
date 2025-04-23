import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="College Predictor", layout="centered")

# Now you can use Streamlit


st.markdown("""
    <style>
    /* Background gradient */
    .stApp {
        background: linear-gradient(135deg, #a1c4fd, #c2e9fb);
        background-attachment: fixed;
        font-family: 'Segoe UI', sans-serif;
        color: #003049;
    }

    /* Card feel for widgets */
    .css-1kyxreq, .css-1d391kg, .css-1cpxqw2 {
        background: rgba(255, 255, 255, 0.3) !important;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }

    /* Title Styling */
    h1, h2, h3, .stMarkdown h1 {
        color: #002e56;
        text-shadow: 1px 1px 0 rgba(255, 255, 255, 0.4);
    }

    /* Buttons */
    .stButton > button {
        background-color: #0077b6;
        color: white;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease-in-out;
    }

    .stButton > button:hover {
        background-color: #00b4d8;
        transform: scale(1.02);
    }

    /* Input fields */
    input, select, textarea {
        background-color: rgba(255, 255, 255, 0.6) !important;
        border-radius: 8px !important;
        color: #003049 !important;
    }

    /* Expander */
    .st-expander {
        background: rgba(255, 255, 255, 0.4) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(0, 183, 255, 0.3);
    }

    /* Scrollbar (optional beautify) */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-thumb {
        background: #0077b6;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)


st.title("Welcome to the College Predictor")

# --- Google Sheets Authentication Setup ---
# Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Authenticate using the credentials JSON file
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Open the Google Sheets document by URL
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1APJOILkhM6DWZ-uAp6a6923bYzt9GOrbN4NP-yBD5SU/edit?gid=0#gid=0").sheet1

# --- Function to store data in Google Sheets ---
def store_in_sheet(name, contact, jee_rank, category, city):
    # Use the already authenticated sheet
    sheet.append_row([name, contact, jee_rank, category, city])

# --- UI Setup ---
st.title("🎓 College Predictor - JoSAA Based")
josaa_df = pd.read_csv("data/JOSAA.csv")
josaa_df.columns = josaa_df.columns.str.strip().str.replace(' ', '_')
josaa_df['Closing_Rank'] = josaa_df['Closing_Rank'].astype(str).str.replace('P', '', regex=False)
josaa_df['Closing_Rank'] = pd.to_numeric(josaa_df['Closing_Rank'], errors='coerce')

# --- User Inputs ---
st.header("📋 Enter Your Details")
rank = st.number_input("Enter Your JEE Rank", min_value=1)
category = st.selectbox("Select Category", ['OPEN', 'EWS', 'OBC-NCL', 'SC', 'ST', 'OPEN (PwD)', 'OBC-NCL (PwD)', 'SC (PwD)', 'ST (PwD)', 'EWS (PwD)'])
gender = st.selectbox("Select Gender", ['Gender-Neutral', 'Female-only (including Supernumerary)'])
quota = st.selectbox("Select Quota", ['AI'])

# --- Show Eligible Colleges ---
if st.button("🔍 Show Eligible Colleges", key="show_colleges"):
    eligible_df = josaa_df[
        (josaa_df['Seat_Type'] == category) & 
        (josaa_df['Gender'] == gender) & 
        (josaa_df['Quota'] == quota) & 
        (josaa_df['Closing_Rank'] >= rank)
    ]
    st.success(f"✅ Found {len(eligible_df)} eligible options.")
    st.dataframe(eligible_df[['Institute', 'Academic_Program_Name', 'Seat_Type', 'Gender', 'Closing_Rank']])

# --- Counselling Section ---
with st.expander("🧑‍💼 Need Counselling Support?"):
    st.markdown("Fill the form below. Our expert will reach out to help you personally.")
    name = st.text_input("Name")
    contact = st.text_input("Contact Number")
    jee_rank = st.text_input("Your JEE Rank")
    cat = st.selectbox("Category", ['OPEN', 'EWS', 'OBC-NCL', 'SC', 'ST', 'OPEN (PwD)', 'OBC-NCL (PwD)', 'SC (PwD)', 'ST (PwD)', 'EWS (PwD)'], key="counselling_cat")
    city = st.text_input("City")
    
    if st.button("📨 Submit for Counselling", key="submit_counselling"):
        # Store the form data in Google Sheets
        store_in_sheet(name, contact, jee_rank, cat, city)
        st.success("✅ Details submitted")

# --- Re-attempt Section ---
st.markdown("---")
st.markdown("🎯 Not satisfied with your rank?")
if st.button("🔁 Want to Prepare Again for JEE?", key="prepare_again"):
    st.markdown("[Click here to prepare again! 🚀](https://theaicharya.in/)", unsafe_allow_html=True)
