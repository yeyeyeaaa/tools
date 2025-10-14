#!/usr/bin/env python3
import sys
import subprocess
import importlib

# ========== 自动检测并安装依赖 ==========
def ensure_package(package: str):
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"未检测到依赖 [{package}]，正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--prefer-binary"])
        print(f"✅ 依赖 [{package}] 安装完成。")

# 需要的依赖列表
for pkg in ["pandas", "tabulate"]:
    ensure_package(pkg)

import pandas as pd
from tabulate import tabulate

def main():
    if len(sys.argv) != 2:
        print("用法: python3 view_xlsx.py 文件.xlsx")
        sys.exit(1)

    file = sys.argv[1]
    try:
        # 获取所有Sheet名称
        sheets = pd.ExcelFile(file).sheet_names
        if not sheets:
            print("错误: 未找到任何子表")
            sys.exit(1)

        # 交互选择Sheet
        if len(sheets) > 1:
            print("请选择子表:")
            for i, name in enumerate(sheets, 1):
                print(f"{i}) {name}")
            choice = int(input("输入数字: ")) - 1
            sheet = sheets[choice]
        else:
            sheet = sheets[0]

        # 读取并显示数据
        df = pd.read_excel(file, sheet_name=sheet)
        print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))

    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
