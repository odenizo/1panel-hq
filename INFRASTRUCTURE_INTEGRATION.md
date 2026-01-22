# Integration with infrastructure-hq

## Overview

This repository (**1panel-hq**) is a component of a larger infrastructure management system:

- **infrastructure-hq** (Obsidian Vault) = Master hub for ALL infrastructure
- **1panel-hq** (GitHub Repository) = 1Panel-specific deployments and operations

## Relationship

### infrastructure-hq (Master Vault)

**Purpose**: Single source of truth for all infrastructure

**Contains**:
- Overall infrastructure architecture
- All VMs and servers (Hetzner, local, etc.)
- All services and applications
- All 1Panel instances and their apps
- Network topology and routing
- Security policies and access controls
- Documentation for all systems
- Operational procedures
- Disaster recovery plans
- Capacity and resource planning
- AI automation instructions

**Format**: Obsidian markdown vault

**Access**: `~/0-Projects-local/infrastructure-hq/`

### 1panel-hq (GitHub Repository)

**Purpose**: Operational management and automation for 1Panel

**Contains**:
- GitHub Actions runner deployment
- All 1Panel container documentation
- Container inventory and tracking
- Monitoring and health checks
- Backup and restore scripts
- Data collection and metrics
- Operational runbooks for 1Panel
- Automation workflows
- AI agent integration for 1Panel

**Format**: GitHub repository

**Access**: `~/0-Projects-local/1panel-hq/`

## Directory Structure Mapping

### infrastructure-hq (Obsidian Vault)

```
infrastructure-hq/
├── Overview/
│   ├── Architecture.md
│   ├── Infrastructure Map.md
│   └── Access Points.md
├── Infrastructure/
│   ├── Hetzner/
│   │   ├── VM-01.md
│   │   ├── VM-02.md
│   │   └── Networking.md
│   ├── Services/
│   │   ├── 1Panel/
│   │   │   └── Overview.md (links to 1panel-hq)
│   │   ├── DNS/
│   │   ├── CDN/
│   │   └── [Other services]
│   └── Security/
│       ├── Access Control.md
│       ├── Firewall Rules.md
│       └── Secrets Management.md
├── Applications/
│   ├── Deployed Containers.md
│   ├── Application A.md
│   ├── Application B.md
│   └── ...
├── Operations/
│   ├── Runbooks/
│   ├── Procedures/
│   ├── Incident Management.md
│   └── Disaster Recovery.md
├── AI Automation/
│   ├── Agent Instructions.md
│   ├── Workflows.md
│   └── Remediation Rules.md
├── Monitoring/
│   ├── Health Status.md
│   ├── Alerts.md
│   └── Metrics.md
└── Knowledge Base/
    ├── Tools and Technologies.md
    ├── Best Practices.md
    └── Lessons Learned.md
```

### 1panel-hq (GitHub Repository)

```
1panel-hq/
├── deployments/
│   ├── github-actions-runner/
│   ├── containers/              # Each container documented
│   ├── scripts/
│   ├── configs/
│   └── orchestration/
├── inventory/                   # Auto-generated from 1Panel
│   ├── containers-registry.json
│   ├── access-points.json
│   ├── dependencies-graph.json
│   ├── ports-map.json
│   └── resource-usage.json
├── monitoring/
│   ├── health-checks/
│   ├── dashboards/
│   └── alerts/
├── operations/
│   ├── runbooks/
│   ├── maintenance/
│   └── scripts/
├── automation/
│   ├── ai-agents/
│   ├── workflows/
│   └── python-runners/
├── data/
│   ├── snapshots/
│   ├── reports/
│   ├── metrics/
│   └── logs/
└── docs/
    ├── AGENT_GUIDE.md
    ├── SETUP_GUIDE.md
    └── ARCHITECTURE.md
```

## Information Flow

### From infrastructure-hq to 1panel-hq

```
infrastructure-hq (Master Vault)
├── "1Panel Overview" document
├── Lists all apps running on 1Panel
├── References specific documentation
└── Points to 1panel-hq for operational details
        ↓
    1panel-hq (GitHub)
    ├── deployments/containers/ (actual configs)
    ├── inventory/ (current state)
    ├── monitoring/ (health definitions)
    ├── operations/ (runbooks)
    └── automation/ (workflows)
```

