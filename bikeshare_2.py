import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters(city, month, day):
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities_list = ['chicago', 'new york city', 'washington']
    city = []
    while city not in cities_list:
        city = str(input('Please choose a city to explore: Chicago, New York City, or Washington.\n').lower())
        if city in cities_list:
            break
        print('That is not one of the options. Please type a valid option from the list.\n')

    # TO DO: get user input for month (all, january, february, ... , june)
    months_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = []
    while month not in months_list:
        month = str(
            input('Please choose a month to explore: All, January, February, March, April, May, June.\n').lower())
        if month in months_list:
            break
        print('That is not one of the options. Please type a valid option from the list.\n')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days_list = ['all', 'monday', 'tuesday', 'wednesday',
                 'thursday', 'friday', 'saturday', 'sunday']
    day = []
    while day not in days_list:
        day = str(input(
            'Please choose a day to explore: All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday.\n').lower())
        if day in days_list:
            break
        print('That is not one of the options. Please type a valid option from the list.\n')

    print('-'*40)
    return city, month, day


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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['hour_of_day'] = df['Start Time'].dt.hour

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print(df['month'].mode())

    # TO DO: display the most common day of week
    print(df['day_of_week'].mode())

    # TO DO: display the most common start hour
    print(df['hour_of_day'].mode())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print(df['Start Station'].mode())

    # TO DO: display most commonly used end station
    print(df['End Station'].mode())

    # TO DO: display most frequent combination of start station and end station trip
    df['Start and End Station Combo'] = 'From: ' + df['Start Station'] + ' to: ' + df['End Station']
    print(df['Start and End Station Combo'].mode())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['Total Travel Time'] = df['End Time'] - df['Start Time']
    print(df['Total Travel Time'].mean())

    # TO DO: display mean travel time
    print(df['Total Travel Time'].sum())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print(df['User Type'].value_counts())

    # TO DO: Display counts of gender
    try:
        print(df['Gender'].value_counts())
    except KeyError:
        print("Sorry, this data set does not have user gender information.")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        print(df['Birth Year'].min())
        print(df['Birth Year'].max())
        print(df['Birth Year'].mode())
    except KeyError:
        print("Sorry, this data set does not have user birth year information.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """
    Asks user whether they would like to see 5 lines of raw data from the selected city's file. Continues asking if they would like additional 5 lines of data until they say no.
    """
    raw_data = []
    valid_response = ['yes', 'no']
    n = 0
    raw_data = input(
        '\nWould you like to see 5 lines of raw data for your selected city/s file? Enter Yes or No.\n').lower()
    while raw_data != 'no':
        if raw_data not in valid_response:
            raw_data = input('\nThat is not a valid reponse. Please enter Yes or No.\n').lower()
        elif raw_data == 'no':
            break
        while raw_data == 'yes':
            print(df.iloc[0+n:5+n])
            raw_data = input(
                '\nWould you like to see another 5 lines of raw data? Enter Yes or No.\n').lower()
            if raw_data == 'no':
                break
            n += 5


def main():
    while True:
        city, month, day = get_filters('chicago', 'january', 'monday')
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter Yes or No.\n').lower()
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
