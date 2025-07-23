#!/usr/bin/env python3
import os

print("=== 环境变量测试 ===")
print(f"CF_API_KEY: {'已设置' if os.getenv('CF_API_KEY') else '未设置'}")
print(f"CF_ZONE_ID: {'已设置' if os.getenv('CF_ZONE_ID') else '未设置'}")
print(f"CF_DOMAIN_NAME: {'已设置' if os.getenv('CF_DOMAIN_NAME') else '未设置'}")

# 显示实际值（部分隐藏以保护隐私）
api_key = os.getenv('CF_API_KEY')
zone_id = os.getenv('CF_ZONE_ID')
domain_name = os.getenv('CF_DOMAIN_NAME')

if api_key:
    print(f"CF_API_KEY: {api_key[:8]}...{api_key[-4:] if len(api_key) > 12 else api_key}")
else:
    print("CF_API_KEY: None")

if zone_id:
    print(f"CF_ZONE_ID: {zone_id[:8]}...{zone_id[-4:] if len(zone_id) > 12 else zone_id}")
else:
    print("CF_ZONE_ID: None")

if domain_name:
    print(f"CF_DOMAIN_NAME: {domain_name}")
else:
    print("CF_DOMAIN_NAME: None")
