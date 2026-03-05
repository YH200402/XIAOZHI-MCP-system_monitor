#!/usr/bin/env python3
"""
示例脚本：展示如何使用系统监控 MCP 工具
"""

from fastmcp import FastMCP
import time

def main():
    # 初始化 MCP 客户端
    print("初始化 MCP 客户端...")
    client = FastMCP()
    print("客户端初始化完成！")
    
    # 测试系统监控功能
    print("\n=== 测试系统监控功能 ===")
    try:
        result = client.system_monitor()
        if result.get("success"):
            sys_info = result.get("result")
            print(f"内存使用率: {sys_info.get('memory_usage_percent')}%")
            print(f"CPU 使用率: {sys_info.get('cpu_usage_percent')}%")
            print(f"磁盘使用率: {sys_info.get('disk_usage_percent')}%")
            print(f"GPU 使用率: {sys_info.get('gpu_usage_percent')}%")
            print(f"时间戳: {sys_info.get('timestamp')}")
        else:
            print(f"系统监控失败: {result.get('error')}")
    except Exception as e:
        print(f"调用系统监控工具时出错: {e}")
    
    # 测试日期时间工具
    print("\n=== 测试日期时间工具 ===")
    try:
        # 获取当前时间
        now_result = client.datetime_tool(action="now")
        if now_result.get("success"):
            now_info = now_result.get("result")
            print(f"当前时间: {now_info.get('datetime')}")
            print(f"当前日期: {now_info.get('date')}")
            print(f"当前时间: {now_info.get('time')}")
            print(f"时间戳: {now_info.get('timestamp')}")
        else:
            print(f"获取当前时间失败: {now_result.get('error')}")
    except Exception as e:
        print(f"调用日期时间工具时出错: {e}")
    
    # 测试文件工具
    print("\n=== 测试文件工具 ===")
    try:
        # 列出当前目录内容
        list_result = client.file_tool(action="list", directory=".")
        if list_result.get("success"):
            files = list_result.get("result")
            print("当前目录内容:")
            for file in files:
                print(f"  - {file}")
        else:
            print(f"列出目录内容失败: {list_result.get('error')}")
    except Exception as e:
        print(f"调用文件工具时出错: {e}")
    
    print("\n示例脚本执行完成！")

if __name__ == "__main__":
    main()