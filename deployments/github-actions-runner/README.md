# GitHub Actions Self-Hosted Runner for 1Panel

This directory contains Docker Compose configuration to deploy a self-hosted GitHub Actions runner on your Hetzner VM managed by 1Panel.

## Overview

A self-hosted runner allows you to:

- Run GitHub Actions workflows on your own infrastructure
- Use custom labels to target specific runners
- Avoid GitHub's runner minute limits
- Access private resources on your network
- Maintain full control over the execution environment

## Quick Start

### 1. Generate GitHub Personal Access Token (PAT)

1. Visit: https://github.com/settings/tokens
2. Click "Generate new token"
3. Select these scopes:
   - `repo` (full control of private repositories)
   - `admin:repo_hook` (access to hooks)
   - `admin:org_hook` (organization hooks)
   - `admin:gpg_key` (GPG key management)
   - `admin:public_key` (public key management)
   - `admin:self_hosted_runner` (self-hosted runner management)
4. Copy the token (you won't see it again)

### 2. Configure Environment

```bash
cd ~/0-Projects-local/1panel-hq/deployments/github-actions-runner
cp .env.example .env
```

Edit `.env` with your values:

```bash
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_OWNER=odenizo          # Your username or org name
GITHUB_REPOSITORY=            # Leave blank for org-level, or specify repo
RUNNER_NAME=runner-hetzner-1  # Unique name for this runner
RUNNER_LABELS=hetzner,1panel,self-hosted,linux,docker
RUNNER_EPHEMERAL=false        # true = auto-cleanup, false = persistent
```

### 3. Start the Runner

```bash
chmod +x start.sh stop.sh
./start.sh
```

The script will:
- Validate your configuration
- Create the Docker network if needed
- Start the runner container
- Display verification instructions

### 4. Verify Registration

Check GitHub Settings > Actions > Runners:
- https://github.com/odenizo/settings/actions/runners (for user account)
- https://github.com/organizations/YOUR_ORG/settings/actions/runners (for organization)

Your runner should appear with status "Idle" within 30 seconds.

### 5. Use in Workflows

In your GitHub Actions workflow YAML:

```yaml
jobs:
  build:
    runs-on: [self-hosted, hetzner, 1panel]
    steps:
      - uses: actions/checkout@v3
      - run: echo "Running on self-hosted Hetzner runner"
```

## File Structure

```
.
├── docker-compose.yml    # Container orchestration configuration
├── .env.example         # Template for environment variables
├── .env                 # (created) Your actual configuration (DO NOT COMMIT)
├── start.sh            # Startup script with validation
├── stop.sh             # Shutdown and cleanup script
└── README.md           # This file
```

## Configuration Details

### Environment Variables

| Variable | Purpose | Example |
|----------|---------|----------|
| `GITHUB_TOKEN` | Auth token for GitHub API | `ghp_xxxxx` |
| `GITHUB_OWNER` | GitHub username or org | `odenizo` or `my-org` |
| `GITHUB_REPOSITORY` | (Optional) Specific repo | `1panel-hq` or empty |
| `RUNNER_NAME` | Display name in GitHub | `runner-hetzner-1` |
| `RUNNER_LABELS` | Comma-separated labels | `hetzner,1panel,docker` |
| `RUNNER_EPHEMERAL` | Auto-cleanup after job | `true` or `false` |
| `RUNNER_WORK_DIRECTORY` | Working directory | `/home/runner` |

### Ephemeral vs. Persistent

**Ephemeral** (`RUNNER_EPHEMERAL=true`):
- Runner self-destructs after each job
- Better for security (clean state)
- Slightly slower (startup overhead)
- Recommended for public repositories

**Persistent** (`RUNNER_EPHEMERAL=false`):
- Runner persists between jobs
- Faster (warm cache, dependencies)
- Better for private infrastructure
- Requires more careful cleanup

## Managing the Runner

### View Logs

```bash
docker logs -f github-actions-runner
```

### Stop the Runner

```bash
./stop.sh
```

Then manually remove it from GitHub Settings > Actions > Runners.

### Restart the Runner

```bash
docker-compose restart
```

### Update Runner Image

```bash
docker-compose pull
docker-compose up -d
```

### Check Runner Status

```bash
docker ps | grep github-actions-runner
```

## Resource Limits

The Docker Compose configuration sets resource limits:

- **CPU Limit**: 4 cores (soft: 2 cores)
- **Memory Limit**: 8GB (soft: 4GB)

Adjust in `docker-compose.yml` based on your Hetzner VM specs:

```yaml
deploy:
  resources:
    limits:
      cpus: '4'
      memory: 8G
    reservations:
      cpus: '2'
      memory: 4G
```

## Docker-in-Docker Support

The runner can build and push Docker images thanks to the mounted socket:

```yaml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock
```

Use in workflows:

```yaml
steps:
  - uses: docker/build-push-action@v4
    with:
      context: .
      push: true
      tags: my-image:latest
```

## Security Considerations

1. **Token Rotation**: Rotate your GitHub PAT periodically
2. **Network Access**: Runner can access resources on your network
3. **Ephemeral Mode**: Consider enabling for public repositories
4. **Logs**: Logs may contain sensitive information (passwords, tokens)
5. **Firewall**: Consider restricting outbound network access if needed

## Troubleshooting

### Runner not appearing in GitHub

```bash
# Check logs
docker logs github-actions-runner

# Verify network
docker network ls

# Check token
echo $GITHUB_TOKEN  # Should not be empty
```

### Network errors

```bash
# Verify 1panel network exists
docker network inspect 1panel

# Recreate if needed
docker network create 1panel
```

### Container won't start

```bash
# Check Docker
sudo systemctl status docker

# Check permissions
sudo usermod -aG docker $USER

# Restart Docker daemon
sudo systemctl restart docker
```

## Limits & Quotas

- **GitHub API Rate Limit**: 5,000 requests/hour (per token)
- **Runner Concurrent Jobs**: 1 per runner instance
- **Job Timeout**: 6 hours (configurable per workflow)

For higher concurrency, deploy multiple runner instances with different `RUNNER_NAME` values.

## Next Steps

1. Run your first workflow using `runs-on: [self-hosted, hetzner]`
2. Monitor logs: `docker logs -f github-actions-runner`
3. Integrate with 1Panel data collection scripts
4. Set up alerts for runner failures

## Support

For issues or questions:

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Self-Hosted Runner Guide](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners)
- [1Panel Documentation](https://1panel.cn/docs/en/)
