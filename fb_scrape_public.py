'''
This script can download posts and comments from public Facebook pages and groups. It requires Python 3.

INSTRUCTIONS

1.    This script is written for Python 3 and won't work with previous Python versions.
2.    The main function in this module is scrape_fb (see comments on lines 147-148). It is the only function most users will need to run directly.
3.    To make this script work, you will need to either:
    a. Create your own Facebook app, which you can do here: https://developers.facebook.com/apps . Doesn't matter what you call your new app, you just need to pull its unique client ID (app ID) and app secret.
    b. Generate your own FB access token using the Graph API Explorer (https://developers.facebook.com/tools/explorer/) or other means.  
4.    Next, you can authenticate using one of the following three methods:
    a. Run the save_creds() function, which will save your credentials to a local file. You will then be able to run scrape_fb from the directory containing the file without including your ID and secret as arguments. Alternatively you can insert a path to your credentials file into the cred_file parameter.
    b. Include your client ID and secret AS STRINGS in the appropriate scrape_fb parameters. 
    c. Include a user-generated token in the token parameter. 
5.    scrape_fb accepts FB page IDs (e.g. 'barackobama') and post IDs preceded by the page ID and an underscore. You can load them into the ids field using a comma-delimited string or by creating a plain text file in the same folder as the script containing one or more names of the Facebook pages you want to scrape, one ID per line (this file MUST have a .csv or .txt extension). For example, if you wanted to scrape Barack Obama's official FB page (http://facebook.com/barackobama/) using the text file method, your first line would simply be 'barackobama' without quotes. I suggest starting with only one ID to make sure it works. You'll only be able to collect data from public pages.
6.    The only required parameters for the scrape_fb function are one of the three authentication methods (see step 4 above) and ids. I recommend not changing the other defaults (except for outfile) unless you know what you're doing.
7.    If you did everything correctly, the command line should show you some informative status messages. Eventually it will save a CSV full of data to the same folder where this script was run. If something went wrong, you'll probably see an error.
'''

import copy
import csv
import datetime
import json
import os
import socket
import time
import urllib.request
socket.setdefaulttimeout(30)

def load_data(data,enc='utf-8'):
    if type(data) is str:
        csv_chunk = []
        with open(data,'r',encoding = enc,errors = 'replace') as f:
            reader = csv.reader((line.replace('\0','') for line in f)) #remove NULL bytes
            for row in reader:
                if row != []:
                    csv_chunk.append(row)
        return csv_chunk
    else:
        return copy.deepcopy(data)

def save_csv(filename,data,use_quotes=True,file_mode='w',enc='utf-8'): #this assumes a list of lists wherein the second-level list items contain no commas
    with open(filename,file_mode,encoding = enc) as out:
        for line in data:
            if use_quotes == True:
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
        except Exception as e:
            print(str(e))
            if 'HTTP Error 4' in str(e):
                return False
            else:
                time.sleep(1)
    return json_out

def optional_field(dict_item,dict_key):
    try:
        if dict_key == 'shares':
            out = dict_item[dict_key]['count']
        elif dict_key == 'likes':
            out = dict_item[dict_key]['summary']['total_count']
        elif dict_key == 'name' or dict_key == 'id':
            out = dict_item['from'][dict_key]
        else:
            out = dict_item[dict_key]
    except (KeyError,TypeError):
        out = 'NA'
    return out
    
