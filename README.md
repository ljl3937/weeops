# LangChain SSH 工具

这是一个基于 Paramiko 的 LangChain SSH 工具，用于在远程服务器上执行命令。

## 安装

1. 克隆仓库
2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 配置

1. 复制 `.env.example` 文件并重命名为 `.env`
2. 在 `.env` 文件中填入你的配置：
   - SSH_HOST：SSH 服务器地址
   - SSH_USERNAME：SSH 用户名
   - SSH_PASSWORD：SSH 密码
   - OPENAI_API_KEY：OpenAI API 密钥

## 使用方法

### 直接使用 SSH 工具

```python
from ssh_tool import SSHTool

ssh_tool = SSHTool()
result = ssh_tool.invoke({
    "command": "ls -la",
    "host": "your_host",
    "username": "your_username",
    "password": "your_password"
})
print(result)
```

### 在 LangChain Agent 中使用

运行示例程序：

```bash
python example.py
```

## 功能特点

- 支持基本的 SSH 命令执行
- 集成 LangChain 工具接口
- 支持环境变量配置
- 错误处理和异常报告
- 可以作为 Agent 工具使用

## 注意事项

- 请妥善保管你的 SSH 凭据和 API 密钥
- 建议使用 SSH 密钥认证而不是密码认证
- 在生产环境中使用时要注意安全性 