import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_raw = input("Name one city to be analyzed (chicago, new york city,washington):")
    # CHECK if this line that follows is ok; should there be a print command also
    city =city_raw.lower()
    if city =='new york city':
        city ="new_york_city"
    # get user input for month (all, january, february, ... , june)
    month = input("Name the month the analyzed (enter 'all', or for individual months say for January as '1' upto June as '6'):")
    # check only if needed
    if month != 'all':
        month = int(month)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Name the day of week to analyze ('all' else individual days like Monday as '0', Sunday as '6'):")
    if day != 'all':
        day = int(day)

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
    # filename has to be .csv
    filename = city+".csv"

    df = pd.read_csv(filename)

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['Month'] = df['Start Time'].dt.month

    df['Day'] = df['Start Time'].dt.dayofweek

    df['Hour'] = df['Start Time'].dt.hour

    # condition for month and day
    if month !='all':
        df=df[df['Month'] == month]

    if day !='all':
        df=df[df['Day'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['Month'].mode()[0]

    # display the most common day of week
    popular_day = df['Day'].mode()[0]

    # display the most common start hour
    popular_hour = df['Hour'].mode()[0]

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("The most popular start station is:", popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("The most popular end station is:", popular_end_station)



    #Also display the first 5 popular start/end stations
    list_popular_start_station = df['Start Station'].value_counts().head(5)
    print("\nList of popular start stations are:",list_popular_start_station)

    list_popular_end_station = df['End Station'].value_counts().head(5)
    print("\nList of popular end stations are:", list_popular_end_station)

    # display most frequent combination of start station and end station trip
    df1=df[['Start Station','End Station']].copy()
    print ("\nList of popular routes:",df1.drop_duplicates(['Start Station','End Station']))
    # Note the statement does not work: print("\nList of popular routes:", df1.groupby(['Start Station','End Station']).count().head(5))
    #another thing change label and add

    # Some reference
        # https://stackoverflow.com/questions/33346591/what-is-the-difference-between-size-and-count-in-pandas
        # the above link suggests how to use groupby
            # https://stackoverflow.com/questions/11285613/selecting-multiple-columns-in-a-pandas-dataframe
            # above link for reframing the dataframe with the 2 columns

    print("\nThis took %s seconds." % (time.time() - start_time))
    print()
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['total_travel_time'] = df['End Time']-df['Start Time']
    print("\nTotal travel time is:", df['total_travel_time'])

    # display mean travel time
    cnt=df.count()
    print("\nMean travel time is:", df['total_travel_time'].mean())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df,city):
    # A informal pointer for myself: interesting concept of local and global variable
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if city != "washington":
        gender_type_counts = df['Gender'].value_counts()
        print(gender_type_counts)

    # Display earliest, most recent, and most common year of birth
    common_year_birth = int(df['Birth Year'].mode()[0])
    recent_year_birth = int(df['Birth Year'].max())
    earliest_year_birth = int(df['Birth Year'].min())

    print("\nMost common year of birth is:",common_year_birth)
    print("\nMost recent year of birth is:",recent_year_birth)
    print("\nEarliest year of birth is:",earliest_year_birth)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        # https://stackoverflow.com/questions/16043797/python-passing-variables-between-functions
        # the above link clarifies arguments within a function returne to another function very very clearly

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