def make_csv_chunk(fb_json_page,scrape_mode,thread_starter='',msg='',msg_id='',msg_ctime=''):
    csv_chunk = []
    if scrape_mode == 'feed' or scrape_mode == 'posts':
        try:
            for line in fb_json_page['data']:
                csv_line = [optional_field(line,'name'), \
                optional_field(line,'id'), \
                optional_field(line,'message'), \
                optional_field(line,'picture'), \
                optional_field(line,'link'), \
                optional_field(line,'name'), \
                optional_field(line,'description'), \
                optional_field(line,'type'), \
                line['created_time'], \
                optional_field(line,'shares'), \
                optional_field(line,'likes'), \
                optional_field(line,'LOVE'), \
                optional_field(line,'WOW'), \
                optional_field(line,'HAHA'), \
                optional_field(line,'SAD'), \
                optional_field(line,'ANGRY'), \
                line['id']]
                csv_chunk.append(csv_line)
        except KeyError:
            pass
    if scrape_mode == 'comments':
        try:
            for line in fb_json_page['data']:
                try:
                    app = line['application']
                except KeyError:
                    app = {}
                csv_line = [thread_starter, \
                msg, \
                msg_id, \
                msg_ctime, \
                line['id'], \
                line['created_time'], \
                optional_field(line,'message'), \
                optional_field(line,'comment_count'), \
                optional_field(line,'like_count'), \
                optional_field(line,'LOVE'), \
                optional_field(line,'WOW'), \
                optional_field(line,'HAHA'), \
                optional_field(line,'SAD'), \
                optional_field(line,'ANGRY'), \
                optional_field(line,'permalink_url'), \
                optional_field(app,'category'), \
                optional_field(app,'link'), \
                optional_field(app,'name'), \
                optional_field(app,'namespace'), \
                optional_field(app,'id')]
                csv_chunk.append(csv_line)
        except KeyError:
            pass
            
    return csv_chunk
    
def save_creds():
    print("This program saves your Facebook app credentials so you don't have to enter them every time.")
    client_id = input("Please enter your client (app) ID: ")
    client_secret = input("Please enter your client (app) secret: ")
    cred_json = {"client_id":client_id.strip(),"client_secret": client_secret.strip()}
    with open(".fbcreds",'w',encoding='utf8') as out:
        out.write(json.dumps(cred_json))
    print('Credentials written to file "' + os.getcwd().replace('\\','/') + '/.fbcreds". Assuming you entered valid credentials, you should now be able to use FSP without including them as arguments to the scrape_fb function (within the current directory only). Run this program again to save new credentials.')

'''
# scrape_mode can accept three arguments: "feed," "posts," or "comments." The first pulls all posts from a wall, regardless of author; the second pulls only posts authored by the page owner; and the third pulls comments from a given post permalink. Only use "comments" if your IDs are post permalinks.
# You can use end_date to specify a date around which you'd like the program to stop. It won't stop exactly on that date, but rather a little after it. If present, it needs to be a string in yyyy-mm-dd format. If you leave the field blank, it will extract all available data. 
'''

