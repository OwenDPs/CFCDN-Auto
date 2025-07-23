#!/usr/bin/env python3
"""
IP提取器调试脚本
用于诊断IP提取器无法获取数据的问题
"""

import sys
import traceback

def test_basic_imports():
    """测试基本导入"""
    print("=== 测试基本导入 ===")
    try:
        import requests
        print("✓ requests 导入成功")
    except ImportError as e:
        print(f"✗ requests 导入失败: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✓ BeautifulSoup 导入成功")
    except ImportError as e:
        print(f"✗ BeautifulSoup 导入失败: {e}")
        return False
    
    try:
        from ip_extractor import IPExtractor
        print("✓ IPExtractor 导入成功")
        return True
    except ImportError as e:
        print(f"✗ IPExtractor 导入失败: {e}")
        return False

def test_text_url():
    """测试文本URL数据源"""
    print("\n=== 测试文本URL数据源 ===")
    try:
        from ip_extractor import IPExtractor
        extractor = IPExtractor()
        
        url = "https://raw.githubusercontent.com/ymyuuu/IPDB/main/BestCF/bestcfv4.txt"
        print(f"测试URL: {url}")
        
        data = extractor.extract_from_text_url(url)
        print(f"获取到 {len(data)} 条数据")
        
        if data:
            print(f"前5条数据: {data[:5]}")
            return True
        else:
            print("未获取到任何数据")
            return False
            
    except Exception as e:
        print(f"测试文本URL时出错: {e}")
        traceback.print_exc()
        return False

def test_api_source():
    """测试API数据源"""
    print("\n=== 测试API数据源 ===")
    try:
        from ip_extractor import IPExtractor
        extractor = IPExtractor()
        
        api_config = {
            'url': 'https://api.hostmonit.com/get_optimization_ip',
            'method': 'POST',
            'headers': {'Content-Type': 'application/json'},
            'data': {"key": "o1zrmHAF", "type": "v4"},
            'parser': 'hostmonit_api'
        }
        
        print(f"测试API: {api_config['url']}")
        
        data = extractor.extract_from_api(api_config)
        print(f"获取到 {len(data)} 条数据")
        
        if data:
            print(f"前5条数据: {data[:5]}")
            return True
        else:
            print("未获取到任何数据")
            return False
            
    except Exception as e:
        print(f"测试API时出错: {e}")
        traceback.print_exc()
        return False

def test_local_file():
    """测试本地文件数据源"""
    print("\n=== 测试本地文件数据源 ===")
    try:
        from ip_extractor import IPExtractor
        extractor = IPExtractor()
        
        file_path = 'CloudflareST/sgcs.txt'
        print(f"测试本地文件: {file_path}")
        
        data = extractor.extract_from_local_file(file_path)
        print(f"获取到 {len(data)} 条数据")
        
        if data:
            print(f"前5条数据: {data[:5]}")
            return True
        else:
            print("未获取到任何数据（文件可能不存在或为空）")
            return False
            
    except Exception as e:
        print(f"测试本地文件时出错: {e}")
        traceback.print_exc()
        return False

def test_specific_sources():
    """测试特定数据源组合"""
    print("\n=== 测试特定数据源组合 ===")
    try:
        from ip_extractor import IPExtractor
        extractor = IPExtractor()
        
        print("测试：只使用文本文件和API")
        filtered_data, ip_addresses = extractor.get_ips_from_specific_sources(
            include_html=False,
            include_text=True,
            include_api=True,
            include_local=False,
            max_latency=1000.0
        )
        
        print(f"获取到 {len(ip_addresses)} 个IP地址")
        
        if ip_addresses:
            print(f"前5个IP: {ip_addresses[:5]}")
            return True
        else:
            print("未获取到任何IP地址")
            return False
            
    except Exception as e:
        print(f"测试特定数据源时出错: {e}")
        traceback.print_exc()
        return False

def test_network_connectivity():
    """测试网络连接"""
    print("\n=== 测试网络连接 ===")
    try:
        import requests
        
        # 测试基本网络连接
        test_urls = [
            "https://httpbin.org/ip",
            "https://raw.githubusercontent.com/ymyuuu/IPDB/main/BestCF/bestcfv4.txt",
            "https://api.hostmonit.com/get_optimization_ip"
        ]
        
        for url in test_urls:
            try:
                response = requests.get(url, timeout=10)
                print(f"✓ {url} - 状态码: {response.status_code}")
            except Exception as e:
                print(f"✗ {url} - 错误: {e}")
        
        return True
        
    except Exception as e:
        print(f"网络连接测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("IP提取器调试脚本")
    print("=" * 50)
    
    # 运行所有测试
    tests = [
        ("基本导入", test_basic_imports),
        ("网络连接", test_network_connectivity),
        ("文本URL数据源", test_text_url),
        ("API数据源", test_api_source),
        ("本地文件数据源", test_local_file),
        ("特定数据源组合", test_specific_sources)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"测试 {test_name} 时发生异常: {e}")
            traceback.print_exc()
            results[test_name] = False
    
    # 输出测试结果摘要
    print("\n" + "=" * 50)
    print("测试结果摘要:")
    
    for test_name, result in results.items():
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {test_name}: {status}")
    
    # 给出建议
    print("\n建议:")
    if not results.get("基本导入", False):
        print("- 请确保安装了所需的依赖包: pip install -r requirements.txt")
    
    if not results.get("网络连接", False):
        print("- 请检查网络连接是否正常")
    
    if not any([results.get("文本URL数据源", False), 
                results.get("API数据源", False), 
                results.get("本地文件数据源", False)]):
        print("- 所有数据源都无法获取数据，请检查网络连接和API配置")
    
    return all(results.values())

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
