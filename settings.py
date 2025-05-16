import os
CLOUDFLARE_API_BASE = 'https://api.cloudflare.com/client/v4'
CLOUDFLARE_API_TOKEN = 'NOT_SET'
HEADERS = {
    'Authorization': f'Bearer {CLOUDFLARE_API_TOKEN}',
    'Content-Type': 'application/json'
}
SETTINGS_PATCH = os.path.abspath(__file__)
DIR_PATCH = os.path.dirname(SETTINGS_PATCH)
DEFAULT_DOMAIN = ""
DEFAULT_CONTENT = ""
DEFAULT_SRV_NAME = ""
SETUP = False