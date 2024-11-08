import nbconvert
import nbformat
from nbconvert import PythonExporter
import importlib.util
import sys
import joblib
from sklearn.preprocessing import StandardScaler


def import_from_ipynb(notebook_path, var_name):
    # Załaduj notebook
    with open(notebook_path)as f:
        nb = nbformat.read(f, as_version=4)

    # Konwertuj notebook na kod Python
    exporter = PythonExporter()
    source_code, _ = exporter.from_notebook_node(nb)

    # Zapisz kod Python do tymczasowego pliku
    tmp_file = '_tmp_notebook_code.py'
    with open(tmp_file, 'w') as f:
        f.write(source_code)

    # Załaduj kod z tymczasowego pliku
    spec = importlib.util.spec_from_file_location(
        '_tmp_notebook_module', tmp_file)
    module = importlib.util.module_from_spec(spec)
    sys.modules['_tmp_notebook_module'] = module
    spec.loader.exec_module(module)

    # Pobierz zmienną z załadowanego modułu
    return getattr(module, var_name)


# Użycie funkcji do zaimportowania zmiennej 'model' oraz 'skaler' z notebooka 'Project3.ipynb'
model = import_from_ipynb('Project3.ipynb', 'model')
scaler = import_from_ipynb('Project3.ipynb', 'scaler')
