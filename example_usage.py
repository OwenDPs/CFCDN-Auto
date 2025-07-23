"""
IP提取器使用示例

这个文件展示了如何在其他程序中使用ip_extractor.py模块
"""

from ip_extractor import (
    IPExtractor, get_cloudflare_ips, get_singapore_ips,
    get_ips_by_regions, get_taiwan_ips, get_japan_ips,
    get_hongkong_ips, get_korea_ips, get_asia_ips
)


def example_basic_usage():
    """基本使用示例"""
    print("=== 基本使用示例 ===")
    
    # 创建IP提取器实例
    extractor = IPExtractor()
    
    # 获取所有IP数据
    all_ips = extractor.get_all_ips()
    print(f"获取到 {len(all_ips)} 条原始IP数据")
    
    # 去重
    unique_ips = extractor.remove_duplicates(all_ips)
    
    # 按延迟过滤（延迟小于50ms）
    fast_ips = extractor.filter_by_latency(unique_ips, max_latency=50.0)
    
    # 提取纯IP地址
    ip_addresses = extractor.extract_ip_addresses(fast_ips)
    
    print(f"延迟小于50ms的IP地址（前10个）:")
    for i, ip in enumerate(ip_addresses[:10], 1):
        print(f"  {i}. {ip}")
    
    # 保存到文件
    extractor.save_to_file(fast_ips, 'fast_ips.txt')


def example_one_step_processing():
    """一站式处理示例"""
    print("\n=== 一站式处理示例 ===")
    
    extractor = IPExtractor()
    
    # 一次性获取处理后的数据
    filtered_data, ip_addresses = extractor.get_processed_ips(
        max_latency=80.0,  # 延迟小于80ms
        remove_duplicates=True
    )
    
    print(f"处理后的IP地址（前5个）:")
    for i, ip in enumerate(ip_addresses[:5], 1):
        print(f"  {i}. {ip}")
    
    return ip_addresses


def example_custom_sites():
    """自定义网站示例"""
    print("\n=== 自定义网站示例 ===")
    
    extractor = IPExtractor()
    
    # 只从特定网站获取数据
    custom_urls = [
        "https://cf.090227.xyz/",
        "https://ip.164746.xyz/"
    ]
    
    custom_ips = extractor.get_all_ips(urls=custom_urls)
    print(f"从自定义网站获取到 {len(custom_ips)} 条IP数据")
    
    # 处理数据
    unique_ips = extractor.remove_duplicates(custom_ips)
    filtered_ips = extractor.filter_by_latency(unique_ips, max_latency=100.0)
    ip_addresses = extractor.extract_ip_addresses(filtered_ips)
    
    return ip_addresses


def example_convenience_function():
    """便捷函数示例"""
    print("\n=== 便捷函数示例 ===")

    # 使用便捷函数快速获取IP（包含所有数据源）
    all_source_ips = get_cloudflare_ips(max_latency=60.0, limit=5, include_all_sources=True)
    print(f"从所有数据源获取的IP地址（延迟<60ms，限制5个）:")
    for i, ip in enumerate(all_source_ips, 1):
        print(f"  {i}. {ip}")

    # 只从HTML网站获取IP
    html_only_ips = get_cloudflare_ips(max_latency=60.0, limit=5, include_all_sources=False)
    print(f"\n只从HTML网站获取的IP地址（延迟<60ms，限制5个）:")
    for i, ip in enumerate(html_only_ips, 1):
        print(f"  {i}. {ip}")

    # 获取新加坡IP（主要来自API和本地文件）
    sg_ips = get_singapore_ips(max_latency=100.0, limit=3)
    print(f"\n新加坡IP地址（限制3个）:")
    for i, ip in enumerate(sg_ips, 1):
        print(f"  {i}. {ip}")

    return all_source_ips


