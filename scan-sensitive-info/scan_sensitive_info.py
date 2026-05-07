import paramiko
import sys
import os
import json

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'environments.json')

def get_default_env():
    return json.load(open(CONFIG_FILE, 'r', encoding='utf-8'))

def load_env(name):
    config = json.load(open(CONFIG_FILE, 'r', encoding='utf-8'))
    envs = config.get('environments', {})
    if not name:
        name = config.get('default_env', 'lab')
    if name in envs:
        return envs[name]
    else:
        print(f"Error: environment '{name}' not found in {CONFIG_FILE}")
        print(f"Available: {', '.join(envs.keys())}")
        sys.exit(1)

def scan_sensitive(host, port=22, user='root', password='5Groo@23', directories=None):
    if directories is None:
        directories = ['/opt/bbu/oam/log', '/opt/loads']

    PLMNS = ['46000', '46001', '46002', '46003', '46004', '46005',
             '46006', '46007', '46008', '46009', '46010',
             '46011', '46012', '46013', '46015', '46020']
    KEYWORDS = ['SJ', 'Femto', 'femto']

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port, user, password, timeout=30)

    results = {}
    for d in directories:
        dir_results = []
        stdin, stdout, stderr = client.exec_command(f'find "{d}" -type f 2>/dev/null | wc -l', timeout=30)
        total = stdout.read().decode().strip()
        dir_results.append(f"目录: {d}（共 {total} 个文件）")

        for plmn in PLMNS:
            cmd = f"""grep -rnI '{plmn}' "{d}" 2>/dev/null | sort -u | head -30"""
            stdin, stdout, stderr = client.exec_command(cmd, timeout=60)
            out = stdout.read().decode('utf-8', errors='replace').strip()
            if out:
                lines = [f"  {l}" for l in out.split('\n') if l.strip()]
                dir_results.append(f"  [PLMN {plmn}] {len(lines)} 处:")
                dir_results.extend(lines)

        for kw in KEYWORDS:
            cmd = f"""grep -rnI '{kw}' "{d}" 2>/dev/null | sort -u | head -30"""
            stdin, stdout, stderr = client.exec_command(cmd, timeout=60)
            out = stdout.read().decode('utf-8', errors='replace').strip()
            if out:
                lines = [f"  {l}" for l in out.split('\n') if l.strip()]
                dir_results.append(f"  [{kw}] {len(lines)} 处:")
                dir_results.extend(lines)

        results[d] = dir_results

    client.close()
    return results

def usage():
    print("Usage:")
    print("  python scan_sensitive_info.py                      # 使用默认环境")
    print("  python scan_sensitive_info.py -e lab                # 指定环境名称")
    print("  python scan_sensitive_info.py -e test_v6            # V6环境")
    print("  python scan_sensitive_info.py 192.168.5.100         # 直接指定IP")
    print("  python scan_sensitive_info.py 192.168.5.100 /opt    # 指定IP+目录")
    print()
    print("环境配置文件: environments.json")
    config = get_default_env()
    for name, info in config.get('environments', {}).items():
        print(f"  {name}: {info.get('user','')}@{info.get('host','')}  ({info.get('note','')})")

if __name__ == '__main__':
    args = sys.argv[1:]

    if not args:
        env = load_env(None)
        host, port, user, password = env['host'], env.get('port',22), env['user'], env['password']
        dirs = None
    elif args[0] == '-e' or args[0] == '--env':
        if len(args) < 2:
            usage()
            sys.exit(1)
        env = load_env(args[1])
        host, port, user, password = env['host'], env.get('port',22), env['user'], env['password']
        dirs = args[2:] if len(args) > 2 else None
    elif args[0] in ('-h', '--help'):
        usage()
        sys.exit(0)
    else:
        host, port, user, password = args[0], 22, 'root', os.environ.get('BBU_PASSWORD', '5Groo@23')
        dirs = args[1:] if len(args) > 1 else None

    print(f"连接: {user}@{host}:{port}")
    results = scan_sensitive(host, port, user, password, directories=dirs)

    total_hits = 0
    for d, lines in results.items():
        print(f"\n{'='*60}")
        for l in lines:
            print(l)
            if l.startswith('  [') and '处' in l:
                import re
                m = re.search(r'(\d+) 处', l)
                if m:
                    total_hits += int(m.group(1))
        print()

    print(f"\n扫描完成，共 {total_hits} 处匹配。" if total_hits else "\n扫描完成，无匹配。")
