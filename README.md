
# gRPC + SQLite Python 示例

本项目演示如何用 Python 实现基于 gRPC 的用户管理服务，数据存储使用 SQLite，支持用户的增删改查。

## 环境准备

1. **创建并激活虚拟环境（推荐）**

```powershell
python -m venv .venv
# Windows Bash:
source .venv/Scripts/activate
# 或 PowerShell:
.\.venv\Scripts\Activate.ps1
```

2. **安装依赖**

```powershell
pip install grpcio grpcio-tools protobuf
# 或使用 pyproject.toml: pip install .
```

3. **生成 gRPC 代码**

每次修改 `proto/user.proto` 后，都需要重新生成 Python 代码：

```bash
python -m grpc_tools.protoc -I=./proto --python_out=. --grpc_python_out=. ./proto/user.proto
```

会生成 `user_pb2.py` 和 `user_pb2_grpc.py`。

4. **启动 gRPC 服务端**

```bash
python servers.py
```

5. **运行客户端示例**

另开一个终端，运行：

```bash
python client.py
```

## 主要文件说明

- `proto/user.proto` - Protobuf 协议定义，描述用户消息和服务接口
- `user_pb2.py`、`user_pb2_grpc.py` - 由 proto 文件自动生成的 Python 代码
- `db.py` - SQLite 数据库操作（用户表的增删改查）
- `main.py` - gRPC 服务端实现，注册所有用户相关接口
- `client.py` - gRPC 客户端示例，演示所有接口的调用

## 常见问题

- **proto 文件有变动时，必须重新生成 Python 代码，否则服务端和客户端无法识别新接口或消息。**
- 端口默认 50051，如需更改请修改 `main.py`。

---
如需自定义 proto 或扩展功能，修改 proto 后重新执行第 3 步即可。
