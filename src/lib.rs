use pyo3::prelude::*;
use num_complex::Complex;
use rayon::prelude::*;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;
use log::{info, error};

fn apply_gate(z: Complex<f64>, gate: &str, phase: f64) -> PyResult<Complex<f64>> {
    match gate {
        "pauli_x" => Ok(Complex::new(z.im, z.re)),
        "pauli_y" => Ok(Complex::new(-z.im, z.re)),
        "hadamard" => Ok((Complex::new(z.re, z.re) + Complex::new(z.im, -z.im)) / (2f64).sqrt()),
        "phase_shift" => Ok(Complex::new(z.re, z.im * phase)),
        _ => {
            let err_msg = format!("Unknown quantum gate: {}", gate);
            error!("{}", err_msg);
            Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(err_msg))
        }
    }
}

fn complex_fractal_algorithm(z: Complex<f64>, c: Complex<f64>, max_iter: u32, hbar: f64, quantum_effect: &str) -> u32 {
    let mut z = z;
    let mut iter = 0;

    while iter < max_iter && z.norm() <= 4.0 {
        z = match quantum_effect {
            "phase_kickback" => z * c,
            "quantum_tunneling" => z * c + z,
            "superposition" => z * z + c / Complex::new(hbar, hbar),
            _ => match apply_gate(z, quantum_effect, hbar) {
                Ok(val) => val,
                Err(err) => {
                    error!("{}", err);
                    return 0; // or any other appropriate value indicating failure
                }
            }
        };
        iter += 1;
    }

    iter
}

#[pyfunction]
fn generate_quantum_fractal(
    width: usize, height: usize,
    x_min: f64, x_max: f64,
    y_min: f64, y_max: f64,
    c_real: f64, c_imag: f64,
    max_iter: u32, hbar: f64,
    quantum_effect_name: String,
) -> PyResult<Vec<Vec<u32>>> {
    info!("Starting fractal generation");
    let c = Complex::new(c_real, c_imag);
    let mut fractal = vec![vec![0; width]; height];
    let counter = Arc::new(AtomicUsize::new(0));

    let quantum_effect_name_arc = Arc::new(quantum_effect_name);

    fractal.par_iter_mut().enumerate().for_each(|(y, row)| {
        let counter_clone = Arc::clone(&counter);
        let quantum_effect_name = Arc::clone(&quantum_effect_name_arc);
        row.iter_mut().enumerate().for_each(move |(x, pixel)| {
            let zx = x_min + (x_max - x_min) * (x as f64 / width as f64);
            let zy = y_min + (y_max - y_min) * (y as f64 / height as f64);
            let z = Complex::new(zx, zy);

            *pixel = complex_fractal_algorithm(z, c, max_iter, hbar, &quantum_effect_name);
            counter_clone.fetch_add(1, Ordering::Relaxed);
        });
    });

    let total_iterations = counter.load(Ordering::Relaxed);
    info!("Fractal generation completed. Total iterations: {}", total_iterations);

    Ok(fractal)
}

#[pymodule]
fn q_julia(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_quantum_fractal, m)?)?;
    Ok(())
}