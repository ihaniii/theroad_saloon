# THE ROAD OPERATING SYSTEM (THE ROAD OS)
## PLATFORM ARCHITECTURE & MASTER ROADMAP — PHASE 03

---

### 01 | SYSTEM ARCHITECTURE Overview
The Road OS is built as a single, multi-tenant database using an enterprise Odoo framework backend, decoupled into seven highly tailored, responsive front-end experience layers.

```
                  ┌──────────────────────────────────────┐
                  │           THE ROAD CORE OS           │
                  │   (Secure Odoo / PostgreSQL Cloud)   │
                  └──────────────────┬───────────────────┘
                                     │
     ┌───────────────┬───────────────┼───────────────┬───────────────┐
     │               │               │               │               │
┌────▼────┐     ┌────▼────┐     ┌────▼────┐     ┌────▼────┐     ┌────▼────┐
│01 OWNER │     │02 SALON │     │03 STAFF │     │04 CLIENT│     │05 ACADEMY
│   OS    │     │  OPS    │     │  PORTAL │     │   APP   │     │  PORTAL │
└─────────┘     └─────────┘     └─────────┘     └─────────┘     └─────────┘
                                     │
                             ┌───────┴───────┐
                             │               │
                        ┌────▼────┐     ┌────▼────┐
                        │06 SUCCESS     │07 EXEC  │
                        │  PORTAL │     │  OS     │
                        └─────────┘     └─────────┘
```

---

### 02 | THE SEVEN INTEGRATED PORTALS

#### 01 | OWNER OS (لوحة تحكم الملاك)
Designed as a quiet, typography-first executive ledger. 
*   **Core Modules:** 
    *   **BI Analytics (ذكاء الأعمال):** Multi-branch cohort analysis, customer lifetime value (CLV), treatment recurrence trends.
    *   **Financial Reports (التقارير المالية):** Net revenue, gross margins, EBITDA, tax reports (VAT), multi-currency conversions.
    *   **Branch Control (التحكم بالفروع):** Real-time occupancy comparisons across GCC locations.
    *   **Growth Insights (مؤشرات النمو):** Auto-generated recommendations for service package pricing optimization.

#### 02 | SALON OPERATIONS (إدارة الصالون)
The operational engine driving salon workflow.
*   **Core Modules:**
    *   **Symmetrical Booking Calendar (الجدولة الذكية):** Drag-and-drop bookings aligned with chair availability.
    *   **Unified POS (نقاط البيع):** Splits invoices, manages custom package redemptions, and integrates directly with local GCC payment terminals (K-Net, Benefit, Mada).
    *   **Inventory Control (المخازن):** Separate tracking for retail products vs. internal salon-use containers.
    *   **Payroll & Commissions (المرتبات والعمولات):** Automated calculations based on tier levels and client retention rates.

#### 03 | STAFF EXPERIENCE (بوابة الخبيرات)
Mobile-first portal for technicians, hair stylists, and masseuses.
*   **Core Modules:**
    *   **Daily Agenda (جدول اليوم):** Clean timeline displaying upcoming guest appointments and details.
    *   **Commission Ledger (متابعة العمولات):** Real-time earnings breakdown per service and product sale.
    *   **Attendance (حضور وانصراف):** Minimalist check-in using localized geolocation tags.
    *   **Communication (التواصل الداخلي):** Handover notes for guests moving between sections (e.g. Hair to Spa).

#### 04 | CLIENT EXPERIENCE (تطبيق العميلات)
Web and native mobile application focused on guest autonomy.
*   **Core Modules:**
    *   **Visual Booking Engine (الحجز السريع):** Symmetrical interface for selecting preferred specialists and spaces.
    *   **Membership Card (العضوية الرقمية):** Walnut/ivory digital wallet card displaying active tier levels.
    *   **Visit History & Receipts (سجل الزيارات):** PDF receipt vault and past treatment notes.
    *   **Product Recommender (مستحضراتي):** Recommended care routines matching current hair and skin diagnostic records.

