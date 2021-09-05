import requests


""""
Funções de complemento para as views
"""

def powerReles(action=None, ip=None):
    if action == 'ON' and len(action) == 2:
        try:
            if len(ip) <= 15:
                requests.get("http://" + ip + "/cm?cmnd=Power%20On", timeout=2)
        except:
            return
    elif action == 'OFF' and len(action) == 3:
        try:
            if len(ip) <= 15:
                requests.get("http://" + ip + "/cm?cmnd=Power%20Off", timeout=2)
        except:
            return
