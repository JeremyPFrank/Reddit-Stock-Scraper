import praw
import datetime
import yfinance as yf

subreddits = ['pennystocks','stocks','stockmarket','wallstreetbets','investing','options','finance','dividends','securityanalysis','daytrading']

reddit = praw.Reddit(client_id="Qcfec1wiO5C6Vw5k75t0CA", client_secret="OKXUlnL4CXoQu9P4n2hY-MkNivqxlA",user_agent="Jeremy Frank")#gain access to reddit         
comments = [] #make a list to hold comments
tickers = []

count=0
first = ""

def get_date(submission):#Gets the Date of submission
	time = submission.created
	return datetime.date.fromtimestamp(time)


for subreddit_in_list in subreddits: 
    for submission in reddit.subreddit(subreddit_in_list).new(limit=5000):#Determines the date program was run
        first = get_date(submission)
        break
            
    for submission in reddit.subreddit(subreddit_in_list).new(limit=5000): #iterates through subreddit __ with limit __
        if get_date(submission) != first:
            break
        if "$" in submission.title or ":" in submission.title:  # if __ is in submission title, add the title to the list
           comments.append(submission.title)
        elif "$" in submission.selftext or ":" in submission.selftext: # if __ is in submission text and not in title, add text to list
            comments.append(submission.selftext)

for text in comments:#remove any posts without text
    if text == "":
        comments.remove(text)

for com_text in comments:
    known = [] #stores tickers already found in each comment
    for x in range(0,len(com_text)):
        if com_text[x] == "$" or com_text[x] ==':':
            temp=""
            for y in range(x+1,len(com_text)):
                if(not com_text[y].isalpha()):#locate tickers by isolating words starting with '$'
                    break
                else: 
                    temp+=com_text[y]
            if temp not in known: #confirm that ticker was not already found in same comment
                known.append(temp)
                tickers.append(temp)
index=0
while (index<len(tickers)):
    if (tickers[index]=='' or tickers[index]=='Ticker'):#confirm that '$' is followed by alpha and that it is not followed by the common 'Ticker'
        tickers.remove(tickers[index])
        index-=1
    index+=1

for item in tickers:
    item = item.upper() #set all tickers to all capital letters to make data analysis easier


distribution = [] #create imbedded lists with each ticker along with how often it appears in the sample
in_distribution=[]
for stock in tickers:
    if (stock not in in_distribution):
        distribution.append([stock,1])
        in_distribution.append(stock)
    else:
        for item in distribution:
            if stock==item[0]:
                item[1]+=1
                
#Iterate through all comments and add to counts based on dicussion in comments
for each_subreddit in subreddits:
    all_comments=[]
    for submission in reddit.subreddit(each_subreddit).new(limit=5000):
        if get_date(submission) != first:
            break
        submission.comments.replace_more(limit=5000)
        for top_level_comment in submission.comments:
            all_comments.append(top_level_comment.body)
    for indiv_comment in all_comments:
        for indiv_ticker in distribution:
           if indiv_ticker[0] in indiv_comment:
                indiv_ticker[1]+=1
                
rng = len(distribution) #bubble sort to place list in order from highest post frequency to lowest frequency
for i in range(rng):
    done = True #turn to true when sorting is compelte
    for j in range(rng-i-1):
        if distribution[j][1] < distribution[j+1][1]:
            distribution[j],distribution[j+1]=distribution[j+1],distribution[j]#swap in decending order based on the ticker's frequency
        if distribution[j][1] == distribution[j+1][1]:
            if distribution[j][0] > distribution[j+1][0]:
                distribution[j],distribution[j+1]=distribution[j+1],distribution[j] #swap into alphabetical order if frequency is equal


stock_stats=[]
the_temp=[]
yf_ticker = yf.Ticker('GOOGL').info
for spef_stock in distribution: #Add in Stock Info 
    the_temp = spef_stock[0]
    yf_ticker = yf.Ticker(the_temp).info
    spef_stock.append(yf_ticker['previousClose'])
    spef_stock.append(yf_ticker['open'])
#'Distribution' is currently in form [ticker symbol, frequency, previous close price, open price]
print(distribution)



