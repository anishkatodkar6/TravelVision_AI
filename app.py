import streamlit as st
from PIL import Image
import re

from services.gemini_service import (
    analyze_travel_image,
    ask_travel_question,
    generate_trip_plan
)
# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="TravelVision AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #f7f9fc;
    }

    /* Main title */
    .main-title {
        font-size: 48px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        font-size: 20px;
        color: #666666;
        margin-bottom: 35px;
    }

    /* Feature cards */
    .feature-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        min-height: 150px;
        box-shadow: 0px 3px 12px rgba(0,0,0,0.08);
    }

    .feature-icon {
        font-size: 35px;
    }

    .feature-title {
        font-size: 20px;
        font-weight: 700;
    }

    .feature-text {
        color: #666666;
    }

    /* Result box */
    .result-box {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0px 3px 12px rgba(0,0,0,0.08);
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #777777;
        padding: 30px;
        font-size: 14px;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)
# --------------------------------------------------
# NAVIGATION FUNCTION
# --------------------------------------------------

def go_to_trip_planner(city):
    st.session_state["trip_destination"] = city
    st.session_state["selected_page"] = "🗺️ Trip Planner"


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

# Set default page
if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "🏠 Home"


with st.sidebar:

    st.title("🌍 TravelVision AI")

    st.markdown("---")

    st.subheader("Navigation")

    page = st.radio(
        "Go to",
        [
            "🏠 Home",
            "🔍 Explore Place",
            "🗺️ Trip Planner"
        ],
        key="selected_page"
    )

    st.markdown("---")

    st.caption(
        "Snap a place. Discover the story."
    )

# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

