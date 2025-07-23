# IP提取器更新总结

## 更新概述

本次更新将 `sgfdip.py` 中的额外IP数据源整合到了 `ip_extractor.py` 模块中，使IP提取器成为一个更完整、更强大的工具。

## 新增功能

### 1. 多种数据源支持

现在IP提取器支持4种不同类型的数据源：

#### HTML网站（原有功能）
- https://cf.090227.xyz/
- https://stock.hostmonit.com/CloudFlareYes
- https://ip.164746.xyz/
- https://monitor.gacjie.cn/page/cloudflare/ipv4.html
- https://345673.xyz/

#### 文本文件URL（新增）
- https://raw.githubusercontent.com/ymyuuu/IPDB/main/BestCF/bestcfv4.txt
- 返回纯IP地址列表，无需解析HTML

#### API接口（新增）
- https://api.hostmonit.com/get_optimization_ip
- 返回带速度信息的IP数据（格式：`IP#速度mb/s`）

#### 本地文件（新增）
- CloudflareST/sgcs.txt
- 支持读取本地测速结果文件

### 2. 新增方法

#### `get_ips_from_specific_sources()`
允许用户选择性地从特定类型的数据源获取IP：

```python
# 只从API和本地文件获取数据
filtered_data, ip_addresses = extractor.get_ips_from_specific_sources(
    include_html=False,
    include_text=False,
    include_api=True,
    include_local=True,
    max_latency=100.0
)
```

#### 增强的 `get_all_ips()`
现在支持更细粒度的控制：

```python
all_ips = extractor.get_all_ips(
    html_urls=custom_html_urls,      # 自定义HTML网站
    text_urls=custom_text_urls,      # 自定义文本文件URL
    api_sources=custom_api_sources,  # 自定义API源
    local_files=custom_local_files,  # 自定义本地文件
    include_all_sources=True         # 是否包含默认源
)
```

#### 改进的 `filter_by_latency()`
现在能够处理多种数据格式：
- 带延迟信息：`IP#线路-25ms`
- 带速度信息：`IP#5mb/s`
- 纯IP地址：`1.1.1.1`

```python
filtered_ips = extractor.filter_by_latency(
    ip_list, 
    max_latency=100.0, 
    keep_no_latency=True  # 是否保留没有延迟信息的IP
)
```

### 3. 新增便捷函数

#### `get_singapore_ips()`
专门用于获取新加坡IP地址：

```python
from ip_extractor import get_singapore_ips

sg_ips = get_singapore_ips(max_latency=100.0, limit=5)
```

#### 增强的 `get_cloudflare_ips()`
现在支持选择数据源：

```python
# 从所有数据源获取
all_source_ips = get_cloudflare_ips(include_all_sources=True)

# 只从HTML网站获取（原有行为）
html_only_ips = get_cloudflare_ips(include_all_sources=False)
```

## 对现有项目的影响

### `yx_ips.py`
- ✅ **完全兼容**：功能保持不变
- ✅ **性能提升**：使用统一的IP提取器
- ✅ **代码简化**：从237行减少到130行

### `sgfdip.py`
- ✅ **功能增强**：现在使用统一的IP提取器
- ✅ **代码简化**：IP获取逻辑大幅简化
- ✅ **维护性提升**：IP提取逻辑统一管理

## 使用示例

### 基本使用（所有数据源）

```python
from ip_extractor import IPExtractor

extractor = IPExtractor()

# 获取所有数据源的IP（推荐）
filtered_data, ip_addresses = extractor.get_processed_ips(
    max_latency=100.0,
    remove_duplicates=True
)

print(f"获取到 {len(ip_addresses)} 个IP地址")
```

### 选择性使用数据源

```python
# 只使用文本文件和API（适合获取大量IP）
text_api_data, text_api_ips = extractor.get_ips_from_specific_sources(
    include_html=False,
    include_text=True,
    include_api=True,
    include_local=False,
    max_latency=80.0
)

# 只使用HTML网站（原有行为，适合获取带延迟信息的IP）
html_data, html_ips = extractor.get_ips_from_specific_sources(
    include_html=True,
    include_text=False,
    include_api=False,
    include_local=False,
    max_latency=50.0
)
```

### 便捷函数使用

```python
from ip_extractor import get_cloudflare_ips, get_singapore_ips

# 快速获取Cloudflare IP（所有数据源）
cf_ips = get_cloudflare_ips(max_latency=80.0, limit=10)

# 快速获取新加坡IP
sg_ips = get_singapore_ips(max_latency=100.0, limit=5)
```

## 数据格式支持

IP提取器现在能够处理多种数据格式：

1. **HTML解析格式**：`IP#线路-延迟ms`（如：`1.1.1.1#电信-25ms`）
2. **API速度格式**：`IP#速度mb/s`（如：`1.1.1.1#5mb/s`）
3. **纯IP格式**：`IP`（如：`1.1.1.1`）
4. **简单延迟格式**：`IP-延迟ms`（如：`1.1.1.1-25ms`）

## 配置说明

IP提取器的默认配置在类初始化时设置：

```python
class IPExtractor:
    def __init__(self, timeout: int = 10, user_agent: str = None):
        # HTML网站列表
        self.html_urls = [...]
        
        # 文本文件URL列表
        self.text_urls = [...]
        
        # API源配置
        self.api_sources = [...]
        
        # 本地文件路径
        self.local_files = [...]
```

用户可以通过参数自定义这些配置。

## 性能优化

1. **并发处理**：不同数据源可以并行获取
2. **错误隔离**：单个数据源失败不影响其他源
3. **智能过滤**：根据数据格式自动选择合适的过滤策略
4. **内存优化**：及时清理临时数据

## 向后兼容性

- ✅ 所有原有API保持兼容
- ✅ 原有的便捷函数继续工作
- ✅ 现有项目无需修改即可使用

## 测试和验证

更新后的功能已通过以下方式验证：

1. **单元测试**：`test_ip_extractor.py`
2. **使用示例**：`example_usage.py`
3. **实际项目测试**：`yx_ips.py` 和 `sgfdip.py`

## 总结

这次更新使IP提取器成为了一个真正统一的IP数据获取解决方案：

- 🎯 **统一接口**：一个模块处理所有IP数据源
- 🔧 **灵活配置**：支持选择性使用数据源
- 📈 **功能增强**：支持更多数据格式和来源
- 🛠️ **易于维护**：集中管理所有IP提取逻辑
- 🔄 **完全兼容**：不破坏现有项目的功能

现在，无论是需要快速获取大量IP，还是需要精确的延迟信息，或是特定地区的IP，IP提取器都能提供合适的解决方案。
