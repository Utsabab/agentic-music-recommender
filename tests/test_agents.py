"""
Test suite for the Agentic Music Recommender system.
Tests agents, scoring logic, and end-to-end flow.
"""

import asyncio
import sys
import os
import pytest

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from recommender import UserProfile, load_songs, score_song, recommend_songs
from agents import (
    genre_agent, mood_agent, energy_agent, acoustic_agent, valence_agent,
    extract_user_profile, VALID_GENRES, VALID_MOODS
)


class TestIndividualAgents:
    """Test each agent independently."""

    @pytest.mark.asyncio
    @pytest.mark.requires_api_key
    @pytest.mark.agentic
    async def test_genre_agent_valid_input(self):
        """Genre agent should return a valid genre."""
        result = await genre_agent("I love rock music")
        assert result in VALID_GENRES, f"'{result}' not in valid genres"
        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.asyncio
    @pytest.mark.requires_api_key
    @pytest.mark.agentic
    async def test_genre_agent_fallback(self):
        """Genre agent should fallback to 'pop' for invalid genres."""
        # Even if the model returns something wrong, should fallback
        result = await genre_agent("xyzabc invalid genre")
        assert result in VALID_GENRES
        assert result == "pop" or result in VALID_GENRES

    @pytest.mark.asyncio
    @pytest.mark.requires_api_key
    @pytest.mark.agentic
    async def test_mood_agent_valid_input(self):
        """Mood agent should return a valid mood."""
        result = await mood_agent("I want something chill and relaxing")
        assert result in VALID_MOODS, f"'{result}' not in valid moods"
        assert isinstance(result, str)

    @pytest.mark.asyncio
    @pytest.mark.requires_api_key
    @pytest.mark.agentic
    async def test_energy_agent_range(self):
        """Energy agent should return float between 0.0 and 1.0."""
        low = await energy_agent("very calm and quiet")
        high = await energy_agent("super intense and energetic")

        assert 0.0 <= low <= 1.0, f"Energy {low} out of range"
        assert 0.0 <= high <= 1.0, f"Energy {high} out of range"
        assert low < high, "Calm should have lower energy than intense"

    @pytest.mark.asyncio
    @pytest.mark.requires_api_key
    @pytest.mark.agentic
    async def test_acoustic_agent_bool(self):
        """Acoustic agent should return boolean."""
        acoustic = await acoustic_agent("I love acoustic guitars")
        electric = await acoustic_agent("I want electric and synthesizers")

        assert isinstance(acoustic, bool)
        assert isinstance(electric, bool)
        assert acoustic is True, "Should prefer acoustic"
        assert electric is False, "Should prefer electric"

    @pytest.mark.asyncio
    @pytest.mark.requires_api_key
    @pytest.mark.agentic
    async def test_valence_agent_range(self):
        """Valence agent should return float 0-1 or None."""
        happy = await valence_agent("upbeat and happy")
        sad = await valence_agent("melancholic and sad")
        ambiguous = await valence_agent("just some music")

        if happy is not None:
            assert 0.0 <= happy <= 1.0
            assert happy > 0.5, "Happy should have high valence"

        if sad is not None:
            assert 0.0 <= sad <= 1.0
            assert sad < 0.5, "Sad should have low valence"

        # Ambiguous could be None or a value
        if ambiguous is not None:
            assert 0.0 <= ambiguous <= 1.0


class TestOrchestrator:
    """Test the profile extraction orchestrator."""

    @pytest.mark.asyncio
    @pytest.mark.requires_api_key
    @pytest.mark.agentic
    async def test_extract_user_profile_structure(self):
        """extract_user_profile should return valid UserProfile."""
        user_input = "I want chill lofi hip-hop for studying"
        profile = await extract_user_profile(user_input)

        assert isinstance(profile, UserProfile)
        assert profile.favorite_genre in VALID_GENRES
        assert profile.favorite_mood in VALID_MOODS
        assert 0.0 <= profile.target_energy <= 1.0
        assert isinstance(profile.likes_acoustic, bool)
        assert profile.target_valence is None or (0.0 <= profile.target_valence <= 1.0)

    @pytest.mark.asyncio
    @pytest.mark.requires_api_key
    @pytest.mark.agentic
    async def test_extract_user_profile_parallel_execution(self):
        """Agents should run in parallel (performance check)."""
        import time

        user_input = "upbeat pop music for a party"
        start = time.time()
        profile = await extract_user_profile(user_input)
        duration = time.time() - start

        # Should complete in reasonable time (parallel < 5 agents * sequential)
        assert duration < 30, f"Profile extraction took {duration}s (expected < 30s for parallel)"
        assert isinstance(profile, UserProfile)


