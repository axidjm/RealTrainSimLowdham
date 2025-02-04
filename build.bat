call poetry env use python
call poetry run python -m pip install --upgrade pip
call poetry install
call poetry run pre-commit run --all-files
@echo.
@echo Building EXE
call poetry run pyinstaller RealTrainSimLowdham.spec --clean 2> dist\build.log
@tail dist\build.log
