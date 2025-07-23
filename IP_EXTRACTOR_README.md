# IP提取器模块使用说明

## 概述

`ip_extractor.py` 是一个独立的IP提取模块，可以从多个公开网站提取Cloudflare IP地址和延迟信息。该模块设计为可复用的组件，可以被其他程序导入和使用。

## 支持的数据源

### HTML网站（需要解析网页内容）
- https://cf.090227.xyz/
- https://stock.hostmonit.com/CloudFlareYes
- https://ip.164746.xyz/
- https://monitor.gacjie.cn/page/cloudflare/ipv4.html
- https://345673.xyz/

### 文本文件URL（纯IP列表）
- https://raw.githubusercontent.com/ymyuuu/IPDB/main/BestCF/bestcfv4.txt

### API接口
- https://api.hostmonit.com/get_optimization_ip（返回带速度信息的IP）

### 本地文件
- CloudflareST/sgcs.txt（测速结果文件）

## 安装依赖

### 基础功能
```bash
pip install requests beautifulsoup4
```

### 地区过滤功能（可选）
```bash
pip install ipwhois
```

### 完整安装
```bash
pip install -r requirements.txt
```

## 基本使用

### 1. 导入模块

```python
from ip_extractor import IPExtractor, get_cloudflare_ips
```

### 2. 创建提取器实例

```python
# 使用默认配置
extractor = IPExtractor()

# 自定义配置
extractor = IPExtractor(
    timeout=10,  # 请求超时时间（秒）
    user_agent="自定义User-Agent"  # 可选
)
```

### 3. 获取IP数据

#### 方法一：一站式处理（推荐）

```python
# 获取处理后的IP数据（去重、延迟过滤）
filtered_data, ip_addresses = extractor.get_processed_ips(
    max_latency=100.0,  # 最大延迟阈值（毫秒）
    remove_duplicates=True  # 是否去重
)

print(f"获取到 {len(ip_addresses)} 个IP地址")
for ip in ip_addresses[:5]:  # 显示前5个
    print(ip)
```

#### 方法二：分步处理

```python
# 1. 获取所有原始数据
all_ips = extractor.get_all_ips()

# 2. 去重
unique_ips = extractor.remove_duplicates(all_ips)

# 3. 按延迟过滤
fast_ips = extractor.filter_by_latency(unique_ips, max_latency=50.0)

# 4. 提取纯IP地址
ip_addresses = extractor.extract_ip_addresses(fast_ips)
```

#### 方法三：使用便捷函数

```python
# 快速获取指定数量的IP地址（包含所有数据源）
ips = get_cloudflare_ips(
    max_latency=80.0,  # 最大延迟
    limit=5,  # 限制数量
    include_all_sources=True  # 包含所有数据源
)

# 只从HTML网站获取IP（原有功能）
html_only_ips = get_cloudflare_ips(
    max_latency=80.0,
    limit=5,
    include_all_sources=False
)

# 获取新加坡IP（主要来自API和本地文件）
singapore_ips = get_singapore_ips(
    max_latency=100.0,
    limit=3
)
```

#### 方法四：从特定数据源获取

```python
# 从特定数据源获取IP
filtered_data, ip_addresses = extractor.get_ips_from_specific_sources(
    include_html=True,   # 是否包含HTML网站
    include_text=True,   # 是否包含文本文件
    include_api=True,    # 是否包含API接口
    include_local=True,  # 是否包含本地文件
    max_latency=100.0
)
```

#### 方法五：地区过滤（新功能）

```python
from ip_extractor import get_taiwan_ips, get_japan_ips, get_ips_by_regions

# 获取台湾IP
taiwan_ips = get_taiwan_ips(max_latency=100.0, limit=5)

# 获取日本IP
japan_ips = get_japan_ips(max_latency=100.0, limit=5)

# 获取多个地区的IP
multi_region_ips = get_ips_by_regions(
    target_regions=['SG', 'TW', 'JP', 'HK'],  # 新加坡、台湾、日本、香港
    max_latency=100.0,
    limit=10
)

# 使用IP提取器进行高级地区过滤
extractor = IPExtractor()
filtered_data, ip_addresses = extractor.get_ips_by_regions(
    target_regions=['TW', 'JP'],
    max_latency=80.0,
    include_html=False,  # 不使用HTML网站（更快）
    include_text=True,   # 使用文本文件
    include_api=True,    # 使用API
    include_local=False  # 不使用本地文件
)
```

### 4. 保存数据到文件

```python
# 保存完整数据（包含延迟信息）
extractor.save_to_file(filtered_data, 'ips_with_latency.txt')

# 或者只保存IP地址
with open('ips_only.txt', 'w') as f:
    for ip in ip_addresses:
        f.write(ip + '\n')
```

## 支持的地区代码

IP提取器支持以下地区的过滤：

| 地区代码 | 地区名称 | 关键词示例 |
|---------|---------|-----------|
| SG | 新加坡 | Singapore, 新加坡 |
| TW | 台湾 | Taiwan, 台湾, 臺灣 |
| JP | 日本 | Japan, 日本 |
| HK | 香港 | Hong Kong, 香港 |
| KR | 韩国 | Korea, 韩国, 南韩 |
| US | 美国 | United States, 美国, USA |
| UK | 英国 | United Kingdom, 英国, Britain |
| DE | 德国 | Germany, 德国 |
| FR | 法国 | France, 法国 |
| CA | 加拿大 | Canada, 加拿大 |
| AU | 澳大利亚 | Australia, 澳大利亚 |
| IN | 印度 | India, 印度 |
| TH | 泰国 | Thailand, 泰国 |
| MY | 马来西亚 | Malaysia, 马来西亚 |
| ID | 印尼 | Indonesia, 印尼 |
| PH | 菲律宾 | Philippines, 菲律宾 |
| VN | 越南 | Vietnam, 越南 |
| RU | 俄罗斯 | Russia, 俄罗斯 |
| BR | 巴西 | Brazil, 巴西 |
| NL | 荷兰 | Netherlands, 荷兰 |
| CH | 瑞士 | Switzerland, 瑞士 |
| SE | 瑞典 | Sweden, 瑞典 |
| NO | 挪威 | Norway, 挪威 |
| FI | 芬兰 | Finland, 芬兰 |
| DK | 丹麦 | Denmark, 丹麦 |

