#Importing various libraries useful to the program
import matplotlib
import matplotlib.dates as dates
from tkinter import *
from bs4 import BeautifulSoup
import requests
import lxml
import datetime
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

#Graphical User Interface
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
root = Tk()
root.title("Stock Price")
root.configure(background="white")

Calculator = Frame(root, height=300, width=700, bg="white").grid(column=0, row=2)
title = Label(root, bg="white", text="Stock Price Calculator", font="Sans 25 bold", fg="black").grid(row=0)

Stock_ticker = Label(root, text="Input stock ticker here:", font="Sans 18 bold")
Stock_ticker.place(x=7, y=60)
Ticker_entry = Entry(root, width=20)
Ticker_entry.place(x=235, y=64)

Stock_price = Label(root, text="Current stock price:", font="Sans 15")
Stock_price.place(x=7, y=100)

Stock_price_output = Entry(root, width=10)
Stock_price_output.place(x=160, y=100)

Stock_price_day = Label(root, text="Opening price for the day:", font="Sans 15")
Stock_price_day.place(x=7, y=140)

Stock_price_day_output = Entry(root, width=10)
Stock_price_day_output.place(x=195, y=141)

Last_closing_price = Label(root, text="Last closing price:", font="Sans 15")
Last_closing_price.place(x=7, y=180)

Last_closing_price_output = Entry(root, width=10)
Last_closing_price_output.place(x=180, y=181)

Stock_news = Label(root, text="News about stock:", font="Sans 15")
Stock_news.place(x=7, y=220)

Stock_news_output1 = Entry(root, width=50)
Stock_news_output1.place(x=150, y=221)

Stock_news_output2 = Entry(root, width=50)
Stock_news_output2.place(x=150, y=242)

Stock_news_output3 = Entry(root, width=50)
Stock_news_output3.place(x=150, y=263)

Submit = Button(root, text="Submit", font="Sans 14", command = lambda: Calculation())
Submit.place(x=165, y=300)

Reset = Button(root, text="Reset", font="Sans 14", command = lambda: Cleaning(Ticker_entry, Stock_price_output, Stock_price_day_output, Last_closing_price_output, Stock_news_output1, Stock_news_output2, Stock_news_output3))
Reset.place(x=250, y=300)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def make_url(ticker_symbol): #making a function that returns a useful URL when a ticker is passed through it
    return "https://www.bloomberg.com/quote/%s:US" % ticker_symbol

def make_historical_url(ticker_symbol): #making a function that returns another useful URL when a ticker is passed through it
    return "https://www.nasdaq.com/symbol/%s/historical" % ticker_symbol

