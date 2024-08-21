# -*- coding: utf-8 -*-

from urllib.request import urlopen
#from urllib.request import Request
#from time import sleep
import requests
import pandas as pd
import ssl
import urllib.error
import http

ssl.match_hostname = lambda cert, hostname: True
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

t1 = None
t2 = None
code1 = None
code2 = None
s1_url = None
s2_url = None
s1_http = None
s2_http = None
columns = ['Domain1','Status1','Domain2','Status2','HubSpot Website']
index = [0]
count = 1
df_status = pd.DataFrame(columns = columns,index = index)
result_status = pd.DataFrame(columns = columns,index = index)
   
def CheckDomain(website):
    global code1, code2, s1_url, s2_url, s1_http, s2_http, result_status, t1, t2, count
    print ('Currently Checking: ', website)
    count += 1
    if count == 3000:
        return
    prefix_1 = 'https://'
    prefix_2 = 'http://'
    df_status.iat[0,4] = website
    if website.startswith(prefix_1):
        website1 = website
    if website.startswith(prefix_2):
        website1 = website
    else:
        website1 = prefix_1 + website
        try:
            r1 = requests.get(website1, allow_redirects = True, verify = False, headers = headers)
#            t1 = requests.get(website1).elapsed.total_seconds()
#            print (t1)
            website1 = r1.url
            #print ('url: ', website1)
            #Request(website1, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'})
            response1 = urlopen(website1)
            code1 = response1.getcode()
            #website1 = response1.geturl()
            code1 = str(code1)
            df_status.iat[0,0] = str(website1)
            df_status.iat[0,1] = code1
#            print ('Status Code:', code1)
#            print (type(code1))
        except requests.exceptions.ConnectionError:
            df_status.iat[0,0] = str(website1)
            df_status.iat[0,1] = 'ConnectionError'
        except requests.exceptions.RequestException:
            df_status.iat[0,0] = str(website1)
            df_status.iat[0,1] = 'RequestError'
        except urllib.error.URLError as e1:
            s1_url = e1.reason
            s1_url = str(s1_url)
            df_status.iat[0,0] = str(website1)
            df_status.iat[0,1] = s1_url
            #print ('url: ', s1_url)
            #result.iat(1,3) = s1_url
            #print('URL Error:', e1.reason)
        except urllib.error.HTTPError as e1:
            s1_http = e1.code
            df_status.iat[0,0] = str(website1)
            df_status.iat[0,1] = s1_http
            #print ('http: ', s1_http)
            #result.iat(1,4) = s1_http
            #print('HTTP Error:', e1.code)
            #print(type(e.code))
        except http.client.HTTPException:
            df_status.iat[0,0] = str(website1)
            df_status.iat[0,1] = 'HttpError'
        except Exception:
            df_status.iat[0,0] = str(website1)
            df_status.iat[0,1] = 'AllOtherException'           
        finally:
            try:
                website2 = prefix_2 + website
                r2 = requests.get(website2, allow_redirects = True, verify = False, headers = headers)
#                t2 = requests.get(website2).elapsed.total_seconds()
#                print (t2)
                website2 = r2.url
                #Request(website2, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'})
                response2 = urlopen(website2)         
                code2= response2.getcode()
                #website2 = response2.geturl()
                df_status.iat[0,2] = str(website2)
                df_status.iat[0,3] = code2
                #result['Domain2'] = website2
                #result['Code2'] = code2
                #print ('Status Code:',code2)
                #print (type(code2))
            except urllib.error.URLError as e2:
                s2_url = e2.reason
                df_status.iat[0,3] = s2_url
                df_status.iat[0,2] = str(website2)
                #result['s2_url'] = s2_url
                #print('URL Error:', e2.reason)
                #print(type(e.reason))
            except urllib.error.HTTPError as e2:
                s2_http = e2.code
                df_status.iat[0,3] = s2_http
                df_status.iat[0,2] = str(website2)
            except requests.exceptions.ConnectionError:
                df_status.iat[0,2] = str(website2)
                df_status.iat[0,3] = 'ConnectionError'
            except requests.exceptions.RequestException:
                df_status.iat[0,2] = str(website2)
                df_status.iat[0,3] = 'RequestError'
                #result['s2_http'] = s2_http
                #print('HTTP Error:', e2.code)
                #print(type(e.code))
            except http.client.HTTPException:
                df_status.iat[0,2] = str(website2)
                df_status.iat[0,3] = 'HttpError'
            except Exception:
                df_status.iat[0,2] = str(website2)
                df_status.iat[0,3] = 'AllOtherException' 
#        result_status = result_status.append(df_status, ignore_index = True)
        with open('Domain Check Result P7.csv', 'a') as r:
            df_status.to_csv(r, header = False)
        df_status.iloc[0:0]
        return
        

#if __name__ == "__main__":
#    website='footlocker.com'
#    CheckDomain(website)       
        
df = pd.read_csv('HS Company.csv')
df = pd.DataFrame(df)
for i in df['Company Domain Name']:
    CheckDomain(i)



'''
result_status.to_csv('Domain Check Result P3.csv')
'''
