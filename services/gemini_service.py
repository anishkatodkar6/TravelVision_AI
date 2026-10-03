from google import genai
from google.genai import types
import os


# --------------------------------------------------
# CREATE GEMINI CLIENT
# --------------------------------------------------

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# --------------------------------------------------
# ANALYZE TRAVEL IMAGE
# --------------------------------------------------

def analyze_travel_image(image_bytes, mime_type):
    """
    Analyze a travel image using Gemini Vision.
    """

    prompt = """
You are TravelVision AI, an intelligent travel assistant.

Analyze the uploaded travel image and identify the place,
landmark, monument, building, or destination if possible.

Return the answer using EXACTLY this structure:

📍 Place & Location

Place: [name of place or landmark]
City: [city]
Country: [country]

📝 About the Place

Write a short and interesting description in 3-4 sentences.

✨ Interesting Facts

- Fact 1
- Fact 2
- Fact 3

📌 Nearby Attractions

- Attraction 1
- Attraction 2
- Attraction 3

💡 Travel Tips

- Tip 1
- Tip 2

IMPORTANT RULES:

- Do not pretend to know the exact location if the image is unclear.
- If identification is uncertain, clearly mention that it is uncertain.
- Do not invent facts.
- Keep the answer simple and useful.
- Do not put Place, City and Country on the same line.
- Always put Place, City and Country on separate lines.
"""

    # Convert image bytes into Gemini image part
    image_part = types.Part.from_bytes(
        data=image_bytes,
        mime_type=mime_type
    )

    # Send image + prompt to Gemini
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=[
            image_part,
            prompt
        ]
    )

    return response.text

# --------------------------------------------------
# FOLLOW-UP TRAVEL CHAT
# --------------------------------------------------

def ask_travel_question(place_context, question):
    """
    Answer a follow-up travel question using the
    previously analyzed place as context.
    """

    prompt = f"""
You are TravelVision AI, a helpful travel assistant.

The user previously uploaded a travel image and Gemini
identified/analyzed the following place:

{place_context}

Now the user has asked:

{question}

Answer the user's question using the place information
above as context.

Rules:
- Give a clear and useful answer.
- Keep the answer simple and easy to understand.
- If the information is uncertain, clearly say so.
- Do not invent specific facts.
- If the question is unrelated to the place, answer normally.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text 
# --------------------------------------------------
# FOLLOW-UP TRAVEL CHAT
# --------------------------------------------------

def ask_travel_question(place_context, question):
    """
    Answer a follow-up travel question using the
    previously analyzed place as context.
    """

    prompt = f"""
You are TravelVision AI, a helpful travel assistant.

The user previously uploaded a travel image and Gemini
identified/analyzed the following place:

{place_context}

The user now asks:

{question}

Answer the question using the place information above
as context.

Rules:
- Give a clear and useful answer.
- Keep the answer simple and easy to understand.
- If information is uncertain, clearly say so.
- Do not invent specific facts.
- If the question is unrelated to the place, answer normally.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text 
# --------------------------------------------------
# AI TRIP PLANNER
# --------------------------------------------------

def generate_trip_plan(
    destination,
    days,
    travelers,
    budget,
    interests
):
    """
    Generate a personalized travel itinerary
    using Gemini.
    """

    interests_text = (
        ", ".join(interests)
        if interests
        else "General sightseeing"
    )

    prompt = f"""
You are TravelVision AI, an intelligent travel planner.

Create a practical travel itinerary for:

Destination: {destination}
Number of days: {days}
Number of travelers: {travelers}
Budget: {budget}
Interests: {interests_text}

Return the answer using this structure:

## 🗺️ {days}-Day {destination} Trip

Give a short introduction to the trip.

## 📅 Day 1

- Morning:
- Afternoon:
- Evening:

Continue for all {days} days.

## 🍴 Food Suggestions

- Suggest suitable local foods or food experiences.

## 💰 Budget Guidance

Give simple budget guidance suitable for the selected
budget level.

## 💡 Travel Tips

- Give 3-5 useful travel tips.

IMPORTANT:
- Keep the itinerary practical.
- Consider the user's interests.
- Avoid inventing specific information.
- Do not repeat the same attraction unnecessarily.
- Keep the language simple and useful.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text
