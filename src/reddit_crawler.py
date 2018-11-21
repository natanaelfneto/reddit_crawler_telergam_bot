#!/usr/bin/env python
# -*- coding: utf-8 -*-

__project__ = 'reddit_crawler'
__author__ = 'natanaelfneto'
__description__ = "An apprentice scrapper bot"


# python imports
import argparse
import csv
import http.client
import json
import sys
# third party imports
import bs4


# base url for reddit
base_url = 'www.reddit.com'

# check if upvotes are higher than N * 1000
minimum_votes = 5

# start connection
headers = { 'User-Agent' : __description__ }


# get item upvotes
def get_upvotes(div):
    '''
    Argument(s):
        div: a beautiful soup result
    '''

    # get div content
    content = div.get_text()

    # try to parse upvotes number
    try:
        if 'k' in content.split('Posted by')[0]:

            # check if value can be parsed as a float number
            upvotes = float(content.split('Posted by')[0].replace('k',''))

            # check if it is bigger than minimum value
            if upvotes > minimum_votes:
                upvotes = '{0}k'.format(str(upvotes))
            else:
                upvotes = None
        else:
            # upvotes = int(content.split('Posted by')[0])
            upvotes = None
    except:
        upvotes = None
        pass

    # return upvotes value
    return upvotes


# get item title 
def get_title(div):
    '''
    Argument(s):
        div: a beautiful soup result
    '''

    # aux variable
    head = None

    # get head content
    head_content = div.find('h2')

    # get head string content when exist
    if head_content is not None:
        head = head_content.get_text()
        
    # return head content value
    if head is not None:
        return ''.join([i if ord(i) < 128 else '' for i in head])
    else:
        return None


# get link for commentaries
def get_commentaries_link(div):
    '''
    Argument(s):
        div: a beautiful soup result
    '''

    # aux variable
    href = None

    # get all links inside div
    links = div.find_all('a')

    # loop though links
    for link in links:

        # check if it is a 'comments' link
        if link.get('data-click-id') is not None and 'comments' in link.get('data-click-id'):

            # get link content
            href = link.get('href')
            
    # check for no subthreads
    if href is not None:
        return '{0}{1}{2}'.format('https://', base_url, href)
    else:
        return 'No subthreads were found'


# get link for subthreads
def get_subthread_link(div):
    '''
    Argument(s):
        div: a beautiful soup result
    '''

    # aux variable
    href = None

    # get all links inside div
    links = div.find_all('a')

    # loop though links
    for link in links:

        # check if it is a subthread link
        if link.get('href') is not None and 'search?' in link.get('href'):

            # get link content
            href = link.get('href')

    # check for no subthreads
    if href is not None:
        return '{0}{1}{2}'.format('https://', base_url, href)
    else:
        return 'No subthreads were found'


# get html from connection
def get_connection_html(sub):

    # try closing any lost connection
    try:
        # finish connection
        connection.close()
    except:
        pass

    # number of attempts to retrieve posts
    for i in range(5):

        # set connection instance
        connection = http.client.HTTPSConnection(base_url)

        # get request for sub content
        connection.request('GET', '/r/{0}'.format(sub), headers=headers)

        # get response
        html = connection.getresponse()

        if str(html.status) == '200':
            break

    return html


# command line argument parser
def args(args):
    '''
        Main function for terminal call of library
        Arguments:
            args: receive all passed arguments and filter them using
                the argparser library
    '''

    # argparser init
    parser = argparse.ArgumentParser(description=__description__)

    # files to be limited
    parser.add_argument(
        'threads',
        nargs='+',
        help='threads to be crawled', 
        default=None
    )

    # passing filtered arguments as array
    args = parser.parse_args(args)

    # call function
    run(threads=args.threads)


# run function
def run(threads=None, api=False):
    '''
    Argument(s):
        threads: names for threads that will be crawled
    '''

    # aux variable
    subs = threads
    scrapped_subs = []

    # loop through subs
    for sub in subs:

        # aux variable
        array = []

        # get html response from connection
        html = get_connection_html(sub)

        # output connection status and reason
        output = '\nURL: https://{0}/r/{1}\nSTATUS: {2}\nREASON: {3}'.format(base_url, sub, html.status, html.reason)
        print(output)

        if str(html.status) != '200':
            print('No server response')

        # soup html content
        soup = bs4.BeautifulSoup(html,'lxml')

        # get divs
        divs = soup.find_all('div')

        # loop thought founded divs
        for index, div in enumerate(divs):

            # check if it has desired class name
            if div.get('class') is not None and 'scrollerItem' in div.get('class'):
                
                # get upvotes value from div
                upvotes = get_upvotes(div)

                # get title value from div
                title = get_title(div)

                # get commentaries link
                commentaries_link = get_commentaries_link(div)

                # get thread link
                subthread_link = get_subthread_link(div)
                
                # append value if any are None
                if all(v is not None for v in [upvotes, title, commentaries_link, subthread_link]):
                    array.append({
                        'upvotes': str(upvotes),
                        'subreddit': str(sub),
                        'title': title,
                        'commentaries_link': str(commentaries_link),
                        'subthread_link': str(subthread_link)
                    })
        
        # for api call reset scrapped variable
        if api:
            scrapped_subs = []

        # append sub content in a dictionary
        scrapped_subs.append({
            str(sub): array
        })

    # try closing any lost connection
    try:
        # finish connection
        connection.close()
    except:
        pass

    # check is api call to determinate output
    if not api:
        # console output
        output = json.dumps(scrapped_subs, sort_keys=True, indent=4)
        print(output)
    else:
        return (scrapped_subs[0], html.status)


# run function on command call
if __name__ == "__main__":
    args(sys.argv[1:])
# end of code