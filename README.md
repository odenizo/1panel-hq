# 1panel-hq: Central Management Hub for 1Panel Infrastructure

**1panel-hq** is a comprehensive **coding agent hub** for managing, operating, monitoring, and automating 1Panel and all deployed containers/applications on your Hetzner infrastructure.

This repository serves as the **single source of truth** for:
- All deployed container documentation
- Deployment configurations and orchestration
- Data collection and monitoring scripts
- Health checks and system audits
- Infrastructure automation workflows
- AI-driven operations and intelligence

## 🎯 Purpose

Provide a centralized, version-controlled, AI-friendly repository to:

1. **Inventory** all containers and applications running on 1Panel
2. **Document** deployment configurations, dependencies, and access points
3. **Automate** routine operations (backups, updates, data collection)
4. **Monitor** system health, performance, and security
5. **Manage** via GitHub Actions workflows (CI/CD for infrastructure)
6. **Integrate** with AI agents for intelligent automation and decision-making
7. **Audit** changes, deployments, and configuration drift
8. **Backup** critical configurations and state snapshots

## 📋 Repository Structure

```
1panel-hq/
├── deployments/                          # All deployment configurations
│   ├── README.md                        # Deployments overview
│   ├── github-actions-runner/           # GitHub Actions runner
│   │   ├── docker-compose.yml
│   │   ├── .env.example
│   │   ├── start.sh / stop.sh
│   │   └── README.md
│   ├── containers/                      # (NEW) Inventory of all deployed containers
│   │   ├── README.md                     # How to document containers
│   │   ├── app-name/                    # One directory per app/container
│   │   │   ├── metadata.json             # App info, ports, dependencies
│   │   │   ├── docker-compose.yml        # Deployment config
│   │   │   ├── env.example               # Environment variables
│   │   │   ├── README.md                 # Usage and management
│   │   │   ├── backups/                  # Backup configs
│   │   │   └── scripts/                  # App-specific scripts
│   │   ├── postgres/
│   │   ├── redis/
│   │   ├── nginx/
│   │   └── [other-apps]/
│   ├── scripts/                         # Shared automation scripts
│   │   ├── collect-1panel-data.py
│   │   ├── export-config.py
│   │   ├── health-check.sh
│   │   └── requirements.txt
│   ├── configs/                         # Configuration templates
│   │   ├── runner-labels.json
│   │   └── container-metadata-schema.json
│   └── orchestration/                   # Multi-container workflows
│       ├── docker-compose-full.yml
│       ├── scaling.yml
│       └── dependencies.yml
├── inventory/                           # (NEW) Infrastructure inventory
│   ├── containers-registry.json         # Master list of all containers
│   ├── ports-map.json                   # Port allocations
│   ├── dependencies-graph.json          # Container dependencies
│   ├── access-points.json               # URLs, APIs, credentials
│   └── resource-usage.json              # CPU, memory, disk allocations
├── monitoring/                          # (NEW) Monitoring and health
│   ├── README.md
│   ├── health-checks/                   # Per-app health definitions
│   │   ├── postgres.yaml
│   │   ├── redis.yaml
│   │   └── [app].yaml
│   ├── dashboards/                      # Monitoring configs
│   │   ├── grafana-dashboards.json
│   │   └── prometheus-alerts.yml
│   ├── alerts/                          # Alert definitions
│   │   ├── critical-failures.yaml
│   │   └── resource-warnings.yaml
│   └── logs/                            # Log aggregation
├── operations/                          # (NEW) Operational procedures
│   ├── README.md
│   ├── runbooks/                        # Step-by-step guides
│   │   ├── backup-strategy.md
│   │   ├── disaster-recovery.md
│   │   ├── upgrade-procedures.md
│   │   ├── scaling-guide.md
│   │   └── troubleshooting.md
│   ├── maintenance/                     # Maintenance tasks
│   │   ├── daily-checks.sh
│   │   ├── weekly-maintenance.sh
│   │   └── monthly-audit.sh
│   └── scripts/                         # Operational scripts
│       ├── backup-all.sh
│       ├── update-all.sh
│       ├── restart-all.sh
│       └── status-report.sh
├── automation/                          # (NEW) AI-driven automation
│   ├── README.md
│   ├── workflows/                       # GitHub Actions workflows
│   │   ├── daily-health-check.yml
│   │   ├── collect-infrastructure-data.yml
│   │   ├── backup-strategy.yml
│   │   ├── auto-update-check.yml
│   │   ├── security-audit.yml
│   │   └── capacity-planning.yml
│   ├── ai-agents/                       # AI agent instructions
│   │   ├── infrastructure-agent.md
│   │   ├── monitoring-agent.md
│   │   ├── remediation-agent.md
│   │   └── capacity-planner-agent.md
│   ├── python-runners/                  # Python automation
│   │   ├── container-optimizer.py
│   │   ├── dependency-analyzer.py
│   │   └── cost-analyzer.py
│   └── triggers/                        # Automation triggers
├── data/                                # (AUTO-GENERATED) Collected data
│   ├── snapshots/                       # Point-in-time snapshots
│   │   ├── 2024-01-22/
│   │   └── 2024-01-23/
│   ├── reports/                         # Generated reports
│   │   ├── health-report-2024-01-22.json
│   │   ├── capacity-report-2024-01-22.json
│   │   └── security-audit-2024-01-22.json
│   ├── metrics/                         # Time-series metrics
│   │   ├── cpu-usage.csv
│   │   ├── memory-usage.csv
│   │   └── disk-usage.csv
│   └── logs/                            # Aggregated logs
├── .github/workflows/                   # GitHub Actions workflows
│   ├── daily-health-check.yml
│   ├── collect-infrastructure-data.yml
│   ├── backup-strategy.yml
│   └── security-audit.yml
├── docs/                                # Documentation
│   ├── SETUP_GUIDE.md
│   ├── QUICK_START.md
│   ├── ARCHITECTURE.md
│   ├── AGENT_GUIDE.md                   # How AI agents use this repo
│   ├── API_REFERENCE.md
│   └── TROUBLESHOOTING.md
├── .gitignore
├── SETUP_GUIDE.md
├── QUICK_START.md
└── README.md (this file)
```

