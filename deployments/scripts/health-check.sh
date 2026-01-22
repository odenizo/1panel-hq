#!/bin/bash

# 1Panel Health Check Script
# Monitors the health of 1Panel instance and GitHub Actions runner

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
PANEL_URL="${PANEL_URL:-http://localhost:5212}"
RUNNER_URL="${RUNNER_URL:-http://localhost:8000}"
LOG_FILE="${ROOT_DIR}/logs/health-check.log"

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Logging function
log_message() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
}

# Test function
test_endpoint() {
    local name=$1
    local url=$2
    local timeout=5
    
    if curl -sf --max-time $timeout "$url" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} $name: OK"
        log_message "INFO" "$name: OK"
        return 0
    else
        echo -e "${RED}✗${NC} $name: FAILED"
        log_message "ERROR" "$name: FAILED"
        return 1
    fi
}

# Docker health check
check_docker() {
    echo ""
    echo -e "${BLUE}=== Docker Status ===${NC}"
    
    if ! docker ps > /dev/null 2>&1; then
        echo -e "${RED}✗ Docker daemon not running${NC}"
        log_message "ERROR" "Docker daemon not running"
        return 1
    fi
    echo -e "${GREEN}✓ Docker daemon running${NC}"
    
    # Check 1Panel network
    if ! docker network inspect 1panel > /dev/null 2>&1; then
        echo -e "${RED}✗ 1panel network not found${NC}"
        log_message "ERROR" "1panel network not found"
    else
        echo -e "${GREEN}✓ 1panel network exists${NC}"
    fi
    
    # Check GitHub Actions runner
    echo ""
    echo "GitHub Actions Runner:"
    if docker ps | grep -q github-actions-runner; then
        local status=$(docker inspect -f '{{.State.Running}}' github-actions-runner)
        if [ "$status" = "true" ]; then
            echo -e "${GREEN}✓ Running${NC}"
            log_message "INFO" "GitHub Actions runner: Running"
        else
            echo -e "${RED}✗ Not running${NC}"
            log_message "ERROR" "GitHub Actions runner: Not running"
        fi
    else
        echo -e "${YELLOW}⚠ Not deployed${NC}"
        log_message "WARN" "GitHub Actions runner: Not deployed"
    fi
}

# API health checks
check_apis() {
    echo ""
    echo -e "${BLUE}=== API Health ===${NC}"
    
    test_endpoint "1Panel API" "${PANEL_URL}/api/dashboard/info" || true
    test_endpoint "GitHub Actions Runner" "${RUNNER_URL}/status" || true
}

# Disk space check
check_disk() {
    echo ""
    echo -e "${BLUE}=== Disk Space ===${NC}"
    
    local usage=$(df -h / | awk 'NR==2 {print $5}')
    local percent=${usage%\%}
    
    if [ "$percent" -ge 90 ]; then
        echo -e "${RED}✗ Critical: ${usage} used${NC}"
        log_message "ERROR" "Disk usage critical: ${usage}"
    elif [ "$percent" -ge 75 ]; then
        echo -e "${YELLOW}⚠ Warning: ${usage} used${NC}"
        log_message "WARN" "Disk usage high: ${usage}"
    else
        echo -e "${GREEN}✓ OK: ${usage} used${NC}"
        log_message "INFO" "Disk usage: ${usage}"
    fi
}

# Memory check
check_memory() {
    echo ""
    echo -e "${BLUE}=== Memory ===${NC}"
    
    local mem_info=$(free -h | awk 'NR==2')
    local mem_used=$(echo $mem_info | awk '{print $3}')
    local mem_total=$(echo $mem_info | awk '{print $2}')
    
    echo "Used: $mem_used / Total: $mem_total"
    log_message "INFO" "Memory: Used=$mem_used, Total=$mem_total"
}

# Process check
check_processes() {
    echo ""
    echo -e "${BLUE}=== Key Processes ===${NC}"
    
    if pgrep -f docker > /dev/null; then
        echo -e "${GREEN}✓ Docker running${NC}"
    else
        echo -e "${RED}✗ Docker not running${NC}"
    fi
}

# Network connectivity check
check_network() {
    echo ""
    echo -e "${BLUE}=== Network Connectivity ===${NC}"
    
    if ping -c 1 8.8.8.8 > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Internet connectivity: OK${NC}"
        log_message "INFO" "Internet connectivity: OK"
    else
        echo -e "${RED}✗ Internet connectivity: FAILED${NC}"
        log_message "ERROR" "Internet connectivity: FAILED"
    fi
}

# Main
main() {
    echo -e "${BLUE}=== 1Panel Infrastructure Health Check ===${NC}"
    echo "Timestamp: $(date)"
    echo ""
    
    log_message "INFO" "Health check started"
    
    check_docker
    check_apis
    check_disk
    check_memory
    check_processes
    check_network
    
    echo ""
    echo -e "${BLUE}=== Summary ===${NC}"
    echo "Check complete. Review log at: $LOG_FILE"
    echo ""
    
    log_message "INFO" "Health check completed"
}

main
