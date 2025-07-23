import requests
import os
from ipwhois import IPWhois

# 配置
CF_API_KEY = os.getenv('CF_API_KEY')
CF_ZONE_ID = os.getenv('CF_ZONE_ID')  # 修正环境变量名
CF_DOMAIN_NAME = os.getenv('CF_DOMAIN_NAME')  # 修正环境变量名
FILE_PATH = 'sgfd_ips.txt'
SGCS_FILE_PATH = 'CloudflareST/sgcs.txt'

# 第一步：从URL和本地文件获取IP数据
def get_ip_data():
    url1 = 'https://raw.githubusercontent.com/ymyuuu/IPDB/main/BestCF/bestcfv4.txt'

    print(f"正在从URL获取IP数据: {url1}")
    try:
        response1 = requests.get(url1, timeout=10)
        print(f"URL请求状态码: {response1.status_code}")

        if response1.status_code == 200:
            ip_list1 = response1.text.splitlines()
            print(f"从URL获取到 {len(ip_list1)} 个IP地址")
            # 显示前几个IP作为示例
            if ip_list1:
                print(f"URL中的前5个IP示例: {ip_list1[:5]}")
        else:
            print(f"URL请求失败，状态码: {response1.status_code}")
            ip_list1 = []
    except Exception as e:
        print(f"从URL获取IP数据时出错: {e}")
        ip_list1 = []

    # 从本地文件获取IP数据
    ip_list2 = []
    print(f"检查本地文件: {SGCS_FILE_PATH}")
    if os.path.exists(SGCS_FILE_PATH):
        print(f"本地文件存在，正在读取...")
        try:
            with open(SGCS_FILE_PATH, 'r', encoding='utf-8') as f:
                ip_list2 = f.read().splitlines()
            print(f"从本地文件获取到 {len(ip_list2)} 个IP地址")
            # 显示前几个IP作为示例
            if ip_list2:
                print(f"本地文件中的前5个IP示例: {ip_list2[:5]}")
        except Exception as e:
            print(f"读取本地文件时出错: {e}")
            ip_list2 = []
    else:
        print(f"本地文件不存在: {SGCS_FILE_PATH}")

    # 合并IP地址列表
    ip_list = ip_list1 + ip_list2
    print(f"合并后总共有 {len(ip_list)} 个IP地址")

    return ip_list

# 新步骤：去除IP地址中的速度信息
def clean_ip_data(ip_list):
    cleaned_ips = []
    for ip in ip_list:
        cleaned_ip = ip.split('#')[0]  # 去除速度信息，只保留IP地址
        cleaned_ips.append(cleaned_ip)
    return cleaned_ips

