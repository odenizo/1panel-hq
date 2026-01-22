#!/usr/bin/env python3

"""
1Panel Configuration Export Utility

Exports 1Panel configuration, settings, and deployment details.
Useful for backing up and documenting infrastructure state.
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import subprocess
import logging
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ConfigExporter:
    """Exports 1Panel configuration and deployment state"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.timestamp = datetime.now().isoformat()
        self.config_dir = output_dir / 'configs' / self.timestamp.split('T')[0]
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def export_docker_compose(self, runner_dir: Path):
        """Export GitHub Actions runner Docker Compose configuration"""
        logger.info("Exporting Docker Compose configuration...")
        
        compose_file = runner_dir / 'docker-compose.yml'
        env_file = runner_dir / '.env'
        
        export_data = {
            'timestamp': self.timestamp,
            'docker_compose': {
                'path': str(compose_file),
                'exists': compose_file.exists()
            },
            'environment': {
                'path': str(env_file),
                'exists': env_file.exists(),
                'configured': False
            }
        }
        
        # Check if .env is configured (not just a template)
        if env_file.exists():
            with open(env_file) as f:
                content = f.read()
                export_data['environment']['configured'] = 'ghp_' in content
        
        self._save_json('runner_docker_config', export_data)
        logger.info("✓ Docker Compose config exported")
    
    def export_docker_status(self):
        """Export current Docker status and containers"""
        logger.info("Exporting Docker status...")
        
        try:
            # Get running containers
            result = subprocess.run(
                ['docker', 'ps', '--format', 'json'],
                capture_output=True,
                text=True,
                check=True
            )
            containers = json.loads(f"[{','.join(result.stdout.strip().split(chr(10)))}]") if result.stdout.strip() else []
            
            # Get all containers
            result_all = subprocess.run(
                ['docker', 'ps', '-a', '--format', 'json'],
                capture_output=True,
                text=True,
                check=True
            )
            all_containers = json.loads(f"[{','.join(result_all.stdout.strip().split(chr(10)))}]") if result_all.stdout.strip() else []
            
            # Get networks
            result_networks = subprocess.run(
                ['docker', 'network', 'ls', '--format', 'json'],
                capture_output=True,
                text=True,
                check=True
            )
            networks = json.loads(f"[{','.join(result_networks.stdout.strip().split(chr(10)))}]") if result_networks.stdout.strip() else []
            
            # Get volumes
            result_volumes = subprocess.run(
                ['docker', 'volume', 'ls', '--format', 'json'],
                capture_output=True,
                text=True,
                check=True
            )
            volumes = json.loads(f"[{','.join(result_volumes.stdout.strip().split(chr(10)))}]") if result_volumes.stdout.strip() else []
            
            status = {
                'timestamp': self.timestamp,
                'containers': {
                    'running_count': len(containers),
                    'total_count': len(all_containers),
                    'running': containers,
                    'all': all_containers
                },
                'networks': {
                    'count': len(networks),
                    'networks': networks
                },
                'volumes': {
                    'count': len(volumes),
                    'volumes': volumes
                }
            }
            
            self._save_json('docker_status', status)
            logger.info("✓ Docker status exported")
        
        except subprocess.CalledProcessError as e:
            logger.warning(f"Docker status export failed: {e}")
        except Exception as e:
            logger.error(f"Error exporting Docker status: {e}")
    
    def export_system_info(self):
        """Export system information"""
        logger.info("Exporting system information...")
        
        system_info = {}
        
        # Hostname
        try:
            result = subprocess.run(['hostname'], capture_output=True, text=True, check=True)
            system_info['hostname'] = result.stdout.strip()
        except Exception as e:
            logger.warning(f"Failed to get hostname: {e}")
        
        # Uptime
        try:
            result = subprocess.run(['uptime'], capture_output=True, text=True, check=True)
            system_info['uptime'] = result.stdout.strip()
        except Exception as e:
            logger.warning(f"Failed to get uptime: {e}")
        
        # CPU info
        try:
            result = subprocess.run(['nproc'], capture_output=True, text=True, check=True)
            system_info['cpu_cores'] = int(result.stdout.strip())
        except Exception as e:
            logger.warning(f"Failed to get CPU info: {e}")
        
        # Memory
        try:
            result = subprocess.run(['free', '-h'], capture_output=True, text=True, check=True)
            system_info['memory_info'] = result.stdout
        except Exception as e:
            logger.warning(f"Failed to get memory info: {e}")
        
        # Disk usage
        try:
            result = subprocess.run(['df', '-h'], capture_output=True, text=True, check=True)
            system_info['disk_usage'] = result.stdout
        except Exception as e:
            logger.warning(f"Failed to get disk usage: {e}")
        
        system_info['timestamp'] = self.timestamp
        self._save_json('system_info', system_info)
        logger.info("✓ System information exported")
    
    def export_deployment_manifest(self, runner_dir: Path, scripts_dir: Path):
        """Export deployment manifest"""
        logger.info("Exporting deployment manifest...")
        
        manifest = {
            'timestamp': self.timestamp,
            'deployment_structure': {
                'runner_dir': str(runner_dir),
                'scripts_dir': str(scripts_dir),
                'files': {}
            }
        }
        
        # List runner files
        for file in runner_dir.glob('*'):
            if file.is_file() and not file.name == '.env':
                manifest['deployment_structure']['files'][f"runner/{file.name}"] = {
                    'size': file.stat().st_size,
                    'exists': True
                }
        
        # List script files
        for file in scripts_dir.glob('*.py') | scripts_dir.glob('*.sh'):
            if file.is_file():
                manifest['deployment_structure']['files'][f"scripts/{file.name}"] = {
                    'size': file.stat().st_size,
                    'exists': True
                }
        
        self._save_json('deployment_manifest', manifest)
        logger.info("✓ Deployment manifest exported")
    
    def _save_json(self, name: str, data: Dict[str, Any]):
        """Save data as JSON file"""
        filepath = self.config_dir / f"{name}.json"
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        logger.debug(f"Saved {name} to {filepath}")
    
    def export_all(self, runner_dir: Path, scripts_dir: Path):
        """Export all configuration"""
        logger.info("Starting configuration export...")
        logger.info(f"Output directory: {self.config_dir}")
        
        self.export_docker_compose(runner_dir)
        self.export_docker_status()
        self.export_system_info()
        self.export_deployment_manifest(runner_dir, scripts_dir)
        
        logger.info("\n✓ Configuration export complete")
        logger.info(f"Files saved to: {self.config_dir}")


def main():
    parser = argparse.ArgumentParser(
        description='Export 1Panel and deployment configuration'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path.cwd(),
        help='Output directory (default: current directory)'
    )
    parser.add_argument(
        '--runner-dir',
        type=Path,
        help='Path to github-actions-runner directory'
    )
    parser.add_argument(
        '--scripts-dir',
        type=Path,
        help='Path to scripts directory'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Auto-detect directories if not provided
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent.parent
    
    runner_dir = args.runner_dir or (root_dir / 'deployments' / 'github-actions-runner')
    scripts_dir = args.scripts_dir or (root_dir / 'deployments' / 'scripts')
    
    try:
        exporter = ConfigExporter(args.output)
        exporter.export_all(runner_dir, scripts_dir)
    except Exception as e:
        logger.error(f"Export failed: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
