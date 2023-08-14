import time
import pandas as pd
import numpy as np
from statistics import mode
from collections import Counter

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_month_filter():
    """
    Asks user to specify the month to analyze.
    
    Returns: (str) month - name of the month to filter by
    """
    # Define a set of valid_months
    valid_months = {'all','january','february','march','april','may','june'}
    
    # Ask the user to select a month to filter by from the set of valid_months
    while True:
        month = str(input('Which month? The following months are available to filter: January, February, March, April, May, or June.\n')).lower().strip()
        
        # check if the user input is a valid month in the set valid_months and return if valid
        if month in valid_months:
            return month
        else:
            print('\nYour entry is invalid. Please try again.\n')

    return month        

def get_dow_filter():
    """
    Asks user to specify the day of the week (dow) to analyze.
    
    Returns: (str) dow - name of the day of the week to filter by
    """
    # Define the set of valid days of the week (valid_dow)
    valid_dow = {'sunday','monday','tuesday','wednesday','thursday','friday','saturday'}
   
    # Ask the user to select a day of the week by its full name
    while True:
        dow = str(input('\nWhich day of the week? Please enter the full name of the day (e.g. Sunday, Monday, etc.).\n')).lower().strip()
        
        # Check if the user's input is in the set valid_dow and return if valid
        if dow in valid_dow:
            return dow
        else:
            print('\nYour entry is invalid. Please try again.\n')
            

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # Greet the user
    print('Hello! Let\'s explore some US bikeshare data!\n')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_city_flag = False
    valid_cities = {'chicago', 'new york city', 'washington'} # set of valid_cities a user can type in
    while not valid_city_flag:
        city = str(input('There are 3 cities that we can explore: Chicago, New York City, and Washington. Which city would you like to explore? \n').lower().strip())
        
        # Check to see if the user typed in a valid city
        if city in valid_cities:
            
            # Verify with the user that their entry is correct
            while True:
                yn = str(input('\nYou typed in "{}" as the city. Is that correct? Please type in yes or no.\n'.format(city.title()))).lower().strip()
                if yn == 'yes' or yn == 'y':
                    print("\n{} is a great city! We can now filter the information based on months and days of the week.\n".format(city.title()))
                    valid_city_flag = True
                    break
                elif yn =='no' or yn == 'n':
                    print("\nLet's try again.")
                    month = None
                    break
                else:
                    print("\nPlease enter a yes or no.\n")
        else:
            print('\nYour entry was invalid. Please try again.\n')

    # Ask the user how they want to filter the data
    filter_flag = False
    valid_filters = {'month','day','both','none'} # set of valid_filters a user can type in
    while not filter_flag:
        filter_criteria = str(input('Would you like to filter by month, day, both, or none at all? Type "none" for no filters. \n')).strip().lower()
        
        # Check to see if the user typed in a valid filter
        if filter_criteria in valid_filters:
            print("\nGreat! We'll filter by {}.".format(filter_criteria))
            filter_flag = True
        else:
            print('\nYour entry was invalid. Please try again.\n')
        
    # Based on how the user wants to filter the data, set the return values for the month and day
    if filter_criteria == 'month':
        # get user input for month (all, january, february, ... , june)
        month = get_month_filter()
        day = 'all'
    elif filter_criteria == 'day':
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = get_dow_filter()
        month = 'all'
    elif filter_criteria == 'both':
        # get user input for both month and day of week
        month = get_month_filter()
        day = get_dow_filter()
    else:
        print('You have chosen not to filter on anything. We will show you information for everything we have.\n')
        month = 'all'
        day = 'all'
       
    print('-'*40)
    return [city, month, day]

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Read in the city file into a Pandas dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])
    
    # Convert the "Start Time" column to datetime data type
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Create a column for the month and day of week
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # Filter the dataframe by the month if "all" is not passed
    months = {'january':1,
              'february':2,
              'march':3,
              'april':4,
              'may':5,
              'june':6,
              'july':7,
              'august':8,
              'september':9,
              'october':10,
              'november':11,
              'december':12
             }
    
    if month.lower() != 'all':
        df = df.loc[df['month'] == months[month.lower()]]
    
    # Filter the dataframe by the day if "all" is not passed
    if day.lower() != 'all':
        df = df.loc[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    month_dict = {1:'January',
                  2:'February',
                  3:'March',
                  4:'April',
                  5:'May',
                  6:'June',
                  7:'July',
                  8:'August',
                  9:'September',
                  10:'October',
                  11:'November',
                  12:'December'
        
    }
    month_mode = df.month.mode()[0]
    month = month_dict[month_mode]
    print('The most common month to travel was {}.\n'.format(month))

    # display the most common day of week
    dow_mode = df['day_of_week'].mode()[0]
    print('The most common day of the week to travel was {}.\n'.format(dow_mode))

    # display the most common start hour in military time
    hour_mode = df['Start Time'].dt.hour.mode()[0]
    if hour_mode < 10:
        hour_mode = '0' + str(hour_mode) + '00'
    else:
        hour_mode = str(hour_mode) + '00'
    print('The most common start hour was {}.\n'.format(hour_mode))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_ctr = Counter(df['Start Station'])
    start_station_mode = df['Start Station'].mode()[0]
    print('The most commonly used start station was used {} times at "{}".\n'.format(start_station_ctr[start_station_mode], start_station_mode))

    # display most commonly used end station
    end_station_ctr = Counter(df['End Station'])
    end_station_mode = df['End Station'].mode()[0]
    print('The most commonly used end station was used {} times at "{}".\n'.format(end_station_ctr[end_station_mode], end_station_mode))

    # display most frequent combination of start station and end station trip
    station_combos = list(zip(df['Start Station'], df['End Station']))
    station_combos_ctr = Counter(station_combos)
    station_combos_mode = mode(station_combos)
    print('The most frequent combination of start and end station trips was used {} times with START STATION: "{}" and END STATION: "{}".\n'.format(station_combos_ctr[station_combos_mode], station_combos_mode[0], station_combos_mode[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def time_conversion(x):
    """
    Converts the given time "x" in seconds to days, hours, minutes, and seconds
    Returns:
        days: number of days in x
        hours: number of hours remaining in x after determining the number of days
        minutes: number of minutes remaining in x after determining the number of hours
        seconds: number of seconds remaining in x after determining the number of minutes
    """
    # Calculate the number of days in x
    days = int(x/(24*3600))
    
    # Determine how many seconds are remaining and then calculate the number of hours
    x = x % (24*3600)
    hours = int(x/3600)
    
    # Determine how many seconds are remaining and then calculate the number of minutes
    x = x % 3600
    minutes = int(x/60)
    
    #Determine how many seconds are remaining and the calculate the number of seconds
    x = x % 60
    seconds = int(x)
    
    return (days, hours, minutes, seconds)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    days, hours, mins, secs = time_conversion(total_time) 
    print('The total travel time for all trips during this time period was {} days, {} hours, {} minutes and {} seconds.\n'.format(days, hours, mins, secs))

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    days_m, hours_m, mins_m, secs_m = time_conversion(mean_time)
    print('The average travel time for all trips during this time period was {} days, {} hours, {} minutes and {} seconds.\n'.format(days_m, hours_m, mins_m, secs_m))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """
    Displays statistics on bikeshare users.
    Uses exception handling due to some datasets not having the same user information.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        user_types = df.groupby(['User Type'])['User Type'].count()
        print('These are the different types of users that used the bikeshare during this time period.\n')
        print(user_types, '\n')
    except:
        print('This location does not have the user types to share.\n')

    # Display counts of gender
    try:
        gender = df.groupby(['Gender'])['Gender'].count()
        print('This shows the gender of users that used the bikeshare during this time period.\n')
        print(gender, '\n')
    except:
        print('This location does not have any gender data to share.\n')

    # Display earliest, most recent, and most common year of birth
    try:
        birth_year = list(df['Birth Year'].sort_values().dropna())
        birth_year_mode = int(mode(birth_year))
        birth_year_earliest = int(birth_year[0])
        birth_year_recent = int(birth_year[-1])
        print('The earliest birth year from the list of users was {}.\n'.format(birth_year_earliest))
        print('The most recent birth year from the list of users was {}.\n'.format(birth_year_recent))
        print('The most common birth year from the list of users was {}.\n'.format(birth_year_mode))
    except:
        print('This location does not have any birth year data to share.\n')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    stop_flag = False
    while not stop_flag:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        
        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart == 'yes' or restart == 'y':
                print('\n')
                break
            elif restart == 'no' or restart == 'n':
                stop_flag = True
                break
            else:
                print("\nPlease enter a yes or no.\n")


if __name__ == "__main__":
	main()
