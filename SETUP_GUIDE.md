# Setup & Quick Start Guide

## What's Included

### Working Components

1. **Scoring Logic** ✅
   - Genre, mood, energy, acoustic, and valence scoring
   - 80% preference match + 20% discovery sampling
   - All test cases passing

2. **Song Loading & Catalog** ✅
   - CSV data loading from `data/songs.csv`
   - 20+ songs with full metadata
   - Tested and working

3. **Recommender Class** ✅
   - OOP wrapper around scoring logic
   - Recommendation generation
   - Per-song explanation generation

4. **Agentic Framework** (requires API key)
   - 5 parallel specialist agents (genre, mood, energy, acoustic, valence)
   - Natural language preference extraction
   - Recommendation explanation generation

---

## Quick Start

### Install dependencies

pip install -r requirements.txt

### 1️⃣ Run Without API Key (Classic Mode)

The system works perfectly in classic mode without any API configuration:

```bash
python src/main.py --classic
```

**Output:**
```
Loading songs from data/songs.csv...
Successfully loaded 20 songs.

Top recommendations:

Thunder Strike - Score: 59.50
Because: matches your metal preference | energy level 0.9 matches | valence level 0.3 matches

Island Vibes - Score: 43.70
Because: has the peaceful you like | energy level 0.6 complements | valence level 0.8 complements

...
```

### 2️⃣ Run Tests (No API Key Required)

```bash
# Run all tests that don't require API key (10 tests)
pytest tests/ -m "not requires_api_key" -v

# Run specific test class
pytest tests/test_agents.py::TestScoringLogic -v

# Run with coverage
pytest tests/ -m "not requires_api_key" -v --cov=src
```

---

## Setup with Google Gemini API (Optional)

To enable natural language preference extraction:

### Step 1: Get Free API Key

1. Visit https://makersuite.google.com/app/apikey
2. Click **"Create API key"**
3. Copy your API key

### Step 2: Set Environment Variable

```bash
# One-time for current session
export GOOGLE_API_KEY='paste-your-key-here'

# OR add to ~/.zshrc for permanent setup
echo "export GOOGLE_API_KEY='paste-your-key-here'" >> ~/.zshrc
source ~/.zshrc
```

### Step 3: Run Agentic Mode

```bash
python src/main.py
```

You'll be prompted to describe the music you want, and the system will:
1. Extract preferences using 5 parallel agents
2. Score songs against your preferences
3. Generate personalized recommendations with explanations

**Example Input:**
```
> I want chill lofi hip-hop for late night studying
```

**Example Output:**
```
Extracted preferences:
  Genre:    lofi
  Mood:     chill
  Energy:   0.35
  Acoustic: True
  Valence:  0.55

Top recommendations:

Midnight Coding - Score: 87.50
Because: matches your lofi preference | has the chill you like | energy level 0.42 complements

Library Rain - Score: 83.20
Because: matches your lofi preference | has the chill you like | energy level 0.35 matches

...

Why These Songs?
These recommendations align perfectly with your desire for late-night study music. 
The lofi tracks feature that relaxed, acoustic quality with moderate energy...
```

---

## Test Suite Overview

### ✅ Unit Tests (10 tests - No API Required)

**Scoring Logic (5 tests):**
- Genre match scoring
- Mood match scoring
- Energy proximity scoring
- Acoustic preference scoring
- Multiple preference combination scoring

**Recommendation Logic (2 tests):**
- Returns proper recommendation structure
- Implements 80/20 preference/discovery split

**Module Integration (3 tests):**
- Real CSV loading
- Recommender class functionality
- Per-song explanations

### 🔐 Integration Tests (9 tests - Requires API Key)

**Individual Agents (5 tests):**
- Genre agent validation
- Mood agent validation
- Energy agent range validation
- Acoustic agent boolean validation
- Valence agent range validation

**Orchestrator (2 tests):**
- Profile structure validation
- Parallel execution performance

**End-to-End (2 tests):**
- Full pipeline integration
- Real CSV + agents + recommendations

### Run Specific Test Groups

```bash
# Unit tests only (no API key)
pytest tests/ -m unit -v

# Integration tests only (no API key)
pytest tests/ -m integration -v

# Agentic tests (requires API key)
pytest tests/ -m agentic -v

# Everything except API-dependent tests
pytest tests/ -m "not requires_api_key" -v
```

---

## Architecture Overview

```
Natural Language Input (Agentic Mode) OR
Hardcoded Preferences (Classic Mode)
    ↓
[5 Parallel Gemini Agents] (optional, requires API key)
    ↓
Extracted UserProfile
    ↓
load_songs() → CSV catalog
    ↓
score_song() × N
    ↓
Sort + Split (80% preference / 20% discovery)
    ↓
Top 5 Recommendations
    ↓
explanation_agent() (optional, requires API key)
    ↓
Final Output with Scores & Explanations
```

---

## Directory Structure

```
agentic-music-recommender/
├── src/
│   ├── main.py                  # Entry point with 2 modes
│   ├── agents.py                # 5 specialist agents + orchestrator
│   ├── recommender.py           # Scoring, loading, recommendation logic
│   └── __init__.py
├── tests/
│   ├── test_agents.py           # 19 comprehensive tests
│   ├── test_recommender.py      # Module 3 logic tests
│   └── __init__.py
├── data/
│   └── songs.csv                # 20+ songs with metadata
├── assets/
    ├── AGENTIC_FLOW.md          # Architecture diagram
    ├── agenticRecommender.png
    ├── recommendationLogicFlow.png
├── requirements.txt             # google-generativeai, pandas, pytest, pytest-asyncio, streamlit
├── README.md
├── SETUP_GUIDE.md               # Quick start guide
├── model_card.md                # Reflections
├── IMPLEMENTATION_SUMMARY.md    # Implementation summary   
└── pytest.ini                   # Test configuration 
```

---

## Troubleshooting

### ❌ "ModuleNotFoundError: No module named 'recommender'"

**Solution:** The tests add `src/` to Python path automatically. If running scripts directly, run from project root:
```bash
cd /path/to/agentic-music-recommender
python src/main.py
```

### ❌ "Error: GOOGLE_API_KEY is not set"

**Solution:** Only needed for agentic mode. Use classic mode instead:
```bash
python src/main.py --classic
```

Or set the API key:
```bash
export GOOGLE_API_KEY='your-key-here'
python src/main.py
```

### ❌ "FutureWarning: google.generativeai package has ended"

**Info:** This is just a deprecation warning. The package still works. Future versions may need migration to `google.genai`.

### ❌ Tests failing with "No API_KEY or ADC found"

**Solution:** This is expected for API-dependent tests. Run without them:
```bash
pytest tests/ -m "not requires_api_key" -v
```

---

## Common Commands

```bash
# Classic mode (no API key needed)
python src/main.py --classic

# Agentic mode (requires GOOGLE_API_KEY)
python src/main.py

# Run all unit tests
pytest tests/ -m unit -v

# Run all tests (skip API-dependent ones if no key)
pytest tests/ -m "not requires_api_key" -v

# Run with test output
pytest tests/ -m "not requires_api_key" -v -s

# Run specific test
pytest tests/test_agents.py::TestScoringLogic::test_score_song_genre_match -v

# Manual evaluation (requires API key)
python -c "import asyncio; from tests.test_agents import manual_evaluation_test; asyncio.run(manual_evaluation_test())"
```
