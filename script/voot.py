import urllib.request
import json
import re
import sys

def fetch_cookie(m3u_urls):
    headers = {
        'User-Agent': 'OTT Navigator',
        'Accept': '*/*'
    }
    
    for url in m3u_urls:
        try:
            print(f"Attempting to fetch cookie from: {url}")
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = resp.read().decode('utf-8', errors='ignore')
            
            # Check for EXTVLCOPT cookie match
            match = re.search(r'#EXTVLCOPT:http-cookie=(.+)', content)
            if match:
                return match.group(1).strip()
            
            # Fallback search for hdnea cookie string
            match_alt = re.search(r'hdnea=[^;\r\n\s"]+', content)
            if match_alt:
                return match_alt.group(0).strip()
        except Exception as err:
            print(f"Warning: Failed fetching cookie from {url} ({err})")
            continue

    raise RuntimeError('Cookie not found in any of the provided endpoints.')

def fetch_json(json_url):
    print(f"Fetching JSON metadata from: {json_url}")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    req = urllib.request.Request(json_url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.load(resp)

def generate_m3u(data, cookie, output_file):
    user_agent = 'Virat Kohli'
    lines = ['#EXTM3U']

    for item in data:
        name = item.get('name', 'Unknown')
        logo = item.get('logo', '')
        group = item.get('group', 'Other')
        mpd = item.get('mpd_url', '')
        kid = item.get('keyId', '').strip()
        key = item.get('key', '').strip()

        if kid and len(kid) < 32:
            kid = kid.zfill(32)
        if key and len(key) < 32:
            key = key.zfill(32)

        # Build stream URL with parameters
        url_with_params = (
            f"{mpd}?"
            f"cookie={cookie}&"
            f"Referer=https://www.hotstar.com/&"
            f"Origin=https://www.hotstar.com/&"
            f"User-Agent={user_agent}"
        )

        lines.append(f'#EXTINF:-1 tvg-name="{name}" tvg-logo="{logo}" group-title="{group}", {name}')
        lines.append('#KODIPROP:inputstream=inputstream.adaptive')
        lines.append('#KODIPROP:inputstream.adaptive.manifest_type=mpd')
        lines.append('#KODIPROP:inputstream.adaptive.license_type=clearkey')
        lines.append(f'#KODIPROP:inputstream.adaptive.license_key={kid}:{key}')
        lines.append(f'#EXTVLCOPT:http-user-agent={user_agent}')
        lines.append(f'#EXTVLCOPT:http-cookie={cookie}')
        lines.append(f'#EXTVLCOPT:http-referrer=https://www.hotstar.com/')
        lines.append(f'#EXTVLCOPT:http-extra-headers=Origin: https://www.hotstar.com/')
        lines.append(f'#EXTHTTP:{{"Origin":"https://www.hotstar.com/","Referer":"https://www.hotstar.com/","Cookie":"{cookie}"}}')
        lines.append(url_with_params)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

def main():
    m3u_urls = [
        'https://premiumplugx.com/VIP/pluglist.php',
        'https://premiumplugx.com/htt/hot.php?playlist=1'
    ]
    json_url = 'https://sportlink-jtv.pages.dev/jhs.json'
    output = 'digital.m3u'

    try:
        cookie = fetch_cookie(m3u_urls)
        print(f"Cookie extracted successfully: {cookie[:30]}...")
        data = fetch_json(json_url)
        generate_m3u(data, cookie, output)
        print(f"Successfully generated {output} with {len(data)} channels.")
    except Exception as e:
        print(f"Execution Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
    
