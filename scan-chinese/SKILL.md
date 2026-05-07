---
name: scan-chinese
description: 扫描 BBU 设备目录中的中文字符及全角标点
metadata:
  {
    "openclaw": { "requires": { "paramiko": "" }, "install": ["pip install paramiko"] }
  }
---

# Scan Chinese

扫描 BBU 设备指定目录下所有文本文件中的中文字符及全角标点符号。

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
# 使用默认环境
python scan_chinese.py

# 指定环境名称
python scan_chinese.py -e lab
python scan_chinese.py --env v6

# 直接指定 IP
python scan_chinese.py 192.168.5.100
python scan_chinese.py 192.168.5.100 /opt/test

# 查看所有可用环境
python scan_chinese.py -h
```

## 扫描内容

- 中文汉字: CJK 统一汉字 U+4E00~U+9FFF
- 全角标点: 全角括号（）逗号，冒号：分号；句号。等

## 扫描范围

仅文本文件: `*.html *.xml *.sh *.py *.txt *.conf *.cfg *.md *.json *.log *.properties *.yml *.yaml *.csv`

## 输出格式

```
============================================================
目录: /opt/loads（共 2976 个文件）
  中文汉字匹配: 3 处
    /opt/loads/.../cpCellAppPmDef_m.xml:65: ...reestablish，sorted by cause
  中文全角标点匹配: 205 处
    /opt/loads/.../DSP_PmInstaneousResult_m.html:69: ...（3GPP TS 38.474）
============================================================
```

## 文件

- `scan_chinese.py` — 扫描脚本
- `environments.json` — 环境配置（按需修改）
