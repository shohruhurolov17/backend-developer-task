from typing import Dict
from collections import Counter
from django.conf import settings
import os


def analyze_log_file(file_path: str = 'logs/access.log') -> Dict:

    ips = set()
    endpoints = Counter()
    requests_per_hour = Counter()

    with open(os.path.join(settings.BASE_DIR, file_path), "r") as file:

        for row in file:

            parts = row.split()
            ip = parts[0]
            endpoint = parts[6]

            hour = f"{parts[3].split(':')[1]}:00"

            ips.add(ip)
            endpoints[endpoint] += 1
            requests_per_hour[hour] += 1
    
    endpoints = dict(endpoints.most_common(10))
    requests_per_hour = dict(requests_per_hour)

    return {
        "ips": ips,
        "endpoints": endpoints,
        "requests_per_hour": requests_per_hour
    }
    
    
