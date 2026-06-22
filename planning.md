# TakeMeter Planning Document

## 1. Community
**Community:** `r/nba`
**Why:** The NBA subreddit provides varied discourse. Discussion falls into three categories: data-driven analysis, emotional reactions, and assertions (hot takes). These distinctions matter to the community.

## 2. Labels
1. `analysis`: The post makes a structured argument backed by statistics, historical comparison, or tactical observation. Evidence is specific.
   - *Example 1:* "The Lakers' defensive rating drops by 8.4 points per 100 possessions when Davis sits. They are giving up too many corner threes because Rui keeps over-helping on the strong side drive."
   - *Example 2:* "If you look at the 2014 Spurs, their ball movement was predicated on secondary actions. This current Celtics team is trying to emulate that but they stall out because Tatum holds the ball for 3 seconds before initiating."
2. `hot_take`: A bold opinion stated without supporting evidence. The post asserts rather than argues.
   - *Example 1:* "Embiid will never win a championship as the number one option. He’s too soft when the lights get bright."
   - *Example 2:* "Ant is already better than prime D-Wade. It's not even close anymore."
3. `reaction`: An emotional response to an event. Little to no argument.
   - *Example 1:* "OH MY GOD HE JUST DUNKED ON HIM SO HARD"
   - *Example 2:* "I am so sick of this team. Trade everyone."

## 3. Hard Edge Cases
**Case 1:** A post that makes a bold claim and includes one piece of statistical evidence, but the evidence is cherry-picked.
*Example:* "LeBron is overrated — his playoff win rate against top-seeded opponents is below .500."
**Decision Rule:** If the post provides verifiable evidence supporting the claim, label it `analysis`. If the evidence is cherry-picked, label it `hot_take`. The post above is labeled `hot_take`.

**Case 2:** A post that contains emotion and a stat, but primarily functions as an emotional complaint.
*Example:* "I can't believe Darvin Ham played Prince over Rui for 30 minutes. The stats literally show the Lakers are +8 with Rui on the floor. Terrible coaching."
**Decision Rule:** If the primary function is emotional venting rather than a structured argument, label it `reaction`.

**Case 3:** A bold opinion that relies on a widespread narrative rather than verifiable stats.
*Example:* "Rudy Gobert is useless in the playoffs. Teams just go small and play him off the floor every year because he can't guard the perimeter."
**Decision Rule:** Even if a narrative sounds analytical, if it lacks verifiable stats and asserts a bold claim, label it `hot_take`.

## 4. Data Collection Plan
- **Where:** A Python script interacts with the reddit34 RapidAPI to pull comments from `r/nba` posts.
- **How many:** The script collects examples and annotates them using a length-based heuristic. It balances the dataset to 80 examples per class.

## 5. Evaluation Metrics
Evaluation uses:
- **Overall Accuracy:** To measure correctness.
- **Per-Class F1 Score:** To ensure the model predicts all classes well.
- **Confusion Matrix:** To see which boundaries the model struggles with.

## 6. Definition of Success
The classifier is successful if:
1. Overall accuracy is >75% on the test set.
2. The F1 score for `analysis` is >0.70.

## 7. AI Tool Plan
- **Label stress-testing:** An LLM generates 5 ambiguous posts to test label definitions.
- **Annotation assistance:** A script pre-labels the dataset, followed by manual review.
- **Failure analysis:** Incorrect predictions are fed to an LLM to identify underlying patterns.
