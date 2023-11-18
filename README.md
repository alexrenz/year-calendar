# Year Calendar

[![Example](example.png)](editionen/cal_2024.pdf)

## Install dependencies 

Depends on [cairo](https://www.cairographics.org/) and [its Python bindings](https://pycairo.readthedocs.io/) for drawing, and [pandas](https://pandas.pydata.org/) for parsing the special day CSV file.

E.g., on macOS:
```bash
brew install cairo
pip install pycairo pandas
```

## Generate a calendar

```bash
python3 cal.py 2024
```

or just `make`
