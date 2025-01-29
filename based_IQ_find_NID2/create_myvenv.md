### ! Enable virtual environment with requirement.txt
1. create `.venv` environment
```
python3 -m venv .venv
```
2. activate the `.venv` environment
```
source .venv/bin/activate
```
3. install requirement in `requirement.txt`
```
pip install -r requirement.txt
```
then your environment can run python with requirement

### Create `requirement.txt`
create `requirement.txt` in folder you want to run the file and environment, then put your requirement
```
numpy
scipy
matplotlib
py3gpp
ipykernel
```
note: the `csv` cannot install for now, it is deprecated

### (Optional) In case want to install all requirement line by line

```
python3 -m venv .venv
source .venv/bin/activate
pip install numpy
pip install scipy
pip install matplotlib
pip install py3gpp
pip install ipykernel
```
in case cannot install `py3gpp` with `pip`, can run this line instead
```
python3 -m pip install py3gpp
```

4. in case after everything and still cannot use command inside py3gpp, just close the program and open again, try run command again. It works!