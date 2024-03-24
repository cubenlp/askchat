# AskChat

<div align="center">
    <a href="https://pypi.python.org/pypi/askchat">
        <img src="https://img.shields.io/pypi/v/askchat.svg" alt="PyPI version" />
    </a>
    <a href="https://github.com/cubenlp/askchat/actions/workflows/test.yml">
        <img src="https://github.com/cubenlp/askchat/actions/workflows/test.yml/badge.svg" alt="Tests" />
    </a>
    <a href="https://cubenlp.github.io/askchat/">
        <img src="https://img.shields.io/badge/docs-github_pages-blue.svg" alt="Documentation Status" />
    </a>
    <a href="https://codecov.io/gh/cubenlp/askchat">
        <img src="https://codecov.io/gh/cubenlp/askchat/branch/main/graph/badge.svg" alt="Coverage" />
    </a>
</div>

<div align="center">
<img src="https://qiniu.wzhecnu.cn/PicBed6/picgo/askchat.jpeg" alt="Ask Chat" width="256">

[English](README-en.md) | [简体中文](README.md)
</div>

Interact with ChatGPT from the command line.

## Installation and Configuration

```bash
pip install askchat --upgrade
```

Configure the environment variables:

```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_API_BASE_URL="https://api.openai.com"
export OPENAI_API_BASE="https://api.openai.com/v1"
export OPENAI_MODEL="gpt-3.5-turbo"
```

Note: The `OPENAI_API_BASE` variable has priority over `OPENAI_API_BASE_URL`. Use one of them as needed.

## Usage

To run using the default environment variables, simply execute:

```bash
ask hello world
```

## AskChat

`askchat`, beyond direct use, supports more flexible conversation management with the following options:

```bash
❯ askchat --help
Usage: askchat [OPTIONS] [MESSAGE]...

  Interact with ChatGPT in terminal via chattool

Options:
  -m, --model TEXT     Model name
  -b, --base-url TEXT  Base URL of the API (without suffix `/v1`)
  --api-base TEXT      Base URL of the API (with suffix `/v1`)
  -a, --api-key TEXT   OpenAI API key
  -u, --use-env TEXT   Use environment variables from the ENV_PATH
  -c                   Continue the last conversation
  -r, --regenerate     Regenerate the last conversation
  -l, --load TEXT      Load the conversation from a file
  -p, --print          Print the last conversation or a specific conversation
  -s, --save TEXT      Save the conversation to a file
  -d, --delete TEXT    Delete the conversation from a file
  --list               List all the conversation files
  --generate-config    Generate a configuration file by environment table
  --debug              Print debug log
  --valid-models       Print valid models that contain "gpt" in their names
  --all-valid-models   Print all valid models
  -v, --version        Print the version
  --help               Show this message and exit.
```

### Conversation Management

Manage conversation history, including saving, loading, deleting, and listing conversations, as well as continuing previous dialogues.

| Option          | Example                | Description                                   |
|-----------------|------------------------|-----------------------------------------------|
| `-c`            | `askchat -c <message>` | Continue the last conversation               |
| `--regenerate`  | `askchat -r`           | Regenerate the last response of the conversation |
| `--load`        | `askchat -l <file>` | Load conversation history from a file |
| `--print`       | `askchat -p [<file>]`  | Print the last or a specified conversation history |
| `--save`        | `askchat -s <file>`    | Save the current conversation history to a file |
| `--delete`      | `askchat -d <file>`    | Delete a specified conversation history file |
| `--list`        | `askchat --list`       | List all saved conversation history files     |

All conversations are saved in `~/.askchat/`, with the most recent conversation saved in `~/.askchat/_last_chat.json`.

### Specified Parameters

Default parameters for `askchat`, used for direct interaction with ChatGPT or configuring the API connection.

| Option          | Example                          | Description                                  |
|-----------------|----------------------------------|----------------------------------------------|
| `<message

>`     | `askchat hello`                  | The simplest form of dialogue                |
| `--model`       | `-m gpt-3.5-turbo`               | Specify the model name                       |
| `--base-url`    | `-b https://api.example.com`     | Set the Base URL (excluding `/v1`)           |
| `--api-base`    | `--api-base https://api.example.com/v1` | Set the Base URL           |
| `--api-key`     | `-a sk-xxxxxxx`                  | Provide the OpenAI API key                   |
| `--option` | `-o top_p 1 temperature 0.5` | Set request parameters |
| `--use-env`     | `-u prod`                        | Load environment variables from the specified config file, see [AskEnv](#askenv) |

Note: Some model APIs, like ChatGPT, use `/v4` as the base path of the API, so the `--api-base` parameter would be needed.

### Other Options

Auxiliary features such as generating configuration files, printing debug logs, listing models, and showing version information.

| Option                  | Example                         | Description                                    |
|-------------------------|---------------------------------|------------------------------------------------|
| `--generate-config`     | `askchat --generate-config`     | Generate a config file, saved in `~/.askchat/.env` |
| `--debug`               | `askchat --debug`               | Print debug logs                               |
| `--valid-models`        | `askchat --valid-models`        | Print a list of models containing "gpt" in their names |
| `--all-valid-models`    | `askchat --all-valid-models`    | Print all models                               |
| `--version`             | `askchat -v`                    | `askchat` version information                  |

Note: `--all-valid-models` prints all available models, including Embedding, dalle-3, tts, etc., use `--valid-models` to filter these out.

## AskEnv

`askenv` is used to manage different environment configurations, supporting operations such as create, activate, delete, etc. It facilitates switching between different environments, managing API keys, model names, and API base URLs.

1. Create a new environment configuration using the `new` command.

    ```bash
    askenv new <name> [-a API_KEY] [-b BASE_URL] [--api-base API_BASE] [-m MODEL]
    ```

2. Activate an environment, setting it as the current configuration.

    ```bash
    askenv use <name>
    ```

3. Delete a specified environment configuration file.

    ```bash
    askenv delete <name>
    askenv delete --default
    ```

4. List all available environments.

    ```bash
    askenv list
    ```

5. Display the configuration information for a specified environment, or the default environment if no name is provided.

    ```bash
    askenv show [name]
    ```

6. Save the currently active environment configuration to a specified name.

    ```bash
    askenv save <name>
    ```

7. Update one or more settings for a specified or default environment configuration.

    ```bash
    askenv config [name] [-a API_KEY] [-b BASE_URL] [--api-base API_BASE] [-m MODEL]
    ```