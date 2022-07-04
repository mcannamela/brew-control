brew-control
============

Controls our brewery. 

## Getting Started

### Python via pyenv
You will need an appropriate Python version, like 3.9 at the time of this writing. It's recommended to _not_ use your system's Python --even if it is the right version -- but to instead use (pyenv)[https://github.com/pyenv/pyenv] to install the version you need. Don't forget to first obtain (build dependencies for your system)[https://github.com/pyenv/pyenv/wiki#suggested-build-environment]. Also the installer is kind of sneaky on the pyenv README, but can be found (here)[https://github.com/pyenv/pyenv-installer]. 

For pyenv to work, you need to adjust your `.bashrc` so that it loads its shims when a new shell is started, then restart your shell.

Once you have pyenv installed, you can find an appropriate version via e.g.:
```console
$ pyenv install --list | grep 3\.9
```

and picking the latest point release from the list (3.9.12, for instance, at the time of this writing), then: 
```console
$ pyenv install 3.9.13
```

and finally setting this to be the local Python version in the `brew-control` repo:
```console
$ cd brew-control
$ pyenv local 3.9.13
```

You will know you're ready to go with:
```console
$ which python
/home/your_username/.pyenv/shims/python

$ python --version
Python 3.9.13
```

### Dependencies via Poetry

Python dependencies and virtualenvs are managed via (Poetry)[https://python-poetry.org/docs/], so set that up first. 

By default Poetry puts virtualenvs in the user's home folder, but some prefer to put them in the project directory, which can be done via
```console
$ poetry config virtualenvs.in-project true
```

Now if you:
```console
$ poetry install
```

you should get a virtualenv suitable for running brew control.

## Project Structure

The project consists of server-side code for the Arduino, which must be appropriately wired to the physical brewery, and a Python client. All the dependencies for the Arduino's code are reproduced in this project, and you will need to set up for Arduino development separately if you wish to change it. This should rarely be neccessary. The Arduino's server implements a simple interface that allows client code to read the values of its sensors and set a pin high or low. All logic to interpret those readings and decide when to change pin states is done from the client side, using Python in this project. 

The Python client lives in (brew_control_client)[./brew_control_client]. It includes code to talk to the Arduino and get it's state or set some input pins, logic to interpret that state as temperatures or flowrates, and brewing control logic to turn heaters on and off as needed. 

## Brewing

To brew, run (`brew.py`)[brew.py] and adjust setpoint temperatures as needed.

You can plot the contents of the logfile using (`plot_brew.py`)[plot_brew.py].
