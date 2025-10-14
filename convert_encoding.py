#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import importlib
from pathlib import Path

# ========== 自动检测并安装依赖 ==========
def ensure_package(package: str):
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"未检测到依赖 [{package}]，正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--prefer-binary"])
        print(f"✅ 依赖 [{package}] 安装完成。")

# 需要的依赖列表
for pkg in ["chardet"]:
    ensure_package(pkg)

# ========= 导入依赖 =========
import chardet

def detect_encoding(file_path: str) -> dict:
    """检测文件的编码格式"""
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    return chardet.detect(raw_data)

def convert_encoding(
    file_path: str,
    target_encoding: str = 'utf-8',
    source_encoding: str = None
) -> str:
    """转换文件编码到目标编码（默认UTF-8）"""
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    
    # 如果没有指定源编码，则自动检测
    if not source_encoding:
        detection = chardet.detect(raw_data)
        source_encoding = detection['encoding']
        confidence = detection['confidence']
        print(f"检测到编码: {source_encoding} (置信度: {confidence:.2%})")
    
    try:
        decoded_text = raw_data.decode(source_encoding)
    except UnicodeDecodeError as e:
        print(f"错误：无法用 {source_encoding} 解码文件！")
        print(f"详细错误: {e}")
        return None
    
    # 转换为目标编码
    try:
        encoded_data = decoded_text.encode(target_encoding)
        return encoded_data.decode(target_encoding)
    except UnicodeEncodeError as e:
        print(f"错误：无法转换为 {target_encoding}！")
        print(f"详细错误: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python detect_and_convert_encoding.py <文件路径> [目标编码]")
        print("示例: python detect_and_convert_encoding.py test.txt utf-8")
        sys.exit(1)
    
    file_path = sys.argv[1]
    target_encoding = sys.argv[2] if len(sys.argv) > 2 else 'utf-8'
    
    if not Path(file_path).exists():
        print(f"错误：文件 {file_path} 不存在！")
        sys.exit(1)
    
    print(f"正在处理文件: {file_path}")
    converted_text = convert_encoding(file_path, target_encoding)
    
    if converted_text:
        print("\n转换后的文本内容：")
        print("----------------------")
        print(converted_text)
        print("----------------------")
    else:
        print("转换失败，请检查文件编码或尝试手动指定编码。")
