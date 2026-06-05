# BladeAI

BladeAI is an open-source tool for wind turbine blade design. It covers the full workflow from airfoil and geometry definition, laminate plan generation, stiffness matrix calculation, and stability analysis (HAWCStab2), to automated engineering report generation with AI assistance.

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
cd blade-ai
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

Or install the package directly:

```bash
pip install -e .
```

If you need development/testing dependencies:

```bash
pip install -e ".[dev]"
```

### 4. Initialize the database

The application uses SQLite (`data/data.sqlite`). The tables are created automatically on first use via Flask-SQLAlchemy.

## Running the Application

### Start the Flask server

The main web portal runs on Flask using `flask_script`.

```bash
python app.py runserver -h 0.0.0.0 -p 8181
```

Then open your browser at: [http://localhost:8181](http://localhost:8181)

The default landing page redirects to `/login`.

### Start the Streamlit module (optional)

If you want to run the aerodynamics/shape Streamlit app (`Application/aero_shape/bbs.py`):

```bash
cd Application/aero_shape
streamlit run bbs.py --server.enableXsrfProtection=false --server.port 8551
```

Then open your browser at: [http://localhost:8551](http://localhost:8551)

### Run using the provided shell script

You can also start both services in the background using:

```bash
bash run_flask.sh
```

Or the combined startup script:

```bash
bash fl.sh
```

## Running Tests

```bash
pytest
```

Or with verbose output:

```bash
pytest -v
```

## Project Structure

```
blade-ai/
├── app.py                  # Flask application entry point
├── config.py               # Flask configuration
├── model.py                # SQLAlchemy models (User, Token)
├── requirements.txt        # Python dependencies
├── pyproject.toml          # Package metadata
├── data/                   # SQLite database
├── static/                 # Static assets (CSS, JS, images)
├── templates/              # Jinja2 HTML templates
├── tests/                  # pytest test suite
├── Application/
│   ├── Airfoils/           # Airfoil data
│   ├── aero_shape/         # Streamlit aerodynamics app
│   ├── b3p/                # Blade geometry/meshing tools
│   ├── fem/                # FEM pipeline (makefile)
│   ├── stab2/              # Stability analysis
│   └── sys/                # System configuration files
└── docs/                   # Documentation and videos
```

## License

MIT License

## Contact

Michael Zhang - mich@mich.com
