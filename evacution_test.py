import unittest
from unittest.mock import patch
from evacuation_planner import EvacuationPlanner

class TestEvacuationPlanner(unittest.TestCase):
    def setUp(self):
        self.planner = EvacuationPlanner('test_config.json')

    def test_load_config(self):
        self.assertIsNotNone(self.planner.config)

    @patch('evacuation_planner.requests.get')
    def test_get_weather_forecast(self, mock_get):
        mock_get.return_value.json.return_value = {'forecast': {'forecastday': [{'day': {'totalprecip_mm': 10}}]}}
        result = self.planner._get_weather_forecast(1)
        self.assertEqual(result['rainfall'], 10)

    # Add more tests for other methods...
    @patch('evacuation_planner.requests.get')
    def test_get_earthquake_data(self, mock_get):
        mock_get.return_value.json.return_value = {
            'features': [
                {'properties': {'mag': 3.5}},
                {'properties': {'mag': 4.2}},
                {'properties': {'mag': 3.8}}
            ]
        }
        result = self.planner._get_earthquake_data()
        self.assertEqual(len(result['features']), 3)
        self.assertEqual(max(f['properties']['mag'] for f in result['features']), 4.2)

    @patch('evacuation_planner.EvacuationPlanner._get_weather_forecast')
    @patch('evacuation_planner.EvacuationPlanner._get_earthquake_data')
    def test_get_real_time_data(self, mock_earthquake, mock_weather):
        mock_weather.return_value = {'rainfall': 50}
        mock_earthquake.return_value = {'features': [{'properties': {'mag': 4.0}}]}
        self.planner._get_real_time_data(1)
        self.assertIn('rainfall', self.planner.region_data)
        self.assertIn('landslide_risk', self.planner.region_data)
        self.assertIn('soil_saturation', self.planner.region_data)
        self.assertIn('slope_angle', self.planner.region_data)

    def test_assess_threat(self):
        self.planner.region_data = {
            'rainfall': [50],
            'landslide_risk': [0.5],
            'soil_saturation': [0.7],
            'slope_angle': [30]
        }
        self.planner._assess_threat()
        self.assertIsNotNone(self.planner.threat_level)
        self.assertTrue(0 <= self.planner.threat_level.max() <= 1)

    def test_identify_affected_areas(self):
        self.planner.threat_level = [0.8, 0.3, 0.6]
        self.planner.region_data = {'population_density': [100, 200, 300]}
        self.planner.config = {'threat_percentile': 50}
        self.planner._identify_affected_areas()
        self.assertIsNotNone(self.planner.affected_areas)
        self.assertEqual(len(self.planner.affected_areas), 3)

    def test_determine_evacuation_routes(self):
        self.planner.affected_areas = [100, 0, 200]
        self.planner.config = {'safe_zones': [[0, 0], [5, 5]]}
        self.planner.region_data = {'road_network': [1, 1, 1]}
        self.planner._determine_evacuation_routes()
        self.assertIsNotNone(self.planner.evacuation_routes)
        self.assertEqual(len(self.planner.evacuation_routes), 2)

    def test_prioritize_evacuations(self):
        self.planner.affected_areas = [100, 0, 200]
        self.planner.threat_level = [0.8, 0.3, 0.6]
        self.planner.region_data = {'vulnerability_index': [0.5, 0.7, 0.9]}
        self.planner._prioritize_evacuations()
        self.assertIsNotNone(self.planner.evacuation_priority)
        self.assertEqual(len(self.planner.evacuation_priority), 3)

    def test_estimate_evacuation_time(self):
        self.planner.evacuation_routes = [((0, 0), (1, 1)), ((2, 2), (3, 3))]
        self.planner.region_data = {
            'population_density': [[100, 200], [300, 400]],
            'road_capacity': [[50, 60], [70, 80]]
        }
        self.planner.config = {'people_per_vehicle': 4}
        self.planner._estimate_evacuation_time()
        self.assertIsNotNone(self.planner.evacuation_time)
        self.assertGreater(self.planner.evacuation_time, 0)

    def test_allocate_resources(self):
        self.planner.evacuation_routes = [((0, 0), (1, 1)), ((2, 2), (3, 3))]
        self.planner.evacuation_priority = [0.8, 0.6]
        self.planner.evacuation_time = 5
        self.planner.region_data = {'available_resources': {'vehicles': 10, 'personnel': 20}}
        self.planner._allocate_resources()
        self.assertIsNotNone(self.planner.resource_allocation)
        self.assertEqual(len(self.planner.resource_allocation), 2)

    def test_generate_plan(self):
        self.planner.threat_level = [0.8, 0.3, 0.6]
        self.planner.affected_areas = [100, 0, 200]
        self.planner.evacuation_routes = [((0, 0), (1, 1)), ((2, 2), (3, 3))]
        self.planner.evacuation_priority = [0.8, 0.6]
        self.planner.evacuation_time = 5
        self.planner.resource_allocation = {0: 10, 1: 20}
        plan = self.planner._generate_plan()
        self.assertIn('threat_level', plan)
        self.assertIn('affected_areas', plan)
        self.assertIn('evacuation_routes', plan)
        self.assertIn('evacuation_priority', plan)
        self.assertIn('evacuation_time', plan)
        self.assertIn('resource_allocation', plan)

    @patch('evacuation_planner.EvacuationPlanner._get_real_time_data')
    @patch('evacuation_planner.EvacuationPlanner._assess_threat')
    @patch('evacuation_planner.EvacuationPlanner._identify_affected_areas')
    @patch('evacuation_planner.EvacuationPlanner._determine_evacuation_routes')
    @patch('evacuation_planner.EvacuationPlanner._prioritize_evacuations')
    @patch('evacuation_planner.EvacuationPlanner._estimate_evacuation_time')
    @patch('evacuation_planner.EvacuationPlanner._allocate_resources')
    def test_plan_evacuation(self, mock_allocate, mock_estimate, mock_prioritize, mock_routes, mock_identify, mock_assess, mock_data):
        plan = self.planner.plan_evacuation(1)
        self.assertIsNotNone(plan)
        mock_data.assert_called_once()
        mock_assess.assert_called_once()
        mock_identify.assert_called_once()
        mock_routes.assert_called_once()
        mock_prioritize.assert_called_once()
        mock_estimate.assert_called_once()
        mock_allocate.assert_called_once()

if __name__ == '__main__':
    unittest.main()
