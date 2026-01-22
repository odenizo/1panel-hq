#!/usr/bin/env python3

"""
1Panel Comprehensive Data Collector

Collects infrastructure data from 1Panel API and saves to repository.
Supports multiple output formats (JSON, YAML, CSV).
"""

import os
import sys
import json
import yaml
import requests
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class CollectionResult:
    """Result of data collection"""
    timestamp: str
    endpoint: str
    status: int
    data_count: int
    success: bool
    error: Optional[str] = None

class OnePanel:
    """1Panel API client"""
    
    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url.rstrip('/')
        self.api_token = api_token
        self.headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """GET request to 1Panel API"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for {endpoint}: {e}")
            raise
    
    def get_dashboard(self) -> Dict[str, Any]:
        """Get dashboard information"""
        logger.info("Fetching dashboard information...")
        return self.get('/api/dashboard/info')
    
    def get_websites(self) -> Dict[str, Any]:
        """Get website listings"""
        logger.info("Fetching websites...")
        return self.get('/api/websites')
    
    def get_databases(self) -> Dict[str, Any]:
        """Get database information"""
        logger.info("Fetching databases...")
        return self.get('/api/databases')
    
    def get_ssl_certificates(self) -> Dict[str, Any]:
        """Get SSL certificate information"""
        logger.info("Fetching SSL certificates...")
        return self.get('/api/ssl')
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        logger.info("Fetching system information...")
        return self.get('/api/system/info')
    
    def get_backups(self) -> Dict[str, Any]:
        """Get backup information"""
        logger.info("Fetching backup information...")
        return self.get('/api/backups')
    
    def get_services(self) -> Dict[str, Any]:
        """Get running services"""
        logger.info("Fetching services...")
        return self.get('/api/services')
    
    def get_firewall(self) -> Dict[str, Any]:
        """Get firewall rules"""
        logger.info("Fetching firewall rules...")
        return self.get('/api/firewall')
    
    def get_logs(self, limit: int = 100) -> Dict[str, Any]:
        """Get system logs"""
        logger.info(f"Fetching logs (limit: {limit})...")
        return self.get('/api/logs', params={'limit': limit})


class DataCollector:
    """Collects data from 1Panel and saves to repository"""
    
    def __init__(self, panel: OnePanel, output_dir: Path):
        self.panel = panel
        self.output_dir = output_dir
        self.timestamp = datetime.now().isoformat()
        self.results: List[CollectionResult] = []
        
        # Create output directory structure
        self.data_dir = output_dir / 'data' / self.timestamp.split('T')[0]
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def collect_all(self) -> bool:
        """Collect all data from 1Panel"""
        logger.info(f"Starting comprehensive data collection")
        logger.info(f"Output directory: {self.data_dir}")
        
        collectors = [
            ('dashboard', self.panel.get_dashboard),
            ('websites', self.panel.get_websites),
            ('databases', self.panel.get_databases),
            ('ssl_certificates', self.panel.get_ssl_certificates),
            ('system_info', self.panel.get_system_info),
            ('backups', self.panel.get_backups),
            ('services', self.panel.get_services),
            ('firewall', self.panel.get_firewall),
            ('logs', self.panel.get_logs),
        ]
        
        success_count = 0
        for name, collector in collectors:
            try:
                data = collector()
                self.save_data(name, data)
                success_count += 1
                logger.info(f"✓ Collected {name}")
            except Exception as e:
                logger.error(f"✗ Failed to collect {name}: {e}")
        
        self.save_summary()
        logger.info(f"\nCollection complete: {success_count}/{len(collectors)} successful")
        return success_count == len(collectors)
    
    def save_data(self, name: str, data: Dict[str, Any], format: str = 'json'):
        """Save collected data to file"""
        filename = f"{name}.{format}"
        filepath = self.data_dir / filename
        
        try:
            if format == 'json':
                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=2, default=str)
            elif format == 'yaml':
                with open(filepath, 'w') as f:
                    yaml.dump(data, f, default_flow_style=False)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            logger.debug(f"Saved {name} to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save {name}: {e}")
            raise
    
    def save_summary(self):
        """Save collection summary"""
        summary = {
            'timestamp': self.timestamp,
            'collection_date': self.timestamp.split('T')[0],
            'collection_time': self.timestamp.split('T')[1],
            'status': 'complete',
            'results': [
                asdict(result) for result in self.results
            ]
        }
        
        summary_file = self.data_dir / 'collection_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Summary saved to {summary_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Collect comprehensive data from 1Panel instance'
    )
    parser.add_argument(
        '--url',
        default=os.getenv('PANEL_URL', 'http://localhost:5212'),
        help='1Panel API URL (default: http://localhost:5212)'
    )
    parser.add_argument(
        '--token',
        default=os.getenv('PANEL_TOKEN'),
        help='1Panel API token (required, can set PANEL_TOKEN env var)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=os.getenv('OUTPUT_DIR', Path.cwd()),
        help='Output directory for collected data (default: current directory)'
    )
    parser.add_argument(
        '--format',
        choices=['json', 'yaml'],
        default='json',
        help='Output format (default: json)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    if not args.token:
        logger.error("Error: PANEL_TOKEN not provided")
        logger.error("Provide via --token flag or PANEL_TOKEN environment variable")
        sys.exit(1)
    
    try:
        # Initialize 1Panel client
        panel = OnePanel(args.url, args.token)
        
        # Test connection
        logger.info(f"Connecting to 1Panel at {args.url}...")
        panel.get_dashboard()
        logger.info("✓ Connected successfully")
        
        # Collect data
        collector = DataCollector(panel, args.output)
        success = collector.collect_all()
        
        sys.exit(0 if success else 1)
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
