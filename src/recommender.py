from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_valence: Optional[float] = None

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        user_prefs = {
            'favorite_genre': user.favorite_genre,
            'favorite_mood': user.favorite_mood,
            'target_energy': user.target_energy,
            'likes_acoustic': user.likes_acoustic,
            'target_valence': user.target_valence,
        }
        scored = [(song, score_song(user_prefs, self._song_to_dict(song))[0]) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        user_prefs = {
            'favorite_genre': user.favorite_genre,
            'favorite_mood': user.favorite_mood,
            'target_energy': user.target_energy,
            'likes_acoustic': user.likes_acoustic,
            'target_valence': user.target_valence,
        }
        _, reasons = score_song(user_prefs, self._song_to_dict(song))
        if reasons:
            return ' | '.join(reasons)
        return f"'{song.title}' by {song.artist} may match your taste."

    @staticmethod
    def _song_to_dict(song: Song) -> Dict:
        """Helper method to convert Song dataclass to dictionary."""
        return {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'genre': song.genre,
            'mood': song.mood,
            'energy': song.energy,
            'tempo_bpm': song.tempo_bpm,
            'valence': song.valence,
            'danceability': song.danceability,
            'acousticness': song.acousticness
        }

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    print(f"Loading songs from {csv_path}...")

    try:
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                song = {
                    'id': int(row['id']),
                    'title': row['title'],
                    'artist': row['artist'],
                    'genre': row['genre'],
                    'mood': row['mood'],
                    'energy': float(row['energy']),
                    'tempo_bpm': float(row['tempo_bpm']),
                    'valence': float(row['valence']),
                    'danceability': float(row['danceability']),
                    'acousticness': float(row['acousticness'])
                }
                songs.append(song)
    except FileNotFoundError:
        print(f"Error: File {csv_path} not found.")
        return []
    except ValueError as e:
        print(f"Error: Could not convert value to numeric type: {e}")
        return []

    print(f"Successfully loaded {len(songs)} songs.")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Gracefully handles missing preference parameters by skipping those scores.
    Required by recommend_songs() and src/main.py
    """
    score = 0
    reasons = []

    # Genre scoring (only if favorite_genre is specified)
    favorite_genre = user_prefs.get("favorite_genre")
    if favorite_genre and favorite_genre == song["genre"]:
        score += 30
        reasons.append(f"matches your {favorite_genre} preference")

    # Mood scoring (only if favorite_mood is specified)
    favorite_mood = user_prefs.get("favorite_mood")
    if favorite_mood and favorite_mood == song["mood"]:
        score += 25
        reasons.append(f"has the {favorite_mood} you like")

    # Energy scoring (only if target_energy is specified)
    target_energy = user_prefs.get("target_energy")
    if target_energy is not None:
        energy_diff = abs(target_energy - song["energy"])
        energy_score = 20 * (1 - energy_diff)
        score += energy_score
        reasons.append(f"energy level {song['energy']:.1f}" +
                       (" matches" if energy_diff < 0.1 else " complements"))

    # Acousticness scoring (only if likes_acoustic is specified)
    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic and song["acousticness"] > 0.7:
        score += 15
        reasons.append("has the acoustic sound you enjoy")

    # Valence scoring (only if target_valence is specified)
    target_valence = user_prefs.get("target_valence")
    if target_valence is not None:
        valence_diff = abs(target_valence - song["valence"])
        valence_score = 10 * (1 - valence_diff)
        score += valence_score
        reasons.append(f"valence level {song['valence']:.1f}" +
                       (" matches" if valence_diff < 0.1 else " complements"))

    return [score, reasons]

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Returns k recommendations: 80% from top-ranked + 20% from 40-60th percentile (discovery).
    Expected return format: (song_dict, score, explanation_string)
    """
    import random

    # Score all songs and create (song, score, reasons) tuples
    scored_songs = [(song, *score_song(user_prefs, song)) for song in songs]

    # Sort by score descending (best matches first)
    scored_songs.sort(key=lambda x: x[1], reverse=True)

    # Calculate split: 80% top-ranked, 20% from 40-60th percentile
    top_count = max(1, int(k * 0.8))
    discovery_count = k - top_count

    # Select top 80% of recommendations
    top_recommendations = scored_songs[:top_count]

    # Calculate 40-60th percentile range for "decent but different" discovery songs
    n = len(scored_songs)
    p40_idx = int(0.4 * n)  # 40th percentile index
    p60_idx = int(0.6 * n)  # 60th percentile index
    middle_range = scored_songs[p40_idx:p60_idx]

    # Randomly sample from middle range to add variety
    discovery_recommendations = (random.sample(middle_range, min(discovery_count, len(middle_range))) if middle_range else [])

    # Combine: top-ranked first, then discovery picks
    results = top_recommendations + discovery_recommendations

    # Format as (song_dict, score, explanation_string)
    return [(song, score, ' | '.join(reasons)) for song, score, reasons in results[:k]]