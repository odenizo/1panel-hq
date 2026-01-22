# AI Agent Integration Guide

This guide explains how AI agents (like Claude, GPT-4, or other coding agents) can use **1panel-hq** as a central hub for infrastructure management and automation.

## Overview

1panel-hq provides a structured, machine-readable repository that AI agents can:

1. **Understand** - Read documentation and metadata to comprehend system state
2. **Query** - Analyze JSON files to find information
3. **Execute** - Run scripts and workflows to make changes
4. **Report** - Commit findings back to repository
5. **Recommend** - Suggest improvements based on analysis

## Getting Started as an AI Agent

### 1. Repository Structure Overview

When you clone this repository, understand these key directories:

```
1panel-hq/
├── deployments/              # How containers are deployed
│   ├── containers/           # Each container's documentation
│   ├── github-actions-runner/# CI/CD runner
│   └── scripts/              # Automation scripts you can run
├── inventory/                # Current infrastructure state
│   ├── containers-registry.json
│   ├── access-points.json
│   ├── dependencies-graph.json
│   ├── ports-map.json
│   └── resource-usage.json
├── monitoring/               # Health check definitions
│   ├── health-checks/        # Per-container health checks
│   └── alerts/               # Alert configurations
├── operations/               # Operational procedures
│   ├── runbooks/             # How-to guides
│   └── maintenance/          # Maintenance tasks
├── automation/               # Automation workflows
│   ├── ai-agents/            # Agent-specific instructions
│   ├── workflows/            # GitHub Actions workflows
│   └── python-runners/       # Python automation scripts
└── data/                     # (Auto-generated) Collected metrics
```

### 2. Understanding the System

Start by reading these files in order:

1. **README.md** (root) - Overall purpose and structure
2. **inventory/containers-registry.json** - What containers are running
3. **inventory/dependencies-graph.json** - How they relate to each other
4. **inventory/access-points.json** - How to reach each service
5. **deployments/containers/[app]/README.md** - Specific app documentation

### 3. Common Tasks

## Agent Tasks You Can Perform

### A. Infrastructure Discovery

**Goal**: Understand what's currently deployed

**Steps**:
1. Read `inventory/containers-registry.json`
2. Count containers by type (database, application, infrastructure)
3. Check `inventory/resource-usage.json` for capacity
4. Report findings

**Example Code**:
```python
import json

with open('inventory/containers-registry.json') as f:
    registry = json.load(f)

total = registry['summary']['total_running']
containers_by_type = {}

for container in registry['containers']:
    ctype = container['type']
    if ctype not in containers_by_type:
        containers_by_type[ctype] = 0
    containers_by_type[ctype] += 1

print(f"Total containers: {total}")
print(f"By type: {containers_by_type}")
```

### B. Health Monitoring

**Goal**: Check if all containers are healthy

**Steps**:
1. Read `inventory/containers-registry.json`
2. For each container, run its health check script
3. Collect results
4. Report any unhealthy containers
5. Recommend remediation

**Example**:
```bash
#!/bin/bash
# Health check all containers

for container_dir in deployments/containers/*/; do
  container_name=$(basename "$container_dir")
  if [ -f "${container_dir}scripts/health-check.sh" ]; then
    echo "Checking $container_name..."
    bash "${container_dir}scripts/health-check.sh"
  fi
done
```

### C. Backup Verification

**Goal**: Ensure all critical containers are backed up

**Steps**:
1. Read `deployments/containers/[app]/metadata.json` for all apps
2. Check `backup.enabled` field
3. Verify backup scripts exist
4. Run backup scripts if enabled
5. Report backup status

### D. Dependency Analysis

**Goal**: Understand what depends on what

**Steps**:
1. Read `inventory/dependencies-graph.json`
2. Identify critical path (containers others depend on)
3. Check if critical containers are healthy
4. Alert if critical container goes down

**Example**:
```python
import json

with open('inventory/dependencies-graph.json') as f:
    deps = json.load(f)

# Find containers that are critical
critical = [d for d in deps['dependencies'] if d['criticality'] == 'critical']
print(f"Critical containers: {[c['name'] for c in critical]}")

# Find what depends on postgres
for dep in deps['dependencies']:
    if dep['name'] == 'postgres':
        print(f"Postgres is required by: {dep['required_by']}")
```

### E. Capacity Planning

