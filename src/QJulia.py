import sys
import os
import ctypes
import threading
from numpy.ctypeslib import ndpointer
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QSlider, QComboBox, QPushButton, QStatusBar, QMessageBox, QTextEdit,
    QProgressBar, QGridLayout
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
from numba import jit
import time

# Function to determine the path to the compiled Rust library
def get_library_path():
    library_name = "QJulia"
    library_file = f"{library_name}.dll"  # Assuming Windows .dll file
    project_root = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(project_root, "target", "release", library_file)

# Load the Rust library
rust_lib_path = get_library_path()
rust_lib = ctypes.CDLL(rust_lib_path)

class FractalWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.width, self.height = 800, 600  # Default fractal image dimensions
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Quantum Fractal Generator')
        self.setGeometry(100, 100, self.width + 200, self.height + 200)

        # Main Layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        main_layout = QHBoxLayout(self.central_widget)

        # Left Panel - Parameters and Controls
        left_panel = QVBoxLayout()
        main_layout.addLayout(left_panel, 1)

        # Quantum Effect Selection
        self.effectCombo = QComboBox()
        self.effectCombo.addItems(["phase_kickback", "quantum_tunneling", "superposition", "pauli_x", "pauli_y", "hadamard", "phase_shift"])
        left_panel.addWidget(self.create_labeled_control("Select Quantum Effect:", self.effectCombo))

        # Parameter Sliders
        self.x_min_slider = self.create_slider(-100, 100, -20, "X Min:")
        self.x_max_slider = self.create_slider(-100, 100, 20, "X Max:")
        self.y_min_slider = self.create_slider(-100, 100, -15, "Y Min:")
        self.y_max_slider = self.create_slider(-100, 100, 15, "Y Max:")
        self.c_real_slider = self.create_slider(-100, 100, -8, "C Real:")
        self.c_imag_slider = self.create_slider(-100, 100, 15, "C Imag:")
        self.max_iter_slider = self.create_slider(1, 10000, 1000, "Max Iterations:")
        self.hbar_slider = self.create_slider(1, 100, 10, "H Bar:")
        for slider in [self.x_min_slider, self.x_max_slider, self.y_min_slider, self.y_max_slider,
                       self.c_real_slider, self.c_imag_slider, self.max_iter_slider, self.hbar_slider]:
            left_panel.addWidget(slider)

        # Generate Button
        self.generateButton = QPushButton("Generate Fractal")
        self.generateButton.clicked.connect(self.startFractalGeneration)
        left_panel.addWidget(self.generateButton)

        # Info Panel
        self.infoPanel = QTextEdit()
        self.infoPanel.setReadOnly(True)
        self.infoPanel.setFixedHeight(100)
        left_panel.addWidget(self.infoPanel)

        # Right Panel - Fractal Display and Toolbar
        right_panel = QVBoxLayout()
        main_layout.addLayout(right_panel, 3)

        # Fractal Display
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        right_panel.addWidget(self.canvas)

        # Adding Navigation Toolbar for zooming and panning
        self.toolbar = NavigationToolbar(self.canvas, self)
        right_panel.addWidget(self.toolbar)

        # Status Bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

    def create_labeled_control(self, label_text, control):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        layout.addWidget(label)
        layout.addWidget(control)
        return layout

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

        return layout

    def update_slider_value(self, label, value, min_val, max_val):
        label.setText(f"{value / 10.0:.1f}")

    def startFractalGeneration(self):
        threading.Thread(target=self.generateFractal, daemon=True).start()

    def generateFractal(self):
        self.progressBar.setValue(0)
        QApplication.processEvents()

        # Retrieve values from sliders and combobox
        x_min = self.x_min_slider.value() / 10.0
        x_max = self.x_max_slider.value() / 10.0
        y_min = self.y_min_slider.value() / 10.0
        y_max = self.y_max_slider.value() / 10.0
        c_real = self.c_real_slider.value() / 10.0
        c_imag = self.c_imag_slider.value() / 10.0
        max_iter = self.max_iter_slider.value()
        hbar = self.hbar_slider.value() / 10.0
        quantum_effect_name = self.effectCombo.currentText()

        # Define function signatures for the Rust library
        rust_lib.generate_quantum_fractal.argtypes = [
            ctypes.c_size_t, ctypes.c_size_t, ctypes.c_double, ctypes.c_double,
            ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double,
            ctypes.c_uint, ctypes.c_double, ctypes.c_char_p
        ]
        rust_lib.generate_quantum_fractal.restype = ndpointer(dtype=ctypes.c_uint, shape=(self.height, self.width))

        start_time = time.time()

        try:
            # Call the Rust function
            fractal = rust_lib.generate_quantum_fractal(
                self.width, self.height, x_min, x_max, y_min, y_max,
                c_real, c_imag, max_iter, hbar, quantum_effect_name.encode('utf-8')
            )

            # Plotting the fractal
            self.figure.clear()
            plt.imshow(fractal, cmap="viridis")  # Using a fixed colormap for simplicity
            plt.colorbar()
            self.canvas.draw()

            end_time = time.time()
            self.infoPanel.append(f"Fractal generated in {end_time - start_time:.2f} seconds.")

            self.progressBar.setValue(100)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            self.statusBar.showMessage("Failed to generate fractal")
            self.progressBar.setValue(0)

def main():
    app = QApplication(sys.argv)
    ex = FractalWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()