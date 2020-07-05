# Loads Numpy & pandas library into program
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    _city, _month, _day = "","",""
    #The user will specify their search criteria by using the filters below.
    print('''Hello user! Let's begin looking at some bikeshare data.''')

    #Select which city you wish to analyse & designates which csv file to read.
    city_input = input("Please select one of the following cities to begin: Chicago, New York City or Washington \n").lower()
    while city_input not in ['chicago', 'new york city', 'washington']:
        print("Apologies, your entry is invalid. Please try again!")
        city_input = input("Please select one of the following cities to begin: Chicago, New York City or Washington \n").lower()
    print('Fantastic! you have chosen {}.\n' .format(city_input).title())
    _city = city_input

    #Either select which month you wish to filter or select 'all'
    month_input = input('Please specify which month you would like to see or enter "all" to have no filter by month.\n').lower()
    while month_input not in ['all', 'january', 'feburary', 'march', 'april', 'may', 'june']:
        print("Oh dear, your entry was invalid or outside the first six months of the year. Please try again!")
        month_input = input('Please specify which month you would like to see or enter "all" to have no filter by month.\n').lower()
    print('Great, you have chosen the month of {}.\n'.format(month_input).title())
    _month = month_input

    #Either select which day you wish to filter or select 'all'
    day_input = input("To initiate the search, please specify a day or 'all'.\n").lower()
    while day_input not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        print("Sorry, but your input was invalid. Please try again!")
        day_input = input("To initiate the search, please specify a day or 'all'.\n").lower()
    print('Great, you have chosen {}.\n'.format(day_input).title())
    _day = day_input

    #city=CITY_DATA[city_input]
    print('-'*40)
    return _city, _month, _day

def load_data(city, month, day):
    #Loads data based on filters designated by the user in the get_filters function.
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'feburary', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    print('\nChecking the most frequent times of travel\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Most common month
    df['month']= df['Start Time'].dt.month
    most_common_month = df['month'].mode()
    print('Most commonly travelled month is : ', most_common_month[0])

    #Most common day
    df['day'] = df['Start Time'].dt.day_name()
    most_common_weekday = df['day'].mode()
    print('Most commonly travelled day is : ', most_common_weekday[0])

    #Most common hour
    df['start_hour'] = df['Start Time'].dt.hour
    most_common_hour = df['start_hour'].mode()
    print('Most commonly travelled hour is : ', most_common_hour[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    print('\n Checking the most frequent Stations & Trip.\n')
    start_time = time.time()

    #Most common start station
    most_common_start_station = df['Start Station'].mode()
    print('Most commonly used start station is :', most_common_start_station[0])

    #Most common end station
    most_common_end_station = df['End Station'].mode()
    print('Most commonly used end station is :', most_common_end_station[0])

    #most frequent combination of start station and end station trip
    most_common_start_to_end_station = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).nlargest(1)
    print('Most frequent combination of start station and end station trips is :', most_common_start_to_end_station[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration(df):
    print('\n Checking the trip duration.\n')
    start_time = time.time()

    # Display total travel time
    total_duration = df['Trip Duration'].sum()
    print('The total trip duration is : ', total_duration)

    # Display mean travel time
    average_duration =df['Trip Duration'].mean()
    print('The average trip duration is : ', average_duration)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        user_type = df['User Type'].value_counts()
        print('Total user amount of each type is: \n')
        print(user_type)


    # Display counts of gender. Note: Gender/Birth information not available for Washington
    try:
        gender = df['Gender'].value_counts()
        print('The total of each gender are: \n')
        print("Male: ", gender[0], "\nFemale: ", gender[1],"\n")
    except:
          print('No gender information available for the city of Washington.\n')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year_of_birth = min(df['Birth Year'])
        print('The earliest year of birth is : ',int(earliest_year_of_birth))
        recent_year_of_birth = max(df['Birth Year'])
        print('The most recent year of birth is : ', int(recent_year_of_birth))
        most_common_year_of_birth = df['Birth Year'].mode()
        print('The most common birth year is : ',int(most_common_year_of_birth[0]))
    except:
        _city = ['Washington']
    #except:
          #print('There is no birth information for the city of Washington.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration(df)
        user_stats(df)
# Inquires to the user whether they would like to see raw data from their respective city of choice.
        i = 0
        raw = input("Before you finish up, would you like to see the frist five rows of raw data? Type 'yes' or 'no'.\n").lower()
        pd.set_option('display.max_columns', 200)
        while True:
            if raw == 'no':
                break
            print(df[i:i+5])
            raw = input("Would you like to see another five rows of raw data?\n").lower()
            i += 5
# Asks user whether they would like to reset their inquiry.
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
