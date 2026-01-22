# Infrastructure Inventory

This directory contains machine-readable inventories of all deployed infrastructure on 1Panel.

These files serve as the **single source of truth** for:
- What containers are running
- How they communicate
- What resources they use
- How to access them
- What depends on what

## Files in This Directory

### 1. `containers-registry.json`

Master registry of ALL containers deployed on 1Panel.

**Purpose**: Quick reference of what's running, where it is, and what version.

**Used by**:
- Health monitoring scripts
- AI agents querying infrastructure state
- Dependency analysis tools
- Capacity planning reports

**Structure**:
```json
{
  "generated_at": "2024-01-22T03:20:00Z",
  "total_containers": 5,
  "containers": [
    {
      "name": "postgres",
      "status": "running",
      "image": "postgres:15-alpine",
      "version": "15.0",
      "container_id": "abc123def456",
      "type": "database",
      "started_at": "2024-01-20T10:30:00Z",
      "documentation_path": "deployments/containers/postgres/",
      "health_status": "healthy",
      "uptime_seconds": 185723
    },
    {
      "name": "redis",
      "status": "running",
      "image": "redis:7-alpine",
      "version": "7.0",
      "container_id": "def456ghi789",
      "type": "cache",
      "started_at": "2024-01-20T10:31:00Z",
      "documentation_path": "deployments/containers/redis/",
      "health_status": "healthy",
      "uptime_seconds": 185663
    }
  ],
  "summary": {
    "total_running": 5,
    "total_stopped": 0,
    "total_unhealthy": 0,
    "database_containers": 2,
    "application_containers": 1,
    "infrastructure_containers": 2
  }
}
```

### 2. `access-points.json`

All access points to containers (URLs, ports, APIs).

**Purpose**: Know how to reach each service and what credentials to use.

**Used by**:
- Operations teams for manual access
- Health check scripts
- Application deployment configuration
- Security audits

**Structure**:
```json
{
  "generated_at": "2024-01-22T03:20:00Z",
  "access_points": [
    {
      "service": "postgresql",
      "container": "postgres",
      "protocol": "postgresql",
      "host": "localhost",
      "port": 5432,
      "access_methods": [
        "direct_connection_localhost",
        "docker_exec",
        "ssh_tunnel"
      ],
      "credentials_location": "GitHub Secrets: POSTGRES_PASSWORD",
      "default_database": "myapp",
      "default_user": "postgres",
      "connection_string": "postgresql://postgres:***@localhost:5432/myapp",
      "documentation": "deployments/containers/postgres/README.md"
    },
    {
      "service": "redis",
      "container": "redis",
      "protocol": "redis",
      "host": "localhost",
      "port": 6379,
      "access_methods": [
        "direct_connection_localhost",
        "docker_exec"
      ],
      "credentials_location": "GitHub Secrets: REDIS_PASSWORD",
      "connection_string": "redis://:***@localhost:6379",
      "documentation": "deployments/containers/redis/README.md"
    },
    {
      "service": "nginx",
      "container": "nginx",
      "protocol": "http/https",
      "host": "your-domain.com",
      "port": 80,
      "ssl_port": 443,
      "access_methods": [
        "https_browser",
        "curl"
      ],
      "endpoints": [
        "/",
        "/api/v1",
        "/health"
      ],
      "documentation": "deployments/containers/nginx/README.md"
    }
  ]
}
```

### 3. `dependencies-graph.json`

Container dependencies and relationships.

**Purpose**: Understand what depends on what before making changes.

**Used by**:
- Change management procedures
- Scaling decisions
- Disaster recovery planning
- Health check correlations

**Structure**:
```json
{
  "generated_at": "2024-01-22T03:20:00Z",
  "dependencies": [
    {
      "name": "postgres",
      "type": "database",
      "depends_on": [],
      "required_by": [
        "app-backend",
        "data-processor"
      ],
      "startup_order": 1,
      "criticality": "critical"
    },
    {
      "name": "redis",
      "type": "cache",
      "depends_on": [],
      "required_by": [
        "app-backend",
        "session-manager"
      ],
      "startup_order": 1,
      "criticality": "high"
    },
    {
      "name": "app-backend",
      "type": "application",
      "depends_on": [
        "postgres",
        "redis"
      ],
      "required_by": [
        "nginx"
      ],
      "startup_order": 2,
      "criticality": "critical"
    },
    {
      "name": "nginx",
      "type": "reverse_proxy",
      "depends_on": [
        "app-backend"
      ],
      "required_by": [],
      "startup_order": 3,
      "criticality": "critical"
    }
  ],
  "startup_sequence": [
    ["postgres", "redis"],
    ["app-backend"],
    ["nginx"]
  ],
  "shutdown_sequence": [
    ["nginx"],
    ["app-backend"],
    ["redis", "postgres"]
  ]
}
```

### 4. `ports-map.json`

Port allocations and mappings.

**Purpose**: Know which ports are used and avoid conflicts.

**Used by**:
- New deployments (find available ports)
- Network configuration
- Firewall rules
- Documentation

