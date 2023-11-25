# askchat
[![PyPI version](https://img.shields.io/pypi/v/askchat.svg)](https://pypi.python.org/pypi/askchat)
[![Tests](https://github.com/rexwzh/askchat/actions/workflows/test.yml/badge.svg)](https://github.com/rexwzh/askchat/actions/workflows/test.yml/)
[![Documentation Status](https://img.shields.io/badge/docs-github_pages-blue.svg)](https://rexwzh.github.io/askchat/)
[![Coverage](https://codecov.io/gh/rexwzh/askchat/branch/main/graph/badge.svg)](https://codecov.io/gh/rexwzh/askchat)


Interact with ChatGPT in terminal via chattool.

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

You might edit the config at `~/.askchat/.env`.

Other options:
```bash
# current version
askchat -v 
# print the debug log
askchat --debug
# get valid models that contains "gpt"
askchat --valid-models
# get all valid models
askchat --all-valid-models
```

## Advance usage

You can manage your chats with `askchat`:

```bash
askchat hello
# continue the last chat: -c
askchat -c tell me a joke please
# regenerate the last conversation: -r
askchat -r
# regenerate the last conversation with new message: -r
askchat -r give me some jokes please
# save the chat: -s/--save
askchat -s joke
# load the chat: -l/--load
askchat -l joke
# delete the chat: -d/--delete
askchat -d joke
# list all saved chats: --list
askchat --list
# print the last chat: -p/--print
askchat -p
# print the given chat: -p/--print
askchat -p joke
```
