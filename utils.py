import requests
import re
import time
from config import CLIENT_KEY, CLIENT_SECRET

class TikTokAPI:
    def __init__(self):
        self.client_key = CLIENT_KEY
        self.client_secret = CLIENT_SECRET
        self.access_token = None
        self.token_expiry = 0

    def get_access_token(self):
        if self.access_token and time.time() < self.token_expiry:
            return self.access_token

        url = "https://open-api.tiktok.com/oauth/token/"
        payload = {
            "client_key": self.client_key,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0:
                    self.access_token = data['data']['access_token']
                    self.token_expiry = time.time() + data['data']['expires_in']
                    return self.access_token
            return None
        except Exception:
            return None

    def extract_video_id(self, url):
        patterns = [
            r'(?:tiktok\.com/.*?/video/)(\d+)',
            r'(?:tiktok\.com/@.*?/video/)(\d+)',
            r'(?:vm\.tiktok\.com/.*?/)(\d+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def get_video_data(self, url):
        video_id = self.extract_video_id(url)
        if not video_id:
            return {'success': False, 'error': 'ভিডিও আইডি খুঁজে পাওয়া যায়নি'}

        token = self.get_access_token()
        if not token:
            return self.fallback_download(url)

        api_url = "https://open-api.tiktok.com/video/list/"
        params = {
            "client_key": self.client_key,
            "access_token": token,
            "video_ids": [video_id]
        }

        try:
            response = requests.get(api_url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0 and data.get('data', {}).get('videos'):
                    video = data['data']['videos'][0]
                    return {
                        'success': True,
                        'video_url': video.get('share_url', ''),
                        'description': video.get('description', ''),
                        'author': video.get('author_name', ''),
                        'duration': video.get('duration', 0),
                        'cover_url': video.get('cover_url', '')
                    }
        except Exception:
            pass

        return self.fallback_download(url)

    def fallback_download(self, url):
        try:
            api_url = f"https://www.tikwm.com/api/?url={url}"
            response = requests.get(api_url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0:
                    video_data = data.get('data', {})
                    return {
                        'success': True,
                        'video_url': video_data.get('play', ''),
                        'description': video_data.get('title', ''),
                        'author': video_data.get('author', {}).get('nickname', ''),
                        'duration': video_data.get('duration', 0),
                        'cover_url': video_data.get('cover', '')
                    }
            return {'success': False, 'error': 'ভিডিও খুঁজে পাওয়া যায়নি'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def download_video_file(self, url, save_path='temp_video.mp4'):
        try:
            response = requests.get(url, stream=True, timeout=30)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True
            return False
        except Exception:
            return False            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True
            return False
        except Exception:
            return False
