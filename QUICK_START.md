# 1Panel-HQ: Quick Start (5 minutes)

Fast setup for GitHub Actions runner and 1Panel data collection.

## TL;DR - Just Run This

```bash
# 1. Clone repo
cd ~/0-Projects-local
git clone https://github.com/odenizo/1panel-hq.git
cd 1panel-hq

# 2. Configure runner (edit .env with your GitHub token)
cd deployments/github-actions-runner
cp .env.example .env
# Edit .env - add your GITHUB_TOKEN from https://github.com/settings/tokens
vim .env

# 3. Start runner
chmod +x start.sh stop.sh
./start.sh

# 4. Verify (check GitHub Settings > Actions > Runners)
# You should see runner-hetzner-1 listed as "Idle"

# 5. Configure data collection (edit .env)
cd ../scripts
cp .env.example .env  # Doesn't exist yet, so create it
echo "PANEL_URL=http://localhost:5212" > .env
echo "PANEL_TOKEN=your-1panel-api-token" >> .env

# 6. Test data collection
pip install -r requirements.txt
python3 collect-1panel-data.py --verbose

# Done! Check data/ directory for exported JSON files
```

## What You Need

1. **GitHub Personal Access Token (PAT)**
   - Go to: https://github.com/settings/tokens/new
   - Scopes needed: `repo`, `admin:self_hosted_runner`, etc.
   - Copy the token

2. **1Panel API Token**
   - Log into 1Panel
   - Settings > API > Create Token
   - Copy the token

## Files to Edit

### 1. `deployments/github-actions-runner/.env`

Critical:
```bash
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_OWNER=odenizo
```

Optional (keep defaults):
```bash
GITHUB_REPOSITORY=
RUNNER_NAME=runner-hetzner-1
RUNNER_LABELS=hetzner,1panel,self-hosted,linux,docker
RUNNER_EPHEMERAL=false
```

### 2. `deployments/scripts/.env`

Critical:
```bash
PANEL_URL=http://localhost:5212
PANEL_TOKEN=your-1panel-api-token
```

## Verify Setup

### Runner is registered

https://github.com/odenizo/settings/actions/runners

Should see `runner-hetzner-1` with status "Idle"

### Data is collecting

```bash
ls -la data/
# Should show: 2024-01-22/ with .json files inside
```

### Health check passes

```bash
bash deployments/scripts/health-check.sh
# Should show green checkmarks
```

## Use in Workflows

### Target this runner:

```yaml
jobs:
  build:
    runs-on: [self-hosted, 1panel]
    steps:
      - run: echo "Running on Hetzner with 1Panel!"
```

### Run any command:

```yaml
steps:
  - run: docker ps
  - run: python3 --version
  - run: bash deployments/scripts/health-check.sh
```

## Common Commands

```bash
# View runner logs
docker logs -f github-actions-runner

# Stop runner
cd deployments/github-actions-runner && ./stop.sh

# Restart runner
docker-compose restart

# Collect data manually
cd deployments/scripts
python3 collect-1panel-data.py

# Health check
bash deployments/scripts/health-check.sh

# Export config
python3 export-config.py
```

## Troubleshooting

**Runner not appearing?**
```bash
# Check logs
docker logs github-actions-runner

# Verify token
echo $GITHUB_TOKEN  # Should NOT be empty

# Check network
docker network ls | grep 1panel
```

**Data collection fails?**
```bash
# Test API
curl http://localhost:5212/api/dashboard/info

# Check token
echo $PANEL_TOKEN  # Should NOT be empty

# Test with verbose output
python3 collect-1panel-data.py --verbose
```

**Docker errors?**
```bash
# Restart Docker
sudo systemctl restart docker

# Check Docker
sudo systemctl status docker

# Fix permissions
sudo usermod -aG docker $USER
```

## What This Repo Does

✓ **GitHub Actions Runner**: Self-hosted runner on your Hetzner VM✗ Avoid GitHub minute limits✗ Access your private infrastructure✗ Customize the environment

✓ **Data Collection**: Automatically exports:✗ Dashboard info✗ Websites✗ Databases✗ SSL certificates✗ System status✗ Backups✗ Services✗ Firewall rules✗ Logs

✓ **Health Monitoring**: Track:✗ Docker daemon✗ Runner status✗ API connectivity✗ Disk space✗ Memory usage✗ Network connectivity

✓ **Configuration Export**: Backup your:✗ Docker setup✗ Container state✗ System information✗ Deployment manifest

## Next Steps

1. Automate data collection via GitHub Actions (see SETUP_GUIDE.md)
2. Set up health check alerts
3. Integrate with your AI knowledge management system
4. Create custom workflows for your use case

## See Also

- `SETUP_GUIDE.md` - Detailed setup instructions
- `deployments/README.md` - Architecture overview
- `deployments/github-actions-runner/README.md` - Runner documentation
- `deployments/scripts/` - Script documentation

---

**Status**: Your runner is live after running `./start.sh`

**Next**: Use in workflows with `runs-on: [self-hosted, 1panel]`
