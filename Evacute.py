import numpy as np
from scipy.optimize import linear_sum_assignment
from sklearn.cluster import KMeans

class EvacuationPlanner:
    def __init__(self, region_data):
        self.region_data = region_data
        self.threat_level = None
        self.affected_areas = None
        self.evacuation_routes = None
        self.evacuation_priority = None
        self.evacuation_time = None
        self.resource_allocation = None

    def plan_evacuation(self):
        self._assess_threat()
        self._identify_affected_areas()
        self._determine_evacuation_routes()
        self._prioritize_evacuations()
        self._estimate_evacuation_time()
        self._allocate_resources()
        return self._generate_plan()

    def _assess_threat(self):
        rainfall = self.region_data['rainfall']
        landslide_risk = self.region_data['landslide_risk']
        soil_saturation = self.region_data['soil_saturation']
        slope_angle = self.region_data['slope_angle']

        # Combine factors using a weighted sum
        weights = [0.3, 0.3, 0.2, 0.2]
        factors = [rainfall, landslide_risk, soil_saturation, slope_angle]
        self.threat_level = np.average(factors, weights=weights, axis=0)

    def _identify_affected_areas(self):
        population = self.region_data['population_density']
        threat_threshold = np.percentile(self.threat_level, 70)  # Top 30% most threatened areas
        self.affected_areas = np.where(self.threat_level > threat_threshold, population, 0)

    def _determine_evacuation_routes(self):
        affected_coords = np.argwhere(self.affected_areas > 0)
        safe_zones = self.region_data['safe_zones']
        road_network = self.region_data['road_network']

        def path_cost(start, end):
            # Simplified A* pathfinding
            return np.linalg.norm(end - start) / road_network[tuple(start)]

        routes = []
        for coord in affected_coords:
            safe_zone = min(safe_zones, key=lambda sz: path_cost(coord, sz))
            routes.append((tuple(coord), tuple(safe_zone)))

        self.evacuation_routes = routes

    def _prioritize_evacuations(self):
        vulnerability = self.region_data['vulnerability_index']
        self.evacuation_priority = self.affected_areas * self.threat_level * vulnerability

    def _estimate_evacuation_time(self):
        population = self.region_data['population_density']
        road_capacity = self.region_data['road_capacity']

        total_time = 0
        for start, end in self.evacuation_routes:
            distance = np.linalg.norm(np.array(end) - np.array(start))
            pop_to_evacuate = population[start]
            road_cap = road_capacity[start]
            time = (distance / road_cap) * (pop_to_evacuate / 50)  # Assume 50 people per vehicle
            total_time += time

        self.evacuation_time = total_time

    def _allocate_resources(self):
        n_zones = len(self.evacuation_routes)
        n_resources = sum(self.region_data['available_resources'].values())

        # Create a cost matrix based on priority and time
        cost_matrix = self.evacuation_priority.flatten() / self.evacuation_time

        # Solve the assignment problem
        row_ind, col_ind = linear_sum_assignment(cost_matrix, maximize=True)

        self.resource_allocation = {zone: resources for zone, resources in zip(row_ind, col_ind)}

    def _generate_plan(self):
        return {
            'threat_level': self.threat_level,
            'affected_areas': self.affected_areas,
            'evacuation_routes': self.evacuation_routes,
            'evacuation_priority': self.evacuation_priority,
            'evacuation_time': self.evacuation_time,
            'resource_allocation': self.resource_allocation
        }

# Usage
region_data = {
    'rainfall': np.random.rand(100, 100),
    'landslide_risk': np.random.rand(100, 100),
    'soil_saturation': np.random.rand(100, 100),
    'slope_angle': np.random.rand(100, 100),
    'population_density': np.random.randint(0, 1000, (100, 100)),
    'safe_zones': [(10, 10), (90, 90), (10, 90), (90, 10)],
    'road_network': np.random.rand(100, 100),
    'vulnerability_index': np.random.rand(100, 100),
    'road_capacity': np.random.randint(1, 5, (100, 100)),
    'available_resources': {'vehicles': 100, 'personnel': 500, 'shelters': 10}
}

planner = EvacuationPlanner(region_data)
evacuation_plan = planner.plan_evacuation()