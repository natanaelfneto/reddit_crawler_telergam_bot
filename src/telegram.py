# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

__project__ = 'reddit_crawler_bot'
__author__ = 'natanaelfneto'
__description__ = "An apprentice scrapper bot"


# python imports
import sys
import time
# third party imports
import telepot
from telepot.loop import MessageLoop
from telepot.text import apply_entities_as_markdown
# self imports
import reddit_crawler
from reddit_crawler import (
    base_url,
    minimum_votes
)


# update answer 
def answer_update(thread):
    '''
    Argument(s):
        thread: name for reddit threads to be crawled
    '''

    # number of attempts to retrieve posts
    for i in range(3):

        # attempts count output
        output = 'Attempt {0}...'.format(i+1)

        # get crawler output
        crawler_output, status = reddit_crawler.run([thread], api=True)

        # check if answer is nothing due to connection response errors
        if len(crawler_output[thread]) != 0:
            break
        
        # thread does not exist
        if str(status) == '404':
            break
        
        # print output message for attempts
        print(output)
    
    # return output from crawler
    return crawler_output

# format output message
def output_formatter(output, thread):
    '''
    Argument(s):
        output: income object from reddit cralwer
        thread: name for reddit thread
    '''

    # aux variables
    output_head = ''
    output_body = ''

    # check thread name sent and received
    if list(output.keys())[0] != thread:
        formatted_output = None
        print('received thread object does not macth requested')

    else:
        # message head
        output_head = '''
            <b>THREAD</b>: {0} [<a href='{1}/r/{2}/'>thread link</a>]
        '''.format(thread, base_url, thread)

        # message body
        if len(output[thread]) < 1:
            # if no post matches requested parameters
            output_body = '''
                No threads with more than {0}k upvotes could be retrieved, try again in a few minutes
            '''.format(minimum_votes)

        else:
            # for each post that matches requested parameters
            for post in output[thread]:
                
                # build body message for a post
                output_body += '''
                    <b>title</b>: {0}
                    <b>upvotes</b>: {1}
                    <b>link to commentaries</b>: <a href='{2}'>link</a>
                    <b>link to subthread</b>: <a href='{3}'>llink</a>\n
                '''.format(post['title'], post['upvotes'], post['commentaries_link'], post['subthread_link'])

    # build output
    formatted_output = output_head + output_body

    # return formatted message output
    return formatted_output


# handler function for bot message income
def handler(msg):
    '''
    Argument(s):
        msg: receive messagem from user input on telegram bot chat
    '''

    # get message from glance
    content_type, chat_type, chat_id = telepot.glance(msg)
    output = '\nINPUT:\n\tcontent type: {0}\n\ttype: {1}\n\tchat id: {2}'.format(content_type, chat_type, chat_id)
    print(output)

    # standard asnwer
    answer = "Desculpe, não entendi."

    # check if input is a text
    if content_type == 'text':

        # avoid case sensitivity
        command = msg['text'].strip().lower()

        # check command
        the_command = '/nadaprafazer'
        if command.startswith(the_command):

            # putify commmand
            threads = command.replace(the_command, '').strip().split(chr(32))

            # filter empty spaces
            threads =  list(filter(None, threads))

            # aux variables
            total_requests = len(threads)
            sent_requests = 0

            # output total requests
            output = '\tpending requests: {0}'.format(total_requests)
            print(output)

            # get answer for each request
            for thread in threads:

                # aux variables
                answer = None

                # check if request thread is not spaces that went though
                if len(thread.strip()) != 0:
                    
                    # update answer
                    output = answer_update(thread)

                    # format object to a friendly telegram message
                    answer = output_formatter(output, thread)

                # check if there is an answer
                if answer is not None:
                    # send answer
                    bot.sendMessage(chat_id, answer, parse_mode='html')

                # increment
                sent_requests += 1

                # output sent requests
                output = '{0} out of {1} request sent'.format(sent_requests, total_requests)
                print(output)
            
            # 
            return
    
    # send answer
    bot.sendMessage(chat_id, answer)

    # 
    return


# start bot based on token
TOKEN = str(sys.argv[1])
bot = telepot.Bot(TOKEN)

# run bot handler as thread
MessageLoop(bot, handler).run_as_thread()

# output start message
output = 'Starting {0}\nAuthor: {1}\nDescription: {2}\n\nWaiting for inputs...'.format(__project__, __author__, __description__)
print (output)

# Keep the program running.
while 1:
    time.sleep(10)