def scrape_fb(client_id="",client_secret="",cred_file=".fbcreds",token="",ids="",outfile="",version="2.10",scrape_mode="feed",end_date=""):
    time1 = time.time()
    try:
        creds = json.load(open(cred_file))
        client_id = creds['client_id']
        client_secret = creds['client_secret']
    except (FileNotFoundError,json.decoder.JSONDecodeError,KeyError) as e:
        pass
    if type(client_id) is int:
        client_id = str(client_id)
    if token == "":
        fb_urlobj = urllib.request.urlopen('https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret)
        fb_token = 'access_token=' + json.loads(fb_urlobj.read().decode(encoding="latin1"))['access_token']
    else:
        fb_token = 'access_token=' + token
    if "," in ids:
        fb_ids = [i.strip() for i in ids.split(",")]
    elif '.csv' in ids or '.txt' in ids:
        fb_ids = [i[0].strip() for i in load_data(ids)]
    else:
        fb_ids = [ids]

    try:
        end_dateobj = datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
    except ValueError:
        end_dateobj = ''

    if scrape_mode == 'feed' or scrape_mode == 'posts':
        header = ['from','from_id','message','picture','link','name','description','type','created_time','shares','likes','loves','wows','hahas','sads','angrys','post_id']
    else:
        header = ['post_user','post_msg','post_id','post_created_time','comment_id','comment_created_time','comment_message','comment_comment_count','likes','loves','wows','hahas','sads','angrys','comment_permalink_url','app_category','app_link','app_name','app_namespace','app_id']

    csv_chunk = []
    csv_chunk.insert(0,header)
    mem_data = csv_chunk
    if outfile != '':
        save_csv(outfile,csv_chunk,file_mode="a")

    for x,fid in enumerate(fb_ids):
        if scrape_mode == 'comments':
            msg_url = 'https://graph.facebook.com/v' + version + '/' + fid + '?fields=from,message,id,created_time&' + fb_token
            msg_json = url_retry(msg_url)
            if msg_json == False:
                print("URL not available. Continuing...", fid)
                continue
            msg_user = msg_json['from']['name']
            msg_content = optional_field(msg_json,'message')
            msg_id = fid
            msg_ctime = msg_json['created_time']
            field_list = 'message,comment_count,like_count,application,permalink_url,created_time,id'
        else:
            msg_user = ''
            msg_content = ''
            msg_id = ''
            msg_ctime = ''
            field_list = 'from,message,picture,link,name,description,type,created_time,shares,likes.summary(total_count).limit(0)'
            
        data_url = 'https://graph.facebook.com/v' + version + '/' + fid.strip() + '/' + scrape_mode + '?fields=' + field_list + '&limit=100&' + fb_token
        data_rxns = []
        new_rxns = ['LOVE','WOW','HAHA','SAD','ANGRY']
        for i in new_rxns:
            data_rxns.append('https://graph.facebook.com/v' + version + '/' + fid.strip() + '/' + scrape_mode + '?fields=reactions.type(' + i + ').summary(total_count).limit(0)&limit=100&' + fb_token)
        
        next_item = url_retry(data_url)
        
        if next_item != False:
            for n,i in enumerate(data_rxns):
                tmp_data = url_retry(i)
                for z,j in enumerate(next_item['data']):
                    try:
                        j[new_rxns[n]] = tmp_data['data'][z]['reactions']['summary']['total_count']
                    except (KeyError,IndexError):
                        j[new_rxns[n]] = 0
                
            csv_chunk = make_csv_chunk(next_item,scrape_mode,msg_user,msg_content,msg_id,msg_ctime)
            mem_data.extend(csv_chunk)
            if outfile != '':
                save_csv(outfile,csv_chunk,file_mode="a")
        else:
            print("Skipping ID " + fid + " ...")
            continue
        n = 0
        
        while 'paging' in next_item and 'next' in next_item['paging']:
            next_item = url_retry(next_item['paging']['next'])
            try:
                for i in new_rxns:
                    start = next_item['paging']['next'].find("&fields=") + 8
                    end = next_item['paging']['next'].find("&",start+1)
                    next_rxn_url = next_item['paging']['next'][:start] + 'reactions.type(' + i + ').summary(total_count).limit(0)' + next_item['paging']['next'][end:]
                    tmp_data = url_retry(next_rxn_url)
                    for z,j in enumerate(next_item['data']):
                        try:
                            j[i] = tmp_data['data'][z]['reactions']['summary']['total_count']
                        except (KeyError,IndexError):
                            j[i] = 0
            except KeyError:
                continue
            
            csv_chunk = make_csv_chunk(next_item,scrape_mode,msg_user,msg_content,msg_id,msg_ctime)
            mem_data.extend(csv_chunk)
            if outfile != '':
                save_csv(outfile,csv_chunk,file_mode="a")
            try:
                print(n+1,"page(s) of data archived for ID",fid,"at",next_item['data'][-1]['created_time'],".",round(time.time()-time1,2),'seconds elapsed.')
            except IndexError:
                break
            n += 1
            time.sleep(1)
            if end_dateobj != '' and end_dateobj > datetime.datetime.strptime(next_item['data'][-1]['created_time'][:10],"%Y-%m-%d").date():
                break
        print(x+1,'Facebook ID(s) archived.',round(time.time()-time1,2),'seconds elapsed.')

    print('Script completed in',time.time()-time1,'seconds.')
    return mem_data
    