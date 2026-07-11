# THE ROAD OS — PRODUCT SPECIFICATION
## VERSION 1.0 (SINGLE SOURCE OF TRUTH)

---

### SECTION 01 | VISION
*   **What is The Road OS?** The Road OS is a high-performance cloud operating system built specifically for the luxury beauty, spa, and wellness sectors in the GCC. It replaces fragmented tools with a single, unified workflow that handles guest relations, staff scheduling, retail tracking, and multi-branch financials.
*   **Why does it exist?** Traditional beauty ERP software is cluttered, complex, and ignores the nuances of GCC hospitality (e.g., specific commission tier structures, privacy suites, and multi-currency branch scaling). The Road OS removes this friction, making technology invisible to the guest and effortless for the staff.
*   **Who is it built for?** High-end salon chains, luxury spa hotels, wellness clinics, and premium beauty boutiques across Kuwait, Saudi Arabia, Bahrain, and the wider GCC region.

---

### SECTION 02 | CORE PRINCIPLES
1.  **Hospitality First:** Digital interactions must speed up human service, never delay it. Checking in or paying should take under 30 seconds.
2.  **Operational Simplicity:** Flat layouts, zero modal pop-ups, and clear typography. Staff should learn the core POS in less than one hour.
3.  **Human-Centered Workflows:** The software adapts to the user's role. Stylists see a simple mobile schedule, while owners see a quiet, executive ledger.
4.  **Arabic-First:** Fully optimized for Arabic reading directions and local terminology, with English as a secondary option.
5.  **Cloud-Native & Multi-Branch:** Centralized database sync ensuring immediate cross-branch records (e.g., gift card redemptions, package usages, and staff roster shifts).

---

### SECTION 03 | PERSONAS
*   **Salon Owner (المالكة):** Needs macro financial health ledgers, multi-branch comparisons, and product ROI insights.
*   **General Manager (المديرة):** Coordinates employee schedules, runs end-of-day cash counts, and authorizes special pricing/discounts.
*   **Receptionist (الاستقبال):** Coordinates guest arrivals, checks booking details, and processes retail purchases.
*   **Stylist / Therapist (الخبيرة):** Performs treatment services and recommends aftercare products on her mobile portal.
*   **Cashier (المحاسبة):** Finalizes invoices, handles K-Net terminal payments, and prints receipts.
*   **Inventory Officer (مسؤولة المخزن):** Receives stock shipments, distributes bottles to styling stations, and checks inventory counts.
*   **Customer (الضيفة):**Books appointments online, checks active package balances, and views personal treatment history.

---

### SECTION 04 | MODULES
*   **Appointments & Calendar:** Multi-chair calendar layout with color-coded service categories and dragging scheduling blocks.
*   **POS (Point of Sale):** Invoice builder capable of split payments (e.g., K-Net + Cash), tipping, packages redemption, and automatic tax calculation.
*   **CRM & Profiles:** Profile records containing treatment notes, color formulas, and skin sensitivity logs.
*   **Inventory:** Multi-warehouse tracking divided into retail stock (for sale) and professional stock (for backbar usage).
*   **Staff & Payroll:** Hourly rosters, commission rates, and base salary calculators.
*   **Memberships & Packages:** Digital wallets tracking prepaid service card packages and loyalty points.
*   **Settings & Multi-Branch Control:** Access control lists, pricing variables per branch, and fiscal year declarations.

---

### SECTION 05 | USER JOURNEYS
1.  **Daily Opening:** Manager signs in, sets the cash drawer float, and checks today's staff roster.
2.  **First Appointment:** Receptionist greets the guest, verifies booking details, and alerts the stylist with a click.
3.  **Walk-in Customer:** Receptionist reviews calendar slots, selects an available stylist, and adds the guest directly to the active queue.
4.  **POS Checkout:** Cashier pulls up the invoice, applies K-Net payment, splits employee tips, and sends an electronic receipt.
5.  **Inventory Adjustment:** Inventory officer performs a physical count and updates product stock levels directly in the app.
6.  **EOD closing:** Manager counts cash drawer, prints a POS reconciliation report, and closes the terminal session.

---

### SECTION 06 | BUSINESS RULES
*   **Appointment Conflicts:** A stylist cannot be booked for overlapping slots unless the service description allows parallel processing (e.g. hair coloring wait time).
*   **Commission Calculation:** Paid out based on net invoice value (excluding VAT and tips). Service commissions depend on employee tiers, while product commissions use flat-rate incentives.
*   **Package Redemption:** Packages are tied to a unique customer ID. Each service deduction must update the database instantly to prevent double-use at other branches.
*   **Membership Expiry:** Memberships auto-expire at midnight on their termination date. Expired loyalty points cannot be redeemed.
*   **Refund Policy:** Services are non-refundable. Products can be returned within 14 days if the seal is intact, returning funds to customer store credit.

---

### SECTION 07 | NOTIFICATIONS
*   **SMS & WhatsApp:** Automated booking confirmations, appointment reminders (24 hours prior), and low-balance warnings.
*   **Email:** Monthly executive performance reports sent directly to owners.
*   **Internal App:** Low-stock notifications pushed to the inventory manager's dashboard.

---

### SECTION 08 | REPORTS
*   **Daily Sales:** Invoices, payment splits, and tax logs.
*   **Branch Performance:** Occupancy, service profit margins, and average transaction values.
*   **Staff Performance:** Individual revenues, client return rates, and retail cross-sale percentages.
*   **Inventory Ledger:** Stock movements, cost values, and expiration dates.
*   **VAT Reports:** Input vs. output tax declarations formatted to GCC authority regulations.

---

### SECTION 09 | PERMISSIONS
*   **Owner:** Unlimited administrative rights across all branches.
*   **Manager:** Read-write access within designated branches, excluding core bank settings.
*   **Reception / Cashier:** Booking adjustments, POS invoices, and customer registrations.
*   **Stylist:** Read-only access to personal appointment schedules and customer visit histories.
*   **Inventory Officer:** Product catalogs, stock adjustments, and purchasing logs.

---

### SECTION 10 | API DOMAINS
*   `GET /api/v1/appointments` (Scheduling controls)
*   `POST /api/v1/pos/checkout` (Invoice settlement)
*   `GET /api/v1/crm/customer` (Guest profiles & notes)
*   `PUT /api/v1/inventory/stock` (Stock adjustments)
*   `GET /api/v1/reports/sales` (Finance & VAT reports)

---

### SECTION 11 | QUALITY STANDARDS
*   **Performance:** POS pages must load in under **800ms**.
*   **Accessibility:** WCAG 2.1 compliance with optimized screen readers for Arabic text.
*   **Security:** Enforced SSL, daily database backup vaults, and full system logging for manager actions (e.g. refund approvals).

---

### SECTION 12 | DEFINITION OF DONE
A feature is considered **Done** only when it meets the following criteria:
1.  **Goal Defined:** Business value and target metric are clearly outlined.
2.  **UX Validated:** Symmetrical, Arabic-first interface approved by art direction.
3.  **Permissions Mapped:** Access controls configured for all user roles.
4.  **API Documented:** Clear schema endpoints for backend developers.
5.  **Quality Checked:** Passes QA testing with zero critical open tickets.
6.  **Manuals Updated:** Core user help guides and documentation are live.
