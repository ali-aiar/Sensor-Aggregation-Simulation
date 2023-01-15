from models.simulation import SimulationModel
from views.simulation_view import Views
from PyQt6.QtWidgets import  QApplication

if __name__ == '__main__':
    simulator = SimulationModel
    app = QApplication([])
    views = Views(simulator)
    views.show()
    app.exec()
