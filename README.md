# askchat
[![PyPI version](https://img.shields.io/pypi/v/askchat.svg)](https://pypi.python.org/pypi/askchat)
[![Tests](https://github.com/rexwzh/askchat/actions/workflows/test.yml/badge.svg)](https://github.com/rexwzh/askchat/actions/workflows/test.yml/)
[![Documentation Status](https://img.shields.io/badge/docs-github_pages-blue.svg)](https://rexwzh.github.io/askchat/)
[![Coverage](https://codecov.io/gh/rexwzh/askchat/branch/main/graph/badge.svg)](https://codecov.io/gh/rexwzh/askchat)


Interact with ChatGPT in terminal via chattool

## Installation

```bash
pip install askchat
```

## Usage

A simple way:
```bash
ask hello
```

Ask with more options via `askchat`:
```bash
# ask with a specific model
askchat hello -m "baichuan2" --base_url "localhost:8000"
```

Generate config file for default options:
```bash
askchat --generate-config
```

Other options:
```bash
# current version
askchat -v 
# Get debug log
askchat --debug
# get valid models that contains "gpt"
askchat --valid-models
# get all valid models
askchat --all-valid-models
```