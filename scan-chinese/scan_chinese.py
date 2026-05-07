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

def scan_chinese(host, port=22, user='root', password='5Groo@23', directories=None):
    if directories is None:
        directories = ['/opt/bbu/oam/log', '/opt/loads']

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port, user, password, timeout=30)

    results = {}
    for d in directories:
        dir_results = []
        stdin, stdout, stderr = client.exec_command(f'find "{d}" -type f 2>/dev/null | wc -l', timeout=30)
        total = stdout.read().decode().strip()
        dir_results.append(f"目录: {d}（共 {total} 个文件）")

        # Chinese characters (UTF-8 bytes: E4-E9 80-BF 80-BF)
        cmd = """grep -rnI '[\\xe4-\\xe9][\\x80-\\xbf][\\x80-\\xbf]' "%s" 2>/dev/null \
            --include='*.html' --include='*.xml' --include='*.sh' --include='*.py' \
            --include='*.txt' --include='*.conf' --include='*.cfg' --include='*.md' \
            --include='*.json' --include='*.log' --include='*.properties' \
            --include='*.yml' --include='*.yaml' --include='*.csv' | sort -u | head -100""" % d
        stdin, stdout, stderr = client.exec_command(cmd, timeout=90)
        out = stdout.read().decode('utf-8', errors='replace').strip()

        # Fullwidth punctuation (EF BC 80-BF / EF BD 80-BF / ...)
        cmd2 = """grep -rnI '[\\xef\\xbc-\\xbe][\\x80-\\xbf][\\x80-\\xbf]' "%s" 2>/dev/null \
            --include='*.html' --include='*.xml' --include='*.sh' --include='*.py' \
            --include='*.txt' --include='*.conf' --include='*.cfg' --include='*.md' \
            --include='*.json' --include='*.log' --include='*.properties' \
            --include='*.yml' --include='*.yaml' --include='*.csv' | sort -u | head -100""" % d
        stdin2, stdout2, stderr2 = client.exec_command(cmd2, timeout=90)
        out2 = stdout2.read().decode('utf-8', errors='replace').strip()

        if out:
            lines = [f"  {l}" for l in out.split('\n') if l.strip()]
            dir_results.append(f"  中文汉字匹配: {len(lines)} 处")
            dir_results.extend(lines)
        if out2:
            lines2 = [f"  {l}" for l in out2.split('\n') if l.strip()]
            dir_results.append(f"  中文全角标点匹配: {len(lines2)} 处")
            dir_results.extend(lines2)
        if not out and not out2:
            dir_results.append("  无中文字符/全角标点")

        results[d] = dir_results

    client.close()
    return results

def usage():
    print("Usage:")
    print("  python scan_chinese.py                       # 使用默认环境")
    print("  python scan_chinese.py -e test_v6            # 指定环境名称")
    print("  python scan_chinese.py 192.168.5.100         # 直接指定IP")
    print("  python scan_chinese.py 192.168.5.100 /opt    # 指定IP+目录")
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
    elif args[0] in ('-e', '--env'):
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
    results = scan_chinese(host, port, user, password, directories=dirs)

    total_hits = 0
    for d, lines in results.items():
        print(f"\n{'='*60}")
        for l in lines:
            print(l)
        print()

    print(f"扫描完成。" if not any(l for lines in results.values() for l in lines) else "")
