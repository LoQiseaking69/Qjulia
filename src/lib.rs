use pyo3::prelude::*;
use num_complex::Complex;
use rayon::prelude::*;

// Function to apply Pauli-X Gate
fn apply_pauli_x(z: Complex<f64>) -> Complex<f64> {
    Complex::new(z.im, z.re)
}

// Function to apply Pauli-Y Gate
fn apply_pauli_y(z: Complex<f64>) -> Complex<f64> {
    Complex::new(-z.im, z.re)
}

// Function to apply Hadamard Gate
fn apply_hadamard(z: Complex<f64>) -> Complex<f64> {
    (Complex::new(z.re, z.re) + Complex::new(z.im, -z.im)) / (2f64).sqrt()
}

// Function to apply Phase Shift Gate
fn apply_phase_shift(z: Complex<f64>, phase: f64) -> Complex<f64> {
    Complex::new(z.re, z.im * phase)
}

// The main function to generate quantum fractal
#[pyfunction]
fn generate_quantum_fractal(
    width: usize, height: usize, 
    x_min: f64, x_max: f64, 
    y_min: f64, y_max: f64, 
    c_real: f64, c_imag: f64, 
    max_iter: u32, hbar: f64, 
    quantum_effect_name: String
) -> PyResult<Vec<Vec<u32>>> {
    let mut fractal = vec![vec![0; width]; height];

    fractal.par_iter_mut().enumerate().for_each(|(y, row)| {
        row.iter_mut().enumerate().for_each(|(x, pixel)| {
            let zx = x_min + (x_max - x_min) * (x as f64 / width as f64);
            let zy = y_min + (y_max - y_min) * (y as f64 / height as f64);
            let c = Complex::new(c_real, c_imag);

            let mut z = Complex::new(zx, zy);
            let mut iter = 0;

            while iter < max_iter && z.norm() <= 2.0 {
                z = match quantum_effect_name.as_str() {
                    "phase_kickback" => z * c,
                    "quantum_tunneling" => z * c + z,
                    "superposition" => z * z + c / Complex::new(hbar, hbar),
                    "pauli_x" => apply_pauli_x(z),
                    "pauli_y" => apply_pauli_y(z),
                    "hadamard" => apply_hadamard(z),
                    "phase_shift" => apply_phase_shift(z, hbar),
                    _ => z * z + c, // Default case for unknown effects
                };
                iter += 1;
            }

            *pixel = iter;
        });
    });

    Ok(fractal)
}

// Module initialization
#[pymodule]
fn quantum_fractal(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_quantum_fractal, m)?)?;
    Ok(())
}
