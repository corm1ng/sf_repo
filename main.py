import os
import argparse
import requests
import json
import sys

# Функция проверки доступности севрвиса
def do_ping_sweep(ip, num_of_host):
    scanned_ip = ip
    # Проверка доступности домена 
    if ip in "qwertyuiopasdfghjklzxcvbnm.":
        scanned_ip = ip
    # Проверка доступности адреса    
    elif ip in "123456789": 
        ip_parts = ip.split('.')
        network_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'
        scanned_ip = network_ip + str(int(ip_parts[3]) + num_of_host)
    response = os.popen(f'ping -c 2 {scanned_ip}')
    res = response.readlines()
    print(f"[#] Result of scanning: {scanned_ip} [#]\n{res[2]}", end='\n')
 
# Функция отпраки HTTP запросов 
def sent_http_request(target, method, headers=None, payload=None):
    headers_dict = dict()
    if headers:
        for header in headers:
            header_name = header.split(':')[0]
            header_value = header.split(':')[1:]
            headers_dict[header_name] = ':'.join(header_value)
    # Обработал ошибку явнового указания метода
    if method == "GET" or "get":
        response = requests.get(target, headers=headers_dict)
    elif method == "POST" or "post":
        response = requests.post(target, headers=headers_dict, data=payload)
    print(
        f"[#] Response status code: {response.status_code}\n"
        f"[#] Response headers: {json.dumps(dict(response.headers), indent=4, sort_keys=True)}\n"
        f"[#] Response content:\n {response.text}"
    )

# Функция обработки режима работы утилиты
def switch(param):
    match param.task:
        case "scan":
            # На случай, если утилита вызывается без параметра
            if param.num_of_hosts == None: param.num_of_hosts = 10
            for host_num in range(param.num_of_hosts):
                do_ping_sweep(param.ip, host_num)
        case "sendhttp":
            sent_http_request(param.target, param.method, param.headers)
        case _:
            print("error")

# Функция отображения возникновения ошибки
def myerror(message):
    print('Error message:', message)

# Парсинг параметров вызова утилиты
parser = argparse.ArgumentParser(description='Network scanner')
parser.add_argument('task', choices=['scan', 'sendhttp'], help='Network scan or send HTTP request')
parser.add_argument('-i', '--ip', type=str, help='IP address')
parser.add_argument('-n', '--num_of_hosts', type=int, help='Number of hosts')
parser.add_argument('-t', '--target', type=str, help='URL')
parser.add_argument('-m', '--method', type=str, help='Method')
parser.add_argument('-hd', '--headers', type=str, nargs='*', help='Headers')

parser.error = myerror
args=parser.parse_args()

switch(args)
