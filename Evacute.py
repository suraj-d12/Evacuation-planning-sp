import numpy as np
import logging
from typing import Dict, Any, List, Tuple
from scipy.optimize import linear_sum_assignment
from sklearn.cluster import KMeans
import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import json
from pathlib import Path

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EvacuationPlanner:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.region_data = {}
        self.threat_level = None
        self.affected_areas = None
        self.evacuation_routes = None
        self.evacuation_priority = None
        self.evacuation_time = None
        self.resource_allocation = None

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        try:
            with open(config_path, 'r') as config_file:
                return json.load(config_file)
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise

    def _get_real_time_data(self, days_ahead: int) -> None:
        try:
            weather_data = self._get_weather_forecast(days_ahead)
            earthquake_data = self._get_earthquake_data()
            
            rainfall = weather_data['rainfall']
            soil_saturation = min(1.0, rainfall / self.config['max_rainfall'])
            landslide_risk = min(1.0, (rainfall / self.config['max_rainfall'] + soil_saturation) / 2)
            
            max_magnitude = max([feature['properties']['mag'] for feature in earthquake_data['features']], default=0)
            slope_instability = min(1.0, max_magnitude / self.config['max_earthquake_magnitude'])

            self.region_data.update({
                'rainfall': np.full(self.config['grid_size'], rainfall),
                'landslide_risk': np.full(self.config['grid_size'], landslide_risk),
                'soil_saturation': np.full(self.config['grid_size'], soil_saturation),
                'slope_angle': np.full(self.config['grid_size'], slope_instability)
            })
            logger.info(f"Real-time data updated for {days_ahead} days ahead")
        except Exception as e:
            logger.error(f"Error getting real-time data: {e}")
            raise

    def _get_weather_forecast(self, days_ahead: int) -> Dict[str, float]:
        api_key = os.getenv('WEATHER_API_KEY')
        if not api_key:
            raise ValueError("Weather API key not found in environment variables")

        endpoint = f"https://api.weatherapi.com/v1/forecast.json?key={api_key}&q={self.config['location']}&days={days_ahead}&aqi=no"
        
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            data = response.json()
            forecast_day = data['forecast']['forecastday'][days_ahead - 1]['day']
            return {'rainfall': forecast_day['totalprecip_mm']}
        except requests.RequestException as e:
            logger.error(f"Error fetching weather data: {e}")
            raise

    def _get_earthquake_data(self) -> Dict[str, Any]:
        end_time = datetime.now()
        start_time = end_time - timedelta(days=self.config['earthquake_lookback_days'])
        
        params = {
            "format": "geojson",
            "starttime": start_time.isoformat(),
            "endtime": end_time.isoformat(),
            "latitude": self.config['latitude'],
            "longitude": self.config['longitude'],
            "maxradiuskm": self.config['earthquake_radius_km']
        }
        
        try:
            response = requests.get(self.config['earthquake_api_endpoint'], params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching earthquake data: {e}")
            raise

    def _assess_threat(self) -> None:
        try:
            factors = [self.region_data[factor] for factor in self.config['threat_factors']]
            weights = self.config['threat_assessment_weights']

            if len(weights) != len(factors):
                raise ValueError("Number of weights must match number of factors")

            self.threat_level = np.average(factors, weights=weights, axis=0)
            logger.info(f"Threat assessment completed. Max threat level: {np.max(self.threat_level)}")
        except Exception as e:
            logger.error(f"Error in threat assessment: {e}")
            raise

    def _identify_affected_areas(self) -> None:
        try:
            population = self.region_data['population_density']
            threat_threshold = np.percentile(self.threat_level, self.config['threat_percentile'])
            self.affected_areas = np.where(self.threat_level > threat_threshold, population, 0)
            logger.info(f"Affected areas identified. Total affected population: {np.sum(self.affected_areas)}")
        except Exception as e:
            logger.error(f"Error identifying affected areas: {e}")
            raise

    def _determine_evacuation_routes(self) -> None:
        try:
            affected_coords = np.argwhere(self.affected_areas > 0)
            safe_zones = self.config['safe_zones']
            road_network = self.region_data['road_network']

            routes = []
            for coord in affected_coords:
                safe_zone = min(safe_zones, key=lambda sz: self._path_cost(coord, sz, road_network))
                routes.append((tuple(coord), tuple(safe_zone)))

            self.evacuation_routes = routes
            logger.info(f"Evacuation routes determined. Total routes: {len(routes)}")
        except Exception as e:
            logger.error(f"Error determining evacuation routes: {e}")
            raise

    def _path_cost(self, start: np.ndarray, end: np.ndarray, road_network: np.ndarray) -> float:
        return np.linalg.norm(end - start) / road_network[tuple(start)]

    def _prioritize_evacuations(self) -> None:
        try:
            vulnerability = self.region_data['vulnerability_index']
            self.evacuation_priority = self.affected_areas * self.threat_level * vulnerability
            logger.info(f"Evacuations prioritized. Max priority: {np.max(self.evacuation_priority)}")
        except Exception as e:
            logger.error(f"Error prioritizing evacuations: {e}")
            raise

    def _estimate_evacuation_time(self) -> None:
        try:
            population = self.region_data['population_density']
            road_capacity = self.region_data['road_capacity']

            total_time = 0
            for start, end in self.evacuation_routes:
                distance = np.linalg.norm(np.array(end) - np.array(start))
                pop_to_evacuate = population[start]
                road_cap = road_capacity[start]
                time = (distance / road_cap) * (pop_to_evacuate / self.config['people_per_vehicle'])
                total_time += time

            self.evacuation_time = total_time
            logger.info(f"Evacuation time estimated: {self.evacuation_time} hours")
        except Exception as e:
            logger.error(f"Error estimating evacuation time: {e}")
            raise

    def _allocate_resources(self) -> None:
        try:
            n_zones = len(self.evacuation_routes)
            n_resources = sum(self.region_data['available_resources'].values())

            cost_matrix = self.evacuation_priority.flatten() / self.evacuation_time

            row_ind, col_ind = linear_sum_assignment(cost_matrix, maximize=True)

            self.resource_allocation = {zone: resources for zone, resources in zip(row_ind, col_ind)}
            logger.info(f"Resources allocated. Total resources: {n_resources}")
        except Exception as e:
            logger.error(f"Error allocating resources: {e}")
            raise

    def _generate_plan(self) -> Dict[str, Any]:
        return {
            'threat_level': self.threat_level.tolist(),
            'affected_areas': self.affected_areas.tolist(),
            'evacuation_routes': self.evacuation_routes,
            'evacuation_priority': self.evacuation_priority.tolist(),
            'evacuation_time': float(self.evacuation_time),
            'resource_allocation': self.resource_allocation
        }

    def plan_evacuation(self, days_ahead: int) -> Dict[str, Any]:
        try:
            self._get_real_time_data(days_ahead)
            self._assess_threat()
            self._identify_affected_areas()
            self._determine_evacuation_routes()
            self._prioritize_evacuations()
            self._estimate_evacuation_time()
            self._allocate_resources()
            plan = self._generate_plan()
            logger.info(f"Evacuation plan generated for {days_ahead} days ahead")
            return plan
        except Exception as e:
            logger.error(f"Error in evacuation planning: {e}")
            raise

def main():
    config_path = Path("config.json")
    planner = EvacuationPlanner(config_path)

    time_frames = [10, 6, 2, 0]  # 0 represents the day of the disaster
    plans = {}

    for days_ahead in time_frames:
        try:
            plan = planner.plan_evacuation(days_ahead)
            plans[days_ahead] = plan
            logger.info(f"Plan generated for {days_ahead} days ahead")
        except Exception as e:
            logger.error(f"Failed to generate plan for {days_ahead} days ahead: {e}")

    # Here you would typically save or transmit the plans
    # For demonstration, we'll just print a summary
    for days, plan in plans.items():
        print(f"\nSummary for {days} days ahead:")
        print(f"Max threat level: {np.max(plan['threat_level'])}")
        print(f"Total affected population: {np.sum(plan['affected_areas'])}")
        print(f"Number of evacuation routes: {len(plan['evacuation_routes'])}")
        print(f"Estimated evacuation time: {plan['evacuation_time']} hours")

if __name__ == "__main__":
    main()