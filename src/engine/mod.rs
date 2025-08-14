use anyhow::{Result, bail};
use clap::ArgMatches;
use polars::prelude::*;
use polars::sql::sql_expr;
use crate::io::{write_df, infer_reader};

fn parse_cols_opt(s: Option<&String>) -> Option<Vec<Expr>> {
    s.map(|csv| {
        csv.split(',').map(|c| col(c.trim())).collect::<Vec<_>>()
    })
}

fn parse_cols_vec(s: &String) -> Vec<Expr> {
    s.split(',').map(|c| col(c.trim())).collect::<Vec<_>>()
}

// ----- Public command handlers -----
pub fn filter_cmd(m: &ArgMatches) -> Result<()> {
    let input = m.get_one::<String>("input").unwrap();
    let where_expr = m.get_one::<String>("where").unwrap();
    let select = m.get_one::<String>("select");
    let output = m.get_one::<String>("output").unwrap();

    let lf = plan_filter(input, where_expr, select)?;
    let df = lf.collect()?;
    write_df(&df, output)?;
    Ok(())
}

pub fn select_cmd(m: &ArgMatches) -> Result<()> {
    let input = m.get_one::<String>("input").unwrap();
    let cols = m.get_one::<String>("columns").unwrap();
    let output = m.get_one::<String>("output").unwrap();
    let lf = infer_reader(input)?;
    let df = lf.select(parse_cols_vec(cols)).collect()?;
    write_df(&df, output)?;
    Ok(())
}

pub fn convert_cmd(m: &ArgMatches) -> Result<()> {
    let input = m.get_one::<String>("input").unwrap();
    let output = m.get_one::<String>("output").unwrap();
    let df = infer_reader(input)?.collect()?;
    write_df(&df, output)?;
    Ok(())
}

pub fn profile_cmd(m: &ArgMatches) -> Result<()> {
    let input = m.get_one::<String>("input").unwrap();
    let df = infer_reader(input)?.limit(1_000_000).collect()?;
    println!("Rows(sampled): {}", df.height());
    for s in df.get_columns() {
        println!("- {}: {:?}, nulls={}", s.name(), s.dtype(), s.null_count());
    }
    Ok(())
}

pub fn agg_cmd(m: &ArgMatches) -> Result<()> {
    let input = m.get_one::<String>("input").unwrap();
    let group = m.get_one::<String>("group").unwrap();
    let output = m.get_one::<String>("output").unwrap();

    let mut aggs: Vec<Expr> = vec![];
    if let Some(vals) = m.get_many::<String>("sum") {
        for v in vals { aggs.push(col(v).sum().alias(&format!("sum_{}", v))); }
    }
    if let Some(vals) = m.get_many::<String>("mean") {
        for v in vals { aggs.push(col(v).mean().alias(&format!("mean_{}", v))); }
    }
    if let Some(vals) = m.get_many::<String>("count") {
        for v in vals { aggs.push(col(v).count().alias(&format!("count_{}", v))); }
    }

    if aggs.is_empty() { bail!("No aggregations provided. Use --sum/--mean/--count."); }

    let lf = infer_reader(input)?;
    let df = lf.group_by([col(group)]).agg(aggs).collect()?;
    write_df(&df, output)?;
    Ok(())
}

pub fn join_cmd(m: &ArgMatches) -> Result<()> {
    let left = m.get_one::<String>("left").unwrap();
    let right = m.get_one::<String>("right").unwrap();
    let on = m.get_one::<String>("on").unwrap();
    let how = m.get_one::<String>("how").unwrap();
    let output = m.get_one::<String>("output").unwrap();

    let l = infer_reader(left)?;
    let r = infer_reader(right)?;
    let join_type = match how.as_str() {
        "inner" => JoinType::Inner,
        "left" => JoinType::Left,
        other => bail!("Unsupported join how={}. Only 'inner' and 'left' are supported.", other),
    };
    let df = l.join_builder()
        .with(r)
        .left_on([col(on)])
        .right_on([col(on)])
        .how(join_type)
        .finish().collect()?;
    write_df(&df, output)?;
    Ok(())
}

// ----- Core planning helpers reused by PyO3 -----
pub fn plan_filter(input: &str, where_expr: &str, select: Option<&String>) -> Result<LazyFrame> {
    let lf = infer_reader(input)?;
    let filtered = lf.filter(sql_expr(where_expr)?);
    let lf = if let Some(sel) = select {
        filtered.select(parse_cols_vec(sel))
    } else { filtered };
    Ok(lf)
}

// Convenience APIs for Python bindings
pub fn filter_to_path(input: &str, where_expr: &str, select: Option<&Vec<String>>, output: Option<&str>) -> Result<String> {
    let sel = select.map(|v| v.join(","));
    let lf = plan_filter(input, where_expr, sel.as_ref());
    let df = lf?.collect()?;
    let out = output.unwrap_or("dpa_out.parquet");
    crate::io::write_df(&df, out)?;
    Ok(out.to_string())
}

pub fn select_to_path(input: &str, columns: &Vec<String>, output: Option<&str>) -> Result<String> {
    let lf = infer_reader(input)?;
    let df = lf.select(columns.iter().map(|c| col(c)).collect::<Vec<_>>()).collect()?;
    let out = output.unwrap_or("dpa_out.parquet");
    crate::io::write_df(&df, out)?;
    Ok(out.to_string())
}

pub fn convert_to_path(input: &str, output: &str) -> Result<()> {
    let df = infer_reader(input)?.collect()?;
    crate::io::write_df(&df, output)?;
    Ok(())
}

pub fn profile_stats(input: &str) -> Result<std::collections::HashMap<String, String>> {
    let df = infer_reader(input)?.limit(1_000_000).collect()?;
    let mut m = std::collections::HashMap::new();
    m.insert("rows".into(), df.height().to_string());
    for s in df.get_columns() {
        m.insert(format!("dtype:{}", s.name()), format!("{:?}", s.dtype()));
        m.insert(format!("nulls:{}", s.name()), s.null_count().to_string());
    }
    Ok(m)
}
