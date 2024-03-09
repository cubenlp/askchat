# askchat

[![PyPI version](https://img.shields.io/pypi/v/askchat.svg)](https://pypi.python.org/pypi/askchat)
[![Tests](https://github.com/cubenlp/askchat/actions/workflows/test.yml/badge.svg)](https://github.com/cubenlp/askchat/actions/workflows/test.yml/)
[![Documentation Status](https://img.shields.io/badge/docs-github_pages-blue.svg)](https://cubenlp.github.io/askchat/)
[![Coverage](https://codecov.io/gh/cubenlp/askchat/branch/main/graph/badge.svg)](https://codecov.io/gh/cubenlp/askchat)

[English](README-en.md) | [Simplified Chinese](README.md)

Invoke ChatGPT from the command line.

## Installation

```bash
pip install askchat --upgrade
```

## How to Use

Run simply with the default environment variables:

```bash
ask hello
```

Specify other options via `askchat`:

```bash
# Ask using a specific model
askchat hello -m "baichuan2" --base-url "localhost:8000"
```

Generate a default configuration file via environment variables, edit the configuration in `~/.askchat/.env`:

```bash
askchat --generate-config
```

## Chat Options

```bash
# Show the current version
askchat -v

# Print debug logs
askchat --debug

# Get valid models that include "gpt"
askchat --valid-models

# Get all valid models
askchat --all-valid-models
```


## Managing Conversation History

Manage conversations using `askchat`:

```bash
askchat hello
# Continue the last conversation: -c
askchat -c please tell me a joke
# Regenerate the last conversation: -r
askchat -r
# Modify and regenerate the last conversation: -r
askchat -r give me some jokes please
# Save the conversation: -s/--save
askchat -s joke
# Load a conversation: -l/--load
askchat -l joke
# Delete a conversation: -d/--delete
askchat -d joke
# List all saved conversations: --list
askchat --list
# Print the last conversation: -p/--print
askchat -p
# Print a specific conversation: -p/--print
askchat -p joke
```

## Managing Environment Configuration

Manage different environment configurations with `chatenv`:

```bash
# Create a new environment
chatenv create <name> [--api-key "<api_key>"] [--base-url "<base_url>"] [--api-base "<api_base>"] [--model "<model_name>"]

# Activate a specified environment
chatenv use <name>

# Update environment configuration
chatenv config [<name>] [--api-key "<new_api_key>"] [--base-url "<new_base_url>"] [--api-base "<new_api_base>"] [--model "<new_model_name>"]

# List all environments
chatenv list

# Show variables of a specified or default environment
chatenv show [<name>]

# Save the current environment as a new environment file
chatenv save <name>

# Delete a specified or the default environment configuration
chatenv delete [<name>] [--default]
```