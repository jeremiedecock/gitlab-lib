Here is the procedure to submit updates to PyPI
===============================================

C.f. https://packaging.python.org/en/latest/tutorials/packaging-projects/
 
1. Install / update pip, build and twine::

    python3 -m pip install --upgrade pip
    python3 -m pip install --upgrade build
    python3 -m pip install --upgrade twine

2. Build the source distribution::

    python3 -m build

3. Upload the source distribution::

    twine upload dist/*