**Structure**:
```json
{
  "generated_at": "2024-01-22T03:20:00Z",
  "total_ports_used": 8,
  "ports": [
    {
      "port": 5432,
      "protocol": "tcp",
      "service": "postgresql",
      "container": "postgres",
      "internal_port": 5432,
      "access_level": "internal_only",
      "firewall_rule": "Allow from localhost only"
    },
    {
      "port": 6379,
      "protocol": "tcp",
      "service": "redis",
      "container": "redis",
      "internal_port": 6379,
      "access_level": "internal_only",
      "firewall_rule": "Allow from localhost only"
    },
    {
      "port": 80,
      "protocol": "tcp",
      "service": "http",
      "container": "nginx",
      "internal_port": 80,
      "access_level": "public",
      "firewall_rule": "Allow from anywhere"
    },
    {
      "port": 443,
      "protocol": "tcp",
      "service": "https",
      "container": "nginx",
      "internal_port": 443,
      "access_level": "public",
      "firewall_rule": "Allow from anywhere"
    }
  ],
  "available_ranges": {
    "internal_services": "5500-5699",
    "applications": "5700-5899",
    "reserved": "5900-5999"
  }
}
```

### 5. `resource-usage.json`

Resource allocations and current usage.

**Purpose**: Understand capacity and plan scaling.

**Used by**:
- Capacity planning
- Performance monitoring
- Cost analysis
- Scaling decisions

**Structure**:
```json
{
  "generated_at": "2024-01-22T03:20:00Z",
  "host_total": {
    "cpu_cores": 8,
    "memory_gb": 32,
    "disk_gb": 500
  },
  "containers": [
    {
      "name": "postgres",
      "cpu": {
        "limit_cores": 2,
        "current_usage_percent": 15,
        "peak_usage_percent": 45
      },
      "memory": {
        "limit_gb": 2,
        "current_usage_gb": 0.8,
        "peak_usage_gb": 1.5
      },
      "disk": {
        "limit_gb": 50,
        "current_usage_gb": 12.3,
        "growth_per_day_gb": 0.5
      }
    },
    {
      "name": "redis",
      "cpu": {
        "limit_cores": 1,
        "current_usage_percent": 5,
        "peak_usage_percent": 20
      },
      "memory": {
        "limit_gb": 1,
        "current_usage_gb": 0.3,
        "peak_usage_gb": 0.7
      },
      "disk": {
        "limit_gb": 10,
        "current_usage_gb": 0.1,
        "growth_per_day_gb": 0
      }
    }
  ],
  "summary": {
    "total_cpu_allocated": 3,
    "total_cpu_available": 8,
    "total_cpu_percent": 37.5,
    "total_memory_allocated_gb": 3,
    "total_memory_available_gb": 32,
    "total_memory_percent": 9.4,
    "total_disk_allocated_gb": 60,
    "total_disk_available_gb": 500,
    "total_disk_percent": 12
  }
}
```

## Maintaining These Files

These files should be **auto-generated** and kept current:

### Manual Generation
```bash
# Collect current state and update inventory files
cd deployments/scripts
python3 collect-1panel-data.py --inventory
```

### Automated Generation
- GitHub Actions workflow runs every 6 hours
- Collects fresh data from 1Panel API
- Updates all inventory files
- Commits changes to repository

### When Making Changes

1. Deploy/modify container to 1Panel
2. Document in `deployments/containers/[app]/`
3. Run inventory collection script
4. Verify inventory files updated correctly
5. Commit changes

## Querying the Inventory

### Find all containers of a type
```bash
jq '.containers[] | select(.type=="database") | .name' inventory/containers-registry.json
```

### Find what depends on postgres
```bash
jq '.dependencies[] | select(.name=="postgres") | .required_by' inventory/dependencies-graph.json
```

### Check available ports
```bash
jq '.ports[] | select(.port > 5000 and .port < 6000) | .port' inventory/ports-map.json
```

### Estimate disk usage in 30 days
```bash
jq '.containers[] | .disk.current_usage_gb + (.disk.growth_per_day_gb * 30)' inventory/resource-usage.json
```

## AI Agent Integration

AI agents read these files to:

1. **Understand infrastructure**: What's running and how it's organized
2. **Make informed decisions**: Dependencies, resources, capacity
3. **Execute operations**: Know ports, credentials, access methods
4. **Generate reports**: Analyze trends, recommend improvements
5. **Prevent conflicts**: Check port usage before new deployments

## Schema Validation

All JSON files should validate against schemas:

```bash
# Validate container registry
python3 -m jsonschema -i inventory/containers-registry.json deployments/configs/container-metadata-schema.json

# Validate all inventory files
bash inventory/validate-all.sh
```

## Version Control

- All files committed to Git
- Changes tracked with timestamps
- Full history available for audits
- Can see how infrastructure evolved over time

## See Also

- [Container documentation](../deployments/containers/README.md)
- [Monitoring definitions](../monitoring/README.md)
- [Data collection scripts](../deployments/scripts/)
- [GitHub Actions workflows](../../automation/workflows/)
