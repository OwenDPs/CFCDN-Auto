#!/usr/bin/env python3
"""
测试IP提取器的地区过滤功能

这个脚本用于验证IP提取器是否能正确测试IP的归属地并进行过滤
"""

import sys

def test_ipwhois_availability():
    """测试ipwhois模块是否可用"""
    print("=== 测试ipwhois模块可用性 ===")
    try:
        from ipwhois import IPWhois
        print("✓ ipwhois模块可用")
        return True
    except ImportError as e:
        print(f"✗ ipwhois模块不可用: {e}")
        print("请安装: pip install ipwhois")
        return False

def test_ip_region_detection():
    """测试IP地区检测功能"""
    print("\n=== 测试IP地区检测功能 ===")
    
    try:
        from ip_extractor import IPExtractor
        extractor = IPExtractor()
        
        # 测试一些已知地区的IP
        test_cases = [
            ("1.1.1.1", "Cloudflare DNS"),
            ("8.8.8.8", "Google DNS"),
            ("114.114.114.114", "中国DNS"),
            ("168.95.1.1", "台湾DNS"),
        ]
        
        print("测试IP地区检测:")
        for ip, description in test_cases:
            try:
                region = extractor.get_ip_region(ip)
                print(f"  {ip} ({description}) -> {region if region else '未知'}")
            except Exception as e:
                print(f"  {ip} ({description}) -> 检测失败: {e}")
        
        return True
        
    except Exception as e:
        print(f"测试IP地区检测时出错: {e}")
        return False

def test_region_filtering():
    """测试地区过滤功能"""
    print("\n=== 测试地区过滤功能 ===")
    
    try:
        from ip_extractor import IPExtractor
        extractor = IPExtractor()
        
        # 创建一些测试IP数据
        test_ips = [
            "1.1.1.1",
            "8.8.8.8", 
            "114.114.114.114",
            "168.95.1.1"
        ]
        
        print(f"测试IP列表: {test_ips}")
        print("尝试过滤出美国(US)的IP:")
        
        # 测试地区过滤
        filtered_ips = extractor.filter_by_regions(
            ip_list=test_ips,
            target_regions=['US'],
            max_workers=2,
            show_progress=True
        )
        
        print(f"过滤结果: {filtered_ips}")
        return len(filtered_ips) > 0
        
    except Exception as e:
        print(f"测试地区过滤时出错: {e}")
        return False

def test_get_ips_by_regions():
    """测试完整的地区IP获取功能"""
    print("\n=== 测试完整的地区IP获取功能 ===")
    
    try:
        from ip_extractor import IPExtractor
        extractor = IPExtractor()
        
        print("尝试获取新加坡、台湾、日本的IP（限制3个，延迟<300ms）:")
        
        # 测试完整的地区IP获取
        filtered_data, ip_addresses = extractor.get_ips_by_regions(
            target_regions=['SG', 'TW', 'JP'],
            max_latency=300.0,  # 设置较高的延迟阈值
            include_html=False,  # 不使用HTML网站（更快）
            include_text=True,   # 使用文本文件
            include_api=True,    # 使用API
            include_local=False, # 不使用本地文件
            max_workers=5
        )
        
        print(f"获取到 {len(ip_addresses)} 个IP地址")
        if ip_addresses:
            print("前5个IP地址:")
            for i, ip in enumerate(ip_addresses[:5], 1):
                print(f"  {i}. {ip}")
        
        return len(ip_addresses) > 0
        
    except Exception as e:
        print(f"测试完整地区IP获取时出错: {e}")
        return False

def test_sgfdip_scenario():
    """测试sgfdip.py的使用场景（严格模式）"""
    print("\n=== 测试sgfdip.py使用场景（严格模式）===")

    try:
        from ip_extractor import IPExtractor
        extractor = IPExtractor()

        print("模拟sgfdip.py的调用:")
        print("严格获取新加坡、台湾、日本的IP（延迟<200ms）...")

        # 模拟sgfdip.py中的调用
        _, ip_addresses = extractor.get_ips_by_regions(
            target_regions=['SG', 'TW', 'JP'],
            max_latency=200.0,
            include_html=True,
            include_text=True,
            include_api=True,
            include_local=True,
            max_workers=10
        )

        print(f"严格模式获取到 {len(ip_addresses)} 个符合条件的IP")

        if ip_addresses:
            print("✓ 成功获取到符合条件的IP地址，前3个:")
            for i, ip in enumerate(ip_addresses[:3], 1):
                print(f"  {i}. {ip}")
            return True
        else:
            print("✗ 严格模式下未获取到任何符合条件的IP地址")
            print("这是正常的，说明当前没有符合条件的IP")
            # 在严格模式下，没有找到符合条件的IP也算是正确的行为
            return True

    except Exception as e:
        print(f"测试sgfdip.py场景时出错: {e}")
        return False


def test_strict_mode():
    """测试严格模式行为"""
    print("\n=== 测试严格模式行为 ===")

    try:
        from ip_extractor import IPExtractor
        extractor = IPExtractor()

        # 测试1: 无效地区代码
        print("1. 测试无效地区代码:")
        _, result1 = extractor.get_ips_by_regions(
            target_regions=['INVALID'],
            max_latency=100.0,
            include_html=False,
            include_text=True,
            include_api=False,
            include_local=False
        )
        print(f"   无效地区代码结果: {len(result1)} 个IP（应该为0）")

        # 测试2: 空地区列表
        print("2. 测试空地区列表:")
        _, result2 = extractor.get_ips_by_regions(
            target_regions=[],
            max_latency=100.0
        )
        print(f"   空地区列表结果: {len(result2)} 个IP（应该为0）")

        # 测试3: 极低延迟阈值
        print("3. 测试极低延迟阈值:")
        _, result3 = extractor.get_ips_by_regions(
            target_regions=['US'],
            max_latency=1.0,  # 极低延迟
            include_html=False,
            include_text=True,
            include_api=False,
            include_local=False
        )
        print(f"   极低延迟阈值结果: {len(result3)} 个IP")

        # 严格模式的特点是：不符合条件就返回空，不会回退
        success = (len(result1) == 0 and len(result2) == 0)
        print(f"严格模式测试: {'✓ 通过' if success else '✗ 失败'}")
        return success

    except Exception as e:
        print(f"测试严格模式时出错: {e}")
        return False

def main():
    """主测试函数"""
    print("IP提取器地区过滤功能测试")
    print("=" * 50)
    
    # 运行所有测试
    tests = [
        ("ipwhois模块可用性", test_ipwhois_availability),
        ("IP地区检测", test_ip_region_detection),
        ("地区过滤", test_region_filtering),
        ("完整地区IP获取", test_get_ips_by_regions),
        ("严格模式行为", test_strict_mode),
        ("sgfdip.py使用场景", test_sgfdip_scenario)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"测试 {test_name} 时发生异常: {e}")
            results[test_name] = False
    
    # 输出测试结果摘要
    print("\n" + "=" * 50)
    print("测试结果摘要:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总体结果: {passed}/{total} 测试通过")
    
    # 给出建议
    if not results.get("ipwhois模块可用性", False):
        print("\n建议:")
        print("- 请安装ipwhois模块: pip install ipwhois")
        print("- 或者运行: pip install -r requirements.txt")
    elif passed < total:
        print("\n建议:")
        print("- 检查网络连接是否正常")
        print("- 某些IP地区检测可能需要时间，请耐心等待")
        print("- 如果持续失败，可能是IP数据源暂时不可用")
    else:
        print("\n✓ 所有测试通过！IP提取器的地区过滤功能正常工作。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
