mod cli;
mod engine;
mod io;

use anyhow::Result;

fn main() -> Result<()> {
    let app = cli::build_cli();
    let matches = app.get_matches();

    match matches.subcommand() {
        Some(("schema", m)) => io::schema_cmd(m),
        Some(("head", m)) => io::head_cmd(m),
        Some(("filter", m)) | Some(("f", m)) => engine::filter_cmd(m),
        Some(("select", m)) | Some(("s", m)) => engine::select_cmd(m),
        Some(("convert", m)) | Some(("c", m)) => engine::convert_cmd(m),
        Some(("profile", m)) | Some(("p", m)) => engine::profile_cmd(m),
        Some(("agg", m)) | Some(("a", m)) => engine::agg_cmd(m),
        Some(("join", m)) | Some(("j", m)) => engine::join_cmd(m),
        _ => {
            println!("See --help for usage.");
            Ok(())
        }
    }
}
