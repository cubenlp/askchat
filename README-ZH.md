# askchat

[![PyPI版本](https://img.shields.io/pypi/v/askchat.svg)](https://pypi.python.org/pypi/askchat)
[![测试](https://github.com/rexwzh/askchat/actions/workflows/test.yml/badge.svg)](https://github.com/rexwzh/askchat/actions/workflows/test.yml/)
[![文档状态](https://img.shields.io/badge/docs-github_pages-blue.svg)](https://rexwzh.github.io/askchat/)
[![覆盖率](https://codecov.io/gh/rexwzh/askchat/branch/main/graph/badge.svg)](https://codecov.io/gh/rexwzh/askchat)

终端使用 ChatGPT API 的小工具。

## 安装

```bash
pip install askchat
```

## 使用方法

简单运行方式，参数使用默认的环境变量：
```bash
ask hello
```

通过 `askchat` 指定其他选项：
```bash
# 使用特定模型提问
askchat hello -m "baichuan2" --base_url "localhost:8000"
```

生成默认选项的配置文件，您可以在 `~/.askchat/.env` 中编辑配置
```bash
askchat --generate-config
```


其他选项：
```bash
# 当前版本
askchat -v 
# 打印调试日志
askchat --debug
# 获取包含"gpt"的有效模型
askchat --valid-models
# 获取所有有效模型
askchat --all-valid-models
```

## 高级用法

您可以使用 `askchat` 管理您的对话：

```bash
askchat hello
# 继续上一次对话：-c
askchat -c 请给我讲个笑话
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