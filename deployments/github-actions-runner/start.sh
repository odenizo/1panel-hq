#!/bin/bash

# GitHub Actions Runner Startup Script
# This script initializes and registers a GitHub Actions self-hosted runner on 1Panel

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/.env"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== GitHub Actions Runner Startup ===${NC}"

# Check if .env file exists
if [ ! -f "${ENV_FILE}" ]; then
    echo -e "${RED}Error: .env file not found at ${ENV_FILE}${NC}"
    echo -e "${YELLOW}Please copy .env.example to .env and configure it:${NC}"
    echo "  cp .env.example .env"
    exit 1
fi

# Source environment variables
source "${ENV_FILE}"

# Validate required variables
if [ -z "${GITHUB_TOKEN}" ]; then
    echo -e "${RED}Error: GITHUB_TOKEN not set in .env${NC}"
    exit 1
fi

if [ -z "${GITHUB_OWNER}" ]; then
    echo -e "${RED}Error: GITHUB_OWNER not set in .env${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Configuration loaded${NC}"
echo "  Owner: ${GITHUB_OWNER}"
echo "  Repository: ${GITHUB_REPOSITORY:-org-level}"
echo "  Runner Name: ${RUNNER_NAME}"
echo "  Labels: ${RUNNER_LABELS}"
echo ""

# Create 1panel network if it doesn't exist
echo -e "${YELLOW}Checking Docker network...${NC}"
if ! docker network inspect 1panel >/dev/null 2>&1; then
    echo -e "${YELLOW}Creating 1panel network...${NC}"
    docker network create 1panel
else
    echo -e "${GREEN}✓ 1panel network exists${NC}"
fi

# Check Docker daemon
echo -e "${YELLOW}Checking Docker daemon...${NC}"
if ! docker ps >/dev/null 2>&1; then
    echo -e "${RED}Error: Docker daemon is not running${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker daemon is running${NC}"

# Check if container is already running
if docker ps | grep -q github-actions-runner; then
    echo -e "${YELLOW}Container github-actions-runner is already running${NC}"
    echo "Stop it first with: ./stop.sh"
    exit 1
fi

# Start the runner
echo -e "${YELLOW}Starting GitHub Actions runner...${NC}"
cd "${SCRIPT_DIR}"
docker-compose up -d

echo ""
echo -e "${GREEN}=== Runner Started Successfully ===${NC}"
echo ""
echo "View logs with:"
echo "  docker logs -f github-actions-runner"
echo ""
echo "Verify registration at:"
echo "  https://github.com/${GITHUB_OWNER}/settings/actions/runners"
echo ""
echo "To use this runner in workflows, add to your workflow YAML:"
echo "  runs-on: [self-hosted, hetzner, 1panel]"
echo ""
