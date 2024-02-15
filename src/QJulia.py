import sys
import os
import ctypes
import threading
from numpy.ctypeslib import ndpointer
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout,
    QSlider, QComboBox, QPushButton, QStatusBar, QMessageBox, QFileDialog,
    QProgressBar, QToolTip
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)

# Function to determine the path to the compiled Rust library
def get_library_path():
    library_name = "QJulia"
    # For Windows, the compiled library is a .dll file
    library_file = f"{library_name}.dll"
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
        self.setGeometry(100, 100, self.width, self.height + 100)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Quantum Effect Selection
        self.effectLabel = QLabel("Select Quantum Effect:")
        self.layout.addWidget(self.effectLabel)

        self.effectCombo = QComboBox()
        self.effectCombo.addItems(["phase_kickback", "quantum_tunneling", "superposition", "pauli_x", "pauli_y", "hadamard", "phase_shift"])
        self.layout.addWidget(self.effectCombo)

        # Color Map Selection
        self.colorMapLabel = QLabel("Select Color Map:")
        self.layout.addWidget(self.colorMapLabel)

        self.colorMapCombo = QComboBox()
        self.colorMapCombo.addItems(["hot", "viridis", "plasma", "inferno", "magma", "cividis"])
        self.layout.addWidget(self.colorMapCombo)

        # Parameter Sliders
        self.x_min_slider, self.x_min_value = self.create_slider(-100, 100, -20, "X Min:")
        self.x_max_slider, self.x_max_value = self.create_slider(-100, 100, 20, "X Max:")
        self.y_min_slider, self.y_min_value = self.create_slider(-100, 100, -15, "Y Min:")
        self.y_max_slider, self.y_max_value = self.create_slider(-100, 100, 15, "Y Max:")
        self.c_real_slider, self.c_real_value = self.create_slider(-100, 100, -8, "C Real:")
        self.c_imag_slider, self.c_imag_value = self.create_slider(-100, 100, 15, "C Imag:")
        self.max_iter_slider, self.max_iter_value = self.create_slider(1, 10000, 1000, "Max Iterations:")
        self.hbar_slider, self.hbar_value = self.create_slider(1, 100, 10, "H Bar:")

        # Generate Button
        self.generateButton = QPushButton("Generate Fractal")
        self.generateButton.clicked.connect(self.startFractalGeneration)
        self.layout.addWidget(self.generateButton)

        # Progress Bar
        self.progressBar = QProgressBar(self)
        self.layout.addWidget(self.progressBar)

        # Fractal Display
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        # Adding Navigation Toolbar for zooming and panning
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout.addWidget(self.toolbar)

        # Status Bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

    def create_slider(self, min_val, max_val, init_val, label_text):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        layout.addWidget(label)

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(init_val)
        slider.valueChanged.connect(lambda: self.update_slider_value(label, slider.value(), min_val, max_val))
        layout.addWidget(slider)

        value_label = QLabel(f"{init_val / 10.0:.1f}")
        layout.addWidget(value_label)
        return slider, value_label

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
        color_map = self.colorMapCombo.currentText()
        quantum_effect_name = self.effectCombo.currentText()

        # Define function signatures for the Rust library
        rust_lib.generate_quantum_fractal.argtypes = [
            ctypes.c_size_t, ctypes.c_size_t, ctypes.c_double, ctypes.c_double,
            ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double,
            ctypes.c_uint, ctypes.c_double, ctypes.c_char_p
        ]
        rust_lib.generate_quantum_fractal.restype = ndpointer(dtype=ctypes.c_uint, shape=(self.height, self.width))

        try:
            # Call the Rust function
            fractal = rust_lib.generate_quantum_fractal(
                self.width, self.height, x_min, x_max, y_min, y_max,
                c_real, c_imag, max_iter, hbar, quantum_effect_name.encode('utf-8')
            )

            # Plotting the fractal
            self.figure.clear()
            plt.imshow(fractal, cmap=color_map)
            plt.colorbar()
            self.canvas.draw()

            # Save Image Functionality
            save_button = QPushButton("Save Image")
            save_button.clicked.connect(lambda: self.saveFractal(fractal))
            self.layout.addWidget(save_button)

            self.progressBar.setValue(100)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            self.statusBar.showMessage("Failed to generate fractal")
            self.progressBar.setValue(0)

    def saveFractal(self, fractal):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png);;All Files (*)", options=options)
        if fileName:
            plt.imsave(fileName, fractal, cmap=self.colorMapCombo.currentText())

def main():
    app = QApplication(sys.argv)
    ex = FractalWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
