from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as dates
import mysql.connector
from datetime import datetime
import datetime
import matplotlib.pyplot as plt

config = {
  'user': 'esp1',
  'password': '10911091',
  'host': '70.184.211.60',
  'database': 'wd',
  'raise_on_warnings': True
}


def dnsConnector():

    day = []
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = "Select PAR, Date from Data where Date between  %s AND %s;"

    start = '2018-09-06 00:00:00'
    end = '2018-09-08 23:59:59'
    cursor.execute(query, (start, end))

    evaluate = cursor.next()
    PAR_value = 350
    index = 0
    evaluate_day = evaluate[1]
    if evaluate[0] > PAR_value:
        day_bool = False
        day.append([])
        day[index].append("Light")
        day[index].append(evaluate[1])

    else:
        day_bool = True
        day.append([])
        day[index].append("Night")
        day[index].append(evaluate[1])



    for (PAR, Date) in cursor:
        if not Date.day - evaluate_day.day ==0:
            evaluate_day = Date
            index += 1
            day.append([])

        if PAR > PAR_value:
            if day_bool:
                day[index].append("Light")
                day[index].append(Date)
            day_bool = False
        else:
            if not day_bool:
                day[index].append("Night")
                day[index].append(Date)
            day_bool = True


    #TEST
    index_photo = 0
    photoperiod_list = []
    for days in day:
        photoperiod_list.append([])
        photoperiod_list[index_photo].append('Night')
        photoperiod_list[index_photo].append(days[1].replace(hour=00, minute=00, second=00))
        photoperiod_list[index_photo].append('Light')
        photoperiod_list[index_photo].append(days[1].replace(hour=00, minute=00, second=00))

        for hour in range(1, len(days), 2):
            if hour + 2 > len(days) and index_photo < len(day):
                end_of_day = days[hour].replace(hour=23, minute=59, second=59)
                if days[hour - 1] == 'Night':
                    photoperiod_list[index_photo][1] += (end_of_day - days[hour])
                else:
                    photoperiod_list[index_photo][3] += (end_of_day - days[hour])
            else:
                if days[hour-1] == 'Night':
                    photoperiod_list[index_photo][1] += (days[hour+2]-days[hour])
                else:
                    photoperiod_list[index_photo][3] += (days[hour+2]-days[hour])

        if index_photo > 0:
            start_of_day = days[hour].replace(hour=00, minute=00, second=00)
            if days[hour - 1] == 'Night':
                photoperiod_list[index_photo][1] += (days[1] - start_of_day)
            else:
                photoperiod_list[index_photo][3] += (days[1] - start_of_day)

        index_photo += 1

    cursor.close()
    cnx.close()
    for print_data in photoperiod_list:
        print('Photoperiod for Date {}: Night hours {} and Light hours {}"'.format(print_data[1].date(), print_data[1].time(),print_data[3].time() ))




def plotData():

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = "Select PAR, Humidity, Temperature, Date from Data where Date between  %s AND %s;"

    start = '2018-09-12 00:00:00'
    end = '2018-09-16 23:59:59'
    cursor.execute(query, (start, end))

    date_list = []
    par_list = []
    humidity_list =[]
    temperature_list = []


    for (PAR, Humidity,Temperature,Date) in cursor:
        date_list.append(Date)
        par_list.append(PAR)
        humidity_list.append(Humidity)
        temperature_list.append(Temperature)


    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.75)


    par1 = host.twinx()
    par2 = host.twinx()

    offset = 60
    new_fixed_axis = par2.get_grid_helper().new_fixed_axis
    par2.axis["right"] = new_fixed_axis(loc="right",
                                        axes=par2,
                                        offset=(offset, 0))

    par1.axis["right"].toggle(all=True)

    host.set_xlabel("Date")
    host.set_ylabel("PAR")
    par1.set_ylabel("Temperature")
    par2.set_ylabel("Humidity")

    p1, = host.plot(date_list, par_list, label="PAR")
    p2, = par1.plot(date_list, temperature_list, label="Temperature")
    p3, = par2.plot(date_list, humidity_list, label="Humidity")


    host.legend()

    host.axis["left"].label.set_color(p1.get_color())
    par1.axis["right"].label.set_color(p2.get_color())
    par2.axis["right"].label.set_color(p3.get_color())

    plt.draw()
    plt.show()



def main():
    #plotData()
    dnsConnector()

main()