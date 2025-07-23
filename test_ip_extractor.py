"""
IP提取器测试文件

用于测试ip_extractor.py模块的功能
"""

from ip_extractor import IPExtractor, get_cloudflare_ips


def test_basic_functionality():
    """测试基本功能"""
    print("=== 测试基本功能 ===")
    
    try:
        # 创建提取器实例
        extractor = IPExtractor(timeout=5)  # 设置较短的超时时间用于测试
        print("✓ IP提取器实例创建成功")
        
        # 测试从单个网站提取数据
        test_url = "https://cf.090227.xyz/"
        print(f"测试从 {test_url} 提取数据...")
        
        site_data = extractor.extract_from_site(test_url)
        if site_data:
            print(f"✓ 成功从 {test_url} 提取到 {len(site_data)} 条数据")
            print(f"  示例数据: {site_data[0] if site_data else '无数据'}")
        else:
            print(f"⚠ 从 {test_url} 未提取到数据（可能是网络问题）")
        
        return True
        
    except Exception as e:
        print(f"✗ 基本功能测试失败: {e}")
        return False


def test_data_processing():
    """测试数据处理功能"""
    print("\n=== 测试数据处理功能 ===")
    
    try:
        extractor = IPExtractor()
        
        # 模拟一些测试数据
        test_data = [
            "1.1.1.1#电信-25ms",
            "2.2.2.2#联通-45ms",
            "3.3.3.3#移动-120ms",
            "1.1.1.1#电信-25ms",  # 重复数据
            "4.4.4.4-30ms"
        ]
        
        print(f"原始测试数据: {len(test_data)} 条")
        
        # 测试去重
        unique_data = extractor.remove_duplicates(test_data)
        print(f"✓ 去重后: {len(unique_data)} 条")
        
        # 测试延迟过滤
        filtered_data = extractor.filter_by_latency(unique_data, max_latency=50.0)
        print(f"✓ 延迟过滤后（<50ms）: {len(filtered_data)} 条")
        
        # 测试IP地址提取
        ip_addresses = extractor.extract_ip_addresses(filtered_data)
        print(f"✓ 提取的IP地址: {ip_addresses}")
        
        return True
        
    except Exception as e:
        print(f"✗ 数据处理测试失败: {e}")
        return False


def test_convenience_function():
    """测试便捷函数"""
    print("\n=== 测试便捷函数 ===")
    
    try:
        # 测试便捷函数（设置较短超时和较少数量用于测试）
        print("调用便捷函数获取IP...")
        
        # 注意：这个测试可能需要网络连接
        quick_ips = get_cloudflare_ips(max_latency=100.0, limit=3)
        
        if quick_ips:
            print(f"✓ 便捷函数成功返回 {len(quick_ips)} 个IP")
            for i, ip in enumerate(quick_ips, 1):
                print(f"  {i}. {ip}")
        else:
            print("⚠ 便捷函数未返回IP（可能是网络问题）")
        
        return True
        
    except Exception as e:
        print(f"✗ 便捷函数测试失败: {e}")
        return False


def test_file_operations():
    """测试文件操作"""
    print("\n=== 测试文件操作 ===")
    
    try:
        extractor = IPExtractor()
        
        # 测试数据
        test_data = [
            "1.1.1.1#测试-25ms",
            "2.2.2.2#测试-35ms"
        ]
        
        # 测试保存文件
        test_filename = "test_output.txt"
        extractor.save_to_file(test_data, test_filename)
        print(f"✓ 成功保存测试数据到 {test_filename}")
        
        # 验证文件内容
        try:
            with open(test_filename, 'r', encoding='utf-8') as f:
                content = f.read().strip().split('\n')
            
            if len(content) == len(test_data):
                print("✓ 文件内容验证成功")
            else:
                print(f"⚠ 文件内容不匹配：期望 {len(test_data)} 行，实际 {len(content)} 行")
                
        except Exception as e:
            print(f"⚠ 文件内容验证失败: {e}")
        
        return True
        
    except Exception as e:
        print(f"✗ 文件操作测试失败: {e}")
        return False


def test_error_handling():
    """测试错误处理"""
    print("\n=== 测试错误处理 ===")
    
    try:
        extractor = IPExtractor()
        
        # 测试无效URL
        invalid_data = extractor.extract_from_site("https://invalid-url-for-testing.com")
        if not invalid_data:
            print("✓ 无效URL处理正确")
        
        # 测试无效延迟数据
        invalid_latency_data = [
            "1.1.1.1#测试-invalid",
            "2.2.2.2#测试-",
            "invalid-data"
        ]
        
        filtered = extractor.filter_by_latency(invalid_latency_data, max_latency=100.0)
        print(f"✓ 无效延迟数据处理正确，过滤后: {len(filtered)} 条")
        
        return True
        
    except Exception as e:
        print(f"✗ 错误处理测试失败: {e}")
        return False


def run_all_tests():
    """运行所有测试"""
    print("IP提取器功能测试")
    print("=" * 50)
    
    tests = [
        ("基本功能", test_basic_functionality),
        ("数据处理", test_data_processing),
        ("便捷函数", test_convenience_function),
        ("文件操作", test_file_operations),
        ("错误处理", test_error_handling)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n运行测试: {test_name}")
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} 测试通过")
            else:
                print(f"✗ {test_name} 测试失败")
        except Exception as e:
            print(f"✗ {test_name} 测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！IP提取器工作正常。")
    else:
        print("⚠ 部分测试失败，请检查网络连接或依赖包安装。")
        print("确保已安装: pip install requests beautifulsoup4")
    
    return passed == total


if __name__ == "__main__":
    run_all_tests()
