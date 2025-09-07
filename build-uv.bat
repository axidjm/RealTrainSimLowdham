@echo off

mkdir dist

REM Create virtual environment
uv venv .venv

REM Install dependencies
uv sync --extra dev

REM Run tests
uv run pre-commit run --all-files
rem uv run pytest --cov -vv tests
rem uv run coverage report --fail-under=85

REM Build
uv run pyinstaller RealTrainSimLowdham.spec --clean 2> dist\build.log
tail dist\build.log