#### 05 | ACADEMY (أكاديمية الطريق)
The onboarding and training platform for salon workers.
*   **Core Modules:**
    *   **Operational Guides (أدلة التشغيل):** Step-by-step videos for guest welcoming standards, tablet hygiene, and uniform rules.
    *   **Technical Training (التدريب الفني):** Tutorials on Odoo cash reconciliation and catalog configuration.
    *   **Certification (الشهادات الرقمية):** Automated tests and platform competency badges.

#### 06 | CUSTOMER SUCCESS (بوابة النجاح والدعم)
The direct link between the salon operator and The Road support team.
*   **Core Modules:**
    *   **Live Chat & Tickets (الدعم المباشر):** Dedicated Arabic communication channel with accountants and tech leads.
    *   **Knowledge Base (مكتبة المعرفة):** Quick search articles covering VAT filing, K-Net hardware resets, and staff onboarding guides.
    *   **System Roadmap (مسار التطوير):** Updates on upcoming platform features.

#### 07 | EXECUTIVE EXPERIENCE (بوابة الاستثمار والامتياز)
Designed for enterprise and franchise operators.
*   **Core Modules:**
    *   **Franchise Ledger (إدارة الامتياز):** Royalty collection tracking, brand compliance checklists, and supply chain margins.
    *   **Expansion Simulator (محاكي التوسع):** Feasibility models based on demographics and localized real-estate values.

---

### 03 | INFORMATION ARCHITECTURE & NAVIGATION
The navigation relies on the **Arabic First** layout, where menus flow from right to left.

```
[الرئيسية (Home)] ──► [التشغيل (Operations)] ──► [الحجوزات (Bookings)]
                                            ├──► [المبيعات (POS)]
                                            └──► [المخزون (Inventory)]

                  ──► [التقارير (Reports)]    ──► [الملخص المالي (Ledger)]
                                            ├──► [أداء الفروع (Branches)]
                                            └──► [العمولات (Commissions)]

                  ──► [الفريق (Team)]        ──► [الرواتب (Payroll)]
                                            └──► [الحضور (Attendance)]
```

*   **Breadcrumb Strategy:** Always visible, written in clean Amiri serif typography at the top of the interface.
*   **Menu Layout:** A floating right-hand sidebar that collapses into a quiet icon list to maintain a high whitespace ratio (+35%).

---

### 04 | USER JOURNEYS

#### Journey A: The Symmetrical EOD Reconciliation (Manager)
1.  **Step 1:** Salon Manager logs in via **Salon Operations** tablet.
2.  **Step 2:** Navigates to `التشغيل ◄ المبيعات ◄ إغلاق الصندوق`.
3.  **Step 3:** The screen displays a clean overview of K-Net, Cash, and Card sales.
4.  **Step 4:** System automatically reconciles POS records with local bank logs.
5.  **Step 5:** Manager confirms matching amounts. Reconciled reports are instantly pushed to the **Owner OS** ledger.

#### Journey B: The Seamless Guest Visit (Client & Stylist)
1.  **Step 1:** Client checks in at reception; receptionist confirms booking with a single click.
2.  **Step 2:** Stylist accesses **Staff Experience** on a tablet, viewing the guest's hair-profile history.
3.  **Step 3:** After completing the treatment, the stylist adds recommendations (`زيت أرغان لتغذية الشعر`).
4.  **Step 4:** Receptionist views the updated bill at checkout. Guest pays via K-Net.
5.  **Step 5:** A digital receipt and the stylist's recommendations are pushed to the **Client Experience** app.

---

### 05 | INTERACTION & DESIGN PRINCIPLES
To prevent cognitive overload, all front-end experiences must enforce:
*   **No Modal Overload:** Avoid modal popups. Use smooth vertical page expansions and sliding panels.
*   **Zero Placeholders:** Use actual live data formats (currency formatted to KWD/SAR/AED, actual calendar dates).
*   **Warm Palette Integration:** Backgrounds remain `#faf7f2`, cells `#fafafa`, and typography `#142e34` with `#c88a82` indicators.
*   **Quiet Transitions:** Element state changes must use CSS ease-in-out transitions capped at `300ms`.
