import os
import json
import random
from statistics import mean, median
from datetime import datetime


class SimulationModel:
    def __init__(self):
        self.next_id = 1
        self.roomArea = ['roomArea1', 'roomArea2', 'roomArea3']
        self.data = {'array': []}
        self.file_path = (os.path.dirname(os.path.dirname(__file__))) + \
            '/data/sensor_data.json'
        f = open(self.file_path, 'a')
        f.close()

    def get_roomArea(self):
        return self.roomArea

    def generate_data(self, id: int):
        id = min(3, max(1, id))
        temperature = random.randint(20, 25)
        humidity = random.randint(50, 60)
        room = self.roomArea[id-1]
        timestamp = int(round(datetime.now().timestamp())*1000)
        id = self.next_id
        self.data['array'].append({'temperature': temperature,
                                   'humidity': humidity,
                                   'roomArea': room,
                                   'id': id,
                                   'timestamp': timestamp})
        self.next_id += 1
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f)

    def aggregate_by_room_and_time(self):
        grouped_data = {}
        grouped_data_array = {self.roomArea[0]: {'timestamp': [],
                                                 'temp_min': [],
                                                 'temp_max': [],
                                                 'temp_median': [],
                                                 'temp_average': [],
                                                 'humid_min': [],
                                                 'humid_max': [],
                                                 'humid_median': [],
                                                 'humid_average': [],
                                                 },
                              self.roomArea[1]: {'timestamp': [],
                                                 'temp_min': [],
                                                 'temp_max': [],
                                                 'temp_median': [],
                                                 'temp_average': [],
                                                 'humid_min': [],
                                                 'humid_max': [],
                                                 'humid_median': [],
                                                 'humid_average': [],
                                                 },
                              self.roomArea[2]: {'timestamp': [],
                                                 'temp_min': [],
                                                 'temp_max': [],
                                                 'temp_median': [],
                                                 'temp_average': [],
                                                 'humid_min': [],
                                                 'humid_max': [],
                                                 'humid_median': [],
                                                 'humid_average': [],
                                                 },
                              }

        for sensor in self.data['array']:
            room = sensor['roomArea']
            timestamp = datetime.fromtimestamp(
                sensor['timestamp'] / 1e3)
            time = timestamp.strftime(
                '%Y-%m-%d\n%H:%M:')+str(timestamp.second//10)+"0"
            key = f"{room}_{time}"
            if key not in grouped_data:
                grouped_data[key] = {
                    'room': room,
                    'time': time,
                    'temperature': [],
                    'humidity': []
                }
            grouped_data[key]['temperature'].append(sensor['temperature'])
            grouped_data[key]['humidity'].append(sensor['humidity'])

        # Calculate min, max, median, and avg for temperature and humidity
        for key in grouped_data:

            grouped_data_array[grouped_data[key]['room']]['timestamp'].append(
                grouped_data[key]['time'])

            grouped_data_array[grouped_data[key]['room']]['temp_min'].append(min(
                grouped_data[key]['temperature']))

            grouped_data_array[grouped_data[key]['room']]['temp_max'].append(max(
                grouped_data[key]['temperature']))

            grouped_data_array[grouped_data[key]['room']]['temp_median'].append(median(
                grouped_data[key]['temperature']))

            grouped_data_array[grouped_data[key]['room']]['temp_average'].append(mean(
                grouped_data[key]['temperature']))

            grouped_data_array[grouped_data[key]['room']]['humid_min'].append(min(
                grouped_data[key]['humidity']))

            grouped_data_array[grouped_data[key]['room']]['humid_max'].append(max(
                grouped_data[key]['humidity']))

            grouped_data_array[grouped_data[key]['room']]['humid_median'].append(median(
                grouped_data[key]['humidity']))

            grouped_data_array[grouped_data[key]['room']]['humid_average'].append(mean(
                grouped_data[key]['humidity']))

        return grouped_data_array
