#!/bin/bash

# GitHub Actions Runner Shutdown Script
# Gracefully stops and unregisters the runner from GitHub

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/.env"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== GitHub Actions Runner Shutdown ===${NC}"

# Check if .env file exists
if [ ! -f "${ENV_FILE}" ]; then
    echo -e "${RED}Warning: .env file not found, proceeding with container cleanup only${NC}"
else
    source "${ENV_FILE}"
fi

# Check if container is running
if ! docker ps | grep -q github-actions-runner; then
    echo -e "${YELLOW}Container github-actions-runner is not running${NC}"
    exit 0
fi

echo -e "${YELLOW}Stopping container...${NC}"
cd "${SCRIPT_DIR}"
docker-compose down

echo -e "${GREEN}✓ Container stopped${NC}"
echo ""
echo -e "${BLUE}=== Cleanup Instructions ===${NC}"
echo ""
echo "The runner should now be offline in GitHub. To remove it completely:"
echo ""
echo "1. Go to: https://github.com/GITHUB_OWNER/settings/actions/runners"
echo "   (Replace GITHUB_OWNER with your username or organization)"
echo ""
echo "2. Find the runner named '${RUNNER_NAME}'"
echo ""
echo "3. Click the three dots (...) and select 'Remove'"
echo ""
echo "To clean up volumes (working directory):"
echo "  docker volume rm github-actions-runner-runner-work"
echo ""
