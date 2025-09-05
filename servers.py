
# main.py
# gRPC 用户服务端示例，使用 SQLite 数据库实现用户的增删改查。
# 详细注释，便于理解每一步。

import grpc
from concurrent import futures
import time
import user_pb2
import user_pb2_grpc
import db

# 首先初始化数据库，确保用户表存在
db.init_db()

# 实现 gRPC 服务，继承 user_pb2_grpc.UserServiceServicer
class UserService(user_pb2_grpc.UserServiceServicer):
    def CreateUser(self, request, context):
        """
        创建新用户。
        request: CreateUserRequest，包含 username 和 email 字段。
        返回: UserResponse，包含新建的 User。
        """
        user_id = db.create_user(request.username, request.email)
        user = user_pb2.User(id=user_id, username=request.username, email=request.email)
        return user_pb2.UserResponse(user=user)

    def GetUser(self, request, context):
        """
        根据用户ID获取用户信息。
        request: GetUserRequest，包含 id 字段。
        返回: UserResponse，如果用户不存在，user 字段为空。
        """
        user_data = db.get_user(request.id)
        if user_data:
            user = user_pb2.User(id=user_data['id'], username=user_data['username'], email=user_data['email'])
            return user_pb2.UserResponse(user=user)
        else:
            # 返回空 user
            return user_pb2.UserResponse()

    def UpdateUser(self, request, context):
        """
        更新用户信息。
        request: UpdateUserRequest，包含 id, username, email 字段。
        返回: UserResponse，user 字段为更新后的用户。
        """
        success = db.update_user(request.id, request.username, request.email)
        if success:
            user = user_pb2.User(id=request.id, username=request.username, email=request.email)
            return user_pb2.UserResponse(user=user)
        else:
            return user_pb2.UserResponse()

    def DeleteUser(self, request, context):
        """
        删除用户。
        request: DeleteUserRequest，包含 id 字段。
        返回: UserResponse，user 字段为被删除的用户（如果存在）。
        """
        user_data = db.get_user(request.id)
        if user_data:
            db.delete_user(request.id)
            user = user_pb2.User(id=user_data['id'], username=user_data['username'], email=user_data['email'])
            return user_pb2.UserResponse(user=user)
        else:
            return user_pb2.UserResponse()

    def ListUsers(self, request, context):
        """
        列出所有用户。
        request: ListUsersRequest。
        返回: ListUsersResponse，users 字段为所有用户列表。
        """
        users = db.list_users()
        user_list = [user_pb2.User(id=u['id'], username=u['username'], email=u['email']) for u in users]
        return user_pb2.ListUsersResponse(users=user_list)

    def SearchUsers(self, request, context):
        """
        搜索用户。
        request: SearchUsersRequest，包含 query 字段。
        返回: SearchUsersResponse，users 字段为搜索到的用户列表。
        """
        users = db.search_users(request.query)
        user_list = [user_pb2.User(id=u['id'], username=u['username'], email=u['email']) for u in users]
        return user_pb2.SearchUsersResponse(users=user_list)


def serve():
    """
    启动 gRPC 服务器，监听 50051 端口。
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    print('gRPC 服务器启动，监听端口 50051...')
    server.start()
    try:
        while True:
            time.sleep(86400)  # 一天
    except KeyboardInterrupt:
        print('服务器关闭')
        server.stop(0)


if __name__ == "__main__":
    serve()
