# 🎵 Agentic Music Recommender

## Project Summary

Music Recommender Simulation 

The original music recommender system took in static user profile as an input. Based on the user profile, the recommender ranked all the songs in the catalog based on user's favorite_genre, favorite_mood, target_energy, likes_acoustic, and target_valence. The k recommendations for the user is split as 80% top ranked songs based on user preference and 20% 40th - 60th quartile songs in the ranking to add discovery for the user. The result is top k recommended songs with the reason those songs are chosen.

## Agentic Music Recommender

In our extension of the project all the functionalities remain the same, however, we have added agentic capability which takes in user's input in natural language and agents translate the user input into five user attributes defined above. In addition, an agentic explainer summarizes and provides reasoning for why the songs were chosen.

## Architecture Overview

The system can run in both classic mode or new agentic mode. In classic mode, static user profile is defined while in the agentic mode, user is asked for what kind of music they would like to listen to. The input text is processed and Gemini converts the text into the user attributes avorite_genre, favorite_mood, target_energy, likes_acoustic, and target_valence. The songs are loaded and a dictionary is created for the songs to be stored. The scoring method scores each song in the catalog based on user input and the songs are sorted and ranked in descending order. The top 80% of the songs are high rated songs and the rest 20% are randomly chosen from 40th to 60th quartile of the ranked songs. Finally, the recommendations are displayed for the user with an added natural narative explanation through explainer agent. Testing and evaluation are incorporated to validate the functionality of the method through unit testing, integration testing, orchestration testing and agentic testing.

## Setup

### Install dependencies

pip install -r requirements.txt

### Run Without API Key (Classic Mode)

The system works perfectly in classic mode without any API configuration:

```bash
python src/main.py --classic
```

### Setup with Google Gemini API (Optional)

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

## Sample Interactions

### Late Night Study

Top Recommendation: 'Midnight Coding' by LoRoom
Score: 99.20
Why: matches your lofi preference | has the chill you like | energy 0.4 matches | has the acoustic sound you enjoy

AI Explanation: These recommendations perfectly match your late-night 
study vibe with relaxing lofi beats and acoustic warmth. Each track 
balances gentle melodies with energizing yet calm instrumentation 
to keep you focused without distracting from your work.

### Gym Workout

Top Recommendation: 'Gym Hero' by Max Pulse
Score: 84.10
Why: matches your pop preference | has the intense you like | energy 0.9 matches | valence 0.8 matches

AI Explanation: These high-energy pop tracks are perfect for pushing 
through your workout. With driving beats and uplifting vibes, they'll 
keep your motivation high and rhythm on point from warm-up to cool-down.

### Relaxing Evening

Top Recommendation: 'Spacewalk Thoughts' by Orbit Bloom
Score: 74.10
Why: matches your ambient preference | energy 0.3 matches | has the acoustic sound you enjoy

AI Explanation: These recommendations create the perfect peaceful evening 
atmosphere with calming ambient textures and natural acoustic elements. 
The gentle instrumentation promotes relaxation while maintaining engaging 
musical depth.

## Design Decisions

- Five specialist agents where each agent focuses on one preference dimension.
- The original scoring algorithm is kept intact as it is proven to work.
- Utilized async to enable concurrent agent execution for speed (5 agents run in parallel).
- Explainer agent generates naural narratives explaining the recommended songs.
- Integrated fallback mechanism in each agent.

## Testing Summary

Refer to [**Test Report**](test_report.md)

## Reflection

- Multi-agent systems are powerful but costly
- Structured outputs from LLMs is fragile
- Layering agentic framework on top of working implementation is the way to go
- Parallelism is sometimes the simplest solution to latency
- Resilient systems make failure sgraceful, when API fails, the system falls back to classic mode
- Multi-agent architecture makes each agent testable in islotaion