# How to create a new python environment:

These are the basic commands to add and install some packages:

1. `python3 -m venv science`
2. `. science/bin/activate`
3. `pip install -r science_requirements.txt` 

** Note, **science** is just a name example, and **science_requirements** is just an example of commonly used python packages.

I usually add an alias to `.bashrc` (or whatever you use) to activate the python env:

```
# Python venv
alias science='source /home/user/.virtualenvs/science/bin/activate'
```

Reference: [Creating-virtual-environments](https://docs.python.org/3.3/library/venv.html#creating-virtual-environments)
