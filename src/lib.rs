use pyo3::prelude::*;
use pyo3::Py;

mod engine;
mod io;

#[pyfunction]
#[pyo3(signature = (input, where_expr, select=None, output=None))]
fn filter_py(input: String, where_expr: String, select: Option<Vec<String>>, output: Option<String>) -> PyResult<String> {
    engine::filter_to_path(&input, &where_expr, select.as_ref(), output.as_deref())
        .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e.to_string()))
}

#[pyfunction]
#[pyo3(signature = (input, columns, output=None))]
fn select_py(input: String, columns: Vec<String>, output: Option<String>) -> PyResult<String> {
    engine::select_to_path(&input, &columns, output.as_deref())
        .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e.to_string()))
}

#[pyfunction]
fn convert_py(input: String, output: String) -> PyResult<String> {
    engine::convert_to_path(&input, &output)
        .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e.to_string()))?;
    Ok(output)
}

#[pyfunction]
fn profile_py(input: String) -> PyResult<Py<pyo3::types::PyDict>> {
    let stats = engine::profile_stats(&input)
        .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e.to_string()))?;
    Python::with_gil(|py| {
        let d = pyo3::types::PyDict::new_bound(py);
        for (k, v) in stats { d.set_item(k, v).unwrap(); }
        Ok(d.into())
    })
}

#[pymodule]
fn dpa_core(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(filter_py, m)?)?;
    m.add_function(wrap_pyfunction!(select_py, m)?)?;
    m.add_function(wrap_pyfunction!(convert_py, m)?)?;
    m.add_function(wrap_pyfunction!(profile_py, m)?)?;
    Ok(())
}
