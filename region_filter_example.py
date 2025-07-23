#!/usr/bin/env python3
"""
地区过滤功能示例

展示如何使用IP提取器的地区过滤功能获取特定地区的IP地址
"""

from ip_extractor import (
    IPExtractor, 
    get_taiwan_ips, get_japan_ips, get_hongkong_ips, get_korea_ips,
    get_singapore_ips, get_us_ips, get_asia_ips, get_ips_by_regions
)


def demo_single_region():
    """演示获取单个地区的IP"""
    print("=== 单个地区IP获取演示 ===")
    
    regions = [
        ("台湾", get_taiwan_ips),
        ("日本", get_japan_ips),
        ("香港", get_hongkong_ips),
        ("韩国", get_korea_ips),
        ("新加坡", lambda **kwargs: get_singapore_ips(use_region_filter=True, **kwargs)),
        ("美国", get_us_ips)
    ]
    
    for region_name, get_func in regions:
        print(f"\n获取{region_name}IP:")
        try:
            ips = get_func(max_latency=120.0, limit=3)
            if ips:
                for i, ip in enumerate(ips, 1):
                    print(f"  {i}. {ip}")
            else:
                print(f"  未找到{region_name}IP")
        except Exception as e:
            print(f"  获取{region_name}IP时出错: {e}")


def demo_multiple_regions():
    """演示获取多个地区的IP"""
    print("\n=== 多个地区IP获取演示 ===")
    
    # 亚洲主要地区
    print("1. 亚洲主要地区IP:")
    try:
        asia_ips = get_ips_by_regions(['SG', 'TW', 'JP', 'HK', 'KR'], max_latency=100.0, limit=5)
        for i, ip in enumerate(asia_ips, 1):
            print(f"   {i}. {ip}")
    except Exception as e:
        print(f"   获取亚洲IP时出错: {e}")
    
    # 欧美地区
    print("\n2. 欧美地区IP:")
    try:
        western_ips = get_ips_by_regions(['US', 'UK', 'DE', 'FR', 'CA'], max_latency=150.0, limit=5)
        for i, ip in enumerate(western_ips, 1):
            print(f"   {i}. {ip}")
    except Exception as e:
        print(f"   获取欧美IP时出错: {e}")
    
    # 使用便捷函数获取亚洲IP
    print("\n3. 使用便捷函数获取亚洲IP:")
    try:
        asia_convenience_ips = get_asia_ips(max_latency=100.0, limit=5)
        for i, ip in enumerate(asia_convenience_ips, 1):
            print(f"   {i}. {ip}")
    except Exception as e:
        print(f"   获取亚洲IP时出错: {e}")


def demo_advanced_filtering():
    """演示高级地区过滤"""
    print("\n=== 高级地区过滤演示 ===")
    
    extractor = IPExtractor()
    
    # 显示支持的地区
    print("支持的地区代码:")
    for region_code, keywords in list(extractor.region_codes.items())[:10]:  # 只显示前10个
        print(f"  {region_code}: {', '.join(keywords[:2])}...")
    print(f"  ... 总共支持 {len(extractor.region_codes)} 个地区")
    
    # 高级过滤：只使用特定数据源
    print("\n高级过滤示例（只使用文本文件和API）:")
    try:
        filtered_data, ip_addresses = extractor.get_ips_by_regions(
            target_regions=['TW', 'JP', 'SG'],
            max_latency=100.0,
            include_html=False,  # 不使用HTML网站（更快）
            include_text=True,   # 使用文本文件
            include_api=True,    # 使用API
            include_local=False, # 不使用本地文件
            max_workers=5        # 并发查询数
        )
        
        print(f"获取到 {len(ip_addresses)} 个台湾/日本/新加坡IP")
        for i, ip in enumerate(ip_addresses[:5], 1):  # 只显示前5个
            print(f"  {i}. {ip}")
            
    except Exception as e:
        print(f"高级过滤时出错: {e}")


def demo_region_detection():
    """演示IP地区检测"""
    print("\n=== IP地区检测演示 ===")
    
    # 测试一些已知的IP地址
    test_ips = [
        "1.1.1.1",      # Cloudflare (US)
        "8.8.8.8",      # Google DNS (US)
        "114.114.114.114",  # 中国DNS
        "168.95.1.1",   # 台湾DNS
    ]
    
    extractor = IPExtractor()
    
    print("检测测试IP的地区:")
    for ip in test_ips:
        try:
            region = extractor.get_ip_region(ip)
            print(f"  {ip} -> {region if region else '未知'}")
        except Exception as e:
            print(f"  {ip} -> 检测失败: {e}")


def demo_practical_usage():
    """演示实际使用场景"""
    print("\n=== 实际使用场景演示 ===")
    
    # 场景1：为CDN选择最近的IP
    print("场景1: 为亚洲用户选择最近的CDN IP")
    try:
        asia_cdn_ips = get_ips_by_regions(['SG', 'TW', 'JP', 'HK'], max_latency=80.0, limit=3)
        print("推荐的亚洲CDN IP:")
        for i, ip in enumerate(asia_cdn_ips, 1):
            print(f"  {i}. {ip}")
    except Exception as e:
        print(f"获取亚洲CDN IP时出错: {e}")
    
    # 场景2：为不同地区的用户提供不同的IP
    print("\n场景2: 为不同地区用户提供专用IP")
    regions_for_users = {
        "中国大陆用户": ['HK', 'TW', 'SG'],
        "日本用户": ['JP', 'KR', 'SG'],
        "欧洲用户": ['UK', 'DE', 'FR', 'NL'],
        "美洲用户": ['US', 'CA', 'BR']
    }
    
    for user_region, target_regions in regions_for_users.items():
        try:
            ips = get_ips_by_regions(target_regions, max_latency=120.0, limit=2)
            print(f"  {user_region}: {ips[:2] if ips else '无可用IP'}")
        except Exception as e:
            print(f"  {user_region}: 获取失败 - {e}")


def main():
    """主函数"""
    print("IP提取器地区过滤功能演示")
    print("=" * 50)
    
    try:
        # 检查依赖
        from ipwhois import IPWhois
        print("✓ ipwhois 模块可用，地区过滤功能正常")
    except ImportError:
        print("✗ ipwhois 模块不可用，请安装: pip install ipwhois")
        print("部分功能将无法使用")
        return
    
    # 运行演示
    demos = [
        demo_single_region,
        demo_multiple_regions,
        demo_advanced_filtering,
        demo_region_detection,
        demo_practical_usage
    ]
    
    for demo in demos:
        try:
            demo()
        except KeyboardInterrupt:
            print("\n用户中断演示")
            break
        except Exception as e:
            print(f"\n演示 {demo.__name__} 时出错: {e}")
            continue
    
    print("\n" + "=" * 50)
    print("演示完成！")
    print("\n使用提示:")
    print("1. 地区过滤需要网络连接查询IP地理信息")
    print("2. 查询速度取决于网络状况和IP数量")
    print("3. 建议先用小数量测试，再进行大批量处理")
    print("4. 某些IP可能无法准确识别地区")


if __name__ == "__main__":
    main()
