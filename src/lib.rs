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

#[pyfunction]
#[pyo3(signature = (input, schema=None, rules=None))]
fn validate_py(input: String, schema: Option<String>, rules: Option<String>) -> PyResult<()> {
    engine::validate_py(&input, schema.as_deref(), rules.as_deref())
        .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e.to_string()))
}

#[pyfunction]
#[pyo3(signature = (input, output, size=None, method=None, stratify=None, seed=None))]
fn sample_py(
    input: String, 
    output: String, 
    size: Option<usize>, 
    method: Option<String>, 
    stratify: Option<String>, 
    seed: Option<u64>
) -> PyResult<()> {
    let size = size.unwrap_or(1000);
    let method = method.unwrap_or_else(|| "random".to_string());
    engine::sample_py(&input, &output, size, method.as_str(), stratify.as_deref(), seed)
        .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e.to_string()))
}

#[pyfunction]
#[pyo3(signature = (input, train_output, test_output, test_size=None, stratify=None, seed=None))]
fn split_py(
    input: String, 
    train_output: String, 
    test_output: String, 
    test_size: Option<f64>, 
    stratify: Option<String>, 
    seed: Option<u64>
) -> PyResult<()> {
    let test_size = test_size.unwrap_or(0.2);
    engine::split_py(&input, &train_output, &test_output, test_size, stratify.as_deref(), seed)
        .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e.to_string()))
}

#[pymodule]
fn dpa_core(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(filter_py, m)?)?;
    m.add_function(wrap_pyfunction!(select_py, m)?)?;
    m.add_function(wrap_pyfunction!(convert_py, m)?)?;
    m.add_function(wrap_pyfunction!(profile_py, m)?)?;
    m.add_function(wrap_pyfunction!(validate_py, m)?)?;
    m.add_function(wrap_pyfunction!(sample_py, m)?)?;
    m.add_function(wrap_pyfunction!(split_py, m)?)?;
    Ok(())
}
