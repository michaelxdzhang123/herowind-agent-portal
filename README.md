# Herowind-agent-portal

Herowind-agent-portal is an open-source tool for wind turbine blade design. It covers the full workflow from airfoil and geometry definition, laminate plan generation, stiffness matrix calculation, and stability analysis (HAWCStab2), to automated engineering report generation with AI assistance.

## Features

- **System Module**: Airfoils, blade shape, geometry, laminate plan, stiffness matrix
- **Aerodynamics & Structures**: FEM analysis and HAWCStab2 integration
- **AI Reports**: Automated professional analysis report generation
- **Web Portal**: Flask-based backend + Streamlit-based frontend components

## Tech Stack

- **Backend**: Flask, Flask-SQLAlchemy, Flask-Admin, Flask-Script
- **Solver/Compute**: FEniCS, ANBA4, CalculiX (CCX), B3P
- **Frontend**: Streamlit (aerodynamics/shape module), Flask templates (main portal)
- **Database**: SQLite

## Requirements

- Python >= 3.10
- External solvers (optional for full FEM pipeline):
  - FEniCS
  - ANBA4
  - CalculiX (CCX)
  - B3P

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd Herowind-agent-portal
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
uv venv --python 3.13
uv sync
```
Or install the package directly:

uv pip -r requirements.txt

If you need development/testing dependencies:

```bash
pip install -e ".[dev]"
```

### 4. Initialize the database

no databased install maully,  The tables are created automatically on first use via Flask-SQLAlchemy.


### Start the Flask server

The main web portal runs on Flask using `flask_script`.

```bash
uv run main.py
```

Then open your browser at: [http://localhost:9999]

The default landing page redirects to `/login`.



tubine specialist link to hermes by gateway flask

```bash
cd turbine-portal
uv run app.py


run testing manully (not nessissary hermes already did)
```bash
pytest -v
```

## Project Structure

```
Herowind-agent-portal/
├── app.py                  # Flask application entry point
├── config.py               # Flask configuration
├── model.py                # SQLAlchemy models (User, Token)
├── requirements.txt        # Python dependencies
├── pyproject.toml          # Package metadata
├── data/                   # SQLite database
├── static/                 # Static assets (CSS, JS, images)
├── templates/              # Jinja2 HTML templates
├── tests/                  # pytest test suite
```

## License

MIT License

## Contact

Michael Zhang - mich@aiagent.com
