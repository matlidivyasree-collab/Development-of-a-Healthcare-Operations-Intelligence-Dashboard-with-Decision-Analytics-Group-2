# ================================================================
# DATA LOADING
# ================================================================
# Every CSV lives in the data folder at the top of the project, so
# the path is built from this file's location and never depends on
# the folder the app was started from.

from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Cleaned datasets"

PROGRAMS_FILES = [
    "fact_health_programs.csv",
    "dim_program.csv",
    "dim_state.csv",
    "dim_date.csv"
]

PROGRAMS_FILES_MAP = {
    "fact_health_programs.csv": ["fact_health_programs_cleaned.csv", "fact_health_programs.csv"],
    "dim_program.csv": ["dim_program_cleaned.csv", "dim_program.csv"],
    "dim_state.csv": ["dim_state_cleaned.csv", "dim_state.csv"],
    "dim_date.csv": ["dim_dates_cleaned.csv", "dim_dates.csv", "dim_date.csv"],
}


def _find_file(candidates: list[str]) -> Path | None:
    folders = ["Cleaned datasets", "data", "Raw data"]
    for folder in folders:
        for fname in candidates:
            p = BASE_DIR / folder / fname
            if p.exists():
                return p
    return None


def missing_files(file_names):
    """Return the names of any required CSV that cannot be found."""
    missing = []
    for fname in file_names:
        candidates = PROGRAMS_FILES_MAP.get(fname, [fname])
        if _find_file(candidates) is None:
            missing.append(fname)
    return missing


# The dashboard uses friendly display names. The raw column names
# from the CSVs are mapped across here.

PROGRAMS_COLUMN_NAMES = {
    "state_name": "State",
    "year": "Year",
    "month_name": "Month",
    "month_num": "MonthNum",
    "program_name": "Program",
    "program_coverage_pct": "ProgramCoverage",
    "people_screened": "PeopleScreened",
    "beneficiaries_reached": "BeneficiariesReached",
    "maternal_health_beneficiaries": "MaternalHealthBeneficiaries",
    "child_immunization_count": "ChildImmunization",
    "high_risk_individuals": "HighRiskIndividuals",
    "chronic_disease_patients": "ChronicDiseasePatients",
    "health_vulnerability_index": "HealthVulnerabilityIndex",
    "socioeconomic_score": "SocioeconomicScore",
    "children_population": "Children",
    "adults_population": "Adults",
    "elderly_population": "Elderly"
}


PROGRAMS_NUMBER_COLUMNS = [
    "ProgramCoverage",
    "PeopleScreened",
    "BeneficiariesReached",
    "MaternalHealthBeneficiaries",
    "ChildImmunization",
    "HighRiskIndividuals",
    "ChronicDiseasePatients",
    "HealthVulnerabilityIndex",
    "SocioeconomicScore",
    "Children",
    "Adults",
    "Elderly"
]


@st.cache_data
def get_programs_master():
    """Load, clean and join the health programs star schema.

    Returns the joined frame, the number of rows dropped for a
    negative count, and the number of exact duplicate fact rows.
    """

    fact_path = _find_file(PROGRAMS_FILES_MAP["fact_health_programs.csv"])
    program_path = _find_file(PROGRAMS_FILES_MAP["dim_program.csv"])
    state_path = _find_file(PROGRAMS_FILES_MAP["dim_state.csv"])
    date_path = _find_file(PROGRAMS_FILES_MAP["dim_date.csv"])

    fact = pd.read_csv(fact_path)
    program = pd.read_csv(program_path)
    state = pd.read_csv(state_path)
    date = pd.read_csv(date_path)

    # The raw fact file contains exact duplicate rows.

    duplicate_rows = int(fact.duplicated().sum())

    fact = fact.drop_duplicates()

    # Each dimension must have only one row per id.
    # If an id repeats, the merge would create extra fact rows
    # and every total on the dashboard would come out too high.

    program = program.drop_duplicates(subset=["program_id"])
    state = state.drop_duplicates(subset=["state_id"])
    date = date.drop_duplicates(subset=["date_id"])

    # Join the star schema.

    data = (
        fact
        .merge(program, on="program_id", how="left")
        .merge(state, on="state_id", how="left")
        .merge(date, on="date_id", how="left")
    )

    # Rename to the display names used throughout the dashboard.

    data = data.rename(columns=PROGRAMS_COLUMN_NAMES)

    # Make sure the number columns are really numbers.
    # Any blank or text value becomes NaN instead of breaking a chart.

    for column in PROGRAMS_NUMBER_COLUMNS:

        if column in data.columns:

            data[column] = pd.to_numeric(data[column], errors="coerce")

    # A negative number of people is not possible, so those rows go.

    negative_rows = int((data["HighRiskIndividuals"] < 0).sum())

    data = data[data["HighRiskIndividuals"] >= 0]

    # Year as text so the line chart gives each year its own colour.

    data["Year"] = data["Year"].astype(str)

    data = data.reset_index(drop=True)

    return data, negative_rows, duplicate_rows
