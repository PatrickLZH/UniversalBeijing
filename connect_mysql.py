#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql
from pymysql import Error
import sys
import os

# 添加项目路径以便导入配置
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config.config import Config
except ImportError:
    # 如果无法导入配置文件，则使用默认配置
    class Config:
        SQL_HOST = '127.0.0.1'
        SQL_USERNAME = 'root'
        SQL_PASSWORD = '1234'
        SQL_PORT = 3306
        SQL_DB = 'my_project'



def test_pymysql_connection():
    """
    测试PyMySQL数据库连接
    """
    print("🔍 开始测试PyMySQL连接...")
    print("=" * 50)
    
    # 数据库连接配置
    connection_config = {
        'host': Config.SQL_HOST,
        'user': Config.SQL_USERNAME,
        'password': Config.SQL_PASSWORD,
        'port': int(Config.SQL_PORT),
        'database': Config.SQL_DB,
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }
    
    connection = None
    try:
        # 建立数据库连接
        print(f"🔌 正在连接到数据库: {Config.SQL_HOST}:{Config.SQL_PORT}")
        connection = pymysql.connect(**connection_config)
        
        print("✅ 成功连接到MySQL数据库!")
        
        # 获取连接信息
        with connection.cursor() as cursor:
            # 获取MySQL版本
            cursor.execute("SELECT VERSION() as version")
            result = cursor.fetchone()
            print(f"🔧 MySQL版本: {result['version']}")
            
            # 获取当前数据库
            cursor.execute("SELECT DATABASE() as current_db")
            result = cursor.fetchone()
            print(f"📚 当前数据库: {result['current_db']}")
            
            # 获取连接的用户信息
            cursor.execute("SELECT USER() as user, CONNECTION_ID() as connection_id")
            result = cursor.fetchone()
            print(f"👤 连接用户: {result['user']}")
            print(f"🔗 连接ID: {result['connection_id']}")
            
            # 显示数据库中的表（如果连接成功）
            try:
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                print(f"📄 数据库 '{Config.SQL_DB}' 中的表数量: {len(tables)}")
                if tables:
                    print("📋 表列表 (最多显示10个):")
                    for i, table in enumerate(tables[:10]):
                        table_name = list(table.values())[0]  # 获取表名
                        print(f"   {i+1}. {table_name}")
                    if len(tables) > 10:
                        print(f"   ... 还有 {len(tables) - 10} 个表")
            except Exception as e:
                print(f"⚠️  获取表信息时出错: {e}")
        
        # 测试基本查询
        with connection.cursor() as cursor:
            cursor.execute("SHOW STATUS LIKE 'Threads_connected'")
            result = cursor.fetchone()
            print(f"🔗 当前连接数: {result['Value']}")
        
        return True
        
    except pymysql.Error as e:
        print(f"❌ PyMySQL连接错误: {e}")
        return False
        
    except Exception as e:
        print(f"❌ 发生未知错误: {e}")
        return False
        
    finally:
        # 关闭数据库连接
        if connection and connection.open:
            connection.close()
            print("🔒 数据库连接已关闭")

def test_connection_without_db():
    """
    测试不指定数据库的连接
    """
    print("\n" + "=" * 50)
    print("🔍 测试不指定数据库的连接...")
    
    connection_config = {
        'host': Config.SQL_HOST,
        'user': Config.SQL_USERNAME,
        'password': Config.SQL_PASSWORD,
        'port': int(Config.SQL_PORT),
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }
    
    connection = None
    try:
        connection = pymysql.connect(**connection_config)
        print("✅ 成功连接到MySQL服务器 (未指定数据库)!")
        
        with connection.cursor() as cursor:
            # 显示所有数据库
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print(f"📚 可用数据库 ({len(databases)}个):")
            db_names = [list(db.values())[0] for db in databases]
            for i, db_name in enumerate(db_names[:10]):
                print(f"   {i+1}. {db_name}")
            if len(databases) > 10:
                print(f"   ... 还有 {len(databases) - 10} 个数据库")
                
        return True
        
    except pymysql.Error as e:
        print(f"❌ 连接错误: {e}")
        return False
        
    finally:
        if connection and connection.open:
            connection.close()
            print("🔒 数据库连接已关闭")

if __name__ == "__main__":
    print("🧪 PyMySQL连接测试脚本")
    print(f"📍 主机: {Config.SQL_HOST}")
    print(f"👤 用户: {Config.SQL_USERNAME}")
    print(f"🔢 端口: {Config.SQL_PORT}")
    print(f"📂 数据库: {Config.SQL_DB}")
    
    # 测试指定数据库的连接
    success1 = test_pymysql_connection()
    
    # 测试不指定数据库的连接
    success2 = test_connection_without_db()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 所有测试完成，PyMySQL连接正常!")
    else:
        print("💥 部分测试失败，请检查配置信息!")
        sys.exit(1)