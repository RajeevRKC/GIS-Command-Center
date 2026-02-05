"""
NASA Data Harvester
Unified interface for harvesting all NASA data sources

Usage:
    from nasa_harvester import NASAHarvester
    harvester = NASAHarvester()
    harvester.harvest_all()
"""

import os
import sys
import json
import logging
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict

# Load credentials
sys.path.insert(0, os.path.dirname(__file__))
try:
    from load_env import load_credentials
    load_credentials()
except ImportError:
    pass


class NASAHarvester:
    """Harvest and manage NASA data locally"""

    def __init__(self, data_dir: str = None):
        if data_dir is None:
            data_dir = Path(__file__).parent / "data" / "nasa"
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Load credentials
        self.api_key = os.getenv('NASA_API_KEY', 'DEMO_KEY')
        self.earthdata_token = os.getenv('EARTHDATA_TOKEN')

        # Setup logging
        self._setup_logging()

        # Load/create catalog
        self.catalog_file = self.data_dir / "catalog.json"
        self.catalog = self._load_catalog()

    def _setup_logging(self):
        log_file = self.data_dir / "harvest.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('NASAHarvester')

    def _load_catalog(self) -> Dict:
        if self.catalog_file.exists():
            with open(self.catalog_file) as f:
                return json.load(f)
        return {
            "last_updated": None,
            "sources": {},
            "total_files": 0,
            "total_size_mb": 0
        }

    def _save_catalog(self):
        self.catalog["last_updated"] = datetime.now().isoformat()
        with open(self.catalog_file, 'w') as f:
            json.dump(self.catalog, f, indent=2)

    # ===== APOD Harvesting =====

    def harvest_apod(self, days: int = 7) -> List[Dict]:
        """Harvest recent APOD images"""
        self.logger.info(f"Harvesting APOD for last {days} days")

        output_dir = self.data_dir / "apod"
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        response = requests.get(
            'https://api.nasa.gov/planetary/apod',
            params={
                'api_key': self.api_key,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'thumbs': True
            },
            timeout=30
        )
        response.raise_for_status()
        items = response.json()

        harvested = []
        for item in items:
            date = item['date']
            year, month, _ = date.split('-')

            dir_path = output_dir / year / month
            dir_path.mkdir(parents=True, exist_ok=True)

            # Save metadata
            meta_file = dir_path / f"{date}.json"
            with open(meta_file, 'w') as f:
                json.dump(item, f, indent=2)

            # Download image
            if item.get('media_type') == 'image':
                img_url = item.get('hdurl') or item['url']
                ext = img_url.split('.')[-1].split('?')[0]
                img_file = dir_path / f"{date}.{ext}"

                if not img_file.exists():
                    self.logger.info(f"Downloading: {item['title']}")
                    try:
                        img_data = requests.get(img_url, timeout=60).content
                        with open(img_file, 'wb') as f:
                            f.write(img_data)
                    except Exception as e:
                        self.logger.warning(f"Failed to download {img_url}: {e}")

            harvested.append({
                'date': date,
                'title': item['title'],
                'type': item.get('media_type', 'unknown')
            })

        # Update catalog
        self.catalog['sources']['apod'] = {
            'last_harvest': datetime.now().isoformat(),
            'items_harvested': len(harvested),
            'date_range': [start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')]
        }
        self._save_catalog()

        self.logger.info(f"APOD harvest complete: {len(harvested)} items")
        return harvested

    # ===== Mars Rover Harvesting =====

    def harvest_mars_rover(
        self,
        rover: str = "curiosity",
        sol: Optional[int] = None,
        earth_date: Optional[str] = None,
        camera: Optional[str] = None,
        limit: int = 25
    ) -> List[Dict]:
        """Harvest Mars rover photos"""
        self.logger.info(f"Harvesting {rover} photos")

        output_dir = self.data_dir / "mars" / rover

        params = {'api_key': self.api_key}
        if sol:
            params['sol'] = sol
            output_dir = output_dir / f"sol_{sol}"
        elif earth_date:
            params['earth_date'] = earth_date
            output_dir = output_dir / earth_date.replace('-', '')
        else:
            # Get latest sol from manifest
            try:
                manifest_response = requests.get(
                    f'https://api.nasa.gov/mars-photos/api/v1/manifests/{rover}',
                    params={'api_key': self.api_key},
                    timeout=30
                )
                manifest_response.raise_for_status()
                manifest = manifest_response.json()
                latest_sol = manifest['photo_manifest']['max_sol']
                self.logger.info(f"Latest sol for {rover}: {latest_sol}")
            except Exception as e:
                # Fallback to known recent sols if manifest fails
                self.logger.warning(f"Manifest fetch failed: {e}. Using fallback sol.")
                fallback_sols = {
                    'curiosity': 4100,
                    'perseverance': 1000,
                    'opportunity': 5111,
                    'spirit': 2208
                }
                latest_sol = fallback_sols.get(rover, 1000)
            params['sol'] = latest_sol
            output_dir = output_dir / f"sol_{latest_sol}"

        if camera:
            params['camera'] = camera

        output_dir.mkdir(parents=True, exist_ok=True)

        response = requests.get(
            f'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos',
            params=params,
            timeout=30
        )
        response.raise_for_status()
        photos = response.json()['photos'][:limit]

        harvested = []
        for photo in photos:
            img_url = photo['img_src']
            filename = img_url.split('/')[-1]
            img_file = output_dir / filename

            if not img_file.exists():
                self.logger.info(f"Downloading: {filename}")
                try:
                    img_data = requests.get(img_url, timeout=60).content
                    with open(img_file, 'wb') as f:
                        f.write(img_data)
                except Exception as e:
                    self.logger.warning(f"Failed to download {img_url}: {e}")

            # Save metadata
            meta_file = output_dir / f"{photo['id']}.json"
            with open(meta_file, 'w') as f:
                json.dump(photo, f, indent=2)

            harvested.append({
                'id': photo['id'],
                'camera': photo['camera']['name'],
                'sol': photo['sol'],
                'earth_date': photo['earth_date']
            })

        self.catalog['sources'][f'mars_{rover}'] = {
            'last_harvest': datetime.now().isoformat(),
            'items_harvested': len(harvested)
        }
        self._save_catalog()

        self.logger.info(f"Mars {rover} harvest complete: {len(harvested)} photos")
        return harvested

    # ===== NEO Harvesting =====

    def harvest_neo(self, days: int = 7) -> Dict:
        """Harvest Near Earth Object data"""
        self.logger.info(f"Harvesting NEO data for {days} days")

        output_dir = self.data_dir / "neo" / "weekly"
        output_dir.mkdir(parents=True, exist_ok=True)

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        response = requests.get(
            'https://api.nasa.gov/neo/rest/v1/feed',
            params={
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'api_key': self.api_key
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        # Save weekly digest
        week = end_date.strftime('%Y-W%W')
        output_file = output_dir / f"{week}.json"
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)

        # Extract stats
        stats = {
            'total_count': data['element_count'],
            'potentially_hazardous': 0,
            'closest_approach': None
        }

        closest_distance = float('inf')
        for date, asteroids in data['near_earth_objects'].items():
            for ast in asteroids:
                if ast['is_potentially_hazardous_asteroid']:
                    stats['potentially_hazardous'] += 1

                for approach in ast['close_approach_data']:
                    dist = float(approach['miss_distance']['kilometers'])
                    if dist < closest_distance:
                        closest_distance = dist
                        stats['closest_approach'] = {
                            'name': ast['name'],
                            'distance_km': dist,
                            'date': approach['close_approach_date']
                        }

        self.catalog['sources']['neo'] = {
            'last_harvest': datetime.now().isoformat(),
            'stats': stats
        }
        self._save_catalog()

        self.logger.info(f"NEO harvest complete: {stats['total_count']} objects")
        return stats

    # ===== POWER Climate Data =====

    def harvest_power_climate(
        self,
        lat: float,
        lon: float,
        start: str,
        end: str,
        location_name: str = None
    ) -> Dict:
        """Harvest NASA POWER climate data"""
        self.logger.info(f"Harvesting POWER data for ({lat}, {lon})")

        if not location_name:
            location_name = f"{lat}_{lon}"

        output_dir = self.data_dir / "power" / location_name
        output_dir.mkdir(parents=True, exist_ok=True)

        response = requests.get(
            "https://power.larc.nasa.gov/api/temporal/daily/point",
            params={
                "start": start.replace('-', ''),
                "end": end.replace('-', ''),
                "latitude": lat,
                "longitude": lon,
                "community": "RE",
                "parameters": "T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,ALLSKY_SFC_SW_DWN,WS2M,RH2M",
                "format": "JSON"
            },
            timeout=60
        )
        response.raise_for_status()
        data = response.json()

        # Save data
        output_file = output_dir / f"{start}_{end}.json"
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)

        self.catalog['sources'][f'power_{location_name}'] = {
            'last_harvest': datetime.now().isoformat(),
            'location': {'lat': lat, 'lon': lon},
            'temporal': [start, end]
        }
        self._save_catalog()

        self.logger.info(f"POWER harvest complete for {location_name}")
        return data

    # ===== Full Harvest =====

    def harvest_all(self, include_images: bool = True):
        """Run complete harvest of all configured sources"""
        self.logger.info("Starting full NASA data harvest")

        results = {}

        try:
            results['apod'] = self.harvest_apod(days=7)
        except Exception as e:
            self.logger.error(f"APOD harvest failed: {e}")
            results['apod'] = {'error': str(e)}

        if include_images:
            try:
                results['mars'] = self.harvest_mars_rover(rover='curiosity', limit=10)
            except Exception as e:
                self.logger.error(f"Mars harvest failed: {e}")
                results['mars'] = {'error': str(e)}

        try:
            results['neo'] = self.harvest_neo(days=7)
        except Exception as e:
            self.logger.error(f"NEO harvest failed: {e}")
            results['neo'] = {'error': str(e)}

        self.logger.info("Full harvest complete")
        return results

    def get_catalog_summary(self) -> Dict:
        """Get summary of harvested data"""
        return self.catalog


# CLI Interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='NASA Data Harvester')
    parser.add_argument('--source', choices=['apod', 'mars', 'neo', 'power', 'all'],
                        default='all', help='Data source to harvest')
    parser.add_argument('--days', type=int, default=7, help='Number of days to harvest')
    parser.add_argument('--output', type=str, default=None, help='Output directory')

    args = parser.parse_args()

    harvester = NASAHarvester(args.output)

    if args.source == 'all':
        results = harvester.harvest_all()
    elif args.source == 'apod':
        results = harvester.harvest_apod(days=args.days)
    elif args.source == 'mars':
        results = harvester.harvest_mars_rover()
    elif args.source == 'neo':
        results = harvester.harvest_neo(days=args.days)

    print("\n" + "=" * 50)
    print("HARVEST COMPLETE")
    print("=" * 50)
    print(json.dumps(harvester.get_catalog_summary(), indent=2))