def Calculation():
    lower_stock = Ticker_entry.get() #collecting the user input from the entry in the GUI
    stock = lower_stock.upper() #Making sure that even if the ticker entry was lower case, it is converted into upper case so that the URL is correct
    url = make_url(stock) #Passing the ticker through the predefined function
    page = requests.get(url) #Requesting the HTML code of the website whose URL was accessed
    soup = BeautifulSoup(page.content, "lxml") #Converting the HTML code of the website into a beautifulsoup object, so that it can be manipulated

    try:
        #Finding and inserting the current price
        current_number = soup.find('span', attrs={'class':'priceText__1853e8a5'}) #Searching for the piece of HTML code with these specific attributes. These attributes correspond to where the current price of the stock is displayed
        current_price = current_number.text #Taking only the portion of that code that contains actual information, meaning leaving HTML tags behind
        Stock_price_output.insert(0, "$") #Inserting dollar symbol into the entry
        Stock_price_output.insert(1, current_price) #Inserting the stock price into the entry

        #Finding and inserting opening price
        opening_number = soup.find('div', attrs={'class':'value__b93f12ea'}) #Searching for the piece of HTML code with these specific attributes. These attributes correspond to where the opening price of the stock is displayed
        opening_price = opening_number.text #Taking only the portion of that code that contains actual information, meaning leaving HTML tags behind
        Stock_price_day_output.insert(0, "$") #Inserting dollar symbol into the entry
        Stock_price_day_output.insert(1, opening_price) #Inserting the opening price of the stock into the entry

        #Finding and inserting last closing price
        closing_numbers = soup.find_all('div', attrs={'class':'value__b93f12ea'}) #Searching for the piece of HTML code with these specific attributes. These attributes correspond to where the last closing price of the stock is display
        closing_number = closing_numbers[1] #There are multiple closing prices on the website, so this one takes the one that corresponds to the last closing number.
        closing_price = closing_number.text #Taking only the portion of that code that contains actual information, meaning leaving HTML tags behind
        Last_closing_price_output.insert(0, "$") #Inserting dollar symbol into the entry
        Last_closing_price_output.insert(1, closing_price) #Inserting the last closing price of the stock into that entry

        #Finding and inserting news
        news = soup.find_all('div', attrs={'class':'headline__07dbac92'}) #Searching for the piece of HTML code with these specific attributes. These attributes correspond to where news about the stock is displayed
        news_1 = news[1].text #There are 3 news titles on the website that all contain the same tags. This code takes the first one.
        news_2 = news[2].text #There are 3 news titles on the website that all contain the same tags. This code takes the second one.
        news_3 = news[3].text #There are 3 news titles on the website that all contain the same tags. This code takes the third one.

        Stock_news_output1.insert(0, news_1) #Inserting the first news title into the first entry.
        Stock_news_output2.insert(0, news_2) #Inserting the second news title into the second entry.
        Stock_news_output3.insert(0, news_3) #Inserting the third news title into the third entry.

        #Drawing the graph of the stock
        historical_url = make_historical_url(stock) #Receiving the URL that contains a data table with all the information of the stock
        historical_page = requests.get(historical_url) #Requesting the HTML code of the website whose URL was accessed
        soup_2 = BeautifulSoup(historical_page.content, "lxml") #Transforming the HTML code into a beautifulsoup object that can be manipulated
        all_numbers = soup_2.find('tbody') #Finding code segment that corresponds the body of the table, the part that contains all the information about the stocks
        all_nums = all_numbers.text #Taking only the portion of that code that contains actual information, meaning leaving HTML tags behind
        all_nums_1 = all_nums.split() #Transforming the single string of elements into an array that contains each element
        length = len(all_nums_1) #Calling the length of this array 'length'

        prices = [] #Creating an empty array that will contain the prices of the stocks
        dates = [] #Creating an empty array that will contain the corresponding dates of the stocks

        current_time = datetime.datetime.now() #Taking the the date of today, so that it may be used in the array 'dates'
        current_time_format = current_time.strftime("%m/%d/%Y") #Letting the program know what the current time format of the dates is. It is mm/dd/yyyy.
        all_nums_1[0] = current_time_format #Replacing the first element in the array 'all_nums_1' with the current date acquired earlier

        for t in range(int(length/6)): #Creating a for loop that will select the elements to be put inside of the array 'prices'
            index = t * 6 + 4 #There are multiple prices in the table, and the closing prices have a difference of six elements between them, the first element starting from all_nums_1[4].
            prices.append(all_nums_1[index]) #Appending the element to the array

        for t in range(int(length/6)): #Creating a for loop that will select the elements to be put inside of the array 'dates'
            index = t * 6 #The dates are inside of the table, with a difference of six elements between them.
            date_str = all_nums_1[index] #Taking the value stored in the 'index' position of the array 'all_nums_1'
            format_str = '%m/%d/%Y' #Defining the format of the dates that we want (mm/dd/yyyy)
            datetime_object = datetime.datetime.strptime(date_str, format_str) #Using a function in the API 'datetime' to convert the dates to the format mm/dd/yyyy
            dates.append(datetime_object) #Appending the correctly formatted dates to the array 'dates'

        final_dates = matplotlib.dates.date2num(dates) #Converting all the dates in the array into a format that matplotlib can understand

        #plotting the graph of the last 3 months of stock price
        plt.plot_date(final_dates, prices, '-o') #Graphing the function, with the "final_dates" being on the x-axis, and the "prices" being on the y-axis. The '-o' is used to connect the data points in the graph
        plt.xticks(rotation=90) #Rotating the text on the x-axis by 90 degrees, so that it is leggible
        plt.xlabel('Date') #Labeling the x-axis 'Date'
        plt.ylabel('Price ($)') #Labeling the y-axis 'Price ($)'
        plt.suptitle("Price of the %s stock in the last 3 months" % stock) #Titling the graph
        plt.show() #Showing the graph

    except:
        Ticker_entry.delete(0, END)  # Deleting any prior text in the space where the message will be displayed
        Ticker_entry.insert(0, "Please enter a valid ticker!")  # Inserting the message into the entry box

def Cleaning(writing_area1, writing_area2, writing_area3, writing_area4, writing_area5, writing_area6, writing_area7): #A function that deletes all of the content in the entries that are in the GUI
        writing_area1.delete(0, END) #Deleting all content in 'writing_area1'
        writing_area2.delete(0, END) #Deleting all content in 'writing_area2'
        writing_area3.delete(0, END) #Deleting all content in 'writing_area3'
        writing_area4.delete(0, END) #Deleting all content in 'writing_area4'
        writing_area5.delete(0, END) #Deleting all content in 'writing_area5'
        writing_area6.delete(0, END) #Deleting all content in 'writing_area6'
        writing_area7.delete(0, END) #Deleting all content in 'writing_area7'

root.mainloop() #End of program