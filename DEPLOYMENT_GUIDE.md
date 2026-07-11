# DEPLOYMENT GUIDE & OPERATIONS RUNBOOK
## THE ROAD OS — VERSION 1.0 (RELEASE CANDIDATE 1)

---

### 01 | DEPLOYMENT INFRASTRUCTURE

#### 1. PRODUCTION STACK CONFIGURATION
The Road OS utilizes a containerized deployment architecture comprising a FastAPI web application container and a PostgreSQL database.

*   **Dockerfile:** Evaluates a multi-stage Python runtime build.
*   **Docker Compose:** Definitively mounts the web and db containers, establishing proper health checks.

#### 2. STEP-BY-STEP DEPLOYMENT COMMANDS
To deploy The Road OS to a new staging/production environment:

```bash
# 1. Clone the repository
git clone https://github.com/theroad/platform-core.git /app

# 2. Configure variables
cp /app/.env.example /app/.env
# Edit values: DB_ENGINE=postgresql, JWT_SECRET, POSTGRES_PASSWORD

# 3. Spin up the containers
docker-compose up -d --build

# 4. Run verification checks
docker-compose ps
```

---

### 02 | OPERATIONS RUNBOOKS

#### 1. NIGHTLY DATABASE BACKUPS
The database backup script runs automatically at 02:00 AM daily via a system cron job:

```
0 2 * * * /app/scripts/backup_db.sh > /var/log/backup_nightly.log 2>&1
```

#### 2. RESTORING FROM BACKUP (DRY-RUN DRILL)
To recover database states from a compressed backup file:

```bash
# 1. Unzip the target backup
gunzip -c /app/backups/theroad_prod_backup_YYYYMMDD_HHMMSS.sql.gz > /tmp/restore.sql

# 2. Import SQL statements to PostgreSQL database
docker exec -i theroad_postgres psql -U theroad_admin -d theroad_prod < /tmp/restore.sql
```

---

### 03 | INCIDENT PLAYBOOKS

#### 1. INCIDENT: API RESPONSE LATENCY SPIKE (>2000ms)
*   **Identification:** High response time alerts triggered on New Relic / observability channels.
*   **Containment:** Check current database locks and active queries:
    ```sql
    SELECT pid, query, state FROM pg_stat_activity WHERE state != 'idle';
    ```
*   **Mitigation:** Kill long-running lock query processes using `SELECT pg_cancel_backend(pid);`.

#### 2. INCIDENT: MEMORY LEAK IN WEB APPLICATION CONTAINER
*   **Identification:** Container restarts or Out-Of-Memory (OOM) exit codes.
*   **Containment:** Restart the web container immediately:
    ```bash
    docker-compose restart web
    ```
*   **Prevention:** Profile memory consumption profiles via profiling libraries during development.
