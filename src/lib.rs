use pyo3::prelude::*;
use num_complex::Complex;
use rayon::prelude::*;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;
use log::{info, warn};

struct ProgressData {
    counter: AtomicUsize,
    total: usize,
}

enum QuantumGate {
    PauliX,
    PauliY,
    Hadamard,
    PhaseShift(f64),
}

impl QuantumGate {
    fn apply(&self, z: Complex<f64>) -> Complex<f64> {
        match *self {
            QuantumGate::PauliX => Complex::new(z.im, z.re),
            QuantumGate::PauliY => Complex::new(-z.im, z.re),
            QuantumGate::Hadamard => (Complex::new(z.re, z.re) + Complex::new(z.im, -z.im)) / (2f64).sqrt(),
            QuantumGate::PhaseShift(phase) => Complex::new(z.re, z.im * phase),
        }
    }
}

fn parse_quantum_gate(gate: &str, phase: Option<f64>) -> Result<QuantumGate, PyErr> {
    match gate {
        "pauli_x" => Ok(QuantumGate::PauliX),
        "pauli_y" => Ok(QuantumGate::PauliY),
        "hadamard" => Ok(QuantumGate::Hadamard),
        "phase_shift" => phase.map_or_else(
            || Err(PyErr::new::<pyo3::exceptions::PyValueError, _>("Phase required for phase shift gate")),
            |p| Ok(QuantumGate::PhaseShift(p))
        ),
        _ => Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Unknown quantum gate: {}", gate))),
    }
}

fn complex_fractal_algorithm(z: Complex<f64>, c: Complex<f64>, max_iter: u32, hbar: f64, gate: &QuantumGate) -> u32 {
    let mut z = z;
    let mut iter = 0;

    while iter < max_iter && z.norm() <= 4.0 {
        z = z * z + c / Complex::new(hbar, hbar);
        z = gate.apply(z);
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
    phase_shift: Option<f64>,
    progress_callback: PyObject
) -> PyResult<Vec<Vec<u32>>> {
    let gate = parse_quantum_gate(&quantum_effect_name, phase_shift)?;
    let c = Complex::new(c_real, c_imag);
    let progress_data = Arc::new(ProgressData {
        counter: AtomicUsize::new(0),
        total: width * height,
    });

    let progress_callback_clone = progress_callback.clone();

    let mut fractal = vec![vec![0; width]; height];
    fractal.par_iter_mut().enumerate().for_each(|(y, row)| {
        let progress_data_clone = Arc::clone(&progress_data);
        let gate_clone = gate.clone();  // Clone gate variable
        let progress_callback_clone = progress_callback_clone.clone();  // Clone progress_callback_clone variable
        row.iter_mut().enumerate().for_each(move |(x, pixel)| {
            let zx = x_min + (x_max - x_min) * (x as f64 / width as f64);
            let zy = y_min + (y_max - y_min) * (y as f64 / height as f64);
            let z = Complex::new(zx, zy);

            *pixel = complex_fractal_algorithm(z, c, max_iter, hbar, &gate_clone);
            let progress = progress_data_clone.counter.fetch_add(1, Ordering::Relaxed);
            if progress % (progress_data_clone.total / 10) == 0 {
                Python::with_gil(|py| {
                    progress_callback_clone.call1(py, (progress, progress_data_clone.total)).unwrap_or_else(|e| {
                        warn!("Failed to call progress callback: {:?}", e);
                        e.restore(py);
                        py.None()
                    });
                });
            }
        });
    });

    info!("Fractal generation completed");
    Ok(fractal)
}

#[pymodule]
fn q_julia(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_quantum_fractal, m)?)?;
    Ok(())
}