# 第二步：过滤新加坡IP地址，并格式化为IP#SG的形式
def filter_and_format_ips(ip_list):
    singapore_ips = []
    print(f"开始过滤 {len(ip_list)} 个IP地址...")

    for i, ip in enumerate(ip_list):
        clean_ip = ip.split('#')[0].strip()  # 再次确保去除速度信息并去除空格
        print(f"正在处理第 {i+1}/{len(ip_list)} 个IP: {clean_ip}")

        try:
            obj = IPWhois(clean_ip)
            results = obj.lookup_rdap()

            # 打印完整的结果以便调试
            print(f"  IPWhois 查询结果结构: {list(results.keys()) if results else 'None'}")

            # 尝试多种方式获取国家信息
            country = None
            is_singapore = False

            if results:
                # 方法1: 从network字段获取
                if 'network' in results and results['network']:
                    country = results['network'].get('country')
                    print(f"  从network字段获取国家: {country}")

                # 方法2: 从objects字段的地址信息获取
                if 'objects' in results:
                    for _, obj_data in results['objects'].items():
                        if 'contact' in obj_data and 'address' in obj_data['contact']:
                            for addr in obj_data['contact']['address']:
                                if 'value' in addr:
                                    address_text = addr['value'].lower()
                                    print(f"  检查地址文本: {address_text}")

                                    # 检查地址中是否包含新加坡相关关键词
                                    singapore_keywords = ['singapore', 'sg', '新加坡']
                                    for keyword in singapore_keywords:
                                        if keyword in address_text:
                                            is_singapore = True
                                            country = 'SG'
                                            print(f"  ✓ 在地址中发现新加坡关键词: {keyword}")
                                            break

                                    if is_singapore:
                                        break
                        if is_singapore:
                            break

                # 方法3: 检查网络名称是否包含SG
                if not is_singapore and 'network' in results and results['network']:
                    network_name = results['network'].get('name', '').lower()
                    if 'sg' in network_name or 'singapore' in network_name:
                        is_singapore = True
                        country = 'SG'
                        print(f"  ✓ 在网络名称中发现新加坡标识: {network_name}")

            print(f"  最终确定的国家代码: {country}, 是否为新加坡: {is_singapore}")

            if is_singapore or country == 'SG':
                singapore_ips.append(f"{clean_ip}#SG")
                print(f"  ✓ 添加新加坡IP: {clean_ip}")
            else:
                print(f"  ✗ 跳过非新加坡IP: {clean_ip} (国家: {country})")

        except Exception as e:
            print(f"  ✗ 处理IP {clean_ip} 时出错: {e}")

    print(f"过滤完成，找到 {len(singapore_ips)} 个新加坡IP")
    return singapore_ips

# 新步骤：去除重复的IP地址
def remove_duplicate_ips(ip_addresses):
    seen_ips = set()
    unique_ips = []
    for ip in ip_addresses:
        ip_base = ip.split('#')[0]
        if ip_base not in seen_ips:
            seen_ips.add(ip_base)
            unique_ips.append(ip)
    return unique_ips

# 第三步：将格式化后的新加坡IP地址写入到sgfd_ips.txt文件
def write_to_file(ip_addresses):
    try:
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            for ip in ip_addresses:
                f.write(ip + '\n')
        print(f"成功写入 {len(ip_addresses)} 个IP地址到文件 {FILE_PATH}")
    except Exception as e:
        print(f"写入文件时出错: {e}")

# 第四步：清除指定Cloudflare域名的所有DNS记录
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

# 第五步：更新Cloudflare域名的DNS记录为sgfd_ips.txt文件中的IP地址
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

    for ip in ips_to_update:
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

    # 新步骤：去除IP地址中的速度信息
    print("\n步骤2: 清理IP数据")
    cleaned_ip_list = clean_ip_data(ip_list)
    print(f"清理后有 {len(cleaned_ip_list)} 个IP地址")

    # 第二步：过滤并格式化新加坡IP地址
    print("\n步骤3: 过滤新加坡IP地址")
    singapore_ips = filter_and_format_ips(cleaned_ip_list)
    print(f"找到 {len(singapore_ips)} 个新加坡IP地址")

    # 新步骤：去除重复的IP地址
    print("\n步骤4: 去除重复IP地址")
    unique_singapore_ips = remove_duplicate_ips(singapore_ips)
    print(f"去重后有 {len(unique_singapore_ips)} 个唯一的新加坡IP地址")

    # 如果没有找到符合条件的新加坡IP，则不执行任何操作
    if not unique_singapore_ips:
        print("警告: 没有找到新加坡IP地址，保持现有的sgfd_ips.txt文件不变")
        return

    print(f"最终的新加坡IP列表: {unique_singapore_ips}")

    # 第三步：将格式化后的新加坡IP地址写入文件
    print("\n步骤5: 写入IP地址到文件")
    write_to_file(unique_singapore_ips)

    # 第四步：清除指定Cloudflare域名的所有DNS记录
    print("\n步骤6: 清除现有DNS记录")
    clear_dns_records()

    # 第五步：更新Cloudflare域名的DNS记录为sgfd_ips.txt文件中的IP地址
    print("\n步骤7: 更新DNS记录")
    update_dns_records()

    print("\n=== 流程执行完成 ===")

if __name__ == "__main__":
    main()
