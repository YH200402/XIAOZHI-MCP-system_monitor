# 系统监控 MCP 工具

这是一个基于 FastMCP 的系统监控工具，用于检测本地电脑的性能信息，包括内存、CPU、磁盘和 GPU 使用情况，并通过 WebSocket 将数据传输到远程服务器。

## 项目结构

```
mcp-001-system-monitor/
├── system_monitor.py    # 系统监控工具
├── file_tool.py         # 文件操作工具
├── datetime_tool.py     # 日期时间工具
├── mcp_pipe.py          # MCP 管道工具（WebSocket 通信）
├── mcp_config.json      # 配置文件
├── requirements.txt     # 依赖文件
├── example_usage.py     # 示例脚本
└── README.md            # 项目说明
```

## 功能特性

- **系统监控**：监控内存、CPU、磁盘和 GPU 使用百分比
- **文件工具**：读写文件、列出目录内容、检查文件是否存在
- **日期时间工具**：获取当前时间、格式化日期时间、添加时间差、计算日期差异
- **WebSocket 通信**：通过 mcp_pipe.py 将本地数据传输到远程服务器

## 安装依赖

1. 确保已安装 Python 3.6 或更高版本
2. 安装所需依赖：

```bash
pip install -r requirements.txt
```

## 配置文件

`mcp_config.json` 是配置文件，包含了 MCP 服务器的配置信息。默认配置已经指向正确的文件路径。

## 启动服务

### 方法一：使用 MCP 管道启动（推荐）

1. 设置环境变量 `MCP_ENDPOINT` 指向 WebSocket 服务器地址：
   - Windows (CMD)：`set MCP_ENDPOINT=ws://your-server-address:port`
   - Windows (PowerShell)：`$env:MCP_ENDPOINT = "ws://your-server-address:port"`

2. 启动 MCP 管道：

```bash
python mcp_pipe.py
```

这将启动所有配置的服务，并通过 WebSocket 将数据传输到远程服务器。

### 方法二：单独启动每个服务

如果需要单独启动某个服务，可以直接运行对应的 Python 文件：

```bash
# 启动系统监控服务
python system_monitor.py

# 启动文件工具服务
python file_tool.py

# 启动日期时间工具服务
python datetime_tool.py
```

## 使用方法

### 系统监控

调用 `system_monitor` 工具获取系统性能信息：

```python
from fastmcp import FastMCP

# 初始化 MCP 客户端
client = FastMCP()

# 调用系统监控工具
result = client.system_monitor()
print(result)
```

返回结果示例：

```json
{
  "success": true,
  "result": {
    "memory_usage_percent": 45.2,
    "cpu_usage_percent": 12.5,
    "disk_usage_percent": 60.1,
    "gpu_usage_percent": 30.0,
    "timestamp": 1617294000.0
  }
}
```

### 文件工具

#### 读取文件

```python
result = client.file_tool(action="read", file_path="path/to/file.txt")
```

#### 写入文件

```python
result = client.file_tool(action="write", file_path="path/to/file.txt", content="Hello, world!")
```

#### 列出目录内容

```python
result = client.file_tool(action="list", directory=".")
```

#### 检查文件是否存在

```python
result = client.file_tool(action="exists", file_path="path/to/file.txt")
```

### 日期时间工具

#### 获取当前时间

```python
result = client.datetime_tool(action="now")
```

#### 格式化日期时间

```python
result = client.datetime_tool(action="format", datetime="2023-04-01T12:00:00", format="%Y-%m-%d %H:%M:%S")
```

#### 添加时间差

```python
result = client.datetime_tool(action="add", datetime="2023-04-01T12:00:00", days=1, hours=2)
```

#### 计算日期差异

```python
result = client.datetime_tool(action="diff", datetime1="2023-04-01T12:00:00", datetime2="2023-04-02T14:30:00")
```

## 运行示例

运行示例脚本查看系统信息：

```bash
python example_usage.py
```

## 注意事项

- GPU 监控需要安装 `pynvml` 库，并且只有在 NVIDIA GPU 上才能正常工作
- 所有服务默认使用 stdio 传输方式，通过 mcp_pipe.py 与 WebSocket 服务器通信
- 请确保有足够的权限访问系统资源和文件
- 需要设置 `MCP_ENDPOINT` 环境变量才能使用 WebSocket 通信功能

## 故障排除

如果遇到依赖安装问题，可以尝试：

```bash
pip install -r requirements.txt
```

如果 GPU 监控不可用，可能是因为：
- 没有安装 NVIDIA 显卡
- 没有安装 `pynvml` 库
- NVIDIA 驱动程序版本不兼容

在这种情况下，系统会自动禁用 GPU 监控功能，其他功能不受影响。

如果 WebSocket 连接失败，可能是因为：
- 没有设置 `MCP_ENDPOINT` 环境变量
- WebSocket 服务器地址不正确
- 网络连接问题

请检查环境变量设置和网络连接后重试。