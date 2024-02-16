# NSIM CLI

An extendable Python command-line interface for randomly generating and converting custom complex network topology and traffic data for the DSE2.0 research project.

## Set up

1. Install Python 3.11.2 in the Software Center
2. Create a virtual environment by running `python -m venv .venv` in the same directory as this README
3. Enter the virtual environment by running either `.venv\Scripts\activate.bat` in the Windows Command Line, or `source .venv/bin/activate` in Bash.
4. Install the dependencies in the virtual environment by running `pip install -r requirements.txt`
5. Format, check, and test the codebase using the `gray && mypy && python -m pytest --cov=nsim tests` command
6. If you wish to clean the repo of all generated artifacts, use: `pyclean . && rmdir /s /q .mypy_cache .venv` in the Windows Command Line, or `pyclean . && rm -rf .mypy_cache .venv` in Bash.
7. Have a look at the CLI usage docs by running `python -m nsim --help`
8. Optionally, you can create an alias to work with the CLI more easily. Use `doskey nsim=python -m nsim $*` in the Windows Command Line, or `alias nsim="python -m nsim"` in Bash.

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
9. Delete the content of the `src` directory, and copy-paste the code from the `omnet` directory in this repository into it.
10. Generate your topology with -o json or -o xml (e.g. `nsim topology generate -g mesh -o json`). Store it in a file in the `dist` directory in this repository.
11. Convert your topology to -o inet (e.g. `nsim topology convert -o inet dist/mesh.json`), and create a .ned and .ini file in your simulations folder with the generated content.
11. Generate your traffic with -o json or -o xml (e.g. `nsim traffic generate -g poisson -o json`). Create a traffic.json or traffic.xml file in your simulations folder and store the generated content in there.
12. Run the simulation!
