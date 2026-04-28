"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import os
from recommender import load_songs, recommend_songs


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


if __name__ == "__main__":
    main()
