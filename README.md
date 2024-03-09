# askchat

[![PyPI version](https://img.shields.io/pypi/v/askchat.svg)](https://pypi.python.org/pypi/askchat)
[![Tests](https://github.com/cubenlp/askchat/actions/workflows/test.yml/badge.svg)](https://github.com/cubenlp/askchat/actions/workflows/test.yml/)
[![Documentation Status](https://img.shields.io/badge/docs-github_pages-blue.svg)](https://cubenlp.github.io/askchat/)
[![Coverage](https://codecov.io/gh/cubenlp/askchat/branch/main/graph/badge.svg)](https://codecov.io/gh/cubenlp/askchat)

[English](README-en.md) | [简体中文](README.md)

在命令行中调用 ChatGPT。

## 安装

```bash
pip install askchat --upgrade
```

## 使用方法

使用默认的环境变量进行简单运行：

```bash
ask hello
```

通过 `askchat` 指定其他选项：

```bash
# 使用特定模型提问
askchat hello -m "baichuan2" --base-url "localhost:8000"
```

通过环境变量生成默认的配置文件，在 `~/.askchat/.env` 中编辑配置：

```bash
askchat --generate-config
```

## 聊天选项

```bash
# 显示当前版本
askchat -v

# 打印调试日志
askchat --debug

# 获取包含 "gpt" 的有效模型
askchat --valid-models

# 获取所有有效模型
askchat --all-valid-models
```


## 管理对话记录

使用 `askchat` 管理对话：

```bash
askchat hello
# 继续上一次对话：-c
askchat -c 请给我讲个笑话
# 重新生成最后一次对话：-r
askchat -r
# 修改并重新生成最后一次对话：-r
askchat -r give me some jokes please
# 保存对话：-s/--save
askchat -s joke
# 加载对话：-l/--load
askchat -l joke
# 删除对话：-d/--delete
askchat -d joke
# 列出所有保存的对话：--list
askchat --list
# 打印最后一次对话：-p/--print
askchat -p
# 打印指定的对话：-p/--print
askchat -p joke
```

## 管理环境配置

通过 `chatenv` 管理不同的环境配置：

```bash
# 创建新环境
chatenv create <name> [--api-key "<api_key>"] [--base-url "<base_url>"] [--api-base "<api_base>"] [--model "<model_name>"]

# 激活指定环境
chatenv use <name>

# 更新环境配置
chatenv config [<name>] [--api-key "<new_api_key>"] [--base-url "<new_base_url>"] [--api-base "<new_api_base>"] [--model "<new_model_name>"]

# 列出所有环境
chatenv list

# 显示指定环境或默认环境的变量
chatenv show [<name>]

# 保存当前环境为一个新的环境文件
chatenv save <name>

# 删除指定的环境或默认环境配置
chatenv delete [<name>] [--default]
```

