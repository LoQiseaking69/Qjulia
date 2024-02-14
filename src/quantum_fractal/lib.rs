use pyo3::prelude::*;
use num_complex::Complex;
use rayon::prelude::*;

#[pyfunction]
fn generate_quantum_fractal(width: usize, height: usize, x_min: f64, x_max: f64, y_min: f64, y_max: f64, c_real: f64, c_imag: f64, max_iter: u32, hbar: f64, quantum_effect_name: String) -> PyResult<Vec<Vec<u32>>> {
    let mut fractal = vec![vec![0; width]; height];

    // Iterate over each pixel in the fractal
    fractal.par_iter_mut().enumerate().for_each(|(y, row)| {
        row.iter_mut().enumerate().for_each(|(x, pixel)| {
            // Convert pixel coordinates to complex number
            let zx = x_min + (x_max - x_min) * (x as f64 / width as f64);
            let zy = y_min + (y_max - y_min) * (y as f64 / height as f64);
            let c = Complex::new(c_real, c_imag);

            // Perform quantum effect calculation
            let mut z = Complex::new(zx, zy);
            let mut iter = 0;
            while iter < max_iter && z.norm() <= 2.0 {
                match quantum_effect_name.as_str() {
                    "phase_kickback" => {
                        z = z * c;
                    }
                    "quantum_tunneling" => {
                        z = z * c + z;
                    }
                    _ => {
                        z = z * z + c;
                    }
                }
                iter += 1;
            }

            // Assign the number of iterations to the pixel
            *pixel = iter;
        });
    });

    Ok(fractal)
}

#[pymodule]
fn quantum_fractal(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_quantum_fractal, m)?)?;
    Ok(())
}
