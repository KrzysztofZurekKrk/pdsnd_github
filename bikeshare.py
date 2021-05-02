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
    print('Please be advised that this in only partial data. To access full data go to https://www.divvybikes.com/system-data')
    
    #retrieve city name from user
    while True:
        city = input("\nPlease choose city name: \"chicago\", \"new york city\" or \"washington\":\n").lower()
        if city == "chicago":
            break
        elif city == "new york city":
            break
        elif city == "washington":
            break
        else:
            print("Sorry, wrong city. Please correct your input")
    
    #retrieve month from user
    available_months = ["all", "january", "february", "march", "april", "may", "june"]
    while True:
        month = input("\nPlease provide month (all, january, february, ... , june):\n").lower()
        if month in available_months:
            break
        else:
            print("Sorry, wrong month. Please correct your input")
            
    #retrieve day from user
    available_days = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    while True:
        day = input("\nPlease provide day of week (all, monday, tuesday, ... sunday):\n").lower()
        if day in available_days:
            break
        else:
            print("Sorry, wrong day. Please correct your input")
    
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
    #load data into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    #convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #retrieve hour, month and day of week from Start Time column
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    #apply filter by month if necessery
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
        df = df[df['month'] == month]
    
    #apply filter by day of week if necessery
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    return df            

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('Calculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    common_month = df['month'].mode()[0]
    print('Most common month:', common_month)

    common_day = df['day_of_week'].mode()[0]
    print('Most common day:', common_day)

    popular_hour = df['hour'].mode()[0]
    print('Most popular start hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('Calculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station:', common_start_station)

    common_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station:', common_end_station)

    common_start_end_station = (df['Start Station'] + ' - ' + df['End Station']).mode()[0]
    print('Most frequent combination of start station and end station trip:', common_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('Calculating Trip Duration...\n')
    start_time = time.time()

    travel_time = df['Trip Duration'].sum()
    print('Total travel time:', travel_time, '[s]', '(', travel_time/3600, '[h]', ')')

    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:', mean_travel_time, '[s]', '(', mean_travel_time/3600, '[h]', ')')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('Calculating User Stats...\n')
    start_time = time.time()

    user_count = df['User Type'].value_counts()
    print ('Counts of user types:\n', user_count)
    
    #conditionals for columns which are not present in all cities
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print ('\nCounts of gender:\n', gender_count)
    else:
        print ('\nThere is no Gender column in data for chosen city\n')
    
    if 'Birth Year' in df.columns:
        earliest_birth = df['Birth Year'].min()
        latest_birth = df['Birth Year'].max()
        common_birth = df['Birth Year'].mode()[0]
        print ('\nEarliest year of birth:', earliest_birth)
        print ('\nMost recent year of birth:', latest_birth)
        print ('\nMost common year of birth:', common_birth)
    else:
        print ('\nEarliest year of birth: There is no Brith Year column in data for chosen city\n')
        print ('\nMost recent year of birth: There is no Brith Year column in data for chosen city\n')
        print ('\nMost common year of birth: There is no Brith Year column in data for chosen city\n')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays 5 lines of raw data in the same order as in source file. Then asks if display next 5 etc. until users decide to stop."""
    
    row = 0
    message = "\nWould you like to see the raw data? Type 'yes' or 'no'.\n"
    #drop columns which were not present in raw data
    df = df.drop(['hour', 'month', 'day_of_week'], axis = 1)
    while True: 
        view_data = input(message) 
        if view_data.lower() == "yes":
            print()
            print(df.iloc[row])
            print()
            print(df.iloc[row + 1])
            print()
            print(df.iloc[row + 2])
            print()
            print(df.iloc[row + 3])
            print()
            print(df.iloc[row + 4])
            row += 5
            message = "\nYou've seen 5 lines of raw data, would you like to see next 5 lines? Type 'yes' or 'no'.\n"
        else:
            break
    
def main():
    """Main function using all previously defined functions."""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
            
        raw_data(df)

        restart = input("\nWould you like to restart? Enter 'yes' or 'no'.\n")
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()