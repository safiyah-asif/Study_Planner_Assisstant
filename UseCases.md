# Use Cases

## Use Case 1 – Create New Study Plan

| Item               | Description                                                                                                             |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| **Actor**          | Student                                                                                                                 |
| **Trigger**        | User wants a schedule for an upcoming exam/project                                                                      |
| **Preconditions**  | User has study goals/topics available                                                                                   |
| **Main Flow**      | 1. User enters goal <br> 2. Adds topics + difficulty <br> 3. Enters weekly free hours <br> 4. System generates schedule |
| **Alternate Flow** | User enters no topics → system shows error                                                                              |

---

## Use Case 2 – Edit Topics Before Schedule

| Item               | Description                                                                            |
| ------------------ | -------------------------------------------------------------------------------------- |
| **Actor**          | Student                                                                                |
| **Trigger**        | User needs to update topic or difficulty                                               |
| **Preconditions**  | User is on Step 2                                                                      |
| **Main Flow**      | 1. User edits text fields <br> 2. Removes or adds topics <br> 3. Proceeds to next step |
| **Alternate Flow** | User enters blank topic → warning appears                                              |

---

## Use Case 3 – Generate Multi-Week Plan

| Item               | Description                                                                                                |
| ------------------ | ---------------------------------------------------------------------------------------------------------- |
| **Actor**          | Student                                                                                                    |
| **Trigger**        | User selects 1-2 weeks of planning                                                                         |
| **Preconditions**  | Hours for each week/day provided                                                                           |
| **Main Flow**      | 1. User selects duration <br> 2. Enters hours for each week <br> 3. System distributes topics across weeks |
| **Alternate Flow** | Missing hours → system sets default values (hours = 02)                                                    |

---