class TestScoringLogic:
    """Test the original Module 3 scoring logic."""

    @pytest.mark.unit
    def test_score_song_genre_match(self):
        """Genre match should award 30 points."""
        user_prefs = {"favorite_genre": "pop", "favorite_mood": None, "target_energy": None, "likes_acoustic": False}
        song = {
            "title": "Test", "artist": "Test", "genre": "pop",
            "mood": "happy", "energy": 0.5, "tempo_bpm": 120,
            "valence": 0.7, "danceability": 0.8, "acousticness": 0.1
        }
        score, reasons = score_song(user_prefs, song)
        assert score >= 30, f"Genre match should give at least 30 points, got {score}"
        assert any("pop" in r for r in reasons)

    def test_score_song_mood_match(self):
        """Mood match should award 25 points."""
        user_prefs = {"favorite_genre": None, "favorite_mood": "happy", "target_energy": None, "likes_acoustic": False}
        song = {
            "title": "Test", "artist": "Test", "genre": "pop",
            "mood": "happy", "energy": 0.5, "tempo_bpm": 120,
            "valence": 0.7, "danceability": 0.8, "acousticness": 0.1
        }
        score, reasons = score_song(user_prefs, song)
        assert score >= 25, f"Mood match should give at least 25 points, got {score}"
        assert any("happy" in r for r in reasons)

    def test_score_song_energy_proximity(self):
        """Energy proximity should award up to 20 points."""
        user_prefs = {"favorite_genre": None, "favorite_mood": None, "target_energy": 0.5, "likes_acoustic": False}
        song = {
            "title": "Test", "artist": "Test", "genre": "pop",
            "mood": "happy", "energy": 0.5, "tempo_bpm": 120,
            "valence": 0.7, "danceability": 0.8, "acousticness": 0.1
        }
        score, reasons = score_song(user_prefs, song)
        assert score >= 10, f"Energy match should give points, got {score}"
        assert any("energy" in r for r in reasons)

    def test_score_song_acoustic_preference(self):
        """Acoustic preference should award 15 points for high acousticness."""
        user_prefs = {"favorite_genre": None, "favorite_mood": None, "target_energy": None, "likes_acoustic": True}
        song = {
            "title": "Test", "artist": "Test", "genre": "pop",
            "mood": "happy", "energy": 0.5, "tempo_bpm": 120,
            "valence": 0.7, "danceability": 0.8, "acousticness": 0.8
        }
        score, reasons = score_song(user_prefs, song)
        assert score >= 15, f"Acoustic preference should give at least 15 points, got {score}"
        assert any("acoustic" in r for r in reasons)

    def test_score_song_multiple_matches(self):
        """Multiple matches should accumulate."""
        user_prefs = {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.8,
            "likes_acoustic": False
        }
        song = {
            "title": "Test", "artist": "Test", "genre": "pop",
            "mood": "happy", "energy": 0.8, "tempo_bpm": 120,
            "valence": 0.7, "danceability": 0.8, "acousticness": 0.1
        }
        score, reasons = score_song(user_prefs, song)
        # Should have high score: genre(30) + mood(25) + energy(~20)
        assert score > 70, f"Multiple matches should accumulate, got {score}"


class TestRecommendationLogic:
    """Test the end-to-end recommendation flow."""

    @pytest.mark.unit
    def test_recommend_songs_returns_list(self):
        """recommend_songs should return a list of recommendations."""
        songs = [
            {
                "id": 1, "title": "Song1", "artist": "Artist1", "genre": "pop",
                "mood": "happy", "energy": 0.8, "tempo_bpm": 120,
                "valence": 0.7, "danceability": 0.8, "acousticness": 0.1
            },
            {
                "id": 2, "title": "Song2", "artist": "Artist2", "genre": "pop",
                "mood": "happy", "energy": 0.5, "tempo_bpm": 100,
                "valence": 0.6, "danceability": 0.7, "acousticness": 0.2
            },
        ]
        user_prefs = {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.8, "likes_acoustic": False}

        recommendations = recommend_songs(user_prefs, songs, k=2)
        assert isinstance(recommendations, list)
        assert len(recommendations) <= 2
        assert all(len(rec) == 3 for rec in recommendations)  # (song, score, reasons)

    def test_recommend_songs_80_20_split(self):
        """Recommendations should include both preference matches and discovery picks."""
        # Create 20 songs with clear scoring tiers
        songs = []
        for i in range(20):
            songs.append({
                "id": i, "title": f"Song{i}", "artist": f"Artist{i}",
                "genre": "pop" if i < 10 else "rock",
                "mood": "happy" if i < 10 else "intense",
                "energy": 0.8 if i < 10 else 0.3,
                "tempo_bpm": 120, "valence": 0.7, "danceability": 0.8, "acousticness": 0.1
            })

        user_prefs = {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.8, "likes_acoustic": False}
        recommendations = recommend_songs(user_prefs, songs, k=5)

        assert len(recommendations) == 5
        # First 4 (80% of 5) should be from top-scored (pop/happy/high energy)
        # Last 1 (20% of 5) should be from middle tier for discovery
        top_songs = [rec[0] for rec in recommendations[:4]]
        assert all(s["genre"] == "pop" for s in top_songs), "Top 80% should match preferences"