## 高级用法

### 自定义网站列表

```python
# 只从特定网站获取数据
custom_urls = [
    "https://cf.090227.xyz/",
    "https://ip.164746.xyz/"
]

custom_ips = extractor.get_all_ips(urls=custom_urls)
```

### 自定义延迟过滤

```python
# 获取延迟在特定范围内的IP
def get_ips_by_latency_range(min_latency, max_latency):
    all_ips = extractor.get_all_ips()
    unique_ips = extractor.remove_duplicates(all_ips)
    
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

# 获取延迟在30-70ms之间的IP
medium_speed_ips = get_ips_by_latency_range(30.0, 70.0)
```

### 按线路类型过滤

```python
def get_ips_by_line_type(line_keywords=['电信', '联通', '移动']):
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

# 获取电信和联通线路的IP
telecom_ips = get_ips_by_line_type(['电信', '联通'])
```

## 在其他程序中使用

### 示例1：为DNS更新获取最佳IP

```python
from ip_extractor import IPExtractor

def get_best_ips_for_dns(count=2, max_latency=80.0):
    """获取最佳IP用于DNS更新"""
    extractor = IPExtractor()
    _, ip_addresses = extractor.get_processed_ips(max_latency=max_latency)
    return ip_addresses[:count]

# 使用
best_ips = get_best_ips_for_dns(count=3, max_latency=60.0)
print(f"选择的IP: {best_ips}")
```

### 示例2：集成到现有项目

```python
# 在你的项目中
from ip_extractor import get_cloudflare_ips

def update_my_config():
    # 获取快速IP
    fast_ips = get_cloudflare_ips(max_latency=50.0, limit=5)
    
    # 更新你的配置
    config = {
        'cloudflare_ips': fast_ips,
        'updated_at': datetime.now()
    }
    
    return config
```

### 示例3：定期更新IP列表

```python
import schedule
import time
from ip_extractor import IPExtractor

def update_ip_list():
    """定期更新IP列表"""
    extractor = IPExtractor()
    _, ip_addresses = extractor.get_processed_ips(max_latency=100.0)
    
    # 保存到文件
    with open('current_best_ips.txt', 'w') as f:
        for ip in ip_addresses[:10]:  # 保存前10个
            f.write(ip + '\n')
    
    print(f"已更新IP列表，共 {len(ip_addresses)} 个IP")

# 每小时更新一次
schedule.every().hour.do(update_ip_list)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## API参考

### IPExtractor类

#### 构造函数
- `__init__(timeout=10, user_agent=None)`

#### 主要方法
- `get_all_ips(urls=None)` - 获取所有IP数据
- `get_processed_ips(max_latency=100.0, remove_duplicates=True)` - 一站式处理
- `remove_duplicates(ip_list)` - 去重
- `filter_by_latency(ip_list, max_latency=100.0)` - 延迟过滤
- `extract_ip_addresses(ip_list)` - 提取纯IP地址
- `save_to_file(ip_list, filename)` - 保存到文件

### 便捷函数

#### 通用函数
- `get_cloudflare_ips(max_latency=100.0, limit=None, include_all_sources=True)` - 快速获取IP
- `get_ips_by_regions(target_regions, max_latency=100.0, limit=None)` - 获取指定地区IP

#### 地区专用函数
- `get_singapore_ips(max_latency=100.0, limit=None, use_region_filter=False)` - 获取新加坡IP
- `get_taiwan_ips(max_latency=100.0, limit=None)` - 获取台湾IP
- `get_japan_ips(max_latency=100.0, limit=None)` - 获取日本IP
- `get_hongkong_ips(max_latency=100.0, limit=None)` - 获取香港IP
- `get_korea_ips(max_latency=100.0, limit=None)` - 获取韩国IP
- `get_us_ips(max_latency=100.0, limit=None)` - 获取美国IP
- `get_asia_ips(max_latency=100.0, limit=None)` - 获取亚洲地区IP

## 数据格式

### 原始数据格式
- 带线路信息：`IP#线路名称-延迟ms`（如：`1.1.1.1#电信-25ms`）
- 不带线路信息：`IP-延迟ms`（如：`1.1.1.1-25ms`）

### 处理后格式
- 纯IP地址列表：`['1.1.1.1', '2.2.2.2', ...]`

## 错误处理

模块内置了完善的错误处理机制：
- 网络请求失败时会跳过该网站
- 数据解析失败时会跳过该条数据
- 无效的延迟数据会被自动过滤

## 测试

运行测试文件验证功能：

```bash
python test_ip_extractor.py
```

查看使用示例：

```bash
python example_usage.py
```

## 注意事项

1. **网络依赖**：需要网络连接才能获取数据
2. **网站可用性**：某些网站可能临时不可用，模块会自动跳过
3. **数据时效性**：IP数据会实时变化，建议定期更新
4. **请求频率**：避免过于频繁的请求，以免被网站限制

## 更新日志

- v1.0.0：初始版本，支持5个网站的IP提取
- 支持延迟过滤、去重、文件保存等功能
- 提供便捷函数和示例代码
