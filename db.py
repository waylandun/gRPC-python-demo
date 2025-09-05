# -*- coding: utf-8 -*-
"""
这个模块用于连接 SQLite 数据库，并提供用户表（users）的增删改查功能。
使用 sqlite3 模块来操作数据库，并对外提供封装好的数据库操作函数。
"""
import sqlite3
import os

# 数据库文件的名称，存放在当前工作目录
DB_FILE = 'users.db'


def get_db_connection():
    """获取数据库连接，如果数据库文件不存在则创建一个连接。
    同时设置 row_factory 为 sqlite3.Row，以便可以通过列名访问数据。
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # 设置为 Row 对象可以使用字典方式访问行数据
    return conn


def init_db():
    """初始化数据库，创建必要的用户表。
    如果用户表已存在，则不进行任何操作。
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    # 创建用户表，包含 id，username 和 email 字段
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()


def create_user(username, email):
    """在用户表中创建一条新的记录。

    参数:
      username (str): 用户的用户名。
      email (str): 用户的邮箱地址。

    返回:
      int: 新创建用户记录的ID。
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, email) VALUES (?, ?)', (username, email))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id


def get_user(user_id):
    """根据用户ID查询对应的用户信息。

    参数:
      user_id (int): 用户的ID。

    返回:
      dict: 包含用户数据的字典，如果用户不存在，返回 None。
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def update_user(user_id, username, email):
    """更新指定用户的记录。

    参数:
      user_id (int): 用户的ID。
      username (str): 更新后的用户名。
      email (str): 更新后的邮箱地址。

    返回:
      bool: 如果更新成功则返回 True，否则返回 False。
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET username = ?, email = ? WHERE id = ?', (username, email, user_id))
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    return updated > 0


def delete_user(user_id):
    """删除指定用户的记录。

    参数:
      user_id (int): 用户的ID。

    返回:
      bool: 如果删除成功返回 True，否则返回 False。
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    return deleted > 0


def list_users():
    """查询所有的用户记录，并以列表形式返回。

    返回:
      list: 每个元素是一个包含用户信息的字典。
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def search_users(query):
    """根据查询条件搜索用户。

    参数:
      query (str): 查询条件，可以是用户名或邮箱地址。

    返回:
      list: 每个元素是一个包含用户信息的字典。
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username LIKE ? OR email LIKE ?', ('%' + query + '%', '%' + query + '%'))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]