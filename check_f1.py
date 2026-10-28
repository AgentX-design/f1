import urllib.request, re
with urllib.request.urlopen('https://www.formula1.com/en/results/', timeout=30) as r:
    data = r.read()
    print('status', r.status, 'len', len(data))
    html = data.decode('utf-8', errors='ignore')
    titles = re.findall(r'<title>(.*?)</title>', html, flags=re.S)
    print('title:', titles[0] if titles else 'none')
