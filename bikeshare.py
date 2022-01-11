import time
import pandas as pd
import numpy as np

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
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    filters = ['day', 'month', 'both', 'none']
    month = 'all'
    day = 'all'
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Which city do you wish to get analysis of? {}: '.format(', '.join(CITY_DATA.keys()))).lower()
            if city not in CITY_DATA.keys():
                raise ValueError
            break
        except ValueError:
            print("Invalid input! Please try again")

    while True:
        try:
            filter_type = input('Would you like to filter by day, month or both? type none for no filter: ').lower()
            if filter_type not in filters:
                raise ValueError
            break
        except ValueError:
            print('Invalid input! Allowed inputs are: day, month, both or none')

    if filter_type == 'day':
        # get user input for day of week (all, monday, tuesday, ... sunday)
        while True:
            try:
                day = input('Which day of week do you wish to get analysis of? {}: '.format(', '.join(days))).title()
                if day not in days:
                    raise ValueError
                break
            except ValueError:
                print("Invalid input! Please try again")
        return city, month, day
    elif filter_type == 'month':
        # get user input for month (all, january, february, ... , june)
        while True:
            try:
                month = input('Which month do you wish to get analysis of? {}: '.format(', '.join(months))).title()
                if month not in months:
                    raise ValueError
                break
            except ValueError:
                print("Invalid input! Please try again")
        return city, month, day
    elif filter_type == 'both':
        # get user input for month (all, january, february, ... , june)
        while True:
            try:
                month = input('Which month do you wish to get analysis of? {}: '.format(', '.join(months))).title()
                if month not in months:
                    raise ValueError
                break
            except ValueError:
                print("Invalid input! Please try again")

        # get user input for day of week (all, monday, tuesday, ... sunday)
        while True:
            try:
                day = input('Which day of week do you wish to get analysis of? {}: '.format(', '.join(days))).title()
                if day not in days:
                    raise ValueError
                break
            except ValueError:
                print("Invalid input! Please try again")
        return city, month, day
    else:
        return city, month, day

    print('-' * 40)


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
    # read data for the specified city into a DataFrame
    df = pd.read_csv('files/{}'.format(CITY_DATA[city]))

    # convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month from Start Time column and save it in a new column named Month
    df['Month'] = df['Start Time'].dt.strftime('%B')

    # extract day from Start Time column and save it in a new column named Day
    df['Day'] = df['Start Time'].dt.strftime('%A')

    # extract hour from Start Time column and save it in a new column named Hour
    df['Hour'] = df['Start Time'].dt.strftime('%H')

    # filter by month if applicable
    if month != 'all':
        df = df[df['Month'] == month]

    # filter by day if applicable
    if day != 'all':
        df = df[df['Day'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['Month'].value_counts().index[0]
    month_count = df['Month'].value_counts()[0]
    print('\nThe most common month is {}\tCount: {}\n.'.format(popular_month, month_count))

    # display the most common day of week
    popular_day = df['Day'].value_counts().index[0]
    day_count = df['Day'].value_counts()[0]
    print('The most common day of the week is {}\tCount: {}.\n'.format(popular_day, day_count))

    # display the most common start hour
    popular_start_hour = df['Hour'].value_counts().index[0]
    hour_count = df['Hour'].value_counts()[0]
    print('The most common start hour is {}\tCount: {}.\n'.format(popular_start_hour, hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    max_start = max(df['Start Station'].value_counts())  # get the End Station with the highest count.
    start_count_series = df['Start Station'].value_counts()
    popular_station_start = start_count_series[start_count_series == max_start]
    print('\nThe most commonly used Start Station trip:\n', popular_station_start)

    # display most commonly used end station
    max_end = max(df['End Station'].value_counts())  # get the End Station with the highest count.
    end_count_series = df['End Station'].value_counts()
    popular_station_end = end_count_series[end_count_series == max_end]
    print('\nThe most commonly used end station trip:\n', popular_station_end)

    # display most frequent combination of start station and end station trip
    # create a column that concatenates Start and End Station
    df['Station Combo'] = df['Start Station'] + ' | ' + df['End Station']

    max_combo = max(df['Station Combo'].value_counts())  # get the Station Combination with the highest count.
    combo_count_series = df['Station Combo'].value_counts()
    popular_station_combo = combo_count_series[combo_count_series == max_combo]
    print('\nThe most frequent combination of start station and end station trip:\n', popular_station_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in seconds
    travel_seconds = df['Trip Duration'].sum()
    print('\nTotal travel time in seconds is {} seconds.\n'.format(travel_seconds))

    # display total travel time in minutes
    travel_minutes = travel_seconds // 60
    rem_sec = travel_seconds % 60
    print('\nTotal travel time in minutes and seconds is {} minutes {} seconds.\n'.format(travel_minutes, rem_sec))

    # display total travel time in hours
    travel_hours = travel_seconds // (60 * 60)
    rem = travel_seconds % (60 * 60)
    rem_min = rem // 60  # converts remainder to minutes
    rem_sec = rem % 60  # converts remainder to seconds
    print('\nTotal travel time in hours, minutes and seconds is {} hours {} minutes '
          '{} seconds.\n'.format(travel_hours, rem_min, rem_sec))

    print('***********Average Travel Time***********')

    # display mean travel time
    mean_travel_seconds = df['Trip Duration'].mean()
    print('\nAverage travel time is {} seconds.\n'.format(mean_travel_seconds))

    # display mean travel time in minutes and seconds
    mean_travel_minutes = int(mean_travel_seconds // 60)
    rem_sec = mean_travel_seconds % 60
    print('\nAverage travel time in minutes and seconds is {} minutes {:0.2f} seconds.\n'
          .format(mean_travel_minutes, rem_sec))

    # display mean travel time in hours, minutes and seconds
    mean_travel_hours = int(mean_travel_seconds // (60 * 60))
    rem = mean_travel_seconds % (60 * 60)
    rem_min = rem // 60  # converts remainder to minutes
    rem_sec = rem % 60  # converts remainder to seconds
    print('\nAverage travel time in hours, minutes and seconds is {} hours {} minutes {:0.2f} '
          'seconds.\n'.format(mean_travel_hours, rem_min, rem_sec))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nUser Type Count:\n', df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df:
        print('\nGender Count:\n', df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        # earliest year of birth
        earliest_birth_year = df['Birth Year'].value_counts().sort_index(ascending=True).index[0].astype(np.int64)
        print('\nThe earliest year of birth is {}.\n'.format(earliest_birth_year))

        # most recent year of birth
        recent_birth_year = df['Birth Year'].value_counts().sort_index(ascending=False).index[0].astype(np.int64)
        print('\nThe most recent year of birth is {}.\n'.format(recent_birth_year))

        # most common year of birth
        popular_birth_year = df['Birth Year'].value_counts().index[0].astype(np.int64)
        print('\nThe most common year of birth is {}.\n'.format(popular_birth_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def chunker(df):
    size = len(df)
    for i in range(0, size, 5):
        yield df[i:i + 5]


def main():
    pd.set_option('display.max_columns',200)  # setting to expand collapsed pandas column
    while True:
        city, month, day = get_filters()
        print(city, month, day)
        df = load_data(city, month, day)
        print(df.shape)

        time_stats(df)
        input("Press Enter to view station statistics...")
        station_stats(df)
        input("Press Enter to view trip duration statistics...")
        trip_duration_stats(df)
        input("Press Enter to view user statistics...")
        user_stats(df)

        while True:
            try:
                view_data = input('\nWould you like to view some data? Enter yes or no.\n').lower()
                cond = ['yes', 'no']
                if view_data not in cond:
                    raise ValueError
                break
            except ValueError:
                print('Invalid input! enter yes or no')

        if view_data.lower() == 'yes':
            for chunk in chunker(df):
                print(chunk)
                while True:
                    try:
                        more = input('\nWould you like to view more data? yes or no:\n').lower()
                        if more not in cond:
                            raise ValueError
                        break
                    except ValueError:
                        print('Invalid input! enter yes or no')

                if more.lower() == 'no':
                    break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
