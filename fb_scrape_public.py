'''
This script can download posts and comments from public Facebook pages. It requires Python 3.

INSTRUCTIONS

1.    This script is written for Python 3 and won't work with previous Python versions.
2.    You need to create your own Facebook app, which you can do here: https://developers.facebook.com/apps Doesn't matter what you call it, you just need to pull the unique client ID (app ID) and app secret for your new app.
3.    Once you create your app, paste in the client ID and app secret into the quoted fields at lines 27 and 28 below.
4.    Create a plain text file in the same folder as the script containing one or more names of Facebook pages you want to scrape, one per line. This will only work for public pages. For example, if you wanted to scrape Barack Obama's official FB page (http://facebook.com/barackobama/), your first line would simply be 'barackobama' without quotes. I suggest starting with only one page to make sure it works.
5.    Enter the filename of the text file containing your FB page names into the quoted field at line 26 below. (It doesn't have to be a csv but it does need to be plain text.)
6.    Change the name of your output file at line 29 if you like.
7.    Now you should be able to run the script from the Python command line. You can use the following command: exec(open('fb_scrape_public.py').read())
8.    If you did everything correctly, the command line should show you some informative status messages. Eventually it will save a CSV full of data to the same folder where this script was run. If something went wrong, you'll see an error.
9.    You can download Facebook page comments by loading a plain text list of post IDs instead of Facebook page names. The IDs can be from different pages.

'''

import copy
import csv
import json
import socket
import time
import urllib.request

socket.setdefaulttimeout(30)
id_file = 'filename.csv' #change to your input filename
clientid = 'client_id_here' #replace with actual client id
clientsecret = 'client_secret_here' #replace with actual client secret
outfile = 'fb_page_posts.csv' #change the output filename if you like

def load_data(data,enc='utf-8'):
    if type(data) is str:
        csv_data = []
        with open(data,'r',encoding = enc,errors = 'replace') as f:
            reader = csv.reader((line.replace('\0','') for line in f)) #remove NULL bytes
            for row in reader:
                if row != []:
                    csv_data.append(row)
        return csv_data
    else:
        return copy.deepcopy(data)

def save_csv(filename,data,quotes_flag='',file_mode='w',enc='utf-8'): #this assumes a list of lists wherein the second-level list items contain no commas
    with open(filename,file_mode,encoding = enc) as out:
        for line in data:
            if quotes_flag.upper() == "USE_QUOTES":
                row = '"' + '","'.join([str(i).replace('"',"'") for i in line]) + '"' + "\n"
            else:
                row = ','.join([str(i) for i in line]) + "\n"
            out.write(row)

def url_retry(url):
    succ = 0
    while succ == 0:
        try:
            json_out = json.loads(urllib.request.urlopen(url).read().decode(encoding="utf-8"))
            succ = 1
        except(urllib.error.HTTPError, socket.timeout) as e:
            print(str(e))
            time.sleep(1)
    return json_out

def optional_field(dict_item,dict_key):
    try:
        out = dict_item[dict_key]
        if dict_key == 'shares':
            out = dict_item[dict_key]['count']
    except KeyError:
        out = ''
    return out

def make_csv_chunk(fb_json_page,scrape_mode,thread_starter='',msg=''):
    csv_chunk = []
    if scrape_mode == 'posts':
        for line in fb_json_page['data']:
            csv_line = [line['from']['name'], \
            '_' + line['from']['id'], \
            optional_field(line,'message'), \
            optional_field(line,'picture'), \
            optional_field(line,'link'), \
            optional_field(line,'name'), \
            optional_field(line,'description'), \
            line['type'], \
            line['created_time'], \
            optional_field(line,'shares'), \
            line['id']]
            csv_chunk.append(csv_line)
    if scrape_mode == 'comments':
        for line in fb_json_page['data']:
            csv_line = [line['from']['name'], \
            '_' + line['from']['id'], \
            optional_field(line,'message'), \
            line['created_time'], \
            optional_field(line,'like_count'), \
            line['id'], \
            thread_starter, \
            msg]
            csv_chunk.append(csv_line)
            
    return csv_chunk

time1 = time.time()
fb_urlobj = urllib.request.urlopen('https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&client_id=' + clientid + '&client_secret=' + clientsecret)
fb_token = fb_urlobj.read().decode(encoding="latin1")
fb_ids = [i[0].strip() for i in load_data(id_file)]
csv_data = []

for x,fid in enumerate(fb_ids):
    if '_' in fid:
        scrape_mode = 'comments'
        msg_url = 'https://graph.facebook.com/v2.3/' + fid + '?' + fb_token
        msg_json = url_retry(msg_url)
        msg_user = msg_json['from']['name']
        msg_content = optional_field(msg_json,'message')
    else:
        scrape_mode = 'posts'
        msg_user = ''
        msg_content = ''
        
    data_url = 'https://graph.facebook.com/v2.3/' + fid + '/' + scrape_mode + '?limit=100&' + fb_token
    next_item = url_retry(data_url)
    csv_data = csv_data + make_csv_chunk(next_item,scrape_mode,msg_user,msg_content)
    n = 0
    
    while 'paging' in next_item and 'next' in next_item['paging']:
        next_item = url_retry(next_item['paging']['next'])
        csv_data = csv_data + make_csv_chunk(next_item,scrape_mode,msg_user,msg_content)
        try:
            print(n,next_item['data'][len(next_item['data'])-1]['created_time'],time.time()-time1,'seconds elapsed')
        except IndexError:
            break
        n += 1
        time.sleep(1)
    if x % 100 == 0:
        print(x+1,'Facebook IDs archived.')

save_csv(outfile,csv_data,'USE_QUOTES')
print('Script completed in',time.time()-time1,'seconds.')
