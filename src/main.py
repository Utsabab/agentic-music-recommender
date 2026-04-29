"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs

Run modes:
  python main.py              → agentic mode (natural language input via 5 parallel Gemini agents)
  python main.py --classic    → classic mode (hardcoded user_prefs dict)
"""

import asyncio
import os
import sys
from recommender import load_songs, recommend_songs
from agents import extract_user_profile, explanation_agent


def main() -> None:
    # Build path relative to this file's location
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(project_root, "data", "songs.csv")
    songs = load_songs(csv_path)

    user_prefs = {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.8}

    # Expected behavior: Will never get the +15 acousticness bonus (no electronic songs have > 0.7 acousticness). 
    # This user gets penalized by their own conflicting preferences.
    # user_prefs = {
    # "favorite_genre": "electronic",      # Electronic is 0.08 acousticness
    # "favorite_mood": "energetic",
    # "target_energy": 0.85,
    # "likes_acoustic": True,              # But wants acoustic sound!
    # "target_valence": 0.80
    # }

    # Expected behavior: Classical songs will likely have low energy, so they'll lose heavily on the energy score despite mood match. 
    # Thunder Strike (metal, 0.95 energy) might rank high due to energy alone, but has 0.35 valence—far from the sad 0.30 target.
    # user_prefs = {
    # "favorite_genre": "classical",       # Classical typically low energy
    # "favorite_mood": "melancholic",      # Sad + energetic don't mix
    # "target_energy": 0.95,               # Near maximum!
    # "target_valence": 0.30               # Very sad
    # }
    
    # Expected behavior: No song matches both mood AND genre (metal songs aren't peaceful). 
    # System can't satisfy both the mood preference (+25 points) and all energy/valence targets. Will force a choice.
    user_prefs = {
    "favorite_genre": "metal",           # 0.95 energy, 0.35 valence
    "favorite_mood": "peaceful",         # 0.62 energy, 0.77 valence
    "target_energy": 0.95,
    "target_valence": 0.30,
    "likes_acoustic": False
    }

    # Expected behavior: All songs score 0. 
    # The system should still return k songs. Does it return the first k? 
    # Does sorting break? Does random sampling apply to an unsorted list?
    # user_prefs = {}


    # # User profile matching the "Late Night Study Session" taste profile
    # user_prefs = {
    #     "favorite_genre": "lofi",
    #     "favorite_mood": "chill",
    #     "target_energy": 0.40,
    #     "likes_acoustic": True,
    #     "target_valence": 0.60
    # }

    # # User profile matching the "Gym Workout" taste profile
    # user_prefs = {
    #     "favorite_genre": "pop",
    #     "favorite_mood": "intense",
    #     "target_energy": 0.90,
    #     "likes_acoustic": False,
    #     "target_valence": 0.80
    # }

    # # User profile matching the "Electronic Dance Party" taste profile
    # user_prefs = {
    #     "favorite_genre": "electronic",
    #     "favorite_mood": "energetic",
    #     "target_energy": 0.85,
    #     "likes_acoustic": False,
    #     "target_valence": 0.80
    # }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


async def agentic_main() -> None:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(project_root, "data", "songs.csv")
    songs = load_songs(csv_path)

    print("\nWelcome to the Agentic Music Recommender!")
    print("Describe the kind of music you're in the mood for:")
    user_input = input("> ").strip()

    if not user_input:
        print("No input provided. Falling back to classic mode.\n")
        main()
        return

    print("\nRunning 5 specialist agents in parallel to extract your preferences...")
    profile = await extract_user_profile(user_input)

    print("\nExtracted preferences:")
    print(f"  Genre:    {profile.favorite_genre}")
    print(f"  Mood:     {profile.favorite_mood}")
    print(f"  Energy:   {profile.target_energy:.2f}")
    print(f"  Acoustic: {profile.likes_acoustic}")
    valence_display = f"{profile.target_valence:.2f}" if profile.target_valence is not None else "not specified"
    print(f"  Valence:  {valence_display}")

    user_prefs = {
        "favorite_genre": profile.favorite_genre,
        "favorite_mood": profile.favorite_mood,
        "target_energy": profile.target_energy,
        "likes_acoustic": profile.likes_acoustic,
        "target_valence": profile.target_valence,
    }
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        song, score, explanation = rec
        print(f"{song['title']} by {song['artist']} — Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()

    # Generate a natural narrative explanation
    print("Generating personalized explanation...")
    narrative = await explanation_agent(profile, recommendations, user_input)
    print("\n" + "=" * 60)
    print("Why These Songs?")
    print("=" * 60)
    print(narrative)
    print("=" * 60)


if __name__ == "__main__":
    if "--classic" in sys.argv:
        main()
    else:
        try:
            asyncio.run(agentic_main())
        except Exception as e:
            error_str = str(e).lower()
            if "api_key" in error_str or "auth" in error_str or "invalid" in error_str:
                print("\nError: GOOGLE_API_KEY is not set.")
                print("Get a free API key at: https://makersuite.google.com/app/apikey")
                print("Then export it before running:")
                print("  export GOOGLE_API_KEY='your-key-here'")
            else:
                raise