# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

 **GrooveGauge 1.0**

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

What kind of recommendations does it generate  

- It generates top 5 recommended songs that match the most with user preference. 80% of songs are the ones that score highest across user preference, 20% songs are from the middle-tier scoring range from 40th to 60th percentile. Each song recommendation includes a reason on why it was recommended.

What assumptions does it make about the user 

- Users know their taste like favorite genre, preferred mood, target energy level, target valence level and if they like acoustic songs or not. Not all the inputs are required but the more the better. There are no information on contextual shifts, time of the day pr recent listening history basically the user activity data is non existent. Users social influence, trend awareness, artist relationships are not accounted for.

Is this for real users or classroom exploration

- This is more of a classroom exploration rather than for real users as it explores fundamentals of recommender systems, ranking, and is a good entry point before exploring collaborative filtering with larger datasets.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

What features of each song are used (genre, energy, mood, etc.)  

- Genre, mood, energy, valence and acousticness are the song features used for the recommendation.

What user preferences are considered

- Users favorite_genre, favorite_mood, target_energy, likes_acoustic, target_valence are considere for the recommendation.

How does the model turn those into a score

- The model compares the above listed user preference and song features to compare if they are a match. If genre and mood are a match, the song incrementally scored with 30 and 25 points respectively. Energy and valence score are compared based on the difference in the target and preferred levels. If the difference is less than 0.1, 20 and 10 points are added respectively for energy and valence. For acousticness, if the song has greater than 0.7 acousticness, 15 point is added to the score of the song.

What changes did you make from the starter logic  

- Added target_valence in UserProfile to make recommendation more meaningful. The recommended songs are a mix of 80% top ranked and 20% 40th to 60th percentile.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

How many songs are in the catalog  

- There are 20 songs in the catalog.

What genres or moods are represented  

- There are 17 genres namely pop, lofi, rock, ambient, synthwave, jazz, indie pop, classical, electronic, hip-hop, country, reggae, metal, folk, r&b, disco, blues and 12 moods namely happy, chill, intense, relaxed, moody, focused, melancholic, energetic, confident, nostalgic, peaceful, aggressive, reflective, smooth, fun represented in the song catalog.

Did you add or remove data  

- Added 10 songs to the existing 10 in the catalog.

Are there parts of musical taste missing in the dataset  

- There are majority lofi and pop songs in the catalog. True spectrum of how people listen to music is missing with genre gaps disregarding geographical context. Romantic, uplifting, triumphant, empowering, nostalgic songs are missing among many.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

User types for which it gives reasonable results  

- Mainstream genre listeners like pop and lofi benefit the most. Acoustic preference is outlined clearly as yes or no.

Any patterns you think your scoring captures correctly  

- Genre is the strongest decision factor while energy is linearly scalable.  Mood reinforces genre and acoustic preference is binary but effective. Valence follows emotional intent and 90/20 split blend prevents stagnation.

Cases where the recommendations matched your intuition 

- User Profile(Lofi, chill, energy 0.4) matches with Midnight Coding(99.2) and Library Rain (99.0).
User Profile(Pop, happy, energy 0.8) matches with Sunrise City (74.6) and Gym Hero (47.4).

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

- The dataset is 35% very high energy songs creating high-energy bias. 
- There are unique genres. Among 20 songs there are 14 unique genres. Users whose genre doesn't match get permanent -55 pts penalty.
- Users outside mainstream genres permanently capped at 45 pts creating genre + mpdd weights dominance.

Prompts:  

Features it does not consider  

- tempo_bpm and danceability could help context-specific recommendations.

Genres or moods that are underrepresented  

- 11/15 moods appear only once and 15/17 genres appeard only once.

Cases where the system overfits to one preference

- When genre and mood match, that will be enough to lock it in top song regardless of how much other features contribute.

Ways the scoring might unintentionally favor some users  

- Users with pop + happy preference have 2.8x advantage to blues user.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

Which user profiles you tested  

- User with pop+happy preference have most chances of getting good recommendation based on data distribution

user_prefs = {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.8}

User with electronic genre preference but wants acoustic, electronic genre has least acoustic

user_prefs = {"favorite_genre": "electronic", "favorite_mood": "energetic", "target_energy": 0.85, "likes_acoustic": True, "target_valence": 0.80}

User with classical genre preference but wants high enerrgy song which is unlikely

user_prefs = {"favorite_genre": "classical", "favorite_mood": "melancholic", "target_energy": 0.95, "target_valence": 0.30}

User wants metal song but peaceful mood, that can't happen

user_prefs = {"favorite_genre": "metal", "favorite_mood": "peaceful", "target_energy": 0.95, "target_valence": 0.30, "likes_acoustic": False}

What you looked for in the recommendations

- Looked for how each of the edge cases recommends songs.

What surprised you

- User searching for classical and high energy song got recommended metal song Thunder Strike as it has high energy match even though genre and mood don't match.

Any simple tests or comparisons you ran  

- User looking for electronic genre usually have high energy and low acoustic preference.
While users looking classical song recommendations have low energy and high acoustic preference.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

Additional features or preferences

- Adding context such as time of the day, activity context, artist diversity, lyrical preference, production style, instrumentals, tempo preference, decade/era preference can enhance the recommendation.

Better ways to explain recommendations

- Providing reason heirarchy, contadiction between preference and recommendation, comparative language in explanation, and showing what preference matched strongly and what didn't can provide users with transparency on recommendation.

Improving diversity among the top results

- Our 80/20 split does take into consideration the diversity in recommendation however it could be improved by taking into consideration the user preferences such as mood micing, genre diversification and energy variance rather than just finding songs from the scored range.

Handling more complex user tastes

- Currently GrooveGauge only assumes static simple preferences, but it could take into consideration preference profiles such as gym mode, study mode,, and evaluate mood by tracking how users bounce between moods. The profile could have hybrid preference like 60% lofi and 40% indie pop. Temporal preference like monday energetic and friday relaxed can be tracked. Discovery tolerance could also be users preference.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

What you learned about recommender systems

- Recommender systems utilizes user and song metadata to make recommendations for a coldstart problem but collaborative filtering is a better way given we have user history dataset which incorporates complex relationship in data. 

Something unexpected or interesting you discovered

- 80/20 split is unfair to niche users as they are penalized by data scarcity masquerading as discovery.

How this changed the way you think about music recommendation apps

- Recommendation apps utilize complex scoring and recommendation engine to suggest users. It is not very straight forward and that's why some apps do it right and some miss the spot.
