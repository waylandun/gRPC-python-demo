# gRPC + SQLite Python 示例

该示例包含一个简单的 gRPC 服务，用 SQLite 存储用户（id, username, email），并实现增删改查接口。

准备步骤：

1. 创建并激活虚拟环境（可选，但推荐）

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. 安装依赖

```powershell
pip install -r requirements.txt
# 或者使用 pyproject.toml: pip install .
```

3. 生成 gRPC 代码

```powershell
python generate_proto.py
```

4. 启动服务

```powershell
python server.py
```

5. 在另一个终端运行客户端示例

```powershell
python client.py
```

文件说明：

- `proto/user.proto` - Protobuf 定义
- `generate_proto.py` - 生成 Python gRPC 代码的脚本
- `generated/` - 生成的 gRPC Python 模块（运行 `generate_proto.py` 后生成）
- `db.py` - 包装 sqlite 的简单 CRUD
- `server.py` - gRPC 服务实现
- `client.py` - 简单示例客户端
