import requests
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('base_url', type=str)
parser.add_argument('username', type=str)
parser.add_argument('password', type=str)

args = parser.parse_args()

params = {
    "username": args.username,
    "password": args.password,
    "cpassword": '',
    "logon": "Login",
}
BASE_URL = f'http://{args.base_url}'

LOGINURL = f'{BASE_URL}/logon.cgi'
LOGOUTURL = f'{BASE_URL}/Logout.htm'
STATURL = f'{BASE_URL}/PortStatisticsRpm.htm'


regex_number_of_ports = r'max_port_num = (\d)'
regex_state = r'state:\[(\d*\S+)\]'
regex_link_status = r'link_status:\[(\d*\S+)\]'
regex_pkts = r'pkts:\[(\d*\S+)\]'

regex_state_info = r'state_info=new Array\((\W\w+\W.+?)\)'
regex_link_into = r'link_info=new Array\((\W\w+\W.+?)\)'


request_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Length": "80",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": BASE_URL,
    "Origin": BASE_URL,
    "Pragma": "no-cache",
    "Referer": f'{BASE_URL}/',
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
}

def clean_states(data):
    return data[:-2]

def clean_links(data):
    return data[:-2]

def clean_pkts(data):
    return list(chunks(data[:-2], 4))

def chunks(l, n):
     
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]
 

def arrange_data(data):
    ret = []
    for port in range(data.get("ports")):
        state_pos = int(data.get('states')[port])
        links_pos = int(data.get('links')[port])
        port_pkts = data.get('pkts')[port]
        ret.append(' '.join([
            f'{port+1}',
            data.get('state_info')[state_pos],
            data.get('link_info')[links_pos],
            port_pkts[0],
            port_pkts[1],
            port_pkts[2],
            port_pkts[3]
        ]))
    return ret


response = requests.post(LOGINURL,headers=request_headers, data=params)
try: 
    stats = requests.get(STATURL)

    html = stats.content.decode("utf-8")

    port = re.search(regex_number_of_ports, html).group(1)
    port_states = re.search(regex_state, html).group(1)
    port_link_status = re.search(regex_link_status, html).group(1)
    port_pkts = re.search(regex_pkts, html).group(1)

    state_info = re.search(regex_state_info, html).group(1)
    link_info = re.search(regex_link_into, html).group(1)

    data = {
        "ports": int(port),
        "states": clean_states(port_states.split(",")),
        "links": clean_links(port_link_status.split(",")),
        "pkts": clean_pkts(port_pkts.split(",")),

        "state_info": state_info.replace('"', "").split(","), 
        "link_info": link_info.replace('"', "").replace("Link Down", "Down").split(",")
    }

    noraml_data = arrange_data(data)
    print(':'.join(noraml_data))
except:
    print("ERROR: Could not parse response")

requests.get(LOGOUTURL)
