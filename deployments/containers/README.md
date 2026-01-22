# Container Documentation Guide

This directory contains documentation and configurations for all deployed containers running on 1Panel.

## Purpose

Each container/application deployed to 1Panel should have a corresponding directory here documenting:
- What the app does
- How it's deployed
- How to access it
- Dependencies and relationships
- Health checks and monitoring
- Backup/restore procedures
- Common operational tasks

## Directory Structure Per Container

For each container, create a directory with this structure:

```
containers/
└── app-name/
    ├── metadata.json              # Machine-readable metadata
    ├── docker-compose.yml         # Deployment configuration (if applicable)
    ├── env.example                # Environment variables template
    ├── README.md                  # Human-readable documentation
    ├── scripts/
    │   ├── backup.sh              # Backup procedure
    │   ├── restore.sh             # Restore procedure
    │   ├── init-db.sh             # Initialization (if needed)
    │   └── health-check.sh        # Health verification
    └── backups/
        ├── latest-backup.tar.gz
        └── backup-log.txt
```

## Required Files

### 1. `metadata.json`

Machine-readable metadata about the container. This is used by scripts and AI agents.

```json
{
  "name": "postgres",
  "version": "15.0",
  "type": "database",
  "description": "PostgreSQL database server",
  "deployed_on": "2024-01-20T10:30:00Z",
  "access_points": {
    "host": "localhost",
    "port": 5432,
    "protocol": "postgresql",
    "web_url": null
  },
  "dependencies": {
    "requires": [],
    "required_by": ["app-backend", "app-api"]
  },
  "resources": {
    "cpu_limit": "2",
    "memory_limit": "2Gi",
    "storage": "50Gi"
  },
  "health_check": {
    "command": "pg_isready -U postgres",
    "interval": "30s",
    "timeout": "10s",
    "retries": 3
  },
  "backup": {
    "enabled": true,
    "schedule": "daily at 02:00 UTC",
    "retention_days": 30,
    "script": "scripts/backup.sh"
  },
  "monitoring": {
    "health_check_file": "../../monitoring/health-checks/postgres.yaml",
    "metrics_exported": true
  },
  "tags": ["database", "critical", "stateful"],
  "owner": "Deniz",
  "documentation_url": "README.md"
}
```

### 2. `README.md`

Human-readable documentation covering:

```markdown
# PostgreSQL

## Overview
- **What**: PostgreSQL 15 database server
- **Why**: Central data store for application
- **When deployed**: 2024-01-20
- **Owner**: Deniz

## Access
- **Host**: localhost
- **Port**: 5432
- **User**: postgres
- **Password**: [stored in GitHub Secrets]

## Deployed with
- Database name: myapp
- Initial tables: created via init-db.sh
- Backup location: /data/postgres/backups/

## Common Tasks

### Connect to Database
```bash
psql -h localhost -U postgres -d myapp
```

### Backup
```bash
bash deployments/containers/postgres/scripts/backup.sh
```

### Restore
```bash
bash deployments/containers/postgres/scripts/restore.sh backup-file.tar.gz
```

## Monitoring
- Health check: Daily automated via GitHub Actions
- Alerts: If unavailable for >5 minutes
- Metrics: CPU, memory, disk usage tracked

## Dependencies
- **Requires**: Nothing
- **Required by**: app-backend, app-api

## Troubleshooting
- [See monitoring/README.md for health checks]
- Connection refused: Check port 5432 is exposed
- Disk full: Check /data/postgres usage

## See Also
- Docker Compose config: docker-compose.yml
- Health definition: ../../monitoring/health-checks/postgres.yaml
- Operations guide: ../../operations/runbooks/
```

### 3. `docker-compose.yml` (if applicable)

Full deployment configuration:

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15-alpine
    container_name: postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: myapp
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init-db.sh:/docker-entrypoint-initdb.d/init.sh
    networks:
      - 1panel
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
    driver: local

networks:
  1panel:
    external: true
```

### 4. `env.example`

Environment variables template:

```bash
# PostgreSQL Configuration
POSTGRES_PASSWORD=change-me-in-production
POSTGRES_USER=postgres
POSTGRES_DB=myapp

