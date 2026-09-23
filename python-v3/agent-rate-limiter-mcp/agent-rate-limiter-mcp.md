# agent-rate-limiter-mcp

> 标签: Python

## 简介

Fleet-wide shared rate limiter for A2A + multi-MCP deployments. Most MCP servers rate-limit independently — a hostile agent hitting 10 MCPs gets 10x quota. This MCP is the shared counter: every MCP checks here before allowing a call. Sliding window + concurrency grants + signed enforcement attestations. By MEOK AI Labs.

## 官网

- 官网：https://meok.ai/agent-rate-limiter-mcp
- 源码仓库：https://github.com/CSOAI-ORG/agent-rate-limiter-mcp
- PyPI 项目页：https://pypi.org/project/agent-rate-limiter-mcp/

## 历史版本号

- 当前版本：1.0.10

- 1.0.0
- 1.0.1
- 1.0.10
- 1.0.2
- 1.0.3
- 1.0.4
- 1.0.5
- 1.0.6
- 1.0.7
- 1.0.8
- 1.0.9

## 获取地址

- pip 安装：`pip install agent-rate-limiter-mcp`
- 下载页面：https://pypi.org/project/agent-rate-limiter-mcp/#files
- 运行要求：Python >=3.10
