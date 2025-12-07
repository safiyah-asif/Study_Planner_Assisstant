# ✅ **TestPlan.md**

```md
# Test Plan

## Test Cases

| ID   | Test Type | Input                                                             | Expected Output                                                                                            | Actual Result               |
| ---- | --------- | ----------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | --------------------------- |
| TC01 | Normal    | Goal + 3 topics + valid hours                                     | Schedule table generated                                                                                   | Pass                        |
| TC02 | Negative  | No topics added                                                   | Error: "Please add at least one topic!"                                                                    | Pass                        |
| TC03 | Edge Case | 0 hours for all days                                              | Empty schedule                                                                                             | Pass                        |
| TC04 | Edge Case | 2-week plan, total 3 hours, 2 topics: Difficulty 5 + Difficulty 3 | System should distribute hours fairly or partially across BOTH topics (not allocate all to one topic only) | Pass |
```