**Goal**: Predict when resources will run out

**Steps**:
1. Read `inventory/resource-usage.json`
2. Calculate growth rate for each resource type
3. Project usage 30/60/90 days forward
4. Alert if any resource will exceed capacity
5. Recommend scaling

**Example**:
```python
import json
from datetime import datetime, timedelta

with open('inventory/resource-usage.json') as f:
    usage = json.load(f)

for container in usage['containers']:
    name = container['name']
    disk_growth = container['disk']['growth_per_day_gb']
    current_disk = container['disk']['current_usage_gb']
    limit_disk = container['disk']['limit_gb']
    
    # Project 30 days
    projected = current_disk + (disk_growth * 30)
    if projected > limit_disk:
        days_to_full = (limit_disk - current_disk) / disk_growth if disk_growth > 0 else 999
        print(f"WARNING: {name} disk will be full in {days_to_full:.0f} days")
```

### F. Configuration Drift Detection

**Goal**: Detect when running config differs from documented config

**Steps**:
1. Read `deployments/containers/[app]/metadata.json` (expected state)
2. Read `inventory/containers-registry.json` (actual state)
3. Compare key fields
4. Report any differences
5. Recommend fixes

### G. Automated Remediation

**Goal**: Fix common issues automatically

**Steps**:
1. Detect problem (e.g., container unhealthy)
2. Look up remediation in `operations/runbooks/troubleshooting.md`
3. Execute fix script
4. Verify fix worked
5. Report what was fixed

## Agent-Specific Instructions

### For GitHub Copilot

Instructions file: `automation/ai-agents/infrastructure-agent.md`

Copilot can:
- Generate new container documentation templates
- Write deployment scripts
- Create GitHub Actions workflows
- Analyze code in deployment configurations

### For Claude/GPT-4 (ChatGPT)

Instructions file: `automation/ai-agents/monitoring-agent.md`

These agents excel at:
- Analyzing logs and reports
- Writing explanations and recommendations
- Generating markdown documentation
- Creating runbooks and procedures
- Suggesting improvements based on patterns

### For Autonomous Agents

Instructions file: `automation/ai-agents/remediation-agent.md`

Autonomous agents can:
- Execute predefined workflows
- Commit changes to repository
- Create GitHub issues
- Trigger further automation
- Report status

## Reading Machine-Readable Files

### JSON Files

```python
import json

# Load and parse
with open('inventory/containers-registry.json') as f:
    data = json.load(f)

# Query
healthy_containers = [c for c in data['containers'] if c['health_status'] == 'healthy']
```

### YAML Files (health checks)

```python
import yaml

with open('monitoring/health-checks/postgres.yaml') as f:
    config = yaml.safe_load(f)

health_check_command = config['health_check']['command']
```

### Executing Scripts

```python
import subprocess

# Run backup script
result = subprocess.run(
    ['bash', 'deployments/containers/postgres/scripts/backup.sh'],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print(f"Backup successful: {result.stdout}")
else:
    print(f"Backup failed: {result.stderr}")
```

## Committing Changes

When you want to update the repository with findings:

### Update Inventory Files

```bash
# After running collection script
git add inventory/
git commit -m "chore: Update infrastructure inventory"
```

### Create Issues for Problems Found

```bash
# Create GitHub issue for found problem
gh issue create \
  --title "PostgreSQL disk usage at 80%" \
  --body "Recommend scaling. Current: 40GB / Limit: 50GB. Growing at 0.5GB/day."
```

### Commit New Documentation

```bash
# Add new container documentation
git add deployments/containers/new-app/
git commit -m "docs: Add documentation for new-app container"
```

## Triggering Workflows

You can trigger GitHub Actions workflows from your analysis:

```bash
# Trigger health check workflow
gh workflow run daily-health-check.yml

# Trigger data collection
gh workflow run collect-infrastructure-data.yml
```

## Error Handling

When something goes wrong:

1. **Script execution fails**: Check `deployments/scripts/` for error handling
2. **Container unavailable**: See `operations/runbooks/troubleshooting.md`
3. **Data collection incomplete**: Check `monitoring/health-checks/` to diagnose
4. **Dependency issues**: Review `inventory/dependencies-graph.json`

## Reporting Findings

### Generate Report

