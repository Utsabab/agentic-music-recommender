import asyncio
import os
from typing import Optional
import google.generativeai as genai
from recommender import UserProfile

VALID_GENRES = [
    "ambient", "blues", "classical", "country", "disco", "electronic",
    "folk", "hip-hop", "indie", "jazz", "lofi", "metal", "pop",
    "r&b", "reggae", "rock", "synthwave",
]

VALID_MOODS = [
    "aggressive", "chill", "confident", "energetic", "focused", "fun",
    "happy", "intense", "melancholic", "moody", "nostalgic", "peaceful",
    "reflective", "relaxed", "smooth",
]

# Initialize Google Generative AI with API key from environment
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


async def genre_agent(user_input: str) -> str:
    """Extracts the best-matching genre from a natural language description."""
    def _call():
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            f"You are a music genre classifier. Given a description of music preference, "
            f"pick the single best-matching genre from: {', '.join(VALID_GENRES)}. "
            f"Reply with ONLY the genre name, nothing else.\n\nUser: {user_input}"
        )
        result = response.text.strip().lower()
        return result if result in VALID_GENRES else "pop"

    return await asyncio.to_thread(_call)


async def mood_agent(user_input: str) -> str:
    """Extracts the best-matching mood from a natural language description."""
    def _call():
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            f"You are a music mood classifier. Given a description of music preference, "
            f"pick the single best-matching mood from: {', '.join(VALID_MOODS)}. "
            f"Reply with ONLY the mood name, nothing else.\n\nUser: {user_input}"
        )
        result = response.text.strip().lower()
        return result if result in VALID_MOODS else "chill"

    return await asyncio.to_thread(_call)


async def energy_agent(user_input: str) -> float:
    """Extracts a target energy level (0.0–1.0) from a natural language description."""
    def _call():
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            f"You are an energy level extractor for music. "
            f"Given a description, output a single float from 0.0 (very calm/quiet) "
            f"to 1.0 (very intense/energetic). Reply with ONLY the number, nothing else.\n\nUser: {user_input}"
        )
        try:
            return max(0.0, min(1.0, float(response.text.strip())))
        except ValueError:
            return 0.5

    return await asyncio.to_thread(_call)


async def acoustic_agent(user_input: str) -> bool:
    """Determines whether the user prefers acoustic over electronic sound."""
    def _call():
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            f"You are an acoustic preference detector for music. "
            f"Given a description, determine if the user prefers acoustic/natural sound "
            f"over electronic/produced sound. Reply with ONLY 'true' or 'false'.\n\nUser: {user_input}"
        )
        return response.text.strip().lower() == "true"

    return await asyncio.to_thread(_call)


async def valence_agent(user_input: str) -> Optional[float]:
    """Extracts emotional positivity (0.0–1.0) or None if ambiguous."""
    def _call():
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            f"You are a valence extractor for music. Valence measures emotional positivity "
            f"(0.0 = very sad/dark, 0.5 = neutral, 1.0 = very happy/uplifting). "
            f"Given a description, output a float 0.0–1.0 if the emotional tone is clear, "
            f"or 'null' if it is ambiguous. Reply with ONLY the number or the word 'null'.\n\nUser: {user_input}"
        )
        text = response.text.strip().lower()
        if text == "null":
            return None
        try:
            return max(0.0, min(1.0, float(text)))
        except ValueError:
            return None

    return await asyncio.to_thread(_call)


async def explanation_agent(
    user_profile: UserProfile,
    recommendations: list,
    user_input: str
) -> str:
    """Generates a natural language explanation for why these songs were recommended.

    Args:
        user_profile: The extracted user preferences
        recommendations: List of tuples (song_dict, score, reasons_str)
        user_input: Original natural language input from user

    Returns:
        A cohesive narrative explanation of the recommendations
    """
    def _call():
        # Format recommendation details
        rec_details = []
        for song, score, reasons in recommendations:
            rec_details.append(
                f"- '{song['title']}' by {song['artist']} (Score: {score:.1f})\n"
                f"  Reasons: {reasons}"
            )
        rec_text = "\n".join(rec_details)

        prompt = (
            f"You are a music recommendation expert explaining why certain songs match a user's taste.\n\n"
            f"User's request: \"{user_input}\"\n\n"
            f"Extracted preferences:\n"
            f"- Genre: {user_profile.favorite_genre}\n"
            f"- Mood: {user_profile.favorite_mood}\n"
            f"- Energy level: {user_profile.target_energy:.1f}/1.0\n"
            f"- Prefers acoustic: {user_profile.likes_acoustic}\n"
            f"- Emotional tone (valence): {user_profile.target_valence if user_profile.target_valence else 'not specified'}\n\n"
            f"Top recommendations:\n{rec_text}\n\n"
            f"Generate a warm, coherent paragraph (2-3 sentences) explaining why these songs match the user's taste. "
            f"Focus on how the recommendations align with their stated preferences and mood. "
            f"Be conversational and insightful, not mechanical."
        )

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()

    return await asyncio.to_thread(_call)


async def extract_user_profile(user_input: str) -> UserProfile:
    """Runs all 5 preference agents in parallel and assembles a UserProfile."""
    genre, mood, energy, acoustic, valence = await asyncio.gather(
        genre_agent(user_input),
        mood_agent(user_input),
        energy_agent(user_input),
        acoustic_agent(user_input),
        valence_agent(user_input),
    )
    return UserProfile(
        favorite_genre=genre,
        favorite_mood=mood,
        target_energy=energy,
        likes_acoustic=acoustic,
        target_valence=valence,
    )