## 🚀 Core Features

### 1. **Container Inventory & Documentation**
- Master registry of all deployed containers
- Metadata for each container (ports, dependencies, health checks)
- Access points and API documentation
- Port allocation tracking
- Dependency graphs

### 2. **Deployment Management**
- Docker Compose configurations for each app
- Standardized deployment structure
- Environment variable templates
- Backup and restore procedures
- Multi-container orchestration

### 3. **Monitoring & Health**
- Health checks for each container/app
- System resource tracking
- Performance baselines
- Alert definitions
- Dashboard configurations

### 4. **Operations**
- Runbooks for common tasks
- Maintenance scripts
- Backup/restore strategies
- Upgrade procedures
- Troubleshooting guides

### 5. **Automation**
- GitHub Actions workflows for routine tasks
- AI agent instructions and integration points
- Python automation runners
- Trigger systems
- Self-healing procedures

### 6. **Data Collection & Reporting**
- Automated infrastructure snapshots
- Health reports
- Capacity planning reports
- Security audit reports
- Metrics aggregation

## 📊 Key Use Cases

### For Human Operators
- **Quick reference**: Find any container's documentation, access points, and status
- **Troubleshooting**: Use runbooks and scripts to diagnose and fix issues
- **Backup/Recovery**: Follow documented procedures for data safety
- **Scaling**: Understand dependencies before making changes
- **Compliance**: Audit all changes through Git history

### For AI Agents
- **Intelligent Monitoring**: Understand system state, correlate issues
- **Automated Remediation**: Execute healing procedures automatically
- **Capacity Planning**: Analyze trends and predict needs
- **Security Scanning**: Audit configurations and detect anomalies
- **Optimization**: Recommend and apply efficiency improvements

