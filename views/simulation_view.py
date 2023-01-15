import sys
import numpy as np

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QFrame, QSpacerItem, QSizePolicy, QPushButton
from PyQt6.QtCore import Qt, QTimer

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from models.simulation import SimulationModel


class Views(QMainWindow):
    def __init__(self, simulator: SimulationModel):
        super().__init__()
        self.setWindowTitle("Sensor Aggregation Simulation")

        self.simulator = simulator()
        self.listRoom = self.simulator.get_roomArea()
        self.roomPosition = 0
        self.roomArea = self.listRoom[self.roomPosition]

        # Create a QTimer object
        self.timer = QTimer()
        self.timer.timeout.connect(self.generate_update)
        self.timer.setInterval(2000)

        main_layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title = QLabel(self.roomArea)
        self.title.setStyleSheet(
            " font-size: 18pt;")
        spaceItem = QSpacerItem(150, 10, QSizePolicy.Policy.Expanding)

        self.button = QPushButton("Start")
        self.button_flag = False
        self.button.setStyleSheet(
            "background-color: #A6BB8D;font-size: 12pt;")
        self.button.clicked.connect(self.start_stop_simulation)

        header_layout.addWidget(self.title)
        header_layout.addSpacerItem(spaceItem)
        header_layout.addWidget(self.button)

        figures_layout = QHBoxLayout()
        figures_layout.setSpacing(35)

        self.fig_temperature = Figure()
        self.ax_temperature = self.fig_temperature.add_subplot()
        self.ax_temperature.grid(True)
        self.ax_temperature.set_xlabel('Timestamp')
        self.ax_temperature.set_xlim(0, 5)

        self.ax_temperature.spines['top'].set_visible(False)
        self.ax_temperature.spines['right'].set_visible(False)
        self.ax_temperature.spines['left'].set_visible(False)

        self.canvas_temperature = FigureCanvas(self.fig_temperature)

        frame_temp = self.create_plot("Temperature", self.canvas_temperature)
        figures_layout.addWidget(frame_temp)

        self.fig_humidity = Figure()
        self.ax_humidity = self.fig_humidity.add_subplot()
        self.ax_humidity.grid(True)
        self.ax_humidity.set_xlabel('Timestamp')
        self.ax_humidity.set_xlim(0, 5)
        self.ax_humidity.spines['top'].set_visible(False)
        self.ax_humidity.spines['right'].set_visible(False)
        self.ax_humidity.spines['left'].set_visible(False)

        self.canvas_humidity = FigureCanvas(self.fig_humidity)

        frame_humidity = self.create_plot("Humidity", self.canvas_humidity)
        figures_layout.addWidget(frame_humidity)

        button_navigate_layout = QHBoxLayout()
        self.buttonNext = QPushButton("Next")
        self.buttonNext.clicked.connect(self.next_navigate)
        self.buttonNext.setEnabled(True)
        self.buttonNext.setStyleSheet(
            "background-color: #A6BB8D;font-size: 12pt;")
        self.buttonBefore = QPushButton("Before")
        self.buttonBefore.clicked.connect(self.before_navigate)
        self.buttonBefore.setEnabled(False)
        self.buttonBefore.setStyleSheet(
            "background-color: #A6BB8D;font-size: 12pt;")

        button_navigate_layout.addWidget(self.buttonBefore)
        button_navigate_layout.addWidget(self.buttonNext)
        button_navigate_layout.setSpacing(35)

        main_layout.addLayout(header_layout)
        main_layout.addLayout(figures_layout)
        main_layout.addLayout(button_navigate_layout)

        self.central_widget = QWidget()
        self.central_widget.setLayout(main_layout)
        self.setCentralWidget(self.central_widget)

    def next_navigate(self):
        self.roomPosition += 1
        self.roomArea = self.listRoom[self.roomPosition]
        self.title.setText(self.roomArea)
        try:
            self.update_plot()
        except AttributeError:
            print("There's no data")
        if self.roomArea == self.listRoom[-1:][0]:
            self.buttonNext.setEnabled(False)
        else:
            self.buttonNext.setEnabled(True)

        if self.roomArea != self.listRoom[0]:
            self.buttonBefore.setEnabled(True)
        ""

    def before_navigate(self):
        self.roomPosition -= 1
        self.roomArea = self.listRoom[self.roomPosition]
        self.title.setText(self.roomArea)
        try:
            self.update_plot()
        except AttributeError:
            print("There's no data")
        if self.roomArea == self.listRoom[0]:
            self.buttonBefore.setEnabled(False)
        else:
            self.buttonBefore.setEnabled(True)

        if self.roomArea != self.listRoom[-1:][0]:
            self.buttonNext.setEnabled(True)
        ""

    def start_stop_simulation(self):
        if self.button_flag:
            self.stop_simulation()
            self.button_flag = False
        else:
            self.start_simulation()
            self.button_flag = True

    def start_simulation(self):
        self.button.setText("Stop")
        self.button.setStyleSheet(
            "background-color: rgba(255, 0, 0, 150);font-size: 12pt;")
        self.timer.start()

    def stop_simulation(self):
        self.button.setText("Start")
        self.button.setStyleSheet(
            "background-color: #A6BB8D;font-size: 12pt;")
        self.timer.stop()

    def generate_update(self):
        # update value
        self.simulator.generate_data(1)
        self.simulator.generate_data(2)
        self.simulator.generate_data(3)
        self.data = self.simulator.aggregate_by_room_and_time()
        self.update_plot()

    def update_plot(self):
        self.ax_temperature.cla()
        self.ax_humidity.cla()

        self.ax_temperature.plot(
            self.data[self.roomArea]['timestamp'][-5:], self.data[self.roomArea]['temp_min'][-5:], label='Min', color='#0099ff')
        self.ax_temperature.plot(
            self.data[self.roomArea]['timestamp'][-5:], self.data[self.roomArea]['temp_max'][-5:], label='Max', color='red')
        self.ax_temperature.plot(
            self.data[self.roomArea]['timestamp'][-5:], self.data[self.roomArea]['temp_median'][-5:], label='Median', color='#ff9900')
        self.ax_temperature.plot(
            self.data[self.roomArea]['timestamp'][-5:],  self.data[self.roomArea]['temp_average'][-5:], label='Average', color='green')
        self.ax_temperature.legend(loc='upper center', bbox_to_anchor=(
            0.5, 1.11), ncol=len(self.ax_temperature.lines), frameon=False)

        temp_min = self.findChild(QLabel, "Temperature_min")
        temp_min.setText("%.0f" % self.data[self.roomArea]['temp_min'][-1:][0])
        temp_max = self.findChild(QLabel, "Temperature_max")
        temp_max.setText("%.0f" % self.data[self.roomArea]['temp_max'][-1:][0])
        temp_median = self.findChild(QLabel, "Temperature_median")
        temp_median.setText("%.0f" %
                            self.data[self.roomArea]['temp_median'][-1:][0])
        temp_average = self.findChild(QLabel, "Temperature_average")
        temp_average.setText(
            "%.0f" % self.data[self.roomArea]['temp_average'][-1:][0])

        self.ax_humidity.plot(
            self.data[self.roomArea]['timestamp'][-5:],  self.data[self.roomArea]['humid_min'][-5:], label='Min', color='#0099ff')
        self.ax_humidity.plot(
            self.data[self.roomArea]['timestamp'][-5:], self.data[self.roomArea]['humid_max'][-5:], label='Max', color='red')
        self.ax_humidity.plot(
            self.data[self.roomArea]['timestamp'][-5:], self.data[self.roomArea]['humid_median'][-5:], label='Median', color='#ff9900')
        self.ax_humidity.plot(
            self.data[self.roomArea]['timestamp'][-5:], self.data[self.roomArea]['humid_average'][-5:], label='Average', color='green')
        self.ax_humidity.legend(loc='upper center', bbox_to_anchor=(
            0.5, 1.11), ncol=len(self.ax_humidity.lines), frameon=False)

        humid_min = self.findChild(QLabel, "Humidity_min")
        humid_min.setText("%.0f" %
                          self.data[self.roomArea]['humid_min'][-1:][0])
        humid_max = self.findChild(QLabel, "Humidity_max")
        humid_max.setText("%.0f" %
                          self.data[self.roomArea]['humid_max'][-1:][0])
        humid_median = self.findChild(QLabel, "Humidity_median")
        humid_median.setText(
            "%.0f" % self.data[self.roomArea]['humid_median'][-1:][0])
        humid_average = self.findChild(QLabel, "Humidity_average")
        humid_average.setText(
            "%.0f" % self.data[self.roomArea]['humid_average'][-1:][0])

        self.canvas_temperature.draw()
        self.canvas_humidity.draw()

    def create_plot(self, plot_name: str, canvas):
        frame = QFrame()
        frame.setObjectName("frameWidget")
        frame.setStyleSheet(
            "QFrame#frameWidget {border: 2px solid black; background-color: white;}")

        # create plot title name
        title_figure = QLabel(plot_name)
        title_figure.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_figure.setContentsMargins(0, 0, 0, 0)
        title_figure.setStyleSheet(
            "background-color: #cacaca; font-size: 16pt; border-bottom: 2px solid black")

        self.status_layout = QHBoxLayout()
        status_min = QLabel(str(0))
        status_min.setObjectName(plot_name+"_min")
        status_min.setStyleSheet(
            "QLabel {background-color: rgba(0, 153, 255, 150); font-size: 20pt;}")
        status_min.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_min.setFixedWidth(75)
        status_min.setFixedHeight(55)

        status_max = QLabel(str(0))
        status_max.setObjectName(plot_name+"_max")
        status_max.setStyleSheet(
            "QLabel {background-color: rgba(255, 0, 0, 150);font-size: 20pt;}")
        status_max.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_max.setFixedWidth(75)
        status_max.setFixedHeight(55)

        status_median = QLabel(str(0))
        status_median.setObjectName(plot_name+"_median")
        status_median.setStyleSheet(
            "QLabel {background-color: rgba(255, 153, 0, 150);font-size: 20pt;}")
        status_median.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_median.setFixedWidth(75)
        status_median.setFixedHeight(55)

        status_average = QLabel(str(0))
        status_average.setObjectName(plot_name+"_average")
        status_average.setStyleSheet(
            "QLabel {background-color: #A6BB8D;font-size: 20pt;}")
        status_average.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_average.setFixedWidth(75)
        status_average.setFixedHeight(55)

        self.status_layout.addWidget(status_min)
        self.status_layout.addWidget(status_max)
        self.status_layout.addWidget(status_median)
        self.status_layout.addWidget(status_average)
        self.status_layout.setSpacing(40)
        self.status_layout.setContentsMargins(0, 0, 0, 0)
        self.status_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_name_layout = QHBoxLayout()
        status_name_min = QLabel("Min")
        status_name_min.setStyleSheet(
            "QLabel {color: rgb(0, 153, 255);; font-size: 10pt;}")
        status_name_min.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_name_min.setFixedWidth(75)

        status_name_max = QLabel("Max")
        status_name_max.setStyleSheet(
            "QLabel {color: rgb(255, 0, 0);font-size: 10pt;}")
        status_name_max.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_name_max.setFixedWidth(75)

        status_name_median = QLabel("Median")
        status_name_median.setStyleSheet(
            "QLabel {color: rgb(255, 153, 0);font-size: 10pt;}")
        status_name_median.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_name_median.setFixedWidth(75)

        status_name_average = QLabel("Average")
        status_name_average.setStyleSheet(
            "QLabel {color: green; font-size: 10pt;}")
        status_name_average.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_name_average.setFixedWidth(75)

        self.status_name_layout.addWidget(status_name_min)
        self.status_name_layout.addWidget(status_name_max)
        self.status_name_layout.addWidget(status_name_median)
        self.status_name_layout.addWidget(status_name_average)
        self.status_name_layout.setSpacing(40)
        self.status_name_layout.setContentsMargins(0, 0, 0, 0)
        self.status_name_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create Layout for canvas
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 15)
        layout.addWidget(title_figure)
        layout.addWidget(canvas)
        layout.addLayout(self.status_layout)
        layout.addLayout(self.status_name_layout)

        frame.setLayout(layout)
        return frame
