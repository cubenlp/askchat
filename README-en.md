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
<img src="docs/assets/askchat.png" alt="Ask Chat" width="256">

[English](README-en.md) | [简体中文](README.md)
</div>

AskChat is a command-line tool for ChatGPT interaction, allowing you to call ChatGPT anytime, anywhere.

<div align="center">
    <figure>
        <div style="margin-top: 10px; color: #555;">Run in Terminal</div>
        <img src="docs/assets/svgs/hello.svg" alt="hello" width="480">
    </figure>
</div>

<div align="center">
    <figure>
    <div style="margin-top: 10px; color: #555;">Jupyter Lab</div>
    <img src="docs/assets/jupyter.gif" alt="jupyter" width="480">
    </figure>
</div>

## Installation and Configuration

```bash
pip install askchat --upgrade
```

Configure environment variables:

```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_API_BASE="https://api.openai.com/v1"
export OPENAI_API_BASE_URL="https://api.openai.com"
export OPENAI_API_MODEL="gpt-3.5-turbo"
```

Note: The `OPENAI_API_BASE` variable takes precedence over the `OPENAI_API_BASE_URL` variable; choose one.

## How to Use

Use environment variables for simple question and answer:

```bash
ask hello world
```

In addition, you can use `askchat` for more flexible dialogue and `askenv` to manage environment configurations.

## AskChat

`askchat` supports API debugging, dialogue management, and other functionalities.

### Usage Examples

<div align="center">
    <figure>
    <div style="margin-top: 10px; color: #555;">1. API debugging</div>
    <img src="docs/assets/svgs/debug.svg" alt="debug" width="480">
    </figure>
</div>

<div align="center">
    <figure>
    <div style="margin-top: 10px; color: #555;">2. Get a list of available models</div>
    <img src="docs/assets/svgs/validmodels.svg" alt="validmodels" width="480">
    </figure>
</div>

<div align="center">
    <figure>
    <div style="margin-top: 10px; color: #555;">3. Multi-turn dialogue, saving dialogues, loading dialogues, etc.</div>
    <img src="docs/assets/svgs/chatlog.svg" alt="chatlog" width="480">
    </figure>
</div>

<div align="center">
    <figure>
    <div style="margin-top: 10px; color: #555;">4. Specify parameters, using different models and APIs</div>
    <img src="docs/assets/svgs/para-models.svg" alt="para-models" width="480">
    </figure>
</div>

### Dialogue Management

Users save, load, delete, and list dialogue histories, as well as continue previous dialogues.

| Parameter         | Example                 | Explanation                              |
|-------------------|-------------------------|------------------------------------------|
| `-c`              | `askchat -c <message>`  | Continue the last conversation           |
| `--regenerate`    | `askchat -r`            | Regenerate the last reply in a conversation |
| `--load`          | `askchat -l <file>`     | Load historical dialogues                |
| `--print`         | `askchat -p [<file>]`   | Print the last or a specified dialogue history |
| `--save`          | `askchat -s <file>`     | Save the current dialogue history to a file |
| `--delete`        | `askchat -d <file>`     | Delete a specified dialogue history file |
| `--list`          | `askchat --list`        | List all saved dialogue history files    |

All dialogues are saved in `~/.askchat/`, with the most recent dialogue saved in `~/.askchat/_last_chat.json`.

### Model Parameters

Default parameters for `askchat`, these are used for direct interaction with ChatGPT or to configure API connection info.

| Parameter        | Example                           | Explanation                        |
|------------------|-----------------------------------|------------------------------------|
| `<message>`      | `askchat hello`                   | Simplest form of dialogue          |
| `--model`        | `-m gpt-3.5-turbo`                | Specify the model to be used       |
| `--base-url`     | `-b https://api.example.com`      | Set the Base URL (excluding `/v1`) |
| `--api-base`     | `--api-base https://api.example.com/v1` | Set the Base URL        |
| `--api-key`      | `-a sk-xxxxxxx`                   | Provide the OpenAI API key         |
| `--option`       | `-o top_p 1 temperature 0.5`      | Set request parameters             |
| `--use-env`      | `-u prod`                         | Load environment variables from a specified config, see [AskEnv](#askenv) |

Note: Some model APIs, such as Zhishu, use `/v4` as the API base path, in which case use the `--api-base` parameter.

### Additional Parameters

Auxiliary features, such as generating configuration files, debugging logs, printing model lists, and showing version information, etc., use `--help` to see all supported parameters.

| Parameter                | Example                          | Explanation                           |
|--------------------------|----------------------------------|---------------------------------------|
| `--generate-config`      | `askchat --generate-config`      | Generate a configuration file, saved in `~/.askchat/.env` |
| `--debug`                | `askchat --debug`                | Print debugging logs                  |
| `--valid-models`         | `askchat --valid-models`         | Print a list of models containing "gpt" in their names |
| `--all-valid-models`     | `askchat --all-valid-models`     | Print all available models            |
| `--version`              | `askchat -v`                     | Version information of `askchat`      |

Note: `--all-valid-models` will print all available models, including Embedding, dalle-3, tts, etc., use `--valid-models` to filter these out.

## AskEnv

`askenv` is used to manage different environment configurations, including creating, activating, deleting, etc., making it easy to switch between different channels.

### Examples

<div align="center">
    <figure>
    <div style="margin-top: 10px; color: #555;">1. Create channel</div>
    <img src="docs/assets/svgs/askenv.svg" alt="askenv" width="480">
    </figure>
</div>

<div align="center">
    <figure>
    <div style="margin-top: 10px; color: #555;">2. Edit channel</div>
    <img src="docs/assets/svgs/editenv.svg" alt="editenv" width="480">
    </figure>
</div>

### Basic Usage

1. Create a new environment configuration using the `new` command.

    ```bash
    askenv new <name> [-a API_KEY] [-b BASE_URL] [--api-base API_BASE] [-m MODEL]
    ```

    Or generate a default config from environment variables using `askchat --generate-config`:

    ```bash
    askchat --generate-config
    ```

2. Activate a certain environment, setting it as the currently used configuration.

    ```bash
    askenv use <name>
    ```

3. Delete a specified environment configuration file.

    ```bash
    askenv delete <name>
    askenv delete --default
    ```

4. List all currently available environments.

    ```bash
    askenv list
    ```

5. Show configuration info of a specified environment, or the default environment if no name is specified.

    ```bash
    askenv show [name]
    ```

6. Save the currently activated environment configuration as a specified name's configuration file.

    ```bash
    askenv save <name>
    ```

7. Update one or more settings of a specified or default environment configuration.

    ```bash
    askenv config [name] [-a API_KEY] [-b BASE_URL] [--api-base API_BASE] [-m MODEL]
    ```

## Issues and Feedback

If you encounter any problems or have suggestions, feel free to submit an [Issue](https://github.com/cubenlp/askchat/issues).