def example_different_data_sources():
    """不同数据源示例"""
    print("\n=== 不同数据源示例 ===")

    extractor = IPExtractor()

    # 只从HTML网站获取数据
    print("1. 只从HTML网站获取数据:")
    html_data, html_ips = extractor.get_ips_from_specific_sources(
        include_html=True,
        include_text=False,
        include_api=False,
        include_local=False,
        max_latency=100.0
    )
    print(f"   获取到 {len(html_ips)} 个IP地址")

    # 只从文本文件和API获取数据
    print("\n2. 只从文本文件和API获取数据:")
    text_api_data, text_api_ips = extractor.get_ips_from_specific_sources(
        include_html=False,
        include_text=True,
        include_api=True,
        include_local=False,
        max_latency=100.0
    )
    print(f"   获取到 {len(text_api_ips)} 个IP地址")

    # 只从本地文件获取数据
    print("\n3. 只从本地文件获取数据:")
    local_data, local_ips = extractor.get_ips_from_specific_sources(
        include_html=False,
        include_text=False,
        include_api=False,
        include_local=True,
        max_latency=100.0
    )
    print(f"   获取到 {len(local_ips)} 个IP地址")

    # 从所有数据源获取数据
    print("\n4. 从所有数据源获取数据:")
    all_data, all_ips = extractor.get_ips_from_specific_sources(
        include_html=True,
        include_text=True,
        include_api=True,
        include_local=True,
        max_latency=100.0
    )
    print(f"   获取到 {len(all_ips)} 个IP地址")

    return all_ips


def example_region_filtering():
    """地区过滤示例"""
    print("\n=== 地区过滤示例 ===")

    # 使用便捷函数获取特定地区的IP
    print("1. 使用便捷函数获取特定地区IP:")

    # 获取台湾IP
    print("   获取台湾IP:")
    taiwan_ips = get_taiwan_ips(max_latency=100.0, limit=3)
    for i, ip in enumerate(taiwan_ips, 1):
        print(f"     {i}. {ip}")

    # 获取日本IP
    print("   获取日本IP:")
    japan_ips = get_japan_ips(max_latency=100.0, limit=3)
    for i, ip in enumerate(japan_ips, 1):
        print(f"     {i}. {ip}")

    # 获取香港IP
    print("   获取香港IP:")
    hk_ips = get_hongkong_ips(max_latency=100.0, limit=3)
    for i, ip in enumerate(hk_ips, 1):
        print(f"     {i}. {ip}")

    print("\n2. 获取多个地区的IP:")
    # 获取多个亚洲地区的IP
    multi_region_ips = get_ips_by_regions(['SG', 'TW', 'JP', 'HK'], max_latency=100.0, limit=5)
    print(f"   获取新加坡、台湾、日本、香港的IP:")
    for i, ip in enumerate(multi_region_ips, 1):
        print(f"     {i}. {ip}")

    print("\n3. 使用IP提取器进行高级地区过滤:")
    extractor = IPExtractor()

    # 获取指定地区的IP（带详细信息）
    filtered_data, ip_addresses = extractor.get_ips_by_regions(
        target_regions=['TW', 'JP'],
        max_latency=80.0,
        include_html=False,  # 不使用HTML网站（速度更快）
        include_text=True,   # 使用文本文件
        include_api=True,    # 使用API
        include_local=False  # 不使用本地文件
    )

    print(f"   高级过滤获取到 {len(ip_addresses)} 个台湾/日本IP")

    return multi_region_ips


def example_region_codes():
    """地区代码示例"""
    print("\n=== 支持的地区代码示例 ===")

    extractor = IPExtractor()

    print("支持的地区代码:")
    for region_code, keywords in extractor.region_codes.items():
        print(f"  {region_code}: {', '.join(keywords[:3])}...")  # 只显示前3个关键词

    print(f"\n总共支持 {len(extractor.region_codes)} 个地区")

    # 示例：获取欧洲地区的IP
    print("\n获取欧洲地区IP示例:")
    european_regions = ['UK', 'DE', 'FR', 'NL', 'CH', 'SE', 'NO', 'FI', 'DK']
    try:
        eu_ips = get_ips_by_regions(european_regions, max_latency=120.0, limit=3)
        print(f"获取到 {len(eu_ips)} 个欧洲IP")
        for i, ip in enumerate(eu_ips, 1):
            print(f"  {i}. {ip}")
    except Exception as e:
        print(f"获取欧洲IP时出错: {e}")


