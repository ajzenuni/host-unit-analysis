import sys
import requests
import json
from helper.api import check_error
from helper.host_unit import calculate_host_unit
import schedule
import time

def get_host(url, headers, host_groups):
    host_url = f'{url}/api/v2/entities'
    init_params = {
        'pageSize': 1000,
        'entitySelector': 'type("host")',
        'from': 'now-1d',
        'fields': 'properties.monitoringMode,properties.memoryTotal,fromRelationships.isInstanceOf'
    } 
    while host_url:
        response = requests.get(host_url, headers=headers, params=init_params)
        data = response.json()
        check_error(data)
        for entity in data['entities']:
            display_name = entity['displayName']
            properties = entity.get('properties', {})
            memory_total = properties.get('memoryTotal', 0)
            monitoring_mode = properties.get("monitoringMode",0)
            host_unit = calculate_host_unit(memory_total, monitoring_mode)
            if 'fromRelationships' in entity and entity['fromRelationships']:
                host_group_id = entity['fromRelationships']['isInstanceOf'][0]['id']
                host_groups[host_group_id]["hosts"].append({
                    "displayName": display_name,
                    "memoryTotal": memory_total,
                    "monitoringMode": monitoring_mode,
                    "hostUnit": host_unit
                })
                host_groups[host_group_id]["totalHostUnit"] += host_unit
            else:
                host_groups["no_host_group"]["hosts"].append({
                    "displayName": display_name,
                    "memoryTotal": memory_total,
                    "monitoringMode": monitoring_mode,
                    "hostUnit": host_unit
                })
                host_groups["no_host_group"]["totalHostUnit"] += host_unit
        host_url = data.get('nextPageKey')
        time.sleep(0.500)

    return host_groups

def get_host_group(url, headers):
    host_group_url = f'{url}/api/v2/entities'
    init_params = {
        'pageSize': 1000,
        'entitySelector': 'type("host_group")',
        'from': 'now-1d'
    }
    host_groups = {'no_host_group':{'displayName':'none','hosts':[],'totalHostUnit':0}}

    while host_group_url:
        response = requests.get(host_group_url, headers=headers, params=init_params)
        data = response.json()
        check_error(data)
        for entity in data['entities']:
            entity_id = entity['entityId']
            display_name = entity['displayName']
            host_groups[entity_id] = {'displayName': display_name, "hosts":[], "totalHostUnit":0}

        host_group_url = data.get('nextPageKey')
        time.sleep(0.500)

    return host_groups

def post_host_unit_analysis_metric(host_group_analysis_final, url, headers):
    metric_url = f'{url}/api/v2/metrics/ingest'

    metric_lines = []

    for host_group_id, host_group_data in host_group_analysis_final.items(): 
        display_name = host_group_data["displayName"]
        total_host_unit = host_group_data["totalHostUnit"]
        metric_lines.append(f'hostUnit.analysis,host_group.name="{display_name}" {total_host_unit:.2f}')
    
    lines = '\n'.join(metric_lines)
    response = requests.post(metric_url,headers=headers,data=lines.encode('utf-8'))
    data = response.json()
    check_error(data)
    print(data)

def main():
    if len(sys.argv) != 5:
            print("Usage: python host_unit_analysis.py managed_url managed_api-token(API v2:Read Entities,API v1:Access problem and event feed, metrics, and topology) saas_url saas_api-token(API v2:Ingest metrics)")
            sys.exit(1)
    urlGet = sys.argv[1].rstrip('/')
    tokenGet = sys.argv[2]
    urlPost = sys.argv[3].rstrip('/')
    tokenPost = sys.argv[4]

    headersGet = {
        'Content-Type': 'application/json', 
        'Authorization' : f'Api-Token {tokenGet}'
    }

    headersPost = {
        'Content-Type': 'text/plain', 
        "charset": 'utf-8',
        'Authorization' : f'Api-Token {tokenPost}'
    }
    # Define a job function that runs your script with provided arguments
    def job():
        print("Job is running...")
        host_groups = get_host_group(urlGet, headersGet)
        final_host_groups = get_host(urlGet, headersGet, host_groups)
        post_host_unit_analysis_metric(final_host_groups, urlPost, headersPost)
        print("Job completed successfully.")

    # Schedule the job to run every 2 minutes
    schedule.every(2).minutes.do(job)

    # Main loop to continuously check and run scheduled jobs
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep for a second to avoid high CPU usage

if __name__ == '__main__':
    main()
