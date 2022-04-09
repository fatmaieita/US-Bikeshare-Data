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
    print('Hello! Let\'s explore some US bikeshare data!\n')

    # initializing lists of cities, months and days to check against inputs for a valid input
    cities = ['chicago', 'new york city', 'washington']
    months = ['all','january', 'february', 'march', 'april', 'may', 'june']
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Which city do you want to see data for? (Chicago, New York City, Washington)\n').lower()
            if city in cities:
                break
            else:
                print('\nAre you sure you entered a valid city? Please try again\n')
        except ValueError:
            print('\nInput is invalid, please enter a valid input\n')


    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('\nDo you want to filter by month? Please write month in full (January to June) or type all for no filter\n').lower()
            if month in months:
                break
            else:
                print('\nAre you sure you entered a valid month? Please try again\n')
        except ValueError:
            print('\nInput is invalid, please enter a valid input\n')


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('\nDo you want to filter by day? Please write day in full or type all for no filter\n').lower()
            if day in days:
                break
            else:
                print('\nAre you sure you entered a valid day? Please try again\n')
        except ValueError:
            print('\nInput is invalid, please enter a valid input\n')


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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':

        day = day.title()

        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    months = ['january', 'february', 'march', 'april', 'may', 'june']

    # display the most common month
    if month == 'all':
        common_month = df.month.mode()[0]
        common_month = months[common_month - 1]
        print("Most Frequent Month is: ", common_month.title())

    # display the most common day of week
    if day == 'all':
        common_day = df.day_of_week.mode()[0]
        print("Most Frequent Day is:", common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df.hour.mode()[0]
    print("Most Frequent Start Hour is: ", common_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    df.columns = [name.replace(' ', '_') for name in df.columns]

    # display most commonly used start station
    common_start_station = df.Start_Station.mode()[0]
    print("Most Frequent Start Station is: ", common_start_station)


    # display most commonly used end station
    common_end_station = df.End_Station.mode()[0]
    print("Most Frequent End Station is: ", common_end_station)

    # display most frequent combination of start station and end station trip
    df['Trips'] = df['Start_Station'] + ' To ' + df['End_Station']
    common_trip = df.Trips.mode()[0]
    print("Most Frequent Trip from start to end is: ", common_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df.Trip_Duration.sum()
    print("Total travel time is {} seconds.".format(total_travel_time))

    # display mean travel time
    average_travel_time = df.Trip_Duration.mean()
    print("Average travel time is {} seconds.".format(average_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    subscriber_count = df['User_Type'].value_counts().Subscriber
    customer_count = df['User_Type'].value_counts().Customer

    print("Number of Subscribers = {}.\nNumber of Customers = {}.".format(subscriber_count, customer_count))


    # Display counts of gender
    if 'Gender' in df: #Checking if Gender data exists for this city
        male_count = df['Gender'].value_counts().Male
        female_count = df['Gender'].value_counts().Female

        print("\nNumber of Males = {}.\nNumber of Females = {}.\n".format(male_count, female_count))
    else:
        print("\nNo gender information available for this city.")


    # Display earliest, most recent, and most common year of birth
    if 'Birth_Year' in df: #Checking if Birth Year data exists for this city
        earliest = int(df['Birth_Year'].min())
        most_recent = int(df['Birth_Year'].max())
        most_common = int(df.Birth_Year.mode()[0])

        print("Earliest year of birth is {}.\nMost Recent year of birth is {}.\nMost common year of birth is {}.\n".format(earliest, most_recent, most_common))
    else:
        print("\nNo year of birth information available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):

    df.drop(['month', 'day_of_week'], axis = 1, inplace = True)
    i = 0

    while True:
        for i in range(i, i+5):
            print(df.iloc[[i]].to_dict(),'\n')
        i += 1

        while True:
            try:
                again = input('\nWould you like to see more raw data? Enter yes or no. \n').lower()
                if again == 'yes' or again == 'no':
                    break
                else:
                    print('\nAre you sure you entered a valid answer? Please try again\n')
            except ValueError:
                print('\nInput is invalid, please enter a valid input\n')

        if again == 'no':
            break





def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)  #original dataframe
        df_comp = load_data(city, month, day) #for computations

        time_stats(df_comp, month, day)
        station_stats(df_comp)
        trip_duration_stats(df_comp)
        user_stats(df_comp, city)

        while True:
            try:
                show = input('\nWould you like to see raw data? Type yes or no.\n').lower()
                if show == 'yes' or show == 'no':
                    break
                else:
                    print('\nAre you sure you entered a valid answer? Please try again\n')
            except ValueError:
                print('\nInput is invalid, please enter a valid input\n')

        if show.lower() == 'yes':
            display_raw_data(df)


        # Loop to check if user wants to restart or not
        while True:
            try:
                restart = input('\nWould you like to restart? Type yes or no.\n').lower()
                if restart == 'yes' or restart == 'no':
                    break
                else:
                    print('\nAre you sure you entered a valid answer? Please try again\n')
            except ValueError:
                print('\nInput is invalid, please enter a valid input\n')

        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
