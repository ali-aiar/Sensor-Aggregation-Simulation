import os
import unittest

from models.simulation import SimulationModel

class TestSimulationModel(unittest.TestCase):
    def setUp(self):
       self.simulation_model = SimulationModel()

    def test_generate_data(self):
       self.simulation_model.generate_data(1)
       data =self.simulation_model.data['array'][0]
       self.assertIsInstance(data['temperature'], int)
       self.assertIsInstance(data['humidity'], int)
       self.assertIsInstance(data['roomArea'], str)
       self.assertIsInstance(data['timestamp'], int)
       self.assertIsInstance(data['id'], int)
       os.remove(self.simulation_model.file_path)
    
 