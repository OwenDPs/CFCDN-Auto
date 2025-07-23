import os
import requests
from ip_extractor import IPExtractor

# Cloudflare API配置信息 - 与sgfdip.py保持一致
CF_API_KEY = os.getenv('CF_API_KEY')
CF_ZONE_ID = os.getenv('CF_ZONE_ID')
CF_DOMAIN_NAME = os.getenv('CF_DOMAIN_NAME')

# IP提取功能已移至ip_extractor.py模块

# 主函数，处理所有网站的数据
def main():
    # 测试 API 连接
    if not test_cf_api():
        print("Cloudflare API 连接失败，请检查配置")
        return

    print("=== 开始提取IP数据 ===")

    # 创建IP提取器实例
    extractor = IPExtractor()

    # 获取处理后的IP数据（延迟低于100ms，去重）
    filtered_data, ip_addresses = extractor.get_processed_ips(max_latency=100.0, remove_duplicates=True)

    if not filtered_data:
        print("没有获取到符合条件的IP数据")
        return

    # 写入到yx_ips.txt文件
    extractor.save_to_file(filtered_data, 'yx_ips.txt')

    # 执行清空DNS记录的操作
    clear_dns_records()

    # 只选择前2个IP地址用于DNS记录
    selected_ips = ip_addresses[:2]

    # 执行添加DNS记录的操作
    print(f"将添加 {len(selected_ips)} 个DNS记录（最多2个）")
    for ip in selected_ips:
        add_dns_record(ip)

    print("=== IP数据处理完成 ===")

# 清空CF_DOMAIN_NAME的所有DNS记录
def clear_dns_records():
    # 检查必要的环境变量
    if not CF_API_KEY or not CF_ZONE_ID or not CF_DOMAIN_NAME:
        print("警告: Cloudflare API配置不完整，跳过DNS记录清除")
        print(f"  CF_API_KEY: {'已设置' if CF_API_KEY else '未设置'}")
        print(f"  CF_ZONE_ID: {'已设置' if CF_ZONE_ID else '未设置'}")
        print(f"  CF_DOMAIN_NAME: {'已设置' if CF_DOMAIN_NAME else '未设置'}")
        return

    url = f"https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records?name={CF_DOMAIN_NAME}"
    headers = {
        "Authorization": f"Bearer {CF_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        records = response.json().get('result', [])
        for record in records:
            delete_url = f"https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records/{record['id']}"
            delete_response = requests.delete(delete_url, headers=headers)
            if delete_response.status_code == 200:
                print(f"Successfully deleted DNS record: {record['id']}")
            else:
                print(f"Failed to delete DNS record: {record['id']}, status code: {delete_response.status_code}, response: {delete_response.text}")
    else:
        print(f"Failed to fetch DNS records, status code: {response.status_code}, response: {response.text}")

# 添加新的IPv4地址为DNS记录
def add_dns_record(ip):
    # 检查必要的环境变量
    if not CF_API_KEY or not CF_ZONE_ID or not CF_DOMAIN_NAME:
        print("警告: Cloudflare API配置不完整，跳过DNS记录添加")
        return

    print(f"Adding DNS record for IP: {ip}")
    url = f"https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records"
    headers = {
        "Authorization": f"Bearer {CF_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "type": "A",
        "name": CF_DOMAIN_NAME,
        "content": ip,
        "ttl": 60,  # 设置TTL为1分钟
        "proxied": False
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Successfully created DNS record for IP: {ip}")
    else:
        print(f"Failed to create DNS record for IP: {ip}, status code: {response.status_code}, response: {response.text}")

def test_cf_api():
    """测试 Cloudflare API 连接"""
    # 检查必要的环境变量
    if not CF_API_KEY or not CF_ZONE_ID:
        print("警告: Cloudflare API配置不完整")
        print(f"  CF_API_KEY: {'已设置' if CF_API_KEY else '未设置'}")
        print(f"  CF_ZONE_ID: {'已设置' if CF_ZONE_ID else '未设置'}")
        print(f"  CF_DOMAIN_NAME: {'已设置' if CF_DOMAIN_NAME else '未设置'}")
        return False

    url = f"https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}"
    headers = {
        "Authorization": f"Bearer {CF_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    print(f"API Test - Status: {response.status_code}")
    print(f"API Test - Response: {response.text}")

    if response.status_code == 200:
        zone_info = response.json()
        print(f"Zone Name: {zone_info['result']['name']}")
        return True
    return False

if __name__ == "__main__":
    main()
