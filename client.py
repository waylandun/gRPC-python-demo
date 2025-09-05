# client.py
# gRPC 客户端示例，演示如何调用用户服务的增删改查接口。
# 详细注释，便于理解每一步。

import grpc
import user_pb2
import user_pb2_grpc


def run():
    """
    客户端主函数，连接 gRPC 服务器并调用各接口。
    """
    # 连接到本地 gRPC 服务器
    channel = grpc.insecure_channel('localhost:50051')
    stub = user_pb2_grpc.UserServiceStub(channel)

    # 1. 创建用户
    print('创建用户:')
    create_resp = stub.CreateUser(user_pb2.CreateUserRequest(username='alice', email='alice@example.com'))
    print('创建结果:', create_resp.user)
    user_id = create_resp.user.id

    # 2. 获取用户
    print('\n获取用户:')
    get_resp = stub.GetUser(user_pb2.GetUserRequest(id=user_id))
    print('获取结果:', get_resp.user)

    # 3. 更新用户
    print('\n更新用户:')
    update_resp = stub.UpdateUser(user_pb2.UpdateUserRequest(id=user_id, username='alice_new', email='alice_new@example.com'))
    print('更新结果:', update_resp.user)

    # 4. 列出所有用户
    print('\n列出所有用户:')
    list_resp = stub.ListUsers(user_pb2.ListUsersRequest())
    for user in list_resp.users:
        print(user)

    # 5. 删除用户
    print('\n删除用户:')
    delete_resp = stub.DeleteUser(user_pb2.DeleteUserRequest(id=user_id))
    print('删除结果:', delete_resp.user)

    # 6. 再次获取用户，验证已删除
    print('\n再次获取用户:')
    get_resp2 = stub.GetUser(user_pb2.GetUserRequest(id=user_id))
    print('获取结果:', get_resp2.user)


if __name__ == "__main__":
    run()
