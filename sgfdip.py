import requests
import os
from ip_extractor import IPExtractor

# 配置
CF_API_KEY = os.getenv('CF_API_KEY')
CF_ZONE_ID = os.getenv('CF_ZONE_ID')
CF_DOMAIN_NAME = os.getenv('CF_DOMAIN_NAME')
FILE_PATH = 'sgfd_ips.txt'

# 第一步：从多个数据源获取IP数据（使用IP提取器）
def get_ip_data():
    print("=== 使用IP提取器获取IP数据 ===")

    # 创建IP提取器实例
    extractor = IPExtractor()

    # 严格按照参数获取新加坡、台湾、日本的IP（延迟小于200ms）
    print("正在获取新加坡、台湾、日本的IP数据（延迟<200ms）...")
    print("注意: 将严格按照地区和延迟条件过滤，如果没有符合条件的IP将返回空")

    _, ip_addresses = extractor.get_ips_by_regions(
        target_regions=['SG', 'TW', 'JP'],  # 新加坡、台湾、日本
        max_latency=200.0,                  # 延迟小于200ms
        include_html=True,                  # 使用HTML网站数据源
        include_text=True,                  # 使用文本文件URL
        include_api=True,                   # 使用API源
        include_local=True,                 # 使用本地文件
        max_workers=10                      # 并发查询数
    )

    if ip_addresses:
        print(f"✓ 成功获取到 {len(ip_addresses)} 个符合条件的IP")
    else:
        print("✗ 未找到符合条件的IP（新加坡、台湾、日本且延迟<200ms）")
        print("可能的原因:")
        print("  1. 当前没有符合延迟要求的IP")
        print("  2. IP地理位置查询失败")
        print("  3. 数据源暂时不可用")
        print("  4. ipwhois模块未正确安装")

    # 将IP地址转换为原始格式（sgfdip.py期望的格式）
    ip_list = ip_addresses  # 这里返回纯IP地址列表

    print(f"IP提取器获取到总共 {len(ip_list)} 个IP地址")

    # 显示前几个IP作为示例
    if ip_list:
        print(f"前5个IP示例: {ip_list[:5]}")

    return ip_list



# 将IP地址写入到sgfd_ips.txt文件
def write_to_file(ip_addresses):
    try:
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            for ip in ip_addresses:
                f.write(ip + '\n')
        print(f"成功写入 {len(ip_addresses)} 个IP地址到文件 {FILE_PATH}")
    except Exception as e:
        print(f"写入文件时出错: {e}")

# 清除指定Cloudflare域名的所有DNS记录
def clear_dns_records():
    # 检查必要的环境变量
    if not CF_API_KEY or not CF_ZONE_ID or not CF_DOMAIN_NAME:
        print("警告: Cloudflare API配置不完整，跳过DNS记录清除")
        print(f"  CF_API_KEY: {'已设置' if CF_API_KEY else '未设置'}")
        print(f"  CF_ZONE_ID: {'已设置' if CF_ZONE_ID else '未设置'}")
        print(f"  CF_DOMAIN_NAME: {'已设置' if CF_DOMAIN_NAME else '未设置'}")
        return

    headers = {
        'Authorization': f'Bearer {CF_API_KEY}',
        'Content-Type': 'application/json',
    }

    # 获取现有的DNS记录
    dns_records_url = f'https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records'
    try:
        response = requests.get(dns_records_url, headers=headers)
        print(f"DNS记录查询响应状态码: {response.status_code}")

        if response.status_code != 200:
            print(f"获取DNS记录失败: {response.text}")
            return

        dns_records = response.json()

        if not dns_records or 'result' not in dns_records:
            print("DNS记录响应格式异常或为空")
            return

        print(f"找到 {len(dns_records['result'])} 条DNS记录")

        # 删除旧的DNS记录
        deleted_count = 0
        for record in dns_records['result']:
            if record['name'] == CF_DOMAIN_NAME:
                delete_url = f'https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records/{record["id"]}'
                delete_response = requests.delete(delete_url, headers=headers)
                if delete_response.status_code == 200:
                    print(f"成功删除DNS记录: {record['name']} -> {record['content']}")
                    deleted_count += 1
                else:
                    print(f"删除DNS记录失败: {delete_response.text}")

        print(f"总共删除了 {deleted_count} 条DNS记录")

    except Exception as e:
        print(f"清除DNS记录时出错: {e}")

