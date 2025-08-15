use anyhow::{Result, bail};
use clap::ArgMatches;
use polars::prelude::*;
use std::path::Path;

pub fn infer_reader(path: &str) -> Result<LazyFrame> {
    let p = Path::new(path);
    let ext = p.extension().and_then(|s| s.to_str()).unwrap_or("").to_ascii_lowercase();
    match ext.as_str() {
        "parquet" | "pq" => Ok(LazyFrame::scan_parquet(path, Default::default())?),
        "csv" => Ok(LazyCsvReader::new(path.to_string()).finish()?),
        "json" | "jsonl" => Ok(LazyJsonLineReader::new(path).finish()?),
        other => bail!("Unsupported input extension: {other}"),
    }
}

pub fn schema_cmd(m: &ArgMatches) -> Result<()> {
    let input = m.get_one::<String>("input").unwrap();
    let lf = infer_reader(input)?;
    let df = lf.collect()?;
    println!("{:?}", df.schema());
    Ok(())
}

pub fn head_cmd(m: &ArgMatches) -> Result<()> {
    let input = m.get_one::<String>("input").unwrap();
    let n: usize = m.get_one::<String>("n").unwrap().parse().unwrap_or(10);
    let df = infer_reader(input)?.fetch(n)?;
    println!("{df}");
    Ok(())
}

// write by extension
pub fn write_df(df: &DataFrame, output: &str) -> Result<()> {
    let ext = std::path::Path::new(output).extension().and_then(|s| s.to_str()).unwrap_or("").to_ascii_lowercase();
    match ext.as_str() {
        "parquet" | "pq" => {
            let w = ParquetWriter::new(std::fs::File::create(output)?);
            w.with_compression(ParquetCompression::Zstd(None))
                .finish(&mut df.clone())?;
        }
        "csv" => {
            let mut w = CsvWriter::new(std::fs::File::create(output)?);
            w.finish(&mut df.clone())?;
        }
        other => bail!("Unsupported output extension: {other}"),
    }
    Ok(())
}
