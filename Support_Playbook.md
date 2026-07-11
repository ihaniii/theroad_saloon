# THE ROAD — SUPPORT PLAYBOOK
## SUPPORT SERVICE LEVEL AGREEMENTS (SLA) & ESCALATION PROTOCOLS

---

### 01 | TICKET PRIORITY MATRIX
All support requests received via the customer success portal must be classified into one of the following priority levels:

| Priority | Criteria | SLA Response | SLA Resolution |
| :--- | :--- | :--- | :--- |
| **P1 - Critical** | Entire system is down; POS checkout blocked; K-Net payments failing across all terminals. | `< 15 mins` | `< 4 hours` |
| **P2 - High** | Major feature unavailable (e.g. appointment calendar not loading, or inventory deductions failing). | `< 1 hour` | `< 12 hours` |
| **P3 - Medium** | Minor operational issue; workaround exists (e.g. employee roster adjustments failing, or invoice layout spacing errors). | `< 4 hours` | `< 48 hours` |
| **P4 - Low** | General questions; feature requests; non-blocking system adjustments. | `< 12 hours` | `< 5 days` |

---

### 02 | ESCALATION MATRIX
If a ticket is not resolved within the specified SLA limits, it must be escalated automatically:

```
[Level 1 Support Agent] ──► [Level 2 Technical Specialist] ──► [Level 3 Engineering Lead]
```

1.  **Level 1 (Support Desk Agent):** Handles initial ticket registration, basic troubleshooting, and knowledge base lookups.
2.  **Level 2 (Technical Support Specialist):** Handles K-Net hardware integration errors, database sync failures, and account permissions. (Escalated if P1 is unresolved for >1 hour).
3.  **Level 3 (Engineering Lead):** Directly accesses cloud code instances to fix core database queries and app bugs. (Escalated if P1 is unresolved for >2 hours).

---

### 03 | BUG TRACKING & RESOLUTION WORKFLOW
1.  **Identification:** Support agent logs the bug in **Linear**, tagging it with the client ID and priority level.
2.  **Verification:** QA engineer attempts to replicate the bug in a staging environment.
3.  **Hotfix Deployment:** If verified as P1/P2, engineering builds a patch and deploys it directly to the cloud instance after testing.
4.  **Verification & Close:** The support agent contacts the Salon General Manager to verify the fix and closes the ticket.

---

### 04 | FEATURE REQUEST PIPELINE
*   **Intake:** All feature requests are tagged as P4 (Low) and logged in Productboard.
*   **Validation:** Product Managers conduct monthly reviews of all logged requests, grouping them by GCC market needs.
*   **Prioritization:** Features that benefit multiple salon chains are moved into the official quarterly product backlog.
