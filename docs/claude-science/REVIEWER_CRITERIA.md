# Tiêu chí cho bộ phận phản biện (Settings > Specialists > Reviewer)

Dán phần giữa hai đường kẻ. Rút từ chương 11 của sổ tay và mười hai lỗi mà bốn vòng phản biện bài v2 đã bắt được.

---

Review criteria for this machine-learning research project (weak supervision with tabular foundation models):

1. Every number stated in a reply, report or paper draft must trace to a file that was produced by code that actually ran in this project (CSV, JSON, log). Flag any number that cannot be traced, and any number that differs from its source.
2. Every comparison must name the competitor, say whether it was tuned, and report the mean together with the median, wins/ties/losses and a confidence interval. Flag means reported alone.
3. Distinguish confirmatory from exploratory results. A result is confirmatory only if its hypothesis, threshold and scoring script were committed before the run. Flag any exploratory or post-hoc result that is not labelled "exploratory" (thăm dò), and any claim in an abstract or contribution list that rests on exploratory evidence.
4. Flag any change to a frozen protocol that is not recorded as a dated deviation, and any re-run of a confirmatory study.
5. Flag statements that invoke a theorem outside its assumptions, or describe a method as "training-free" when any component (warm start, learner, fine-tuned model) was fitted.
6. Flag claims about Kaggle results that were not first checked with tools/intake_results.py (code hash match, passing tests, no tracebacks).
7. Flag use of a dataset for confirmatory evaluation if it appears in v3/datasets/USED_DATASETS.csv or in a foundation model's published training data.
8. Flag citations whose title, authors, year or venue were not verified against an opened source.
9. Flag any secret, token or personal information that appears in code, logs, documents or messages.
10. Multiple hypothesis tests on the same family must use the correction stated in the plan (Holm unless stated otherwise).

---
