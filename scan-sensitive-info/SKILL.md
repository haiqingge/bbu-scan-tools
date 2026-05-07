---
name: scan-sensitive-info
description: 扫描 BBU 设备目录中的中国敏感信息（PLMN 运营商码、SJ、Femto 等）
metadata:
  {
    "openclaw": { "requires": { "paramiko": "" }, "install": ["pip install paramiko"] }
  }
---

# Scan Sensitive Info

扫描 BBU 设备指定目录下是否包含中国相关的敏感信息：
- **PLMN**（46000~46020 中国运营商码）
- **SJ**（三维通信相关标识）
- **Femto**（小基站枚举值）

## 环境配置

编辑 `environments.json` 管理不同环境的连接信息：

```json
{
  "default_env": "lab",
  "environments": {
    "lab":    { "host": "192.168.5.104", "user": "root", "password": "5Groo@23" },
    "v5":     { "host": "192.168.5.100", "user": "root", "password": "Smallcell@5" },
    "v6":     { "host": "192.168.5.100", "user": "f3mto5gus3r", "password": "H@rm@n$Nr!Fmt0$00.5G_$StrnG" },
    "site_a": { "host": "10.88.2.200", "user": "root", "password": "xxx" }
  }
}
```

## 使用

```bash
# 使用默认环境（environments.json 中 default_env 指定）
python scan_sensitive_info.py

# 指定环境名称
python scan_sensitive_info.py -e v6
python scan_sensitive_info.py --env site_a

# 直接指定 IP（不依赖配置文件）
python scan_sensitive_info.py 192.168.5.100
python scan_sensitive_info.py 192.168.5.100 /opt/test

# 查看所有可用环境
python scan_sensitive_info.py -h
```

## 扫描项

- PLMN: 46000 ~ 46020（移动/联通/电信/广电）
- SJ: `ASTRI-SJ-5G-BTS` / `SJ-5GSA` / `vendor-code SJ`
- Femto: `enum femto`

## 输出格式

```
============================================================
目录: /opt/loads（共 2976 个文件）
  [PLMN 46010] 16 处:
    /opt/loads/.../confdb_v2.xml:3191: <PLMNID>46010f</PLMNID>
  [SJ] 20 处:
    /opt/loads/.../confdb.xml:126: ASTRI-SJ-5G-BTS
============================================================
```

## 文件

- `scan_sensitive_info.py` — 扫描脚本
- `environments.json` — 环境配置（按需修改）
