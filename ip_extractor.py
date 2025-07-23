"""
IP提取器模块 - 从多个网站提取Cloudflare IP地址和延迟信息

这个模块提供了从多个公开网站提取IP地址、线路信息和延迟数据的功能，
可以被其他程序导入和使用。

支持的网站：
- https://cf.090227.xyz/
- https://stock.hostmonit.com/CloudFlareYes
- https://ip.164746.xyz/
- https://monitor.gacjie.cn/page/cloudflare/ipv4.html
- https://345673.xyz/

使用示例：
    from ip_extractor import IPExtractor
    
    extractor = IPExtractor()
    all_ips = extractor.get_all_ips()
    filtered_ips = extractor.filter_by_latency(all_ips, max_latency=100)
"""

import os
import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Optional, Tuple


class IPExtractor:
    """IP提取器类，用于从多个网站提取IP地址和延迟信息"""
    
    def __init__(self, timeout: int = 10, user_agent: str = None):
        """
        初始化IP提取器
        
        Args:
            timeout: 请求超时时间（秒）
            user_agent: 自定义User-Agent，如果为None则使用默认值
        """
        self.timeout = timeout
        self.headers = {
            'User-Agent': user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 支持的网站列表（HTML解析类型）
        self.html_urls = [
            "https://cf.090227.xyz/",
            "https://stock.hostmonit.com/CloudFlareYes",
            "https://ip.164746.xyz/",
            "https://monitor.gacjie.cn/page/cloudflare/ipv4.html",
            "https://345673.xyz/"
        ]

        # 支持的文本文件URL（纯IP列表）
        self.text_urls = [
            "https://raw.githubusercontent.com/ymyuuu/IPDB/main/BestCF/bestcfv4.txt"
        ]

        # 支持的API接口
        self.api_sources = [
            {
                'url': 'https://api.hostmonit.com/get_optimization_ip',
                'method': 'POST',
                'headers': {'Content-Type': 'application/json'},
                'data': {"key": "o1zrmHAF", "type": "v4"},
                'parser': 'hostmonit_api'
            }
        ]

        # 本地文件路径
        self.local_files = [
            'CloudflareST/sgcs.txt'
        ]
        
        # 解析延迟数据的正则表达式
        self.latency_pattern = re.compile(r'(\d+(\.\d+)?)\s*(ms|毫秒)?')
    
    def fetch_page_content(self, url: str) -> Optional[BeautifulSoup]:
        """
        获取网页内容并解析为BeautifulSoup对象
        
        Args:
            url: 要获取的网页URL
            
        Returns:
            BeautifulSoup对象，如果获取失败则返回None
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            if response.status_code == 200:
                return BeautifulSoup(response.content, 'html.parser')
            else:
                print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Request failed for {url}: {e}")
        return None
    
    def extract_from_cf_090227(self, soup: BeautifulSoup) -> List[str]:
        """从cf.090227.xyz提取IP数据"""
        data = []
        rows = soup.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if len(columns) >= 3:
                line_name = columns[0].text.strip()
                ip_address = columns[1].text.strip()
                latency_text = columns[2].text.strip()
                latency_match = self.latency_pattern.match(latency_text)
                if latency_match:
                    latency_value = latency_match.group(1)
                    data.append(f"{ip_address}#{line_name}-{latency_value}ms")
        return data
    
    def extract_from_hostmonit(self, soup: BeautifulSoup) -> List[str]:
        """从stock.hostmonit.com提取IP数据"""
        data = []
        rows = soup.find_all('tr', class_=re.compile(r'el-table__row'))
        for row in rows:
            columns = row.find_all('td')
            if len(columns) >= 3:
                line_name = columns[0].text.strip()
                ip_address = columns[1].text.strip()
                latency_text = columns[2].text.strip()
                latency_match = self.latency_pattern.match(latency_text)
                if latency_match:
                    latency_value = latency_match.group(1)
                    data.append(f"{ip_address}#{line_name}-{latency_value}ms")
        return data
    
    def extract_from_164746(self, soup: BeautifulSoup) -> List[str]:
        """从ip.164746.xyz提取IP数据"""
        data = []
        rows = soup.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if len(columns) >= 5:
                ip_address = columns[0].text.strip()
                latency_text = columns[4].text.strip()
                latency_match = self.latency_pattern.match(latency_text)
                if latency_match:
                    latency_value = latency_match.group(1)
                    data.append(f"{ip_address}-{latency_value}ms")
        return data
    
    def extract_from_gacjie(self, soup: BeautifulSoup) -> List[str]:
        """从monitor.gacjie.cn提取IP数据"""
        data = []
        rows = soup.find_all('tr')
        for row in rows:
            tds = row.find_all('td')
            if len(tds) >= 5:
                line_name = tds[0].text.strip()
                ip_address = tds[1].text.strip()
                latency_text = tds[4].text.strip()
                latency_match = self.latency_pattern.match(latency_text)
                if latency_match:
                    latency_value = latency_match.group(1)
                    data.append(f"{ip_address}#{line_name}-{latency_value}ms")
        return data
    
    def extract_from_345673(self, soup: BeautifulSoup) -> List[str]:
        """从345673.xyz提取IP数据"""
        data = []
        rows = soup.find_all('tr', class_=re.compile(r'line-cm|line-ct|line-cu'))
        for row in rows:
            tds = row.find_all('td')
            if len(tds) >= 4:
                line_name = tds[0].text.strip()
                ip_address = tds[1].text.strip()
                latency_text = tds[3].text.strip()
                latency_match = self.latency_pattern.match(latency_text)
                if latency_match:
                    latency_value = latency_match.group(1)
                    data.append(f"{ip_address}#{line_name}-{latency_value}ms")
        return data
    
    def extract_from_text_url(self, url: str) -> List[str]:
        """
        从文本URL获取IP数据（如GitHub上的纯IP列表）

        Args:
            url: 文本文件URL

        Returns:
            IP数据列表
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            if response.status_code == 200:
                ip_list = response.text.splitlines()
                # 过滤空行和无效IP
                valid_ips = [ip.strip() for ip in ip_list if ip.strip()]
                print(f"从文本URL {url} 获取到 {len(valid_ips)} 个IP地址")
                return valid_ips
            else:
                print(f"文本URL请求失败: {url}, 状态码: {response.status_code}")
        except Exception as e:
            print(f"从文本URL获取IP数据时出错 {url}: {e}")
        return []

    def extract_from_api(self, api_config: dict) -> List[str]:
        """
        从API接口获取IP数据

        Args:
            api_config: API配置字典

        Returns:
            IP数据列表
        """
        try:
            if api_config['method'].upper() == 'POST':
                response = requests.post(
                    api_config['url'],
                    headers=api_config.get('headers', {}),
                    json=api_config.get('data', {}),
                    timeout=self.timeout
                )
            else:
                response = requests.get(
                    api_config['url'],
                    headers=api_config.get('headers', {}),
                    timeout=self.timeout
                )

            if response.status_code == 200:
                return self.parse_api_response(response.json(), api_config['parser'])
            else:
                print(f"API请求失败: {api_config['url']}, 状态码: {response.status_code}")
        except Exception as e:
            print(f"从API获取IP数据时出错 {api_config['url']}: {e}")
        return []

    def parse_api_response(self, data: dict, parser_type: str) -> List[str]:
        """
        解析API响应数据

        Args:
            data: API响应的JSON数据
            parser_type: 解析器类型

        Returns:
            IP数据列表
        """
        if parser_type == 'hostmonit_api':
            ip_list = []
            if data.get('code') == 200 and 'info' in data:
                # 提取所有线路的IP地址
                for line_type in ['CM', 'CT', 'CU']:
                    if line_type in data['info']:
                        for item in data['info'][line_type]:
                            ip_with_speed = f"{item['ip']}#{item['speed']}mb/s"
                            ip_list.append(ip_with_speed)
                print(f"从API获取到 {len(ip_list)} 个IP地址")
                return ip_list
            else:
                print("API响应格式异常")
        return []

    def extract_from_local_file(self, file_path: str) -> List[str]:
        """
        从本地文件获取IP数据

        Args:
            file_path: 本地文件路径

        Returns:
            IP数据列表
        """
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    ip_list = f.read().splitlines()
                valid_ips = [ip.strip() for ip in ip_list if ip.strip()]
                print(f"从本地文件 {file_path} 获取到 {len(valid_ips)} 个IP地址")
                return valid_ips
            else:
                print(f"本地文件不存在: {file_path}")
        except Exception as e:
            print(f"读取本地文件时出错 {file_path}: {e}")
        return []

    def extract_from_html_site(self, url: str) -> List[str]:
        """
        从HTML网站提取IP数据

        Args:
            url: 网站URL

        Returns:
            IP数据列表，格式为 "IP#线路-延迟ms" 或 "IP-延迟ms"
        """
        soup = self.fetch_page_content(url)
        if not soup:
            return []

        # 根据URL选择对应的提取方法
        if "cf.090227.xyz" in url:
            return self.extract_from_cf_090227(soup)
        elif "stock.hostmonit.com" in url:
            return self.extract_from_hostmonit(soup)
        elif "ip.164746.xyz" in url:
            return self.extract_from_164746(soup)
        elif "monitor.gacjie.cn" in url:
            return self.extract_from_gacjie(soup)
        elif "345673.xyz" in url:
            return self.extract_from_345673(soup)
        else:
            print(f"Unsupported HTML URL: {url}")
            return []
    
    def get_all_ips(self,
                    html_urls: List[str] = None,
                    text_urls: List[str] = None,
                    api_sources: List[dict] = None,
                    local_files: List[str] = None,
                    include_all_sources: bool = True) -> List[str]:
        """
        从所有支持的数据源获取IP数据

        Args:
            html_urls: 自定义HTML网站URL列表
            text_urls: 自定义文本文件URL列表
            api_sources: 自定义API源列表
            local_files: 自定义本地文件列表
            include_all_sources: 是否包含所有默认数据源

        Returns:
            所有IP数据的列表
        """
        all_data = []

        # 如果启用所有数据源，使用默认配置
        if include_all_sources:
            html_urls = html_urls or self.html_urls
            text_urls = text_urls or self.text_urls
            api_sources = api_sources or self.api_sources
            local_files = local_files or self.local_files
        else:
            html_urls = html_urls or []
            text_urls = text_urls or []
            api_sources = api_sources or []
            local_files = local_files or []

        # 从HTML网站获取数据
        for url in html_urls:
            print(f"正在从HTML网站获取IP数据: {url}")
            site_data = self.extract_from_html_site(url)
            all_data.extend(site_data)
            print(f"从 {url} 获取到 {len(site_data)} 条数据")

        # 从文本URL获取数据
        for url in text_urls:
            print(f"正在从文本URL获取IP数据: {url}")
            text_data = self.extract_from_text_url(url)
            all_data.extend(text_data)
            print(f"从 {url} 获取到 {len(text_data)} 条数据")

        # 从API获取数据
        for api_config in api_sources:
            print(f"正在从API获取IP数据: {api_config['url']}")
            api_data = self.extract_from_api(api_config)
            all_data.extend(api_data)
            print(f"从 {api_config['url']} 获取到 {len(api_data)} 条数据")

        # 从本地文件获取数据
        for file_path in local_files:
            print(f"正在从本地文件获取IP数据: {file_path}")
            file_data = self.extract_from_local_file(file_path)
            all_data.extend(file_data)
            print(f"从 {file_path} 获取到 {len(file_data)} 条数据")

        print(f"总共获取到 {len(all_data)} 条IP数据")
        return all_data
    
    def remove_duplicates(self, ip_list: List[str]) -> List[str]:
        """
        去除重复的IP数据
        
        Args:
            ip_list: IP数据列表
            
        Returns:
            去重后的IP数据列表
        """
        unique_data = list(set(ip_list))
        print(f"去重前: {len(ip_list)} 条数据，去重后: {len(unique_data)} 条数据")
        return unique_data
    
    def filter_by_latency(self, ip_list: List[str], max_latency: float = 100.0, keep_no_latency: bool = True) -> List[str]:
        """
        根据延迟过滤IP数据

        Args:
            ip_list: IP数据列表
            max_latency: 最大延迟阈值（毫秒）
            keep_no_latency: 是否保留没有延迟信息的IP

        Returns:
            过滤后的IP数据列表
        """
        filtered_data = []
        no_latency_count = 0

        for line in ip_list:
            try:
                # 检查是否包含延迟信息
                if 'ms' in line or 'mb/s' in line:
                    # 尝试提取延迟值
                    if 'ms' in line:
                        # 格式如: "IP#线路-25ms" 或 "IP-25ms"
                        latency_str = line.split('-')[-1].replace('ms', '')
                        latency_value = float(latency_str)
                        if latency_value < max_latency:
                            filtered_data.append(line)
                    elif 'mb/s' in line:
                        # 格式如: "IP#5mb/s" (来自API的速度信息，保留所有)
                        filtered_data.append(line)
                else:
                    # 纯IP地址，没有延迟信息
                    if keep_no_latency:
                        filtered_data.append(line)
                        no_latency_count += 1
            except (ValueError, IndexError):
                # 如果无法解析延迟值，根据设置决定是否保留
                if keep_no_latency:
                    filtered_data.append(line)
                    no_latency_count += 1

        print(f"延迟过滤前: {len(ip_list)} 条数据，过滤后: {len(filtered_data)} 条数据（延迟 < {max_latency}ms）")
        if no_latency_count > 0:
            print(f"其中 {no_latency_count} 条数据没有延迟信息{'（已保留）' if keep_no_latency else '（已过滤）'}")
        return filtered_data
    
    def extract_ip_addresses(self, ip_list: List[str]) -> List[str]:
        """
        从IP数据中提取纯IP地址

        Args:
            ip_list: IP数据列表（支持多种格式）

        Returns:
            纯IP地址列表
        """
        ip_addresses = []
        for line in ip_list:
            # 提取IP地址部分（去除线路、延迟、速度等信息）
            ip = line.strip()

            # 处理不同格式
            if '#' in ip:
                # 格式如: "IP#线路-延迟ms" 或 "IP#速度mb/s"
                ip = ip.split('#')[0]
            elif '-' in ip:
                # 格式如: "IP-延迟ms"
                ip = ip.split('-')[0]
            # 否则就是纯IP地址

            ip = ip.strip()
            if ip:  # 确保不是空字符串
                ip_addresses.append(ip)

        return ip_addresses
    
    def save_to_file(self, ip_list: List[str], filename: str) -> None:
        """
        将IP数据保存到文件
        
        Args:
            ip_list: IP数据列表
            filename: 文件名
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for line in ip_list:
                    f.write(line + '\n')
            print(f"成功将 {len(ip_list)} 条IP数据保存到 {filename}")
        except Exception as e:
            print(f"保存文件时出错: {e}")
    
    def get_processed_ips(self, max_latency: float = 100.0, remove_duplicates: bool = True) -> Tuple[List[str], List[str]]:
        """
        获取处理后的IP数据（一站式处理）
        
        Args:
            max_latency: 最大延迟阈值（毫秒）
            remove_duplicates: 是否去重
            
        Returns:
            元组：(完整IP数据列表, 纯IP地址列表)
        """
        # 获取所有IP数据
        all_ips = self.get_all_ips()
        
        # 去重
        if remove_duplicates:
            all_ips = self.remove_duplicates(all_ips)
        
        # 按延迟过滤
        filtered_ips = self.filter_by_latency(all_ips, max_latency)
        
        # 提取纯IP地址
        ip_addresses = self.extract_ip_addresses(filtered_ips)
        
        return filtered_ips, ip_addresses

    def get_ips_from_specific_sources(self,
                                    include_html: bool = True,
                                    include_text: bool = True,
                                    include_api: bool = True,
                                    include_local: bool = True,
                                    max_latency: float = 100.0) -> Tuple[List[str], List[str]]:
        """
        从特定数据源获取IP数据

        Args:
            include_html: 是否包含HTML网站数据源
            include_text: 是否包含文本文件数据源
            include_api: 是否包含API数据源
            include_local: 是否包含本地文件数据源
            max_latency: 最大延迟阈值

        Returns:
            元组：(完整IP数据列表, 纯IP地址列表)
        """
        html_urls = self.html_urls if include_html else []
        text_urls = self.text_urls if include_text else []
        api_sources = self.api_sources if include_api else []
        local_files = self.local_files if include_local else []

        all_ips = self.get_all_ips(
            html_urls=html_urls,
            text_urls=text_urls,
            api_sources=api_sources,
            local_files=local_files,
            include_all_sources=False
        )

        # 去重和过滤
        unique_ips = self.remove_duplicates(all_ips)
        filtered_ips = self.filter_by_latency(unique_ips, max_latency)
        ip_addresses = self.extract_ip_addresses(filtered_ips)

        return filtered_ips, ip_addresses


# 便捷函数，用于快速获取IP数据
def get_cloudflare_ips(max_latency: float = 100.0, limit: int = None, include_all_sources: bool = True) -> List[str]:
    """
    便捷函数：快速获取Cloudflare IP地址

    Args:
        max_latency: 最大延迟阈值（毫秒）
        limit: 限制返回的IP数量，None表示不限制
        include_all_sources: 是否包含所有数据源

    Returns:
        IP地址列表
    """
    extractor = IPExtractor()

    if include_all_sources:
        _, ip_addresses = extractor.get_processed_ips(max_latency=max_latency)
    else:
        # 只使用HTML网站数据源（原有的5个网站）
        _, ip_addresses = extractor.get_ips_from_specific_sources(
            include_html=True,
            include_text=False,
            include_api=False,
            include_local=False,
            max_latency=max_latency
        )

    if limit:
        ip_addresses = ip_addresses[:limit]
        print(f"限制返回前 {limit} 个IP地址")

    return ip_addresses


def get_singapore_ips(max_latency: float = 100.0, limit: int = None) -> List[str]:
    """
    便捷函数：获取新加坡IP地址（主要来自API和本地文件）

    Args:
        max_latency: 最大延迟阈值（毫秒）
        limit: 限制返回的IP数量，None表示不限制

    Returns:
        IP地址列表
    """
    extractor = IPExtractor()

    # 主要从API、文本文件和本地文件获取数据
    _, ip_addresses = extractor.get_ips_from_specific_sources(
        include_html=False,
        include_text=True,
        include_api=True,
        include_local=True,
        max_latency=max_latency
    )

    if limit:
        ip_addresses = ip_addresses[:limit]
        print(f"限制返回前 {limit} 个新加坡IP地址")

    return ip_addresses


if __name__ == "__main__":
    # 示例用法
    print("=== IP提取器示例 ===")
    
    # 创建提取器实例
    extractor = IPExtractor()
    
    # 获取处理后的IP数据
    filtered_data, ip_addresses = extractor.get_processed_ips(max_latency=100.0)
    
    # 保存到文件
    extractor.save_to_file(filtered_data, 'extracted_ips.txt')
    
    # 显示前10个IP地址
    print(f"\n前10个IP地址:")
    for i, ip in enumerate(ip_addresses[:10], 1):
        print(f"{i}. {ip}")
    
    # 使用便捷函数
    print(f"\n使用便捷函数获取前5个IP:")
    quick_ips = get_cloudflare_ips(max_latency=100.0, limit=5)
    for i, ip in enumerate(quick_ips, 1):
        print(f"{i}. {ip}")
