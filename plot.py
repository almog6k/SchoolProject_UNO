from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import mysql.connector
import matplotlib.pyplot as plt

#Config file to connect to the MYSQL database
config = {
  'user': 'USERNAME', #Food Computer SQL user name
  'password': 'Password', #Food Computer SQL Password
  'host': 'IPADRESS',#Food Computer SQL IP
  'database': 'DATABASE', #Food Computer SQL Database
  'raise_on_warnings': True
}

def plotData(start, end):
    # Create SQL Connection
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    # Query to run
    query = "Select PAR, Humidity, Temperature, Date from Data where Date between  %s AND %s;"

    # Run the Query and save the results in the cursor value
    cursor.execute(query, (start, end))

    # Storage for the values extracted for the query
    date_list = []
    par_list = []
    humidity_list = []
    temperature_list = []

    # Append values to the empty lists above
    for (PAR, Humidity, Temperature, Date) in cursor:
        date_list.append(Date)
        par_list.append(PAR)
        humidity_list.append(Humidity)
        temperature_list.append(Temperature)

    # Create the multi axis plot
    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.75)
    par1 = host.twinx()
    par2 = host.twinx()

    # Set an offset for third value scale
    offset = 60
    # Create the scales
    new_fixed_axis = par2.get_grid_helper().new_fixed_axis
    par2.axis["right"] = new_fixed_axis(loc="right",
                                        axes=par2,
                                        offset=(offset, 0))

    par1.axis["right"].toggle(all=True)

    # Label the scales
    host.set_xlabel("Date")
    host.set_ylabel("PAR")
    par1.set_ylabel("Temperature")
    par2.set_ylabel("Humidity")

    # Using the lists data to generate the plots according to the date list and the sensors data accordingly.
    p1, = host.plot(date_list, par_list, label="PAR")
    p2, = par1.plot(date_list, temperature_list, label="Temperature")
    p3, = par2.plot(date_list, humidity_list, label="Humidity")

    # Set the legand
    host.legend()

    # Setting the colors
    host.axis["left"].label.set_color(p1.get_color())
    par1.axis["right"].label.set_color(p2.get_color())
    par2.axis["right"].label.set_color(p3.get_color())

    # Display the plot on the screen
    plt.draw()
    plt.show()

def main():

    #Start and end times
    start = '2018-09-06 00:00:00'
    end = '2018-09-08 23:59:59'

    #Call the function
    plotData(start,end)

main()