# 更新Cloudflare域名的DNS记录为sgfd_ips.txt文件中的IP地址
def update_dns_records():
    # 检查必要的环境变量
    if not CF_API_KEY or not CF_ZONE_ID or not CF_DOMAIN_NAME:
        print("警告: Cloudflare API配置不完整，跳过DNS记录更新")
        return

    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            ips_to_update = [line.split('#')[0].strip() for line in f if line.strip()]
    except Exception as e:
        print(f"读取IP文件时出错: {e}")
        return

    if not ips_to_update:
        print("没有找到要更新的IP地址")
        return

    headers = {
        'Authorization': f'Bearer {CF_API_KEY}',
        'Content-Type': 'application/json',
    }

    dns_records_url = f'https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records'
    success_count = 0

    for ip in ips_to_update[:2]:  # 只取前两个IP
        if not ip:  # 跳过空行
            continue

        data = {
            'type': 'A',
            'name': CF_DOMAIN_NAME,
            'content': ip,
            'ttl': 60,
            'proxied': False,
        }

        try:
            response = requests.post(dns_records_url, headers=headers, json=data)
            if response.status_code == 200:
                print(f"成功更新DNS记录: {CF_DOMAIN_NAME} -> {ip}")
                success_count += 1
            else:
                print(f"更新DNS记录失败: {CF_DOMAIN_NAME} -> {ip}, 状态码: {response.status_code}")
                print(f"错误详情: {response.text}")
        except Exception as e:
            print(f"更新DNS记录时出错: {ip}, 错误: {e}")

    print(f"DNS记录更新完成，成功更新 {success_count}/{len(ips_to_update)} 条记录")

# 主函数：按顺序执行所有步骤
def main():
    print("=== 开始执行IP获取和DNS更新流程 ===")

    # 第一步：获取IP数据
    print("\n步骤1: 获取IP数据")
    ip_list = get_ip_data()

    if not ip_list:
        print("错误: 没有获取到任何IP数据")
        return

    # 为IP添加地区标识（IP提取器已经进行了地区过滤和去重）
    print("\n步骤2: 格式化IP数据")
    formatted_ips = [f"{ip}#SGTWJP" for ip in ip_list]  # 添加地区标识
    print(f"格式化后有 {len(formatted_ips)} 个IP地址")

    # 严格检查：如果没有找到符合条件的IP，则停止执行
    if not formatted_ips:
        print("错误: 没有找到符合条件的IP地址")
        print("程序将退出，不会修改现有的DNS记录")
        print("建议:")
        print("  1. 检查网络连接")
        print("  2. 确认ipwhois模块已正确安装: pip install ipwhois")
        print("  3. 稍后重试，可能是数据源暂时不可用")
        print("  4. 考虑调整延迟阈值或目标地区")
        return

    print(f"最终的IP列表: {formatted_ips}")

    # 将IP地址写入文件
    print("\n步骤3: 写入IP地址到文件")
    write_to_file(formatted_ips)

    # 清除指定Cloudflare域名的所有DNS记录
    print("\n步骤4: 清除现有DNS记录")
    clear_dns_records()

    # 更新Cloudflare域名的DNS记录为sgfd_ips.txt文件中的IP地址
    print("\n步骤5: 更新DNS记录")
    update_dns_records()

    print("\n=== 流程执行完成 ===")

if __name__ == "__main__":
    main()
