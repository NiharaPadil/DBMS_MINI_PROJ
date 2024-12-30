import streamlit as st
import mysql.connector
import base64

from database import establish_connection
from home import display_observations, insert_observation, delete_observation, update_observation_location, \
    display_species, insert_species, delete_species, update_species, display_cons, insert_cons, delete_cons, \
    display_Habitats, insert_Habitats, delete_Habitats, update_Habitats, display_data, \
    insert_data, delete_data, update_data, display_protected_by, \
    search_species, search_habitats, search_cons, search_observation, search_Environmental_data, search_protected, \
    update_cons \

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#",
    database="#"
)
cursor = db.cursor()


import base64

# Read the image file
with open("Background.jpeg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()

# Construct the CSS with the base64 encoded image
bg_img = f'''
<style>
    [data-testid="stAppViewContainer"] {{
        background-image: url('data:image/jpeg;base64,{encoded_string}');
        background-size: cover;
        background-repeat: no-repeat;
    }}
</style>
'''

# Display the CSS in your Streamlit app
st.markdown(bg_img, unsafe_allow_html=True)



def login(cursor):
    with st.expander("Login", expanded=True):
        login_identifier = st.text_input("Username or Email 📧")
        password = st.text_input("Password 🔒", type="password")

        if st.button("Login", key='login'):
            if not login_identifier or not password:
                st.error("Please enter both username/email and password.")
                return False

            cursor.execute(
                "SELECT * FROM ManagementUsers WHERE (BINARY username = %s OR BINARY email = %s) AND BINARY password = %s",
                (login_identifier, login_identifier, password))
            user = cursor.fetchone()
            if user:
                st.success("Logged in successfully! 🎉")
                st.session_state["logged_in"] = True
                st.experimental_rerun()
                return True
            else:
                st.error("Invalid username/email or password ❌")
                return False
    return False

def signup(cursor):
    with st.expander("Sign Up", expanded=True):
        new_username = st.text_input("New Username 🆕")
        new_email = st.text_input("New Email 📧")
        new_password = st.text_input("New Password 🔒", type="password")
        department = st.selectbox("Select Department", ["Operations", "Conservation"])

        if st.button("Sign Up", key='signup'):
            cursor.execute("SELECT * FROM ManagementUsers WHERE BINARY username = %s OR BINARY email = %s",
                           (new_username, new_email))
            existing_user = cursor.fetchone()
            if existing_user:
                st.error("Username or email already exists. Please choose a different username or email. ❌")
            else:
                cursor.execute(
                    "INSERT INTO ManagementUsers (username, email, password, department) VALUES (%s, %s, %s, %s)",
                    (new_username, new_email, new_password, department))
                db.commit()
                st.success("Sign up successful! You can now login. ✅")

def home_page():
    print()
    st.subheader("Welcome to the home page!!")
    with st.expander("Dashboard Options"):
        dashboard_option = st.selectbox("",["Home","Species", "Conservation Project", "Wildlife preserve Info", "Observation", "Environmental_data", "Protected By"])
    if dashboard_option == "":
        st.write("Welcome!!!")
    elif dashboard_option == "Species":
        st.write("Different Species")
        search_query = st.text_input("Search by Species name or ID:")
        if st.button("Search"):
            species_data = search_species(cursor, search_query)

            if species_data:
                st.write("### Search Results:")
                for species in species_data:
                    st.write(f"Species_id: {species[0]}, Species_Name: {species[1]}, classification: {species[2]}")
            else:
                st.write("No Species found matching the search query.")
        menu = st.sidebar.radio("Menu", ["Display Species", "Insert Species", "Delete Species",
                                         "Update Species"])
        if menu == "Display Species":
            display_species(cursor)
        elif menu == "Insert Species":
            insert_species(db, cursor)
        elif menu == "Delete Species":
            delete_species(db, cursor)
        elif menu == "Update Species":
            update_species(db, cursor)

        cursor.close()
        db.close()
        pass
    elif dashboard_option == "Conservation Project":
        st.write("Conservation Project Status")
        search_query = st.text_input("Search by Conservation project name or ID:")
        if st.button("Search"):
            cons_data = search_cons(cursor, search_query)
            if cons_data:
                st.write("### Search Results:")
                for cons in cons_data:
                    st.write(f"Project ID: {cons[0]}, Project Name: {cons[1]}, Start date: {cons[2]}, End date: {cons[3]}, Species: {cons[4]}")
            else:
                st.write("No Species found matching the search query.")
        menu = st.sidebar.radio("Menu", ["Display Conservation Project", "Insert Conservation Project",
                                         "Delete Conservation Project",
                                         "Update Conservation Project"])

        if menu == "Display Conservation Project":
            display_cons(cursor)
        elif menu == "Insert Conservation Project":
            insert_cons(db, cursor)
        elif menu == "Delete Conservation Project":
            delete_cons(db, cursor)
        elif menu == "Update Conservation Project":
            update_cons(db, cursor)
        cursor.close()
        db.close()

    elif dashboard_option == "Wildlife preserve Info":
        st.write("Wildlife preserve Info ")
        search_query = st.text_input("Search by Wildlife Preserve name or ID:")
        if st.button("Search"):
            habitat_data = search_habitats(cursor, search_query)
            if habitat_data:
                st.write("### Search Results:")
                for habitat in habitat_data:
                    st.write(f"Species_preserve ID: {habitat[0]}, Species_preserve Name: {habitat[1]}, Species_id: {habitat[4]}")
            else:
                st.write("No Wildlife Preserves found matching the search query.")
        menu = st.sidebar.radio("Menu", ["Display Wildlife preserve", "Insert Wildlife preserve","Delete Wildlife preserve","Update Wildlife preserve"])
        if menu == "Display Wildlife preserve":
            display_Habitats(cursor)
        elif menu == "Insert Wildlife preserve":
            insert_Habitats(db, cursor)
        elif menu == 'Delete Wildlife preserve':
            delete_Habitats(db,cursor)
        elif menu == "Update Wildlife preserve":
            update_Habitats(db,cursor)
        cursor.close()
        db.close()
    elif dashboard_option == "Observation":
        st.title("Observations Management System")
        search_query = st.text_input("Search by Observation location or ID:")
        if st.button("Search"):
            obs_data = search_observation(cursor, search_query)
            if obs_data:
                st.write("### Search Results:")
                for ob in obs_data:
                    st.write(f"Observation ID: {ob[0]}, Observation date: {ob[1]}, Observation location: {ob[2]}, Species ID: {ob[3]}, Data ID: {ob[4]}")
            else:
                st.write("No Observation found matching the search query.")

        menu = st.sidebar.radio("Menu", ["Display Observations", "Insert Observation", "Delete Observation",
                                         "Update Observation Location"])
        if menu == "Display Observations":
            display_observations(cursor)
        elif menu == "Insert Observation":
            insert_observation(db, cursor)
        elif menu == "Delete Observation":
            delete_observation(db, cursor)
        elif menu == "Update Observation Location":
            update_observation_location(db, cursor)

        cursor.close()
        db.close()

    elif dashboard_option == ("Environmental_data"):
        st.title("Environmental Data")
        search_query = st.text_input("Search by Data ID or Wildlife Preserve ID")
        if st.button("Search"):
            e_data = search_Environmental_data(cursor, search_query)
            if e_data:
                st.write("### Search Results:")
                for data in e_data:
                    st.write(f"Data ID: {data[0]}, Water Quality: {data[1]}, Weather condition: {data[2]}, Soil Quality: {data[3]}, Air Quality: {data[4]},Wildlife preserve ID: {data[5]}")
            else:
                st.write("No environmental data found matching the search query.")
        menu = st.sidebar.radio("Menu",["Display Environmental Data", "Insert Environmental Data", "Delete Environmental Data",
                                  "Update Environmental Data"])

        if menu == "Display Environmental Data":
            display_data(cursor)
        elif menu == "Insert Environmental Data":
            insert_data(db, cursor)
        elif menu == "Delete Environmental Data":
            delete_data(db, cursor)
        elif menu == "Update Environmental Data":
            update_data(db, cursor)

        cursor.close()
        db.close()
    elif dashboard_option == "Protected By":
        st.title("Protected By")
        search_query = st.text_input("Search by Project ID or Species ID")
        if st.button("Search"):
            protected_data = search_protected(cursor, search_query)
            if protected_data is not None:
                if protected_data:
                    st.write("### Search Results:")
                    for data in protected_data:
                        st.write(f"Species ID: {data[1]}, Conservation Status: {data[0]}, Project ID: {data[2]}")
                else:
                    st.write("No protected data found matching the search query.")
            else:
                st.write("Please provide a valid search query.")

        menu = st.sidebar.radio("Menu", ["Display Protected By"])

        if menu == "Display Protected By":
            display_protected_by(cursor)
        cursor.close()
        db.close()


def main():

    st.markdown("<h1 style='text-align: center;'>SPECIES PRESERVATION MANAGEMENT SYSTEM</h2>", unsafe_allow_html=True)


    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if st.session_state["logged_in"]:
        if st.button('Logout', key='logout'):
            st.session_state["logged_in"] = False
            st.experimental_rerun()
        st.write("You are logged in!")  # Add a debug statement to check if this is executed
        home_page()  # Check if home page content is called when logged in
    else:
        action = st.radio("Choose an option:", ["Login", "Sign Up"])

        if action == "Login":
            if login(cursor):
                st.write("Login successful!")
                home_page()
        elif action == "Sign Up":
            signup(cursor)

if __name__ == "__main__":
    main()
