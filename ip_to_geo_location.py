#!/usr/bin/python3 

import os
import csv
import sys
import json
import requests

CSV = {}
CACHE = {}


def convert_ip_to_geo_location(ip_address):
    global CACHE
    
    if CACHE.get(ip_address):
        return CACHE.get(ip_address)

    url = f"https://geolocation-db.com/jsonp/{ip_address}"
    response = requests.get(url)
    raw_content = response.text.split("(")[1].strip(")")
    content = json.loads(raw_content)
    
    CACHE[ip_address] = content
    return content


def grab_access_logs(directory: str):
    all_results = []
    for file in os.listdir(directory):
        if not file.startswith("access"):
            continue
        
        path = f"{directory}/{file}"
        content = ""
        with open(path, "r") as f:
            content = f.read()
        
        results = read_log(content)
        all_results += results
    
    return all_results


def read_log(content: str):
    results = []
    
    for line in content.split("\n"):
        # {"country_code":"KR","country_name":"South Korea","city":null,"postal":null,"latitude":37.5112,"longitude":126.97409999999999,"IPv4":"1.236.16.124","state":null}
        
        ip_address = line.split(" ")[0]
        geo_location = convert_ip_to_geo_location(ip_address)
        print("[ DEBUG ] geo_location :", geo_location)
        results.append(geo_location.values())
    
    return results


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"[ USAGE ] {sys.argv[0]} [directory] [result csv file]")
        sys.exit(-1)
    
    directory = sys.argv[1]
    result = sys.argv[2]

    f = open(result, 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    
    results = grab_access_logs(directory)
    wr.writerows(results)
    
    f.close()
    
    # convert_ip_to_geo_location("1.236.16.124")
