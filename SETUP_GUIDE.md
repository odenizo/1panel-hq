# 1Panel-HQ: Complete Setup and Deployment Guide

This guide walks you through setting up the complete 1Panel infrastructure automation system with GitHub Actions runner and data collection.

## Overview

**1panel-hq** is your infrastructure-as-code repository containing:

- **GitHub Actions Self-Hosted Runner** - Deploy your own CI/CD runner on Hetzner
- **1Panel Data Collection Scripts** - Automatically export infrastructure metrics
- **Health Monitoring** - Track system health and service status
- **Configuration Export** - Document and backup your infrastructure state

## Prerequisites

Before starting, ensure you have:

- ✅ A Hetzner Cloud VM with 1Panel installed
- ✅ Docker & Docker Compose installed on the VM
- ✅ SSH access to your Hetzner VM
- ✅ GitHub account with administrative access to your repos/organization
- ✅ Python 3.9+ installed locally
- ✅ Git installed locally

## Step 1: Clone the Repository

```bash
# Clone to your local projects directory
cd ~/0-Projects-local
git clone https://github.com/odenizo/1panel-hq.git
cd 1panel-hq
```

## Step 2: Set Up GitHub Actions Runner

### 2.1 Generate GitHub Personal Access Token (PAT)

1. Visit: https://github.com/settings/tokens/new
2. Name it: `1panel-runner-token`
3. Select these scopes:
   - ✅ `repo` (full control of repositories)
   - ✅ `admin:repo_hook`
   - ✅ `admin:org_hook`
   - ✅ `admin:gpg_key`
   - ✅ `admin:public_key`
   - ✅ `admin:self_hosted_runner`
4. Click "Generate token" and **copy it immediately**

### 2.2 Configure Runner Environment

```bash
cd deployments/github-actions-runner
cp .env.example .env
```

Edit `.env` with your values:

```bash
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  # Your PAT from Step 2.1
GITHUB_OWNER=odenizo                                    # Your username or org
GITHUB_REPOSITORY=                                       # Leave empty for org-level
RUNNER_NAME=runner-hetzner-1
RUNNER_LABELS=hetzner,1panel,self-hosted,linux,docker
RUNNER_EPHEMERAL=false
```

### 2.3 Start the Runner

```bash
# Make scripts executable
chmod +x start.sh stop.sh

# Start the runner
./start.sh
```

Expected output:

```
=== GitHub Actions Runner Startup ===
✓ Configuration loaded
✓ Docker daemon is running
✓ 1panel network exists

=== Runner Started Successfully ===
View logs with:
  docker logs -f github-actions-runner
```

### 2.4 Verify Registration

1. Go to: https://github.com/odenizo/settings/actions/runners
2. You should see `runner-hetzner-1` with status "Idle"
3. Labels should show: `self-hosted`, `linux`, `hetzner`, `1panel`, `docker`

## Step 3: Set Up Data Collection

### 3.1 Install Python Dependencies

```bash
cd deployments/scripts
pip install -r requirements.txt
```

### 3.2 Configure 1Panel API Access

You need your 1Panel API token:

1. Log into your 1Panel instance
2. Navigate to: Settings > API > Create Token
3. Copy the token

Create `.env` file in deployments/scripts:

```bash
echo "PANEL_URL=http://your-1panel-instance:5212" > .env
echo "PANEL_TOKEN=your-1panel-api-token" >> .env
```

### 3.3 Test Data Collection

```bash
cd deployments/scripts
python3 collect-1panel-data.py --verbose
```

Expected output:

```
=== Collecting 1Panel Data ===
Connecting to 1Panel at http://localhost:5212...
✓ Connected successfully

✓ Collected dashboard
✓ Collected websites
✓ Collected databases
✓ Collected ssl_certificates
...
Collection complete: 9/9 successful
```

Data will be saved to: `data/YYYY-MM-DD/`

## Step 4: Set Up Health Monitoring

### 4.1 Run Health Check

```bash
chmod +x deployments/scripts/health-check.sh
deployments/scripts/health-check.sh
```

This will check:
- ✅ Docker daemon status
- ✅ GitHub Actions runner status
- ✅ API connectivity
- ✅ Disk space
- ✅ Memory usage
- ✅ Network connectivity

### 4.2 Export Configuration

```bash
cd deployments/scripts
python3 export-config.py
```

This creates a backup of your:
- Docker Compose configuration
- Docker status and containers
- System information
- Deployment manifest

