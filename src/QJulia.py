import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QSlider, QComboBox, QPushButton, QStatusBar, QMessageBox, QTextEdit,
    QProgressBar
)
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
import time
import threading
import subprocess
from ctypes import cdll, c_void_p, CFUNCTYPE, c_uint, POINTER

# Constants
MIN_VAL = -100
MAX_VAL = 100
INIT_VAL_X_MIN = -20
INIT_VAL_X_MAX = 20
INIT_VAL_Y_MIN = -15
INIT_VAL_Y_MAX = 15
INIT_VAL_C_REAL = -8
INIT_VAL_C_IMAG = 15
INIT_VAL_MAX_ITER = 1000
INIT_VAL_HBAR = 10

class FractalWindow(QMainWindow):
    update_status_signal = pyqtSignal(str)
    fractal_generated_signal = pyqtSignal(np.ndarray, float)

    def __init__(self):
        super().__init__()
        self.width, self.height = 800, 600
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Quantum Fractal Generator')
        self.setGeometry(100, 100, self.width + 200, self.height + 200)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        main_layout = QHBoxLayout(self.central_widget)

        left_panel = QVBoxLayout()
        main_layout.addLayout(left_panel)

        self.effectCombo = QComboBox()
        self.effectCombo.addItems(["phase_kickback", "quantum_tunneling", "superposition", "pauli_x", "pauli_y", "hadamard", "phase_shift"])
        left_panel.addWidget(self.create_labeled_control("Select Quantum Effect:", self.effectCombo))

        self.x_min_slider = self.create_slider(MIN_VAL, MAX_VAL, INIT_VAL_X_MIN, "X Min:")
        left_panel.addWidget(self.x_min_slider['container_widget'])
        self.x_max_slider = self.create_slider(MIN_VAL, MAX_VAL, INIT_VAL_X_MAX, "X Max:")
        left_panel.addWidget(self.x_max_slider['container_widget'])
        self.y_min_slider = self.create_slider(MIN_VAL, MAX_VAL, INIT_VAL_Y_MIN, "Y Min:")
        left_panel.addWidget(self.y_min_slider['container_widget'])
        self.y_max_slider = self.create_slider(MIN_VAL, MAX_VAL, INIT_VAL_Y_MAX, "Y Max:")
        left_panel.addWidget(self.y_max_slider['container_widget'])
        self.c_real_slider = self.create_slider(MIN_VAL, MAX_VAL, INIT_VAL_C_REAL, "C Real:")
        left_panel.addWidget(self.c_real_slider['container_widget'])
        self.c_imag_slider = self.create_slider(MIN_VAL, MAX_VAL, INIT_VAL_C_IMAG, "C Imag:")
        left_panel.addWidget(self.c_imag_slider['container_widget'])
        self.max_iter_slider = self.create_slider(1, 10000, INIT_VAL_MAX_ITER, "Max Iterations:")
        left_panel.addWidget(self.max_iter_slider['container_widget'])
        self.hbar_slider = self.create_slider(1, 100, INIT_VAL_HBAR, "H Bar:")
        left_panel.addWidget(self.hbar_slider['container_widget'])

        self.generateButton = QPushButton("Generate Fractal")
        self.generateButton.clicked.connect(self.startFractalGeneration)
        left_panel.addWidget(self.generateButton)

        self.progressBar = QProgressBar()
        left_panel.addWidget(self.progressBar)

        self.infoPanel = QTextEdit()
        self.infoPanel.setReadOnly(True)
        self.infoPanel.setFixedHeight(100)
        left_panel.addWidget(self.infoPanel)

        right_panel = QVBoxLayout()
        main_layout.addLayout(right_panel)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        right_panel.addWidget(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas, self)
        right_panel.addWidget(self.toolbar)
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        self.update_status_signal.connect(self.updateStatusBar)
        self.fractal_generated_signal.connect(self.displayFractal)

    def create_labeled_control(self, label_text, control):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        layout.addWidget(label)
        layout.addWidget(control)
        container_widget = QWidget()
        container_widget.setLayout(layout)
        return container_widget

    def create_slider(self, min_val, max_val, init_val, label_text):
        layout = QVBoxLayout()
        label = QLabel(label_text)
        layout.addWidget(label)
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(init_val)
        slider.valueChanged.connect(lambda: self.update_slider_value(label, slider.value(), min_val, max_val))
        layout.addWidget(slider)
        container_widget = QWidget()
        container_widget.setLayout(layout)
        return {'slider': slider, 'container_widget': container_widget}

    def update_slider_value(self, label, value, min_val, max_val):
        label.setText(f"{value / 10.0:.1f}")

    @pyqtSlot(str)
    def updateStatusBar(self, message):
        self.statusBar.showMessage(message)

    @pyqtSlot(np.ndarray, float)
    def displayFractal(self, fractal, generation_time):
        self.figure.clear()
        plt.imshow(fractal, cmap="viridis")
        plt.colorbar()
        self.canvas.draw()
        self.infoPanel.append(f"Fractal generated in {generation_time:.2f} seconds.")
        self.progressBar.setValue(100)

    def startFractalGeneration(self):
        threading.Thread(target=self.generateFractal, daemon=True).start()

    def generateFractal(self):
        self.update_status_signal.emit("Generating fractal...")
        QApplication.processEvents()

        try:
            x_min = self.x_min_slider['slider'].value() / 10.0
            x_max = self.x_max_slider['slider'].value() / 10.0
            y_min = self.y_min_slider['slider'].value() / 10.0
            y_max = self.y_max_slider['slider'].value() / 10.0
            c_real = self.c_real_slider['slider'].value() / 10.0
            c_imag = self.c_imag_slider['slider'].value() / 10.0
            max_iter = self.max_iter_slider['slider'].value()
            hbar = self.hbar_slider['slider'].value() / 10.0
            quantum_effect_name = self.effectCombo.currentText()

            start_time = time.time()

            self.build_rust_dll()
            dir_path = os.path.dirname(os.path.realpath(__file__))
            lib = cdll.LoadLibrary(os.path.join(dir_path, "target", "release", "libq_julia.dll"))

            lib.generate_quantum_fractal.argtypes = [c_uint, c_uint, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_uint, c_void_p, c_void_p]
            lib.generate_quantum_fractal.restype = POINTER(c_uint)

            generate_quantum_fractal = CFUNCTYPE(POINTER(c_uint), c_uint, c_uint, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_uint, c_void_p, c_void_p)(lib.generate_quantum_fractal)

            fractal_ptr = generate_quantum_fractal(
                self.width, self.height, x_min, x_max, y_min, y_max,
                c_real, c_imag, max_iter, hbar, quantum_effect_name.encode()
            )

            end_time = time.time()
            fractal_array = np.ctypeslib.as_array(fractal_ptr, shape=(self.height, self.width))
            self.fractal_generated_signal.emit(fractal_array, end_time - start_time)

        except Exception as e:
            self.handleFractalError(e)

    def handleFractalError(self, error):
        QMessageBox.critical(self, "Error", f"An error occurred: {error}")
        self.update_status_signal.emit("Failed to generate fractal")
        self.progressBar.setValue(0)

    def build_rust_dll(self):
        try:
            subprocess.run(["cargo", "build", "--release"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            self.handleBuildError(e)

    def handleBuildError(self, error):
        QMessageBox.critical(self, "Error", f"An error occurred while building the Rust DLL: {error}")
        self.update_status_signal.emit("Failed to generate fractal")
        self.progressBar.setValue(0)

def main():
    app = QApplication(sys.argv)
    ex = FractalWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()