# THE ROAD — CUSTOMER SUCCESS PLAYBOOK
## CLIENT HEALTH MONITORING & RETENTION SYSTEM

---

### 01 | CUSTOMER HEALTH SCORE SYSTEM
The Customer Health Score determines the risk level of each salon account, computed weekly using four weighted parameters:

$$\text{Health Score} = 0.40 \times \text{Usage Score} + 0.25 \times \text{Training Score} + 0.20 \times \text{Support Score} + 0.15 \times \text{Financial Status}$$

#### 1. USAGE SCORE (40% Weight)
Measures the frequency of core system actions.
*   **Metrics:** POS checks processed per day, calendar changes per week, active employee check-ins.
*   **Risk Indicator:** A drop of >30% in weekly POS invoices indicates operational retreat or system bypass.

#### 2. TRAINING SCORE (25% Weight)
Measures the platform literacy of the salon staff.
*   **Metrics:** Academy video completion rates, certification test pass rates.
*   **Risk Indicator:** Low Academy engagement among new hires is a leading indicator of incorrect platform usage and eventual customer frustration.

#### 3. SUPPORT SCORE (20% Weight)
Measures the frequency and severity of technical support tickets.
*   **Metrics:** Open ticket age, frequency of urgent bugs raised.
*   **Risk Indicator:** Having more than 2 unresolved high-priority tickets open for >48 hours severely damages customer trust.

#### 4. FINANCIAL STATUS (15% Weight)
Measures subscription payment consistency.
*   **Metrics:** On-time subscription bill settlement.
*   **Risk Indicator:** Overdue balances >15 days immediately place the account in "At Risk" status.

---

### 02 | RENEWAL PROBABILITY & PROCESS
The Customer Success Manager (CSM) begins the renewal engagement plan **90 days prior** to subscription expiry:

```
[90 Days Out: Health Review] ──► [60 Days Out: Value Review] ──► [30 Days Out: Contract Deal]
```

1.  **90 Days Out (Health Audit):** Review overall health score. If the score is `<75`, deploy an optimization specialist to perform on-site staff training.
2.  **60 Days Out (Value Presentation):** Present the salon owner with a customized annual ROI report (e.g. showcasing revenue increases from packages, commission calculations saved, and bookings optimized).
3.  **30 Days Out (Contract Settlement):** Finalize annual subscription terms and process renewal invoices.

---

### 03 | RISK DETECTION & CHURN PREVENTION
*   **Trigger Event:** An account's health score drops below `60`.
*   **Immediate Action Plan (within 24 hours):**
    1.  The CSM schedules an urgent call with the Salon General Manager to identify the root operational block.
    2.  If technical bugs are the cause, the issue is escalated to Engineering with a strict 12-hour resolution SLA.
    3.  If training gaps are identified, the CSM schedules a live, on-site refresher session for the receptionist and cashier teams.
