# 1Panel Deployments

This directory contains all deployment configurations and infrastructure-as-code for managing self-hosted services, including GitHub Actions runners.

## Directory Structure

```
deployments/
├── github-actions-runner/     # Self-hosted GitHub Actions runner
│   ├── docker-compose.yml     # Runner container orchestration
│   ├── .env.example           # Environment variables template
│   ├── Dockerfile             # Custom runner image (optional)
│   ├── start.sh               # Initialization script
│   ├── stop.sh                # Cleanup script
│   └── README.md              # Runner-specific documentation
├── scripts/                   # Data collection & automation scripts
│   ├── collect-1panel-data.py # Main data collector
│   ├── export-config.py       # Config export utility
│   ├── health-check.sh        # System health verification
│   └── requirements.txt       # Python dependencies
└── configs/                   # Configuration templates
    └── runner-labels.json     # Runner label definitions
```

## Quick Start

### Deploy GitHub Actions Runner

```bash
cd deployments/github-actions-runner
cp .env.example .env
# Edit .env with your GitHub org/repo and token
docker-compose up -d
```

### Collect 1Panel Data

```bash
cd deployments/scripts
python3 collect-1panel-data.py --output ../../data/
```

## Prerequisites

- Docker & Docker Compose
- Python 3.9+
- 1Panel instance with API access
- GitHub personal access token (PAT) with `admin:self_hosted_runner` scope

## Usage

All deployment and collection operations are intended to be run from a local clone:

```
~/0-Projects-local/1panel-hq/
```

See individual README files in each subdirectory for detailed instructions.
