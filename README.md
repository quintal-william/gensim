# NSIM CLI

A Python command-line interface for randomly generating and converting complex network topology and traffic data for the DSE2.0 research project.

## Set up

1. Install Python 3.11.2 in the Software Center
2. Create a virtual environment by running `python -m venv .venv` in the same directory as this README
3. Enter the virtual environment by running either `.venv\Scripts\activate.bat` in the Windows Command Line, or `source .venv/bin/activate` in Bash.
4. Install the dependencies in the virtual environment by running `pip install -r requirements.txt`
5. Format and check the codebase using the `gray && mypy && python -m pytest --cov=nsim tests` command
7. If you wish to clean the repo of all generated artifacts, use: `pyclean . && rmdir /s /q .mypy_cache .venv` in the Windows Command Line, or `pyclean . && rm -rf .mypy_cache .venv` in Bash.
6. Have a look at the CLI usage docs by running `python -m nsim --help`

## Running OMNEST Output

To use the OMNEST output type, set up an OMNEST project using the following steps:
1. Install the INET framework
2. Right click the Project Explorer, and select "New" > "Project..."
3. Pick "OMNEST Project..." and click "Next >"
<!-- TODO could I create a template? -->
4. Pick "Empty project with 'src' and 'simulations' folders" and click "Finish"
5. Right click on your project, and click "Properties..."
6. Go to "Project References" and select the root directory with the INET framework in it
7. Go to "C/C++ General" > "Paths and Symbols" > "GNU C++" > "Add..." > "Workspace...", and select the "src" directory in the folder with the INET framework
8. Click "Apply and Close"
