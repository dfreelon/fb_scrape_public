# fb_scrape_public

This script can download posts and comments from public Facebook pages and groups (__but not users__). It requires Python 3.

------------
Installation
------------

``pip3 install fb_scrape_public`` will work, but you can also simply download the script and place it in your PYTHONPATH directory. If you attempt the former, you'll need to use ``from fb_scrape_public import fb_scrape_public`` to enable its functionality. If the latter, ``import fb_scrape_public`` will work.

------------
Instructions
------------

1.    This script is written for Python 3 and won't work with previous Python versions.
2.    The main function in this module is scrape_fb (see lines 107-109). It is the only function most users will need to run directly.
3.    You need to create your own Facebook app, which you can do here: https://developers.facebook.com/apps . Doesn't matter what you call it, you just need to pull the unique client ID (app ID) and app secret for your new app.
4.    Once you create your app, you can insert the client ID and secret AS STRINGS into the appropriate scrape_fb fields. 
5.    This function accepts text FB user IDs ('barackobama'), numerical user IDs, and post IDs (but these must contain the page or group ID as a prefix; see [here](https://stackoverflow.com/questions/31353591/how-should-we-retrieve-an-individual-post-now-that-post-id-is-deprecated-in-v)). You can load them into the ids field using a comma-delimited string or by creating a plain text file in the same folder as the script containing one or more names of the Facebook pages you want to scrape, one ID per line. For example, if you wanted to scrape Barack Obama's official FB page (http://facebook.com/barackobama/) using the text file method, your first line would simply be 'barackobama' without quotes. I suggest starting with only one ID to make sure it works. You'll only be able to collect data from public pages and groups.
6.    The only required fields for the scrape_fb function are client_id, client_secret, and ids. I recommend not changing the other defaults unless you know what you're doing (except for ```outfile``` if you want to change the name of the output file and ```scrape_mode``` if you want to pull post comments).
7.    If you did everything correctly, the command line should show you some informative status messages. Eventually it will save a CSV full of data to the same folder where this script was run. If something went wrong, you'll see an error.

-----------
Sample code
-----------

```python
import fb_scrape_public as fsp #if installed manually,
#OR
from fb_scrape_public import fb_scrape_public as fsp #if installed via pip
#below, client_id and client_secret should be your actual client ID and secret

#to get page posts
obama_posts = fsp.scrape_fb("client_id","client_secret","barackobama") 
#to get comments on a single post
comments = fsp.scrape_fb("client_id","client_secret","6815841748_10154508876046749",scrape_mode="comments") 
```