## Step 5: Automate with GitHub Actions (Optional)

### 5.1 Create Data Collection Workflow

Create `.github/workflows/collect-1panel-data.yml`:

```yaml
name: Collect 1Panel Data

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:       # Manual trigger

jobs:
  collect:
    runs-on: [self-hosted, 1panel]
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r deployments/scripts/requirements.txt
      
      - name: Collect 1Panel data
        env:
          PANEL_URL: ${{ secrets.PANEL_URL }}
          PANEL_TOKEN: ${{ secrets.PANEL_TOKEN }}
        run: |
          cd deployments/scripts
          python3 collect-1panel-data.py --output ../../
      
      - name: Commit and push
        run: |
          git config user.email "runner@1panel-hq"
          git config user.name "1Panel Data Collector"
          git add data/
          git commit -m "chore: Update 1Panel data collection" || true
          git push
```

### 5.2 Add Required Secrets

1. Go to: Repository Settings > Secrets and Variables > Actions
2. Add `PANEL_URL`: `http://your-1panel-instance:5212`
3. Add `PANEL_TOKEN`: Your 1Panel API token

## Directory Structure

After setup, your repository will look like:

```
1panel-hq/
├── deployments/
│   ├── github-actions-runner/
│   │   ├── docker-compose.yml
│   │   ├── .env                  # Created after configuration
│   │   ├── .env.example
│   │   ├── start.sh
│   │   ├── stop.sh
│   │   └── README.md
│   ├── scripts/
│   │   ├── collect-1panel-data.py
│   │   ├── export-config.py
│   │   ├── health-check.sh
│   │   ├── requirements.txt
│   │   └── .env                  # Created after configuration
│   ├── configs/
│   │   └── runner-labels.json
│   └── README.md
├── data/                         # Created after first data collection
│   ├── 2024-01-22/
│   │   ├── dashboard.json
│   │   ├── websites.json
│   │   ├── databases.json
│   │   └── ...
│   └── 2024-01-23/
│       └── ...
├── logs/                         # Created after first health check
│   └── health-check.log
├── .github/
│   └── workflows/
│       ├── collect-1panel-data.yml
│       └── ...
└── SETUP_GUIDE.md
```

## Common Tasks

### Check Runner Status

```bash
docker ps | grep github-actions-runner
```

### View Runner Logs

```bash
docker logs -f github-actions-runner
```

### Stop the Runner

```bash
cd deployments/github-actions-runner
./stop.sh
```

Then remove it from GitHub Settings > Actions > Runners.

### Update Runner

```bash
cd deployments/github-actions-runner
docker-compose pull
docker-compose up -d
```

### Manually Collect 1Panel Data

```bash
cd deployments/scripts
PANEL_URL=http://localhost:5212 \
PANEL_TOKEN=your-token \
python3 collect-1panel-data.py
```

## Troubleshooting

### Runner not appearing in GitHub

1. Check logs: `docker logs github-actions-runner`
2. Verify token is correct in `.env`
3. Ensure GitHub network access is available
4. Check that token has `admin:self_hosted_runner` scope

### Data collection fails

1. Verify 1Panel is running: `docker ps | grep 1panel`
2. Check API token is correct
3. Verify network connectivity: `curl http://localhost:5212/api/dashboard/info`
4. Check firewall rules

### Docker errors

```bash
# Restart Docker daemon
sudo systemctl restart docker

# Add user to docker group (if needed)
sudo usermod -aG docker $USER

# Verify Docker socket
ls -l /var/run/docker.sock
```

## Next Steps

1. ✅ Run your first workflow using `runs-on: [self-hosted, 1panel]`
2. ✅ Set up automated data collection via GitHub Actions
3. ✅ Monitor health status with scheduled health checks
4. ✅ Integrate with your AI tools for intelligent automation
5. ✅ Create custom workflows for your specific needs

## Support & Resources

- [1Panel Documentation](https://1panel.cn/docs/en/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Hetzner Cloud Docs](https://docs.hetzner.cloud/)

## Security Best Practices

1. **Rotate tokens regularly** - Regenerate PAT and 1Panel tokens monthly
2. **Use ephemeral runners** - Set `RUNNER_EPHEMERAL=true` for public repos
3. **Limit runner access** - Use specific labels to control which workflows run where
4. **Monitor logs** - Regularly review runner logs for suspicious activity
5. **Secure secrets** - Never commit `.env` files or tokens
6. **Network security** - Use firewall rules to limit access to 1Panel

## License

MIT
