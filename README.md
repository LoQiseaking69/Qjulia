# Quantum Fractal Generator

The Quantum Fractal Generator is an application that allows users to generate fractal images using quantum-inspired algorithms. It provides a graphical user interface (GUI) for users to interactively select parameters and visualize the resulting fractals.

## Features

- **Quantum Effects**: Apply various quantum effects to generate fractals, including Pauli X Gate, Pauli Y Gate, Hadamard Gate, and Phase Shift Gate.
- **Color Mapping**: Choose from different color maps to customize the appearance of the fractals.
- **Parameter Adjustment**: Use sliders to adjust parameters such as the complex constant \( c \), \( \hbar \), and the boundaries of the fractal.
- **Real-time Visualization**: See the fractal image update in real-time as parameters are adjusted.
- **Performance**: Utilize multithreading for efficient fractal computation and visualization.
- **Quantum Circuit Visualization**: Explore the quantum circuit corresponding to the selected quantum effect.

## Requirements

- Python 3.6 or above
- PyQt5
- NumPy
- Matplotlib
- Numba
- Qiskit (for quantum circuit visualization)

## Installation

1. Clone or download the repository to your local machine.
2. Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

Run the application by executing the following command in your terminal:

```bash
python quantum_fractal_generator.py
```

Once the application window opens, you can interact with the GUI to generate fractal images with different quantum effects and parameters.

## Screenshots
**test Output from the project notebook**
![Quantum Fractal Generator](https://github.com/LoQiseaking69/Qjulia/blob/main/Qjulia.png)
*Hbar (Quantum Factor): 1.0
Average number of iterations: 2.26
Maximum number of iterations: 20
Standard deviation of iterations: 1.88
Area with high iterations (>80% of max): 0.00
Area with low iterations (<20% of max): 0.80
Quantum Effect Measure: 0.02
Complexity Ratio (High/Low Iterations): 0.00*

**the test UI from the project notebook**
![QUI](https://github.com/LoQiseaking69/Qjulia/blob/main/ASSETS/ScreenShot_2_10_2024_8_18_41_PM.png)

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues for any bugs or feature requests.

## License

This project is licensed under the MIT License - see the [LICENSE](/LICENSE) file for details.
