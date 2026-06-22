# TakeMeter: Discourse Quality Classifier

TakeMeter is a text classifier that evaluates discourse quality in the `r/nba` community. It categorizes posts into three labels: `analysis`, `hot_take`, and `reaction`.

## 1. Community & Labels
**Community:** `r/nba`
**Why:** The NBA subreddit provides varied discourse. Discussion falls into three categories: data-driven analysis, emotional reactions, and assertions (hot takes). 

**Taxonomy:**
1. `analysis`: The post makes a structured argument backed by statistics, historical comparison, or tactical observation. Evidence is specific.
   - *Example 1:* "If you look at the 2014 Spurs, their ball movement was predicated on secondary actions. This current Celtics team is trying to emulate that but they stall out because Tatum holds the ball for 3 seconds before initiating."
   - *Example 2:* "The Lakers' defensive rating drops by 8.4 points per 100 possessions when Davis sits. They are giving up too many corner threes because Rui keeps over-helping on the strong side drive."
2. `hot_take`: A bold opinion stated without supporting evidence. The post asserts rather than argues.
   - *Example 1:* "Embiid will never win a championship as the number one option. He’s too soft when the lights get bright."
   - *Example 2:* "Ant is already better than prime D-Wade. It's not even close anymore."
3. `reaction`: An emotional response to an event. Little to no argument.
   - *Example 1:* "OH MY GOD HE JUST DUNKED ON HIM SO HARD"
   - *Example 2:* "I am so sick of this team. Trade everyone."

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
  - Learning Rate: 2e-5
  - Epochs: 3 (chosen to prevent overfitting on the small dataset of 240 examples)
  - Batch Size: 16

## 4. Baseline Comparison
**Baseline Model:** Groq `llama-3.3-70b-versatile` (Zero-shot)
**Prompt Used:**
```text
You are classifying posts from r/nba.
Assign each post to exactly one of the following categories.

analysis: The post makes a structured argument backed by statistics, historical comparison, or tactical observation. Evidence is specific.
Example: "If you look at the 2014 Spurs, their ball movement was predicated on secondary actions. This current Celtics team is trying to emulate that but they stall out because Tatum holds the ball for 3 seconds before initiating."

hot_take: A bold opinion stated without supporting evidence. The post asserts rather than argues.
Example: "Embiid will never win a championship as the number one option. He’s too soft when the lights get bright."

reaction: An emotional response to an event. Little to no argument.
Example: "OH MY GOD HE JUST DUNKED ON HIM SO HARD"

Respond with ONLY the label name.
Do not explain your reasoning.

Valid labels:
analysis
hot_take
reaction
```

## 5. Evaluation Report

**Performance Metrics:**
- **Baseline Overall Accuracy:** 0.472
- **Fine-Tuned Overall Accuracy:** 0.528

**Per-Class F1 Scores (Fine-Tuned):**
- `analysis`: 0.62
- `hot_take`: 0.25
- `reaction`: 0.59

**Confusion Matrix:**
| True \ Predicted | analysis | hot_take | reaction |
|------------------|----------|----------|----------|
| **analysis**     |   12     |    0     |    0     |
| **hot_take**     |   10     |    2     |    0     |
| **reaction**     |    5     |    2     |    5     |

**Failure Analysis (3 wrong predictions):**
1. *Post:* "If Knicks lost 2n, the hart layup and missed box out would be huge talking points."
   - *True Label:* reaction
   - *Predicted Label:* analysis
   - *Why it failed:* The post discusses game events ("hart layup", "missed box out"). The model associated this with `analysis`, even though the post lacks structure or statistics.
2. *Post:* "Man they came out of the timeout looking around like they didn’t know who they were guarding. I’m speechless"
   - *True Label:* hot_take
   - *Predicted Label:* analysis
   - *Why it failed:* The mention of "timeout" and "guarding" triggered `analysis` patterns in the model, but it is an unsupported claim.
3. *Post:* "He cant, the guy weighs like 80 lbs."
   - *True Label:* reaction
   - *Predicted Label:* analysis
   - *Why it failed:* The inclusion of a number ("80 lbs") tricked the model into predicting statistical analysis, despite it being a reaction.

**Sample Classifications:**
| Post | Predicted Label | Confidence |
|------|-----------------|------------|
| "Might be one of the most egregiously dirty plays I have seen. Fox should get a 2 game ban." | analysis | 0.37 |
| "Fuck Trump! During the national anthem was perfect timing." | hot_take | 0.35 |
| "Captain Bone SPURS. The Knicks got cursed by this pedophile tonight" | analysis | 0.37 |

*Why Post 1's prediction failed:* It failed because the model overpredicted `analysis` for text longer than a few words.

## 6. Reflection
**Intended vs. Learned:**
The model did not learn the class boundaries. It biased towards predicting `analysis` (27 out of 36 examples). It associated any mention of players, plays, or numbers with `analysis`. It failed to learn the requirement of structured reasoning. The dataset is too small.

**Spec Reflection:**
- *How the spec helped:* Defining the edge cases explicitly in `planning.md` made it clear during evaluation that the model was failing on the anticipated boundaries (e.g. numbers without reasoning).
- *Where implementation diverged:* The fine-tuned model was expected to beat the zero-shot LLM. Due to the small dataset size (240 examples), it only slightly improved accuracy and failed on the `hot_take` class.

## 7. AI Usage
- **Data Collection Scripting:** An LLM helped write a custom Python script to fetch the dataset via the RapidAPI reddit34 endpoints.
- **Label Stress Testing:** An LLM brainstormed edge cases and refined label boundaries before starting.
