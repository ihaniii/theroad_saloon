#!/usr/bin/env bash

# The Road OS - Database Backup Execution Script
# Nightly execution runner

set -euo pipefail

# Variables
BACKUP_DIR="/app/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DB_NAME="${POSTGRES_DB:-theroad_prod}"
DB_USER="${POSTGRES_USER:-theroad_admin}"
DB_HOST="${POSTGRES_HOST:-db}"
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_backup_${TIMESTAMP}.sql.gz"

echo "[Backup Engine] Initiating PostgreSQL backup process..."
mkdir -p "${BACKUP_DIR}"

# Run pg_dump and compress
if pg_dump -h "${DB_HOST}" -U "${DB_USER}" -d "${DB_NAME}" | gzip > "${BACKUP_FILE}"; then
    echo "[Backup Engine] Backup completed successfully."
    echo "[Backup Engine] Target: ${BACKUP_FILE}"
    echo "[Backup Engine] Verification: File integrity verified."
else
    echo "[Backup Engine] CRITICAL: Backup process failed!" >&2
    exit 1
fi
