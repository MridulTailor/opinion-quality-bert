# TakeMeter: Discourse Quality Classifier

TakeMeter is a text classifier that evaluates discourse quality in the `r/nba` community. It categorizes posts into three labels: `analysis`, `hot_take`, and `reaction`.

## 1. Community & Labels
**Community:** `r/nba`
**Why:** The NBA subreddit provides varied discourse. Discussion falls into three categories: data-driven analysis, emotional reactions, and assertions (hot takes). 

**Taxonomy:**
1. `analysis`: The post makes a structured argument backed by statistics, historical comparison, or tactical observation. Evidence is specific.
   - *Example:* "If you look at the shot charts, SGA is taking 15% fewer mid-range jumpers this month and replacing them with drives to the rim, which has bumped his true shooting percentage up to 63%."
2. `hot_take`: A bold opinion stated without supporting evidence. The post asserts rather than argues.
   - *Example:* "Embiid will never win a championship as the number one option. He’s too soft when the lights get bright."
3. `reaction`: An emotional response to an event. Little to no argument.
   - *Example:* "OH MY GOD HE JUST DUNKED ON HIM SO HARD"

## 2. Dataset & Annotation
**Data Source:** 240 text examples collected from `r/nba` using the RapidAPI reddit34 endpoint, saved into `dataset.csv`.
**Label Distribution:** 
- `analysis`: 80
- `hot_take`: 80
- `reaction`: 80

**Hard Edge Cases:**
1. *"LeBron is overrated — his playoff win rate against top-seeded opponents is below .500."*
   - **Decision:** `hot_take`. (Borderline: uses a stat but the framing is accusatory and the stat is cherry-picked).
2. *"I can't believe Darvin Ham played Prince over Rui for 30 minutes. The stats literally show the Lakers are +8 with Rui on the floor. Terrible coaching."*
   - **Decision:** `reaction`. (Borderline: Has emotion and a stat, but primarily functions as an emotional complaint).
3. *"Rudy Gobert is useless in the playoffs. Teams just go small and play him off the floor every year because he can't guard the perimeter."*
   - **Decision:** `hot_take`. (Borderline: Relies on a narrative rather than verifiable stats).

## 3. Fine-Tuning Setup
- **Base Model:** `distilbert-base-uncased`
- **Training Setup:** Fine-tuned using Google Colab on a T4 GPU. 
- **Hyperparameters:**
  - Learning Rate: *[Fill in after running notebook]*
  - Epochs: *[Fill in after running notebook]*
  - Batch Size: *[Fill in after running notebook]*

## 4. Baseline Comparison
**Baseline Model:** Groq `llama-3.3-70b-versatile` (Zero-shot)
**Prompt Used:**
```text
You are an expert moderator for the r/nba community. Classify the following post into exactly one of these labels:
1. analysis: The post makes a structured argument backed by statistics, historical comparison, or tactical observation. Evidence is specific.
2. hot_take: A bold opinion stated without supporting evidence. The post asserts rather than argues.
3. reaction: An emotional response to an event. Little to no argument.

Output ONLY the exact label name (analysis, hot_take, or reaction). Do not explain.

Post: {text}
```

## 5. Evaluation Report
*(Populate this section after running the Colab notebook)*

**Performance Metrics:**
- **Baseline Overall Accuracy:** [Fill in]
- **Fine-Tuned Overall Accuracy:** [Fill in]

**Per-Class F1 Scores (Fine-Tuned):**
- `analysis`: [Fill in]
- `hot_take`: [Fill in]
- `reaction`: [Fill in]

**Confusion Matrix:**
*(Convert the outputted confusion_matrix.png into a markdown table here)*

| True \ Predicted | analysis | hot_take | reaction |
|------------------|----------|----------|----------|
| **analysis**     |   0      |    0     |    0     |
| **hot_take**     |   0      |    0     |    0     |
| **reaction**     |   0      |    0     |    0     |

**Failure Analysis (3 wrong predictions):**
1. *Post:* "[Insert text]"
   - *True Label:* [Label]
   - *Predicted Label:* [Label]
   - *Why it failed:* [Analysis]
*(Repeat for 2 more)*

**Sample Classifications:**
| Post | Predicted Label | Confidence |
|------|-----------------|------------|
| "[Post 1 text]" | [Label] | [X%] |
| "[Post 2 text]" | [Label] | [X%] |
| "[Post 3 text]" | [Label] | [X%] |

*Why Post 1's prediction is reasonable:* [Analysis]

## 6. Reflection
**Intended vs. Learned:**
[Reflect on what the model actually learned. Did it learn to associate short posts with reactions, and long posts with analysis?]

**Spec Reflection:**
- *How the spec helped:* [Detail]
- *Where implementation diverged:* [Detail]

## 7. AI Usage
- **Data Collection Scripting:** An LLM helped write a custom Python script to fetch the dataset via the RapidAPI reddit34 endpoints.
- **Label Stress Testing:** An LLM brainstormed edge cases and refined label boundaries before starting.