### From 1panel-hq to infrastructure-hq

```
1panel-hq (GitHub)
├── inventory/ (JSON files)
├── data/reports/ (generated reports)
├── monitoring/ (health status)
└── automation/ (execution logs)
        ↓
infrastructure-hq (Master Vault)
├── Imported as current state
├── Analyzed for trends
├── Used for decision-making
├── Referenced in procedures
└── Integrated into AI agent decisions
```

## What Goes Where

### Store in infrastructure-hq

✅ **High-level architecture** - How everything relates
✅ **Strategic decisions** - Why things are set up
✅ **Cross-infrastructure concerns** - Affects multiple systems
✅ **Knowledge and context** - Understanding and history
✅ **Long-term plans** - Strategic direction
✅ **Procedures** - Step-by-step operations
✅ **Learning and improvements** - Lessons learned
✅ **Big picture analysis** - Trends and patterns
✅ **AI agent instructions** - High-level automation rules

### Store in 1panel-hq

✅ **1Panel-specific configs** - Docker Compose, environments
✅ **Container documentation** - What each app does
✅ **Current state tracking** - Inventory JSON files
✅ **Health definitions** - Health check YAML
✅ **Operational scripts** - Backup, restore, health-check
✅ **Automation workflows** - GitHub Actions YML
✅ **Data and metrics** - Collected data and reports
✅ **AI integration code** - Agent runners and hooks
✅ **Quick reference** - Access points, ports, APIs

## Cross-References

### In infrastructure-hq (Obsidian)

When documenting 1Panel, reference the GitHub repo:

```markdown
## 1Panel

**Repository**: [[../repos/1panel-hq]]
**GitHub**: https://github.com/odenizo/1panel-hq
**Local Clone**: ~/0-Projects-local/1panel-hq/

### Current Status
- See: [[../1panel-hq/Container Inventory]]
- Link to: `1panel-hq/inventory/containers-registry.json`

### Running Containers
1. **PostgreSQL** - Database
2. **Redis** - Cache
3. **GitHub Actions Runner** - CI/CD

For operational details, see `1panel-hq/deployments/containers/[app]/README.md`

### Monitoring
Health status: See `1panel-hq/monitoring/health-checks/`

### Recent Changes
Git history: `git log --oneline -10` in 1panel-hq
```

### In 1panel-hq (GitHub)

When needing context, reference the vault:

```markdown
# PostgreSQL Container

For context on why PostgreSQL is deployed, see infrastructure-hq:
- Document: Infrastructure > Services > 1Panel > Databases.md
- Architecture overview: Infrastructure > Architecture.md

## Operational Procedures

Day-to-day procedures are documented here in this repository.
Strategic procedures and disaster recovery are in infrastructure-hq.
```

## Workflow Example

### Adding a New Service

```
1. Document in infrastructure-hq (why, when, strategic)
   ├── Create Applications/[App Name].md
   ├── Explain purpose and relationships
   ├── Link to where it will run (1Panel or other)
   └── Record architectural decisions
   
2. Deploy to 1Panel
   └── Update 1panel-hq (how, what, operations)
       ├── Create deployments/containers/[app-name]/
       ├── Add metadata, docker-compose, scripts
       ├── Create README with procedures
       ├── Run collection script
       └── Update inventory files

3. Back-reference in infrastructure-hq
   └── Update Applications/[App Name].md
       ├── Add link to 1panel-hq documentation
       ├── Record deployment date
       ├── Add health check reference
       └── Link to operational runbooks
```

## Data Synchronization

### What auto-syncs

- **1panel-hq inventory files** → Can be imported to infrastructure-hq periodically
- **Health reports** → Referenced in infrastructure-hq status pages
- **Capacity data** → Used in infrastructure-hq planning
- **Incident logs** → Part of infrastructure-hq incident history

### How to keep in sync

```bash
# From 1panel-hq, export current state
python3 deployments/scripts/collect-1panel-data.py

# Results available in inventory/ directory
# Can be imported to infrastructure-hq as of [date]

# In infrastructure-hq, update status
# Reference: 1panel-hq inventory as of [date]
```

## AI Agent Integration

### For AI Agents

