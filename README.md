# fb_scrape_public

This script can download posts and comments from public Facebook pages and groups (__but not users__). It requires Python 3.

Installation
------------

``pip3 install fb_scrape_public`` will work, but you can also simply download the script and place it in your PYTHONPATH directory.

Instructions
------------

1.    This script is written for Python 3 and won't work with previous Python versions.
2.    The main function in this module is ```scrape_fb``` (see lines 113-115). It is the only function most users will need to run directly.
3.    To make this script work, you will need to either:
    a. Create your own Facebook app, which you can do here: https://developers.facebook.com/apps . Doesn't matter what you call your new app, you just need to pull its unique client ID (app ID) and app secret.
    b. Generate your own FB access token using the Graph API Explorer (https://developers.facebook.com/tools/explorer/) or other means. 
4.    Next, you can either insert your client ID and secret AS STRINGS into the appropriate scrape_fb fields OR insert your token into the ```token``` field. 
5.    ```scrape_fb``` accepts FB page IDs ('barackobama') and post IDs preceded by the page ID and an underscore (for more details on post ID format, see [here](https://stackoverflow.com/questions/31353591/how-should-we-retrieve-an-individual-post-now-that-post-id-is-deprecated-in-v)). You can load them into the ```ids``` field using a comma-delimited string or by creating a plain text file in the same folder as the script containing one or more names of the Facebook pages you want to scrape, one ID per line. For example, if you wanted to scrape Barack Obama's official FB page (http://facebook.com/barackobama/) using the text file method, your first line would simply be 'barackobama' without quotes. I suggest starting with only one ID to make sure it works. You'll only be able to collect data from public pages and groups.
6.    6.    The only required fields for the ```scrape_fb``` function are ```token``` OR (```client_id``` AND ```client_secret```), and ```ids```. I recommend not changing the other defaults unless you know what you're doing (except for ```outfile``` if you want to change the name of the output file and ```scrape_mode``` if you want to pull post comments).
7.    If you did everything correctly, the command line should show you some informative status messages. Eventually it will save a CSV full of data to the same folder where this script was run. If something went wrong, you'll see an error.

Sample code
-----------

```python
import fb_scrape_public as fsp

#below, "YourClientID," "YourClientSecret," and "YourAccessToken" should be your actual client ID, secret, and access token

#to get page posts, Facebook App mode
obama_posts = fsp.scrape_fb("YourClientID","YourClientSecret",ids="barackobama") 
#to get page posts, access token mode
obama_posts = fsp.scrape_fb(token="YourAccessToken",ids="barackobama") 
#to get comments on a single post, Facebook App mode
comments = fsp.scrape_fb("YourClientID","YourClientSecret",ids="6815841748_10154508876046749",scrape_mode="comments") 
```
