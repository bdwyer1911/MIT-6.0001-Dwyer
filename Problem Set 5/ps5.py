# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import re
import os


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    
    def get_guid(self):
        return self.guid
    
    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_link(self):
        return self.link
    
    def get_pubdate(self):
        return self.pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):

    #start with initialiazing our phrase and making it all lower case
    def __init__(self, phrase):
        '''
        initializer for our class
        phrase -> string
        returns -> None
        '''
        self.phrase = phrase.lower()

    def is_phrase_in(self, text):
        '''
        checks if the phrase is in the text
        text -> string
        returns -> boolean
        '''

        #start by cleaning up the phrase
        noPunctPhrase = re.split(r'[^A-Za-z]+', self.phrase) #get only alphabetical characters
        while('' in noPunctPhrase):
            noPunctPhrase.remove('') #remove any empty strings from the list
        cleanedPhrase = ' '.join(noPunctPhrase) + ' ' #join it back together. Extra space at the end is so it doesn't say that 'space cow' is in 'space cows'

        #do the same thing to clean up the text
        noPunctText = re.split(r'[^A-Za-z]+', text.lower())
        while('' in noPunctText):
            noPunctText.remove('')
        cleanedText = ' '.join(noPunctText) + ' '
        
        #return true if the cleaned phrase is in the text
        if cleanedPhrase in cleanedText:
            return True
        else:
            return False
    
    '''
    the below was my first attempt. It works, but it's not very elegant
    '''

    # def is_phrase_in(self, text):
    #     #convert our phrase into a list of words
    #     phraseList = self.phrase.split()

        
        
    #     #turn our text into a list of words splitting on any non-alphabetic character
    #     splitText = re.split(r'[^A-Za-z]+', text.lower())
        
    #     #start by checking if the first word of the phrase is in the text
    #     if phraseList[0] in splitText:
            
    #         #helper variable
    #         checker = False
            
    #         #find where in the text the first word of the phrase is
    #         for i, word in enumerate(splitText):
    #             if word == phraseList[0]:
    #                 startingPoint = i

    #         #then check if the rest of the words in the phrase are in the text in the correct order        
    #         for word in phraseList[1:]:
    #             if word == splitText[startingPoint+1]:
    #                 checker = True
    #                 startingPoint += 1
    #             else:
    #                 return False #can return false immediately once a word doesn't match
                
    #         return checker
    #     else:
    #         return False #we know if the first word of the phrase isn't in the text, we can return false
        

# Problem 3
class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())

# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())
    


# TIME TRIGGERS

# Problem 5

class TimeTrigger(Trigger):
    def __init__(self,pubtime):
        pubtime = datetime.strptime(pubtime, '%d %b %Y %H:%M:%S')
        pubtime = pubtime.replace(tzinfo=pytz.timezone("EST"))
        self.pubtime = pubtime

# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        return self.pubtime > story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))

class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        return self.pubtime < story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))


# COMPOSITE TRIGGERS/

# Problem 7
class NotTrigger(Trigger):
    def __init__(self,trigger):
        self.T = trigger

    def evaluate(self, x):
        return not self.T.evaluate(x)

# Problem 8
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.T1 = trigger1
        self.T2 = trigger2
    
    def evaluate(self, x):
        return self.T1.evaluate(x) and self.T2.evaluate(x)

# Problem 9
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.T1 = trigger1
        self.T2 = trigger2
    
    def evaluate(self, x):
        return self.T1.evaluate(x) or self.T2.evaluate(x)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    filteredStories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story) and story not in filteredStories:
                filteredStories.append(story)
    return filteredStories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    print(lines) # for now, print it so you see what it contains!



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    os.chdir('C:\\Users\\bdwye\\Documents\\Python Scripts\\MIT Homework Assignments\\Problem Set 5\\')
    cwd = os.getcwd()  # Get the current working directory (cwd)
    files = os.listdir(cwd)  # Get all the files in that directory
    print("Files in %r: %s" % (cwd, files))
    # os.chdir('C:\\Users\\bdwye\\Documents\\Python Scripts\\MIT Homework Assignments\\Problem Set 5\\')
    # print(os.getcwd())
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

