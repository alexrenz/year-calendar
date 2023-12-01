# Year Calendar

[![Example](example.png)](editionen/cal_2024.pdf)

A clean and minimal year overview calendar, to be printed out on part of an A1 sheet (we usually print it so that the long side is 84cm). 

[PDF for 2024 edition](editionen/cal_2024.pdf)

## Install dependencies 

Depends on [cairo](https://www.cairographics.org/) and [its Python bindings](https://pycairo.readthedocs.io/) for drawing, [pandas](https://pandas.pydata.org/) for parsing the special day CSV file, and uses the [Iosevka](https://github.com/be5invis/Iosevka) font (changeable in [cal.py](./cal.py)).

E.g., on macOS:
```bash
brew install cairo
pip install pycairo pandas
brew tap homebrew/cask-fonts
brew install font-iosevka
```

## Generate a calendar

```bash
python3 cal.py 2024
```

or just `make`