if page == "🏠 Home":

    st.markdown(
        '<div class="main-title">🌍 TravelVision AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Snap a place. Discover the story.'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # HERO SECTION
    # --------------------------------------------------

    st.info(
        "📸 Upload a travel photo and TravelVision AI "
        "will help you explore the place."
    )

    uploaded_file = st.file_uploader(
        "Upload your travel photo",
        type=["jpg", "jpeg", "png", "webp"],
        help="Upload a clear photo of a landmark, monument, "
             "building, landscape or travel destination."
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        st.markdown("### 📷 Your Travel Photo")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.image(
                image,
                caption="Uploaded Travel Photo",
                use_container_width=True
            )

        with col2:

            st.markdown("### 🔍 Ready to explore?")

            st.write(
                "TravelVision AI will analyze your photo "
                "and provide travel information."
            )

            analyze_button = st.button(
                "🌍 Explore Place",
                type="primary",
                use_container_width=True
            )

            if analyze_button:

                st.success(
                    "Image received successfully!"
                )

                st.markdown("### 🤖 TravelVision Analysis")

                st.info(
                    "Gemini Vision will be connected in "
                    "Phase 2. This section will identify "
                    "the place and provide travel information."
                )


    # --------------------------------------------------
    # FEATURES
    # --------------------------------------------------

    st.markdown("---")

    st.markdown("## ✨ What TravelVision AI can do")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📍</div>
                <div class="feature-title">
                    Identify Places
                </div>
                <div class="feature-text">
                    Recognize landmarks and destinations
                    from photographs.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📖</div>
                <div class="feature-title">
                    Discover History
                </div>
                <div class="feature-text">
                    Learn interesting facts and historical
                    information.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🗺️</div>
                <div class="feature-title">
                    Plan Trips
                </div>
                <div class="feature-text">
                    Create personalized travel itineraries.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">💬</div>
                <div class="feature-title">
                    Ask AI
                </div>
                <div class="feature-text">
                    Chat with TravelVision about your
                    destination.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# --------------------------------------------------
# EXPLORE PAGE
# --------------------------------------------------

elif page == "🔍 Explore Place":

    st.title("🔍 Explore a Place")

    st.write(
        "Upload a photo of a landmark, monument, "
        "building or destination."
    )

    uploaded_file = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png", "webp"],
        key="explore_upload"
    )

    if uploaded_file:

        # Display uploaded image
        image = Image.open(uploaded_file)

        st.image(
            image,
            caption="Your uploaded image",
            use_container_width=True
        )

        # Analyze button
        if st.button(
            "🔍 Analyze Image",
            type="primary"
        ):

            with st.spinner(
                "🌍 Gemini is analyzing your travel photo..."
            ):

                try:

                    # --------------------------------
                    # SEND IMAGE TO GEMINI
                    # --------------------------------

                    image_bytes = uploaded_file.getvalue()
                    mime_type = uploaded_file.type

                    result = analyze_travel_image(
                        image_bytes,
                        mime_type
                    )

                    # Save travel context
                    st.session_state["travel_context"] = result

                    st.success(
                        "✅ Analysis completed!"
                    )

                    st.markdown(
                        "## 🌍 Your Travel Guide"
                    )

                    # --------------------------------
                    # DISPLAY GEMINI RESULT
                    # --------------------------------

                    clean_result = result.strip()

                    # Split the Gemini response into sections
                    sections = re.split(
                        r"(?=📍 Place & Location|📝 About the Place|✨ Interesting Facts|📌 Nearby Attractions|💡 Travel Tips)",
                        clean_result
                    )

                    # --------------------------------
                    # PLACE & LOCATION
                    # --------------------------------

                    place_section = next(
                        (s for s in sections if "📍 Place & Location" in s),
                        ""
                    )

                    place_match_name = re.search(
                        r"Place:\s*(.*?)(?=\s+City:|$)",
                        place_section,
                        re.S
                    )

                    city_match = re.search(
                        r"City:\s*(.*?)(?=\s+Country:|$)",
                        place_section,
                        re.S
                    )

                    country_match = re.search(
                        r"Country:\s*(.*)",
                        place_section,
                        re.S
                    )

                    place_name = (
                        place_match_name.group(1).strip()
                        if place_match_name
                        else "Unknown place"
                    )

                    city = (
                        city_match.group(1).strip()
                        if city_match
                        else ""
                    )

                    country = (
                        country_match.group(1).strip()
                        if country_match
                        else ""
                    )

                    location_text = ", ".join(
                        x for x in [city, country]
                        if x
                    )

                    with st.container(border=True):

                        st.markdown("### 📍 Place & Location")

                        st.markdown(f"## {place_name}")

                        if location_text:
                            st.markdown(
                                f"📍 **{location_text}**"
                            )
                    # --------------------------------
                    # PLAN A TRIP HERE
                    # --------------------------------

                    if st.button(
                        "🗺️ Plan a Trip Here",
                        type="primary",
                        on_click=go_to_trip_planner,
                        args=(city,)
                    ):
                        pass
                    # --------------------------------
                    # ABOUT THE PLACE
                    # --------------------------------

                    about_section = next(
                        (s for s in sections if "📝 About the Place" in s),
                        ""
                    )

                    if about_section:

                        about_text = about_section.replace(
                            "📝 About the Place",
                            ""
                        ).strip()

                        with st.container(border=True):

                            st.markdown(
                                "### 📝 About the Place"
                            )

                            st.markdown(about_text)


                    # --------------------------------
                    # INTERESTING FACTS
                    # --------------------------------

                    facts_section = next(
                        (s for s in sections if "✨ Interesting Facts" in s),
                        ""
                    )

                    if facts_section:

                        facts_text = facts_section.replace(
                            "✨ Interesting Facts",
                            ""
                        ).strip()

                        with st.container(border=True):

                            st.markdown(
                                "### ✨ Interesting Facts"
                            )

                            st.markdown(facts_text)


                    # --------------------------------
                    # NEARBY ATTRACTIONS
                    # --------------------------------

                    attractions_section = next(
                        (s for s in sections if "📌 Nearby Attractions" in s),
                        ""
                    )

                    if attractions_section:

                        attractions_text = attractions_section.replace(
                            "📌 Nearby Attractions",
                            ""
                        ).strip()

                        with st.container(border=True):

                            st.markdown(
                                "### 📌 Nearby Attractions"
                            )

                            st.markdown(attractions_text)


                    # --------------------------------
                    # TRAVEL TIPS
                    # --------------------------------

                    tips_section = next(
                        (s for s in sections if "💡 Travel Tips" in s),
                        ""
                    )

                    if tips_section:

                        tips_text = tips_section.replace(
                            "💡 Travel Tips",
                            ""
                        ).strip()

                        with st.container(border=True):

                            st.markdown(
                                "### 💡 Travel Tips"
                            )

                            st.markdown(tips_text)
                except Exception as e:

                        st.error(
                            "❌ Something went wrong while "
                            "analyzing the image."
                        )

                        st.write(str(e))


# --------------------------------------------------
# FOLLOW-UP AI CHAT
# --------------------------------------------------

    if "travel_context" in st.session_state:

        st.markdown("---")

        st.markdown(
            "## 💬 Ask TravelVision"
        )

        st.write(
        "Have a question about this place? "
        "Ask TravelVision AI."
        )

        question = st.chat_input(
            "Ask something about this place..."
        )

        if question:
            with st.chat_message("user"):

                st.write(question)

            with st.chat_message("assistant"):

                with st.spinner(
                    "🌍 TravelVision is thinking..."
                ):

                    try:

                        answer = ask_travel_question(
                            st.session_state["travel_context"],
                            question
                        )

                        st.markdown(answer)

                    except Exception as e:

                        st.error(
                            "❌ Could not get an answer."
                        )

                        st.write(str(e))
# --------------------------------------------------
# TRIP PLANNER PAGE
# --------------------------------------------------

elif page == "🗺️ Trip Planner":

    st.title("🗺️ Trip Planner")

    st.write(
        "Plan your perfect trip with the help of TravelVision AI."
    )

    st.markdown("---")

    # --------------------------------
    # DESTINATION
    # --------------------------------

    default_destination = st.session_state.get(
        "trip_destination",
        ""
    )

    destination = st.text_input(
        "📍 Where do you want to go?",
        value=default_destination,
        placeholder="Example: Mumbai"
    )

    # --------------------------------
    # NUMBER OF DAYS
    # --------------------------------

    days = st.number_input(
        "📅 How many days?",
        min_value=1,
        max_value=30,
        value=3
    )

    # --------------------------------
    # NUMBER OF TRAVELERS
    # --------------------------------

    travelers = st.number_input(
        "👥 Number of travelers",
        min_value=1,
        max_value=20,
        value=2
    )

    # --------------------------------
    # BUDGET
    # --------------------------------

    budget = st.selectbox(
        "💰 Budget",
        [
            "Budget",
            "Moderate",
            "Luxury"
        ]
    )

    # --------------------------------
    # INTERESTS
    # --------------------------------

    interests = st.multiselect(
        "🎯 What are you interested in?",
        [
            "History",
            "Nature",
            "Food",
            "Shopping",
            "Adventure",
            "Culture",
            "Photography",
            "Nightlife"
        ]
    )

    st.markdown("---")

    # --------------------------------
    # PLAN TRIP BUTTON
    # --------------------------------

    if st.button(
        "✨ Plan My Trip",
        type="primary"
    ):

        if not destination:

            st.warning(
                "⚠️ Please enter a destination first."
            )

        else:

            with st.spinner(
                "🌍 TravelVision is creating your itinerary..."
            ):

                try:

                    trip_plan = generate_trip_plan(
                        destination,
                        days,
                        travelers,
                        budget,
                        interests
                    )

                    st.success(
                        "✅ Your trip plan is ready!"
                    )

                    st.markdown("---")

                    st.markdown(
                        "## 🗺️ Your Travel Plan"
                    )

                    st.markdown(
                        trip_plan
                    )

                except Exception as e:

                    st.error(
                        "❌ Could not create your trip plan."
                    )

                    st.write(str(e))
# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <div class="footer">
        🌍 TravelVision AI &nbsp; | &nbsp;
        AI-powered travel exploration
    </div>
    """,
    unsafe_allow_html=True
)