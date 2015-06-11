# fb_scrape_public

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
9.    You can download public Facebook page comments by loading a plain text list of post IDs instead of Facebook page names. The IDs can be from different pages.
