# fb_scrape_public

This script can download posts and comments from public Facebook pages and groups (__but not users__). It requires Python 3.

Installation
------------

``pip3 install fb_scrape_public`` will work, but you can also simply download the script and place it in your PYTHONPATH directory.

Instructions
------------

1.    This script is written for Python 3 and won't work with previous Python versions.
2.    The main function in this module is ```scrape_fb``` (see comments on lines 147-148). It is the only function most users will need to run directly.
3.    To make this script work, you will need to either:
      1. Create your own Facebook app, which you can do here: https://developers.facebook.com/apps . Doesn't matter what you call your new app, you just need to pull its unique client ID (app ID) and app secret.
      2. Generate your own FB access token using the Graph API Explorer (https://developers.facebook.com/tools/explorer/) or other means. 
4.    Next, you can authenticate using one of the following three methods:
      1. Run the ```save_creds()``` function, which will save your FB app credentials to a local file. You will then be able to run ```scrape_fb``` from the directory containing the file without including your ID and secret as arguments. Alternatively you can insert a path to your credentials file into the ```cred_file``` parameter.
      2. Include your client ID and secret AS STRINGS in the appropriate ```scrape_fb``` parameters. 
      3. Include a user-generated token in the ```token``` parameter. 
5.    ```scrape_fb``` accepts FB page IDs ('barackobama') and post IDs preceded by the page ID and an underscore (for more details on post ID format, see [here](https://stackoverflow.com/questions/31353591/how-should-we-retrieve-an-individual-post-now-that-post-id-is-deprecated-in-v)). You can load them into the ```ids``` field using a comma-delimited string or by creating a plain text file in the same folder as the script containing one or more names of the Facebook pages you want to scrape, one ID per line. For example, if you wanted to scrape Barack Obama's official FB page (http://facebook.com/barackobama/) using the text file method, your first line would simply be 'barackobama' without quotes. I suggest starting with only one ID to make sure it works. You'll only be able to collect data from public pages and groups. For groups you'll need the group ID number; the string alias won't work.
6.    The only required fields for the ```scrape_fb``` function are one of the three authentication methods (see step 4 above) and ```ids```. I recommend not changing the other defaults unless you know what you're doing (except for ```outfile``` if you want to save your data to disk and ```scrape_mode``` if you want to pull post comments).
7.    If you did everything correctly, the command line should show you some informative status messages. Eventually it will save a CSV full of data to the same folder where this script was run if you've set ```outfile```. If something went wrong, you'll probably see an error.

Sample code
-----------

```python
import fb_scrape_public as fsp

#below, "YourClientID," "YourClientSecret," and "YourAccessToken" should be your actual client ID, secret, and access token

# to save your Facebook app credentials to disk
fsp.save_creds() 

# if you've run save_creds() once, you can enter the following to get page posts:
obama_posts = fsp.scrape_fb(ids="barackobama") 

# if you haven't run save_creds(), use this (id/secret mode)
obama_posts = fsp.scrape_fb("YourClientID","YourClientSecret",ids="barackobama") 

# or this (access token mode). the outfile attribute is also set, which means the data will be saved to disk
obama_posts = fsp.scrape_fb(token="YourAccessToken",ids="barackobama",outfile='obama_posts.csv') 

# to get comments on a single post (id/secret mode)
comments = fsp.scrape_fb("YourClientID","YourClientSecret",ids="6815841748_10154508876046749",scrape_mode="comments") 
```
