
# Quantum Fractal Generator

The Quantum Fractal Generator is an advanced application that leverages both Python and Rust to generate fractal images using quantum-inspired algorithms. It combines the intuitive graphical user interface (GUI) provided by Python with the high-performance computation capabilities of Rust.

<p align="center">
  <img src="https://github.com/LoQiseaking69/Qjulia/blob/main/ASSETS/IMG_7142.gif" alt="qfrac">
</p>

## Features

- **Quantum Effects**: Apply various quantum-inspired effects to generate fractals, such as Phase Kickback and Quantum Tunneling, along with traditional effects like Pauli X Gate, Pauli Y Gate, Hadamard Gate, and Phase Shift Gate.
- **Color Mapping**: Customize the appearance of fractals with different color maps.
- **Parameter Adjustment**: Interactive sliders to adjust parameters like the complex constant \( c \), \( \hbar \), and fractal boundaries.
- **Real-time Visualization**: Witness the fractal image evolve in real-time as you tweak parameters.
- **Enhanced Performance**: Leverages Rust's performance for efficient and fast fractal computation.
- **Interoperability**: Seamlessly integrates Python and Rust, utilizing the strengths of both languages.

## Requirements

- Python 3.6 or above
- PyQt5
- NumPy
- Matplotlib
- Rust (for running the high-performance backend)

## Installation

1. Clone or download the repository to your local machine.
2. Ensure Rust is installed on your system. If not, install it from [the official Rust website](https://www.rust-lang.org/).
3. Build the Rust library:

   ```bash
   cargo build --release
   ```

4. Setup rust import

    ```bash
    python setup.py install
    ```
5. Install the required Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```
## Usage

Run the application by executing the Python script:

```bash
python QJulia.py
```

Interact with the GUI to generate fractal images using various quantum effects and parameters.

## Screenshots

**Test Output from the Project Notebook**
![Quantum Fractal Generator](https://github.com/LoQiseaking69/Qjulia/blob/main/ASSETS/setx.png)
*Hbar (Quantum Factor): 1.0
Average number of iterations: 2.26
Maximum number of iterations: 20
Standard deviation of iterations: 1.88
Area with high iterations (>80% of max): 0.00
Area with low iterations (<20% of max): 0.80
Quantum Effect Measure: 0.02
Complexity Ratio (High/Low Iterations): 0.00*

**The Test UI from the Project Notebook**
![QUI](https://github.com/LoQiseaking69/Qjulia/blob/main/ASSETS/ScreenShot_2_10_2024_8_18_41_PM.png)

## Contributing

Contributions are highly appreciated! Feel free to submit pull requests or open issues for any enhancements, bug fixes, or feature suggestions.

## License

This project is licensed under the MIT License - see the [LICENSE](/LICENSE) file for details.
