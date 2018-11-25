# ADMM-for-the-Lasso

Python implementation for ADMM for the Lasso

## Getting started

NumPy and Kivy are used for the implmentation of the regression algorithm and a predictor program using the algorithm.

### Prerequisites

The following versions of NumPy and Kivy are used:

```
numpy 1.15.4
kivy 1.10.1
```

### Installing

If NumPy and Kivy are not installed yet, do the following:

```
>> python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
>> python -m pip install kivy
```

```
>> python -m pip install numpy
```

## How to run the predictor program

Do the following to get it started:

```
>> python program.py data-file-path index-file-path lambda rho epochs
```

* **data-file-path**: The path for the data file, containing X and y data to be used for regression
* **index-file-path**: The path for the index file, containing the names for each field in the data
* **lambda**, **rho**: The λ and ρ values to be used in the algorithm
* **epochs**: How many times it will run update() in the algorithm

For example, 

```
>> python program.py data.txt data_index.txt 1 1 25
```

You can also omit the arguments, using the default values

```
>> python program.py
```

On the console, you can see how the β values are being optimized

```
epoch 0: error = 35526.46702966751
epoch 1: error = 27781.20840755786
...
epoch 24: error = 25332.996741103634
```

See the docs in regression.py for more information.

Once in the program, you can randomly pick up a data from the data file and compare it with the predicted value, and change each parameter to predict a new value.