def example_for_other_programs():
    """供其他程序使用的示例"""
    print("\n=== 供其他程序使用的示例 ===")
    
    # 场景1：获取最快的5个IP用于DNS更新
    def get_fastest_ips_for_dns(count=5):
        extractor = IPExtractor()
        _, ip_addresses = extractor.get_processed_ips(max_latency=50.0)
        return ip_addresses[:count]
    
    # 场景2：获取特定延迟范围的IP
    def get_ips_by_latency_range(min_latency=20.0, max_latency=80.0):
        extractor = IPExtractor()
        all_ips = extractor.get_all_ips()
        unique_ips = extractor.remove_duplicates(all_ips)
        
        # 自定义过滤逻辑
        filtered_ips = []
        for line in unique_ips:
            try:
                latency_str = line.split('-')[-1].replace('ms', '')
                latency_value = float(latency_str)
                if min_latency <= latency_value <= max_latency:
                    filtered_ips.append(line)
            except (ValueError, IndexError):
                continue
        
        return extractor.extract_ip_addresses(filtered_ips)
    
    # 场景3：获取特定线路的IP（如电信、联通、移动）
    def get_ips_by_line_type(line_keywords=['电信', '联通', '移动']):
        extractor = IPExtractor()
        all_ips = extractor.get_all_ips()
        
        # 过滤包含特定线路关键词的IP
        line_filtered_ips = []
        for line in all_ips:
            if '#' in line:  # 包含线路信息
                for keyword in line_keywords:
                    if keyword in line:
                        line_filtered_ips.append(line)
                        break
        
        unique_ips = extractor.remove_duplicates(line_filtered_ips)
        filtered_ips = extractor.filter_by_latency(unique_ips, max_latency=100.0)
        return extractor.extract_ip_addresses(filtered_ips)
    
    # 测试这些函数
    fastest_ips = get_fastest_ips_for_dns(3)
    print(f"最快的3个IP（用于DNS）: {fastest_ips}")
    
    range_ips = get_ips_by_latency_range(30.0, 70.0)
    print(f"延迟在30-70ms之间的IP数量: {len(range_ips)}")
    
    line_ips = get_ips_by_line_type(['电信', '联通'])
    print(f"电信/联通线路的IP数量: {len(line_ips)}")


def example_integration_with_dns():
    """与DNS更新集成的示例"""
    print("\n=== 与DNS更新集成示例 ===")
    
    def update_dns_with_best_ips(domain_name, max_count=2):
        """
        获取最佳IP并更新DNS记录的示例函数
        
        Args:
            domain_name: 域名
            max_count: 最大IP数量
        """
        # 获取最佳IP
        extractor = IPExtractor()
        _, ip_addresses = extractor.get_processed_ips(max_latency=80.0)
        
        # 选择前N个IP
        selected_ips = ip_addresses[:max_count]
        
        print(f"为域名 {domain_name} 选择的IP地址:")
        for i, ip in enumerate(selected_ips, 1):
            print(f"  {i}. {ip}")
        
        # 这里可以调用实际的DNS更新函数
        # 例如：update_cloudflare_dns(domain_name, selected_ips)
        
        return selected_ips
    
    # 示例调用
    selected_ips = update_dns_with_best_ips("cdn.example.com", max_count=2)
    print(f"选择了 {len(selected_ips)} 个IP用于DNS更新")


def main():
    """主函数，运行所有示例"""
    print("IP提取器使用示例")
    print("=" * 50)
    
    try:
        # 运行各种示例
        example_basic_usage()
        example_one_step_processing()
        example_custom_sites()
        example_convenience_function()
        example_different_data_sources()
        example_region_filtering()
        example_region_codes()
        example_for_other_programs()
        example_integration_with_dns()
        
        print("\n" + "=" * 50)
        print("所有示例运行完成！")
        
    except Exception as e:
        print(f"运行示例时出错: {e}")
        print("请确保已正确安装依赖包：pip install requests beautifulsoup4")


if __name__ == "__main__":
    main()
