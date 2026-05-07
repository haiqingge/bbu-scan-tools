# BBU Scan Tools

BBU 设备扫描工具集，用于检测设备中的敏感信息和中文内容。

## 工具列表

| 工具 | 功能 | 调用方式 |
|------|------|---------|
| **scan-chinese** | 扫描 BBU 目录下的中文字符及全角标点 | `python scan-chinese/scan_chinese.py` |
| **scan-sensitive-info** | 扫描中国敏感信息（PLMN/SJ/Femto） | `python scan-sensitive-info/scan_sensitive_info.py` |

## 环境配置

每个工具目录下的 `environments.json` 管理不同设备的连接信息：

```json
{
  "default_env": "T5000",
  "environments": {
    "T5000": { "host": "192.168.5.104", "user": "root", "password": "***" },
    "v5":    { "host": "192.168.5.100", "user": "root", "password": "***" },
    "v6":    { "host": "192.168.5.100", "user": "f3mto5gus3r", "password": "***" }
  }
}
```

## 使用

```bash
# 使用默认环境
python scan-chinese/scan_chinese.py
python scan-sensitive-info/scan_sensitive_info.py

# 指定环境
python scan-chinese/scan_chinese.py --env v6
python scan-sensitive-info/scan_sensitive_info.py -e T5000

# 直接指定 IP
python scan-chinese/scan_chinese.py 192.168.5.141
python scan-sensitive-info/scan_sensitive_info.py 192.168.5.141

# 查看可用环境
python scan-chinese/scan_chinese.py -h
python scan-sensitive-info/scan_sensitive_info.py -h
```

## 依赖

- Python 3.6+
- paramiko (`pip install paramiko`)