```python
import json
from datetime import datetime

report = {
    'timestamp': datetime.now().isoformat(),
    'agent': 'monitoring-agent',
    'findings': [
        {
            'severity': 'warning',
            'container': 'postgres',
            'issue': 'Disk usage at 80%',
            'recommendation': 'Scale disk or archive old data'
        }
    ],
    'actions_taken': [
        'Ran health checks on all containers',
        'Updated inventory/containers-registry.json',
        'Created GitHub issue #42'
    ]
}

# Save report
with open(f'data/reports/agent-report-{datetime.now().date()}.json', 'w') as f:
    json.dump(report, f, indent=2)
```

### Commit Report

```bash
git add data/reports/
git commit -m "docs: Agent monitoring report for 2024-01-22"
git push
```

## Security Considerations

### Secrets Management

- **Never** commit `.env` files or credentials
- Read credentials from GitHub Secrets
- Use `github_token` for API calls

```python
import os
token = os.getenv('GITHUB_TOKEN')
db_password = os.getenv('POSTGRES_PASSWORD')
```

### Safe Script Execution

- Validate script paths before executing
- Run with minimal privileges
- Log all executed commands
- Check return codes

```python
import subprocess
import os

# Validate path is safe
script = 'deployments/containers/postgres/scripts/backup.sh'
assert script.startswith('deployments/')
assert '..' not in script  # No directory traversal

# Run safely
result = subprocess.run(
    ['/bin/bash', script],
    cwd=os.getcwd(),
    capture_output=True,
    timeout=300  # 5 minute timeout
)
```

## Integration Examples

### Example 1: Daily Health Check Agent

Creates daily health report:

```python
#!/usr/bin/env python3
import json
import subprocess
from datetime import datetime

# Collect health status
health = {}
for container_dir in os.listdir('deployments/containers'):
    result = subprocess.run(
        ['bash', f'deployments/containers/{container_dir}/scripts/health-check.sh'],
        capture_output=True
    )
    health[container_dir] = 'healthy' if result.returncode == 0 else 'unhealthy'

# Save report
report = {
    'timestamp': datetime.now().isoformat(),
    'health_status': health,
    'summary': {'healthy': sum(1 for v in health.values() if v == 'healthy'),
                'unhealthy': sum(1 for v in health.values() if v == 'unhealthy')}
}

with open(f"data/reports/health-{datetime.now().date()}.json", 'w') as f:
    json.dump(report, f, indent=2)
```

### Example 2: Capacity Planning Agent

Analyzes trends and recommends scaling:

```python
#!/usr/bin/env python3
import json
from datetime import datetime, timedelta

with open('inventory/resource-usage.json') as f:
    usage = json.load(f)

recommendations = []

for container in usage['containers']:
    disk_growth = container['disk']['growth_per_day_gb']
    current = container['disk']['current_usage_gb']
    limit = container['disk']['limit_gb']
    
    if disk_growth > 0:
        days_remaining = (limit - current) / disk_growth
        if days_remaining < 30:
            recommendations.append({
                'container': container['name'],
                'action': 'Scale disk',
                'urgency': 'high' if days_remaining < 7 else 'medium',
                'details': f'Disk will be full in {days_remaining:.0f} days'
            })

report = {
    'timestamp': datetime.now().isoformat(),
    'recommendations': recommendations
}

with open(f"data/reports/capacity-{datetime.now().date()}.json", 'w') as f:
    json.dump(report, f, indent=2)
```

## Permissions & Access

Make sure your agent has:

- Read access to all repository files
- Write access to `data/` and `automation/ai-agents/` directories
- Permission to execute scripts in `deployments/scripts/`
- Permission to create GitHub issues and comments
- Access to GitHub Secrets for credentials

## Debugging

When something goes wrong:

1. Check script output: `cat data/logs/*.log`
2. Review last commits: `git log --oneline -10`
3. Check inventory freshness: `stat inventory/containers-registry.json`
4. Test manually: `bash deployments/containers/[app]/scripts/health-check.sh`

## See Also

- [Automation workflows](../automation/workflows/)
- [Python runners](../automation/python-runners/)
- [Operations runbooks](../operations/runbooks/)
- [Container documentation](../deployments/containers/)
- [Inventory structure](../inventory/)

---

**This repository is designed to be AI-friendly. All information is machine-readable, all procedures are scripted, and all state is versionable.**
