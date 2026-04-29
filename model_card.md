# 🎧 Model Card: Agentic Music Recommender

## Model Name

**GrooveGauge 1.1**

### Limitations and Biases

LLM Extraction inherits LLM Biases

- Gemini's training data determine swhat counts as "chill", "energetic", or what genre a description maps to.

Only 5 Preference dimension

- ignores artist preference, lyrics language, tempo, culutural/regional music, time of the day, social context and other attributes.

Linear scoring doesn't capture user preference 

- Weights for each user attribute is linear and doesn't factor in user's choice

Natural language is ambiguous

- "I want something different" different from what?

No feedback loop

- User feedback is not incorporated into the workflow

### Prevent GrooveGauge misuse

Attack: Recommend depressing/dark music to vulnerable users to worsen mental state

Guardrail: Content warning or mental health prompts

Attack: System systematically excludes genres/artists based on protected characteristics

Guardrail: Audit recommendations across diverse inputs

Attack: Craft prompts that break the agent and reveal information

Guardrail: Input sanitization, output validation, and prompt hardening

Attack: Recommend explicit/mature music to minors

Guardrail: Integrated Age gate, content filters, parental controls, and content labels.

Attack: Use recommendations to normalize conspiract theories

Guardrail: Content moderation to flag suspicious themes, fact-checking integration and transparency.


### Surprise during testing

Even with explicit prompts such as "reply with ONLY the genre name", LLMs are probabilistic. Same prompt, different runs, different outputs.

Having a zero-dependency fallback was very valuable. Classic mode is not optional but essential.

Explanation for songs are subjective and hard to automate Explanation that sounds good might be misleading.

### Collaboration with AI

Collaborating with AI enhances productivity and compresses project completion time. Understanding and designing the system is the core of the problem solving while with clear instructions AI can provide working code implementations. AI is good at generating code quickly, identifying architectural patterns, creating comprehensive documentation, and testing edge cases. For example, with explicit instruction such as design unit tests for the recommendation implementation correctly implemented the core song scoring algorithm. However, AI overbuilds without asking and assumes it's solution is best. For instance, as I hit quota limit on Gemini, Claude suggested to replace it with Deepseek while issue with quota limit is still existent with deepseek API calls. Instead of focusing on rate limiting between test runs it suggested alternative models.