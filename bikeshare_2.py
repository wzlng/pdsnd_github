import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

CITY_OPTIONS = {'chicago', 'new york city', 'washington'}

MONTH_OPTIONS = {
    'all', 'january', 'february', 'march',
    'april', 'may', 'june', 'july', 'august',
    'september', 'october', 'november', 'december'
}

DAY_OF_WEEK_OPTIONS = {
    'all', 'monday', 'tuesday', 'wednesday',
    'thursday', 'friday', 'saturday', 'sunday',
}

PARSE_DATE_COLUMNS = ['Start Time', 'End Time']


def ask_user_input(message, data_validation):
    """
    The utility function requires user input and validates what has been entered.

    Args:
        (str) message - message will be displayed to the user
        (arr) data_validation - the data will be used to validate what the user has entered

    Return:
        (str) value - entered value
    """
    value = ''
    while True:
        value = input(f'{message}\n').lower()
        if value not in data_validation:
            print(f'Invalid value!')
            continue
        break

    return value


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
    city = ask_user_input(
        message='Would you like to see data for Chicago, New York City, or Washington?',
        data_validation=CITY_OPTIONS
    )

    # get user input for month (all, january, february, ... , june)
    month = ask_user_input(
        message='Would you like filter the data by month (January, February, ...), or all?',
        data_validation=MONTH_OPTIONS
    )

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ask_user_input(
        message='Would you like filter the data by day of week (Monday, Tuesday, ...), or all?',
        data_validation=DAY_OF_WEEK_OPTIONS
    )

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

    # Load data according to the entered city
    df = pd.read_csv(CITY_DATA[city], index_col=0,
                     parse_dates=PARSE_DATE_COLUMNS)

    # Filter by month
    if month != 'all':
        df = df[df['Start Time'].dt.month_name() == month.capitalize()]

    # Filter by day of week
    if day != 'all':
        df = df[df['Start Time'].dt.day_name() == day.capitalize()]

    return df


def time_stats(df: pd.DataFrame):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = calendar.month_name[df['Start Time'].dt.month.mode()[0]]
    print(f'Most Popular Start Month: {popular_month}')

    # display the most common day of week
    popular_day = calendar.day_name[df['Start Time'].dt.day_of_week.mode()[0]]
    print(f'Most Popular Start Day: {popular_day}')

    # display the most common start hour
    popular_hour = df['Start Time'].dt.hour.mode()[0]
    print(f'Most Popular Start Hour: {popular_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df: pd.DataFrame):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()
    print(f'Most Popular Start Station: {popular_start_station}')

    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()
    print(f'Most Popular End Station: {popular_end_station}')

    # display most frequent combination of start station and end station trip
    popular_start_end_station = df.groupby(
        ['Start Station', 'End Station']).size().idxmax()
    popular_start_end_station = ' - '.join(popular_start_end_station)
    print(
        f'Most Popular Combination of Start-End Station: {popular_start_end_station}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df: pd.DataFrame):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f'Total Travel Time: {total_travel_time} seconds')

    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print(f'Average Travel Time: {avg_travel_time} seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df: pd.DataFrame):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts().count()
    print(f'Counts of User types: {user_type_count}')

    # Display counts of gender
    if 'Gender' in df:
        gender_count = df['Gender'].value_counts().count()
        print(f'Counts of Gender: {gender_count}')
    else:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth_year = np.nanmin(df['Birth Year'].values)
        print(f'Earliest Year of Birth: {earliest_birth_year}')

        most_recent_birth_year = np.nanmax(df['Birth Year'].values)
        print(f'Most Recent Year of Birth: {most_recent_birth_year}')

        most_common_birth_year = df['Birth Year'].mode()[0]
        print(f'Most Common Year of Birth: {most_common_birth_year}')
    else:
        print('Birth Year stats cannot be calculated because Birth Year does not appear in the dataframe')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