**infrastructure-hq** is the **strategic brain**:
- High-level instructions
- Decision rules
- Constraints and policies
- Learning and history

**1panel-hq** is the **operational executor**:
- Specific configurations
- Scripts and automation
- Current state tracking
- Execution logs

### Agent Workflow

```
1. Agent reads infrastructure-hq
   └── Understands strategic context

2. Agent queries 1panel-hq inventory
   └── Knows current state

3. Agent executes 1panel-hq scripts
   └── Makes changes and collects data

4. Agent reports findings to infrastructure-hq
   └── Updates vault with status and insights

5. Loop: New strategic decisions inform next execution
```

## Access and Permissions

### infrastructure-hq (Obsidian Vault)
- **Local Access**: `~/0-Projects-local/infrastructure-hq/`
- **Tool**: Obsidian
- **Sync**: Local filesystem
- **Backup**: Manual or via Obsidian Sync

### 1panel-hq (GitHub Repository)
- **GitHub Access**: https://github.com/odenizo/1panel-hq
- **Local Clone**: `~/0-Projects-local/1panel-hq/`
- **Permissions**: GitHub team access
- **Backup**: Automatic via GitHub

## Tools and Integration

### infrastructure-hq Consumers
- Obsidian (reading and writing)
- Obsidian Smart Connections (semantic search)
- Obsidian plugins (automation)
- AI agents (reading strategic context)
- Your brain (human decision-making)

### 1panel-hq Consumers
- GitHub (version control)
- GitHub Actions (CI/CD automation)
- Docker (container runtime)
- Python/Bash scripts (automation)
- AI agents (operational execution)
- Monitoring tools (health tracking)

## Relationship Diagram

```
┌─────────────────────────────────────┐
│  infrastructure-hq (Obsidian Vault) │
│     (STRATEGIC MASTER HUB)          │
│                                     │
│  ├─ Architecture & Planning         │
│  ├─ Strategic Decisions             │
│  ├─ Knowledge & Context             │
│  ├─ AI Agent Instructions           │
│  ├─ High-level Procedures           │
│  └─ Disaster Recovery Plans         │
└─────────────────────────────────────┘
            ↕ References
            ↕ Imports Data
            ↕ Exports Instructions
┌─────────────────────────────────────┐
│  1panel-hq (GitHub Repository)      │
│   (OPERATIONAL SUB-COMPONENT)       │
│                                     │
│  ├─ Container Configs               │
│  ├─ Deployment Scripts              │
│  ├─ Monitoring Definitions          │
│  ├─ Operational Runbooks            │
│  ├─ Current State Tracking          │
│  └─ Execution Automation            │
└─────────────────────────────────────┘
            ↕ Provides Data
            ↕ Accepts Instructions
            ↕ Executes Workflows
┌─────────────────────────────────────┐
│  1Panel (Docker Runtime)            │
│   (ACTUAL RUNNING CONTAINERS)       │
│                                     │
│  ├─ PostgreSQL                      │
│  ├─ Redis                           │
│  ├─ Nginx                           │
│  ├─ GitHub Actions Runner           │
│  └─ [Other Apps]                    │
└─────────────────────────────────────┘
```

## Summary

**infrastructure-hq** (Obsidian Vault):
- 🧠 Strategic thinking and planning
- 📚 Knowledge and documentation
- 🎯 Decision-making and policies
- 🤖 AI agent instructions
- 🎨 Big-picture architecture

**1panel-hq** (GitHub Repository):
- ⚙️ Operational execution
- 📦 Deployment configurations
- 📊 Current state tracking
- 🔧 Automation scripts
- 📈 Metrics and reports

**Both Together**:
- ✅ Complete infrastructure management
- ✅ Strategic AND operational
- ✅ Planning AND execution
- ✅ Human judgment AND automation
- ✅ Knowledge AND action

## See Also

- Root `README.md` - 1panel-hq overview
- `docs/AGENT_GUIDE.md` - How agents use this repo
- `infrastructure-hq` vault - Strategic context
- Git history - Change audit trail

---

**This repository is a component of your larger infrastructure management system.**

**Master reference**: infrastructure-hq (Obsidian Vault)  
**Operational hub**: 1panel-hq (GitHub Repository)
