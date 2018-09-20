import mysql.connector



#Config file to connect to the MYSQL database
config = {
  'user': 'USERNAME', #Food Computer SQL user name
  'password': 'Password', #Food Computer SQL Password
  'host': 'IPADRESS',#Food Computer SQL IP
  'database': 'DATABASE', #Food Computer SQL Database
  'raise_on_warnings': True
}


def photoPeriod(start, end):

    #Holder for the night\day change
    day = []
    #Connection to the SQL Database
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    #SQL Query.
    query = "Select PAR, Date from Data where Date between  %s AND %s;"

    #Running the Query in the Database and returning the result in a cursor object.
    #start and end are used to set the begin and end time (have to be passed as parameters
    cursor.execute(query, (start, end))

    #Get next value of the SQL info for valid data
    evaluate = cursor.next()
    #Set the value of what is considered as day from the sensor
    PAR_value = 350
    #Index to store the date and Par value
    index = 0
    #Using the first value to find if we start with night or day, and add the date and the sensor value to the list
    evaluate_day = evaluate[1]
    if evaluate[0] > PAR_value:
        #start with Day
        day_bool = False
        day.append([])
        day[index].append("Light")
        day[index].append(evaluate[1])

    else:
        #Start with night
        day_bool = True
        day.append([])
        day[index].append("Night")
        day[index].append(evaluate[1])


    #Evaluation of the query results.
    #In this for loop, the function looks for a time when day changes to night or the opposite and take a date and
    #reading singature for further analysis
    for (PAR, Date) in cursor:
        #Checking if we moved to a new day.
        if not Date.day - evaluate_day.day ==0:
            #set day to the new date
            evaluate_day = Date
            #increase index by 1
            index += 1
            #open new inner list to store the new date
            day.append([])

        #if Par value is greater than the value, we define it as day.
        if PAR > PAR_value:
            #First value of change.
            if day_bool:
                #State of Day
                day[index].append("Light")
                #Store the date when the state began
                day[index].append(Date)
            #set to false to ignore newer values. We just need to know when day begins
            day_bool = False
            #If value is less than the PAR value
        else:
            #Store first date signature of when the night begins
            if not day_bool:
                #Inserts state and time to the day list
                day[index].append("Night")
                day[index].append(Date)
            #Set to ignore night records. We just need to know when the night begins
            day_bool = True


    #Setting the list to analyse the Photoperiod according to the day
    index_photo = 0
    photoperiod_list = []
    for days in day:
        #Setting the first night and day values with date time objects to evaluate the time for each state.
        #We start with zero and increment in according to data from the day list
        photoperiod_list.append([])
        photoperiod_list[index_photo].append('Night')
        photoperiod_list[index_photo].append(days[1].replace(hour=00, minute=00, second=00))
        photoperiod_list[index_photo].append('Light')
        photoperiod_list[index_photo].append(days[1].replace(hour=00, minute=00, second=00))

        #Reading each day seperatly. Each list contains date and state. Date is found on uneven number. Hence, the
        #starting with 1 and jumping with +2
        for hour in range(1, len(days), 2):
            #If the date signature is the last, we want to compare to the end of the day
            if hour + 2 > len(days) and index_photo < len(day):
                # Set an object to the rest of the day
                end_of_day = days[hour].replace(hour=23, minute=59, second=59)
                #Check state and add the time to the photoperiod_list
                if days[hour - 1] == 'Night':
                    #Increment the value of night
                    photoperiod_list[index_photo][1] += (end_of_day - days[hour])
                else:
                    # Increment the value of light
                    photoperiod_list[index_photo][3] += (end_of_day - days[hour])
            #If the date is not the last on the list
            else:
                #Subtract the time between the states to get the time
                if days[hour-1] == 'Night':
                    photoperiod_list[index_photo][1] += (days[hour+2]-days[hour])
                else:
                    photoperiod_list[index_photo][3] += (days[hour+2]-days[hour])

        #If the date is not on the first day, create a begining day to get the hours between midnight and the first
        #state reading
        if index_photo > 0:
            start_of_day = days[hour].replace(hour=00, minute=00, second=00)
            if days[hour - 1] == 'Night':
                photoperiod_list[index_photo][1] += (days[1] - start_of_day)
            else:
                photoperiod_list[index_photo][3] += (days[1] - start_of_day)

        #Change day
        index_photo += 1

    #Close SQL Connection
    cursor.close()
    cnx.close()
    #Print the results on the screen
    for print_data in photoperiod_list:
        print('Photoperiod for Date {}: Night hours {} and Light hours {}"'.format(print_data[1].date(), print_data[1].time(),print_data[3].time() ))



def main():
    #Start and end values
    start = '2018-09-06 00:00:00'
    end = '2018-09-08 23:59:59'

    #Call the function
    photoPeriod(start,end)


main()