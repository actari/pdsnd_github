import time
import pandas as pd
import numpy as np˜

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        city = input(
            "\nWhich city data you would like to see: Chicago, New York City or Washington?\n").lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print('You should choose one of these: Chicago, New York City or Washington')

    while True:
        month = input("\nWhich month data you would like to see: \nJanuary, February, March,"
                      " April, May, June or All\n").lower()
        if month in ["january", "february", "march", "april", "may", "june", "all"]:
            break
        else:
            print('You should choose one of these: January, February, March, April, May, June or All for no filter')

    while True:
        day = input("\nWhich day data you would like to see: \nMonday, Tuesday, Wednesday, Thursday,"
                    " Friday, Saturday, Sunday or all\n").lower()
        if day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]:
            break
        else:
            print('You should choose one of these: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All for no filter')

    print('-' * 40)
    return city, month, day


def load_data(city, month, Day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # loads data file
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time, End Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month, day from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['Day'] = df['Start Time'].dt.day_name()

    # filter by month
    if month != 'all':

       # to create the new dataframe for month
       df = df[df['month'] == month.capitalize()]

    # filtering by day of week if wanted
    if Day != 'all':

        #to create the new dataframe for day
        df = df[df['Day'] == Day.capitalize()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\n Calculating the Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['month'].mode()[0]
    print('The Most Common Month : ', common_month)

    common_day = df['Day'].mode()[0]
    print('The Most Common Day : ', common_day)

    # Creating new columns for hour
    df['Hour'] = df['Start Time'].dt.hour
    common_start_hour = df['Hour'].mode()[0]
    print('The Most Common Start Hour : ', common_start_hour)

    popular_hour = df['Hour'].mode()[0]

    df['End Hour'] = df['End Time'].dt.hour
    common_end_hour = df['End Hour'].mode()[0]
    print('The Most Common End Hour : ', common_end_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating the Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_st = df['Start Station'].mode().values[0]
    print('Most Common Start Station :', common_start_st)

    common_end_st = df['End Station'].mode().values[0]
    print('Most Common End Station :', common_end_st)

    df['Frequent Start-End Stations'] = df['Start Station'] + ' to ' +  df['End Station']
    common_combination = df['Frequent Start-End Stations'].mode().values[0]
    print('The most common combination of Start Station and End Station :', common_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    trip_duration = df['Trip Duration'].sum()
    print('Total Travel Time:', time.strftime('%H:%M:%S', time.gmtime(trip_duration)))

    mean_time= df['Trip Duration'].mean()
    print('Mean Travel Time:', time.strftime('%H:%M:%S', time.gmtime(mean_time)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_type_count = df['User Type'].value_counts()
    print ('Counts of User Types :\n',user_type_count)

    # No gender information in washington
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('Counts of Gender :\n',gender_counts)
    else:
        print('No Data For Gender')


    if 'Birth Year' in df.columns:
        earliest_birth = df['Birth Year'].min()
        print("Earliest Birth Year: ", int(earliest_birth))
        recent_birth = df['Birth Year'].max()
        print("Most recent year of birth: ", int(recent_birth))
        common_birth = df['Birth Year'].mode()[0]
        print("Most common year of birth: ", int(common_birth))
    else:
        print('No Data For Birth Year ')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def raw_data(df):
    """
    Asks user if they want to see 5 lines of raw data.
    Returns the 5 lines of raw data if user inputs `yes`. Iterate until user response with a `no`

    """
    restart = input('\nWould you like to see raw data? Enter yes or no.\n')
    if restart.lower() != 'yes':
        return
    else:
        index=0
        while True:
            print(df.iloc[index:index+5,:])
            index=index+5
            restart = input('\nWould you like to see more raw data? Enter yes or no.\n')
            if restart.lower() != 'yes':
                return


# origin : All the function will be called through this function
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