# Backup Configuration
BACKUP_RETENTION_DAYS=30
BACKUP_SCHEDULE="daily at 02:00 UTC"
```

### 5. Operational Scripts

#### `scripts/backup.sh`
```bash
#!/bin/bash
set -e

APP_NAME="postgres"
BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/${APP_NAME}_${TIMESTAMP}.tar.gz"

mkdir -p "$BACKUP_DIR"

echo "[$(date)] Starting backup of $APP_NAME"
docker exec postgres pg_dump -U postgres myapp | gzip > "$BACKUP_FILE"
echo "[$(date)] Backup complete: $BACKUP_FILE"
```

#### `scripts/restore.sh`
```bash
#!/bin/bash
set -e

BACKUP_FILE="$1"

if [ -z "$BACKUP_FILE" ]; then
  echo "Usage: $0 <backup-file>"
  exit 1
fi

echo "[$(date)] Restoring from $BACKUP_FILE"
gzip -dc "$BACKUP_FILE" | docker exec -i postgres psql -U postgres -d myapp
echo "[$(date)] Restore complete"
```

#### `scripts/health-check.sh`
```bash
#!/bin/bash

echo "Checking PostgreSQL health..."
docker exec postgres pg_isready -U postgres

if [ $? -eq 0 ]; then
  echo "✓ PostgreSQL is healthy"
  exit 0
else
  echo "✗ PostgreSQL is unhealthy"
  exit 1
fi
```

## Adding a New Container

When you deploy a new container to 1Panel:

1. Create directory: `containers/app-name/`
2. Copy template files
3. Fill in `metadata.json` with app details
4. Write `README.md` with operational procedures
5. Create `docker-compose.yml` if applicable
6. Create backup/health-check scripts in `scripts/`
7. Create health check definition in `monitoring/health-checks/app-name.yaml`
8. Add to `inventory/containers-registry.json`
9. Update `inventory/dependencies-graph.json`
10. Create GitHub Actions workflow for automation

## Container Types

### Database Containers
- postgres
- mysql
- redis
- mongodb

Must include:
- Backup/restore scripts
- Connection health checks
- Data volume documentation

### Application Containers
- app-backend
- app-frontend
- api-server

Must include:
- Health endpoint definition
- Dependency list
- Log location
- Configuration template

### Infrastructure Containers
- nginx (reverse proxy)
- prometheus (monitoring)
- grafana (dashboards)

Must include:
- Configuration templates
- Access point documentation
- Backup procedures for configs

### Utility Containers
- backup-automation
- log-aggregation
- certificate-renewal

Must include:
- Trigger mechanism
- Log output location
- Status verification

## Examples

See these for reference implementations:
- `postgres/` - Database container example
- `redis/` - Cache container example
- `nginx/` - Reverse proxy example

## Testing Documentation

Before committing container documentation:

1. **Metadata validation**
   ```bash
   python3 -m json.tool metadata.json
   ```

2. **Docker Compose validation**
   ```bash
   docker-compose config
   ```

3. **Script execution**
   ```bash
   bash scripts/backup.sh
   bash scripts/health-check.sh
   ```

4. **Documentation completeness**
   - All required sections in README.md
   - All scripts documented
   - All access points listed
   - Dependencies documented

## Updating Documentation

When container configuration changes:

1. Update `metadata.json` with new values
2. Update `docker-compose.yml` with new config
3. Update `README.md` with new procedures
4. Update health check if behavior changed
5. Create PR describing changes
6. Update `inventory/containers-registry.json`

## CI/CD Integration

Containers defined here are automatically:
- Monitored via health checks
- Included in capacity reports
- Tracked for configuration drift
- Backed up on schedule
- Included in disaster recovery plans

See `automation/` directory for workflows.

## Machine Readability

This structure is designed to be:
- **Parseable**: All configs in standard formats (JSON, YAML, Bash)
- **Queryable**: Scripts can extract information from metadata.json
- **Analyzable**: Dependencies and relationships defined structurally
- **Automatable**: All procedures scripted and version-controlled
- **AI-friendly**: Clear structure for agents to understand

## See Also

- [Inventory structure](../inventory/README.md)
- [Monitoring definitions](../monitoring/README.md)
- [Operations runbooks](../operations/runbooks/)
- [GitHub Actions workflows](../../automation/workflows/)
