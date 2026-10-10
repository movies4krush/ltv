import json

# Load the JSON data
with open('jiotvplus_keys.json', 'r', encoding='utf-8') as f:
    channels = json.load(f)

# Start building the M3U playlist content
m3u_content = '#EXTM3U\n'

for ch in channels:
    channel_name = ch.get('channel_name', 'Unknown')
    channel_id = ch.get('channel_id', '')
    logo = ch.get('channel_logo', '')
    group = ch.get('channel_genre', 'General')
    url = ch.get('channel_url', '')
    license_key = ch.get('license_key', '')

    # Format the standard EXTINF line with metadata tags
    m3u_content += f'#EXTINF:-1 tvg-id="{channel_id}" tvg-logo="{logo}" group-title="{group}",{channel_name}\n'
    
    # Add Widevine DRM license key properties
    if license_key:
        m3u_content += f'#KODIPROP:inputstream.adaptive.license_type=widevine\n'
        m3u_content += f'#KODIPROP:inputstream.adaptive.license_key={license_key}\n'
        
    m3u_content += f'{url}\n'

# Save the formatted output to zee.m3u
with open('zee.m3u', 'w', encoding='utf-8') as f:
    f.write(m3u_content)

print("Successfully converted 'jiotvplus_keys.json' to 'zee.m3u'!")
