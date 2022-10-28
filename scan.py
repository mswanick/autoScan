import subprocess
import time
import psutil
import json
import requests
import os
import signal


def spiderSite(port,site): #Spider the site

    params = {
        'url': site
    }
    status = '' # Status of the scan is represented by %

    requests.get('http://127.0.0.1:8081/JSON/pscan/action/disableAllScanners/', headers=headers) # Disable scanner, only are going to use the spider

    requests.get('http://127.0.0.1:8081/JSON/spider/action/scan/', params=params, headers=headers) # Start the scan

    while status != '100': # Wait until scan is 100% complete to fetch results
        rStatus = requests.get('http://127.0.0.1:8081/JSON/spider/view/status/', params=params, headers=headers) # Check the status of the scan
        tmp = rStatus.json()
        status = tmp['status']
        time.sleep(2)

    r = requests.get('http://127.0.0.1:8081/JSON/spider/view/results/', params=params, headers=headers) # Get the results

    siteData = r.json()

    requests.get('http://127.0.0.1:8081/JSON/spider/action/removeAllScans/', headers=headers) # Delete the scan when done

    return siteData


def writeClientOutput(c,client,site,siteData): # Write the pages of the site
    output = {
        'site': site,
        'pages': []
    }

    for page in siteData['results']:
        tmpPage = page.replace(site, '')
        output['pages'].append(tmpPage)

    c.write(json.dumps(output, indent=4))


def main():

    zapProc = subprocess.Popen(['/home/matt/ZAP_2.11.1/zap.sh','-daemon', '-config', 'api.key=change-me-7857589348057389']) # Start ZAP in daemon mode

    time.sleep(15) # Adjust as needed

    p = psutil.Process(zapProc.pid) # Find the listening port # using its process ID
    cons = psutil.net_connections()
    for con in cons:
        pid = con.pid
        if pid == None:
            pass
        elif int(con.pid) == int(zapProc.pid):
            port = con.laddr.port # Finish later

    f = open('sampleMapping.json') # Open the client mapping and begin spidering
    mapping = json.load(f)
    for entry in mapping['clients']:
        with open(str(entry['client']) + '.json', 'w') as c:
            for site in entry['sites']:
                siteData = spiderSite(port,site)
                writeClientOutput(c, entry['client'], site, siteData)
            c.close()

    os.killpg(os.getpgid(zapProc.pid), signal.SIGTERM) # Stop ZAP

apiKey = 'change-me-7857589348057389'
headers = {
    'Accept': 'application/json',
    'X-ZAP-API-Key': 'change-me-7857589348057389'
}
if __name__ == "__main__":
    main()