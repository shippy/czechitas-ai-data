# /// script
# dependencies = ["duckdb"]
# ///
"""Build datacorp.duckdb from the six public CSV tables.

Loads every CSV with all_varchar=true so the deliberate dirt (mixed date
formats, thousands separators, placeholder strings) survives untouched —
cleaning it is the students' job. The payroll xlsx is intentionally NOT
loaded: parsing it is part of assignment 03c.

Ground-truth files are excluded — they'd spoil the SP4 eval.

Usage: uv run scripts/build_duckdb.py [output_path]
"""

import sys
from pathlib import Path

import duckdb

DATA_DIR = Path(__file__).resolve().parent.parent / "notebooks"

TABLES = {
    "zamestnanci": "datacorp.csv",
    "reviews": "datacorp_reviews.csv",
    "exit_interviews": "datacorp_exit_interviews.csv",
    "historie_platu": "datacorp_salary_history.csv",
    "org_struktura": "datacorp_org_chart.csv",
    "tickety": "datacorp_tickets.csv",
}


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else DATA_DIR / "datacorp.duckdb"
    out.unlink(missing_ok=True)

    con = duckdb.connect(str(out))
    for table, filename in TABLES.items():
        path = DATA_DIR / filename
        con.execute(
            f"CREATE TABLE {table} AS "
            f"SELECT * FROM read_csv(?, all_varchar=true)",
            [str(path)],
        )
        n = con.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {n} rows ({filename})")
    con.close()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