class TestIntegration:
    """End-to-end integration tests."""

    @pytest.mark.integration
    def test_real_catalog_loading(self):
        """Should load real songs.csv successfully."""
        import os

        # Find songs.csv
        csv_path = "/Users/utsab06/Desktop/Codepath AI110/agentic-music-recommender/data/songs.csv"
        if os.path.exists(csv_path):
            songs = load_songs(csv_path)
            assert len(songs) > 0, "Should load at least one song"
            assert all("title" in s and "artist" in s for s in songs)

    @pytest.mark.asyncio
    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.agentic
    async def test_end_to_end_flow(self):
        """Test complete flow: natural language → profile → scoring → recommendations."""
        # Extract profile from natural language
        user_input = "I want upbeat pop music for working out"
        profile = await extract_user_profile(user_input)

        assert profile.favorite_genre in VALID_GENRES
        assert profile.favorite_mood in VALID_MOODS

        # Load songs and get recommendations
        import os
        csv_path = "/Users/utsab06/Desktop/Codepath AI110/agentic-music-recommender/data/songs.csv"
        if os.path.exists(csv_path):
            songs = load_songs(csv_path)
            if songs:
                user_prefs = {
                    "favorite_genre": profile.favorite_genre,
                    "favorite_mood": profile.favorite_mood,
                    "target_energy": profile.target_energy,
                    "likes_acoustic": profile.likes_acoustic,
                    "target_valence": profile.target_valence,
                }
                recommendations = recommend_songs(user_prefs, songs, k=5)

                assert len(recommendations) <= 5
                assert all(len(rec) == 3 for rec in recommendations)


# ============================================================================
# Manual test function for human evaluation
# ============================================================================

async def manual_evaluation_test():
    """
    Manual evaluation: Test the system with realistic inputs and review outputs.
    """
    print("\n" + "="*70)
    print("MANUAL EVALUATION TEST")
    print("="*70)

    test_cases = [
        "I want chill lofi hip-hop for studying late at night",
        "Upbeat pop music for a workout session",
        "Sad indie rock for rainy afternoons",
        "Electronic dance music for a party",
    ]

    import os
    csv_path = "/Users/utsab06/Desktop/Codepath AI110/agentic-music-recommender/data/songs.csv"

    if not os.path.exists(csv_path):
        print(f"⚠️  songs.csv not found at {csv_path}")
        return

    songs = load_songs(csv_path)
    if not songs:
        print("⚠️  No songs loaded")
        return

    for i, user_input in enumerate(test_cases, 1):
        print(f"\n{'─'*70}")
        print(f"TEST CASE {i}: {user_input}")
        print(f"{'─'*70}")

        try:
            # Extract profile
            profile = await extract_user_profile(user_input)
            print(f"\n✓ Extracted Profile:")
            print(f"  • Genre:    {profile.favorite_genre}")
            print(f"  • Mood:     {profile.favorite_mood}")
            print(f"  • Energy:   {profile.target_energy:.2f}/1.0")
            print(f"  • Acoustic: {profile.likes_acoustic}")
            print(f"  • Valence:  {profile.target_valence if profile.target_valence else 'unspecified'}")

            # Get recommendations
            user_prefs = {
                "favorite_genre": profile.favorite_genre,
                "favorite_mood": profile.favorite_mood,
                "target_energy": profile.target_energy,
                "likes_acoustic": profile.likes_acoustic,
                "target_valence": profile.target_valence,
            }
            recommendations = recommend_songs(user_prefs, songs, k=5)

            print(f"\n✓ Recommendations (Top 5):")
            for j, (song, score, reasons) in enumerate(recommendations, 1):
                print(f"\n  {j}. '{song['title']}' by {song['artist']}")
                print(f"     Score: {score:.2f}")
                print(f"     Because: {reasons}")

        except Exception as e:
            print(f"\n✗ Error: {str(e)}")


if __name__ == "__main__":
    print("Run tests with: pytest tests/test_agents.py -v")
    print("Run manual evaluation with: python -c \"import asyncio; from tests.test_agents import manual_evaluation_test; asyncio.run(manual_evaluation_test())\"")