### For CI/CD Workflows
- **Scheduled Health Checks**: Daily/weekly automated health audits
- **Data Collection**: Periodic snapshots of infrastructure state
- **Backup Strategy**: Automated backup execution and verification
- **Compliance Reporting**: Generate audit reports automatically
- **Alert Management**: Automated incident creation and notification

## 🔄 Workflow Example

```
1. Container deployed to 1Panel
   ↓
2. Document in deployments/containers/[app-name]/
   - metadata.json
   - docker-compose.yml
   - README.md
   ↓
3. Register in inventory/containers-registry.json
   ↓
4. Create health checks in monitoring/health-checks/[app].yaml
   ↓
5. Add to GitHub Actions workflow for automation
   ↓
6. AI agents can now:
   - Monitor health
   - Execute operations
   - Recommend improvements
   - Handle incidents
```

## 🤖 AI Agent Integration

This repository is designed for AI agents to:

1. **Read** container documentation and current state
2. **Understand** dependencies and relationships
3. **Query** health status and metrics
4. **Execute** defined operations and scripts
5. **Analyze** trends and recommend actions
6. **Automate** routine tasks via GitHub Actions
7. **Report** findings and changes back to repo

See `docs/AGENT_GUIDE.md` for detailed integration instructions.

## 🔒 Security & Governance

- Git audit trail for all changes
- Environment-specific configurations
- Secret management via GitHub Secrets
- Role-based access via GitHub teams
- Compliance reporting and audits
- Configuration drift detection

## 📚 Getting Started

1. **New to this repo?** Start with [QUICK_START.md](QUICK_START.md)
2. **Want to add a container?** See [deployments/containers/README.md](deployments/containers/README.md)
3. **Setting up from scratch?** Follow [SETUP_GUIDE.md](SETUP_GUIDE.md)
4. **Using AI agents?** Read [docs/AGENT_GUIDE.md](docs/AGENT_GUIDE.md)
5. **Need operational procedures?** Check [operations/runbooks/](operations/runbooks/)

## 🎓 Key Concepts

### Containers vs Deployments
- **Deployments** = How to run (docker-compose, configs, scripts)
- **Containers** = Specific instances running on 1Panel
- **Inventory** = Current state of what's running
- **Monitoring** = Health and performance tracking

### Data vs Configuration
- **Configuration** = How things should be (source of truth in Git)
- **Data** = Current snapshots and metrics (auto-generated, in /data/)
- **Artifacts** = Logs, reports, backups

## 🔗 Quick Links

- [Container Inventory](inventory/containers-registry.json) - Master list
- [Access Points](inventory/access-points.json) - URLs and APIs
- [Health Checks](monitoring/health-checks/) - Status definitions
- [Runbooks](operations/runbooks/) - How-to guides
- [GitHub Actions](automation/workflows/) - Automated tasks
- [AI Integration](docs/AGENT_GUIDE.md) - Agent instructions

## 📝 Contributing

When adding new containers or making changes:

1. Document in `deployments/containers/[app]/`
2. Add to `inventory/containers-registry.json`
3. Create health checks if applicable
4. Update dependency graphs
5. Add to appropriate GitHub Actions workflow
6. Create PR with clear description

## 📈 Repository Statistics

- **Deployed Containers**: [count from inventory]
- **Documented Apps**: [count from /containers]
- **Automated Workflows**: [count from .github/workflows]
- **Monitored Services**: [count from health-checks]
- **Runbooks**: [count from operations/runbooks]

## 🤝 Support

For questions or issues:

1. Check [operations/runbooks/troubleshooting.md](operations/runbooks/troubleshooting.md)
2. Review container-specific README in `deployments/containers/[app]/`
3. Check GitHub Issues for known problems
4. Review health reports in `data/reports/`

---

**This repository is the central hub for all 1Panel infrastructure management, automation, and intelligence.**
