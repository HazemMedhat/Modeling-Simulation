


# Importing needed libraries
import random
import pandas as pd
import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt

''' define simulation parameters '''
df = pd.DataFrame()  # data frame to show all list values

# variables
Arrival_time = 0     # customer arrival time
Waiting_time = 0     # customer waiting time
ct_express = 0       # express cashier completion time
ct_regular = 0       # regular cashier completion time
Express_start_service_time = 0      # express customer start service time
Regular_start_service_time = 0      # regular customer start service time
Express_service_time = 0            # express customer service time
Regular_service_time = 0            # regular customer service time
Express_waiting_time=0              # express customer waiting time
Regular_Waiting_time=0              # regular customer waiting time
express_idle_time = 0               # express cashier idle time
regular_idle_time = 0               # regular cashier idle time

final_portion_regular=0
final_portion_express=0
# Lists
inter_arrival_list = []
arrival_Time_list = []
Service_Start_Time_list = []
st_list = []        # service time list
waiting_times = []
customer_type = []     # customer type list
customers = []         # customer number list
regular_Cashier = [0]
express_Cashier = [0]
express_service_times = []
regular_service_times = []
express_waiting_times = []
regular_waiting_times = []
express_queue_lengths = []
regular_queue_lengths = []
idle_time_regular=[]
idle_time_express=[]

Portion_regular=[]
Portion_express=[]
#-------------------------------------------------------------------------------------------

######################################final simulation################################
Avarage_of_avgs_regular_st=[]
Avarage_of_avgs_express_st=[]

Avarage_of_avgs_regular_wt=[]
Avarage_of_avgs_express_wt=[]

Max_of_avgs_regular_max_length=[]
Max_of_avgs_express_max_length=[]

Avg_prop_express_waiting=[]

Avarage_of_avgs_regular_idle_time=[]
Avarage_of_avgs_express_idle_time=[]


'''Random variable'''

# generate inter arrival time
def generate_Time_between_Arrivals():
    r = random.random()
    if r <= 0.16:
        time = 0
    elif r <= 0.39:
        time = 1
    elif r < 0.69:
        time = 2
    elif r < 0.9:
        time = 3
    else:
        time = 4
    return time

# generate express customer service time
def generate_Express_Customers_Service_Time():
    r = random.random()
    if r <= 0.3:
        Eservice = 1
    elif r <= 0.7:
        Eservice = 2
    else:
        Eservice = 3
    return Eservice

# generate regular customer service time
def generate_Regular_Customers_Service_Time():
    r = random.random()
    if r <= 0.2:
        Rservice = 3
    elif r <= 0.7:
        Rservice = 5
    else:
        Rservice = 7
    return Rservice

# generate customer type
def generate_customer_type():
    r = random.random()
    if r <= 0.4:
      cust = "Regular"
    else:
      cust = "Express"
    return cust

#-----------------------------------------------------------------------------------------------
for i in range(10):
    '''Simulate the Cashiers'''


    # define the queue length of express and regular cashiers
    express_queue = 0
    regular_queue = 0

    for i in range(1000):
        # generate customer type
        customertype = generate_customer_type()
        customer_type.append(customertype)

        # generate inter arrival time
        IAT = generate_Time_between_Arrivals()
        inter_arrival_list.append(IAT)

        # if the customer is regular
        if customertype == "Regular":
            Regular_service_time = generate_Regular_Customers_Service_Time()   # regular service time
            st_list.append(Regular_service_time)
            regular_service_times.append(Regular_service_time)

            # check if this the first customer then the inter arrival time will equal the arrival time
            if i == 0:
                Arrival_time = IAT
                arrival_Time_list.append(Arrival_time)

            # if not the first customer
            else:
                # The arrival time will be
                # the sum between the inter arrival time of this customer and the arrival of the previous customer
                Arrival_time = inter_arrival_list[i] + arrival_Time_list[i-1]
                arrival_Time_list.append(Arrival_time)

            

            # start service time of the regular customer will be
            # the max between the arrival time of this customer and the last customer finished time
            Regular_start_service_time = max(Arrival_time, regular_Cashier[i])
            Service_Start_Time_list.append(Regular_start_service_time)

            # waiting customer time will equal the start minus the arrival
            Waiting_time = Regular_start_service_time - Arrival_time
            waiting_times.append(Waiting_time)
            regular_waiting_times.append(Waiting_time)


            if waiting_times[i]>0:
                regular_queue+=1
            
            else: 
                regular_queue_lengths.append(regular_queue)
                regular_queue=0
                
            # completion time of the regular will equal the service blus the start
            ct_regular = Regular_service_time + Regular_start_service_time

            # add completion time to the regular cashier and the past values of the express cashier to the express cashier
            regular_Cashier.append(ct_regular)
            express_Cashier.append(express_Cashier[i])


            #Calculate the idel time for regular cashier
            if i ==0:
                regular_idle_time=Service_Start_Time_list[0]
                idle_time_regular.append(regular_idle_time)
            
            
            else:
                regular_idle_time=Service_Start_Time_list[i]-regular_Cashier[i-1]
                idle_time_regular.append(regular_idle_time)

        # if the customer is express
        else:

            Express_service_time=generate_Express_Customers_Service_Time()    # express service time
            st_list.append(Express_service_time)
            

            # if the express queue length less the 1.5 times the regular queue length.
            if express_queue < 1.5 * regular_queue:
                express_service_times.append(Express_service_time)            # add this service time to the express

                # check if this the first customer then the inter arrival time will equal the arrival time
                if i == 0:
                    Arrival_time = IAT
                    arrival_Time_list.append(Arrival_time)

                # if not the first customer
                else:
                    # The arrival time will be
                    # the sum between the inter arrival time of this customer and the arrival of the previous customer
                    Arrival_time = inter_arrival_list[i] + arrival_Time_list[i - 1]
                    arrival_Time_list.append(Arrival_time)

            

                # start service time of the express customer will be
                # the max between the arrival time of this customer and the last customer finished time
                Express_start_service_time = max(arrival_Time_list[i], express_Cashier[i])
                Service_Start_Time_list.append(Express_start_service_time)

                # waiting customer time will equal the start minus the arrival
                Waiting_time = Express_start_service_time - Arrival_time
                waiting_times.append(Waiting_time)
                express_waiting_times.append(Waiting_time)
                
                if  waiting_times[i] :
                    express_queue += 1

                else:
                    express_queue_lengths.append(express_queue)
                    express_queue=0

                
                # completion time of the express will equal the service blus the start
                ct_express = Express_service_time + Express_start_service_time

                # add completion time to the
                # express cashier and the past values of the regular cashier to the regular cashier
                express_Cashier.append(ct_express)
                regular_Cashier.append(regular_Cashier[i])

                
                #Calculate the idel time for regular cashier
                express_idle_time=Service_Start_Time_list[i]-express_Cashier[i-1]
                idle_time_express.append(express_idle_time)

            # else the express customer will enter the regular cashier
            else:
                regular_service_times.append(Express_service_time)             # add service time to the regular

                # check if this the first customer then the inter arrival time will equal the arrival time
                if i == 0:
                    Arrival_time = IAT
                    arrival_Time_list.append(Arrival_time)

                # if not the first customer
                else:
                    Arrival_time = inter_arrival_list[i] + arrival_Time_list[i - 1]
                    arrival_Time_list.append(Arrival_time)

            


                # start service time of the express customer will be
                # the max between the arrival time of this customer and the last customer finished time in the regular
                Express_start_service_time = max(arrival_Time_list[i], regular_Cashier[i])
                Service_Start_Time_list.append(Express_start_service_time)

                # waiting customer time will equal the start minus the arrival
                Waiting_time = Express_start_service_time - Arrival_time
                waiting_times.append(Waiting_time)
                regular_waiting_times.append(Waiting_time)

                if waiting_times[i]:
                    regular_queue += 1
                else: 
                    regular_queue_lengths.append(regular_queue)
                    regular_queue=0

                # completion time of the regular will equal the service blus the start
                ct_express = Express_service_time + Express_start_service_time

                # add completion time to the
                # regular cashier and the past values of the express cashier to the express cashier
                regular_Cashier.append(ct_express)
                express_Cashier.append(express_Cashier[i])

                if i==0:
                    regular_idle_time=Service_Start_Time_list[0]
                #Calculate the idel time for regular cashier
                else:
                    regular_idle_time=Service_Start_Time_list[i]-regular_Cashier[i-1]
                    idle_time_regular.append(regular_idle_time)




        customers.append(i+1)
    
    avg_regular_st = sum(regular_service_times)/len(regular_service_times)
    Avarage_of_avgs_regular_st.append(avg_regular_st)

    avg_express_st = sum(express_service_times)/len(express_service_times)
    Avarage_of_avgs_express_st.append(avg_express_st)

    avg_regular_wt = sum(regular_waiting_times)/len(regular_waiting_times)
    Avarage_of_avgs_regular_wt.append(avg_regular_wt)

    avg_express_wt = sum(express_waiting_times)/len(express_waiting_times)
    Avarage_of_avgs_express_wt.append(avg_express_wt)

    max_regular_queue_length = max(regular_queue_lengths)
    Max_of_avgs_regular_max_length.append(max_regular_queue_length)

    max_express_queue_length = max(express_queue_lengths)
    Max_of_avgs_express_max_length.append(max_express_queue_length)


    waiting_express = 0
    for i in express_waiting_times:
        if i > 0 :
            waiting_express+=1

    prop_express_waiting = waiting_express / len(express_waiting_times)
    Avg_prop_express_waiting.append(prop_express_waiting)

    portions_regular= sum(idle_time_regular)
    Portion_regular.append(portions_regular)

    portions_express= sum(idle_time_express)
    Portion_express.append(portions_express)




    # inter_arrival_list.clear
    # arrival_Time_list.clear
    # Service_Start_Time_list.clear
    # st_list.clear        # service time list
    # waiting_times.clear
    # customer_type.clear    # customer type list
    # customers.clear         # customer number list
    # regular_Cashier.clear
    # express_Cashier.clear
    # express_service_times.clear
    # regular_service_times.clear
    # express_waiting_times.clear
    # regular_waiting_times.clear
    # express_queue_lengths.clear
    # regular_queue_lengths.clear
    # idle_time_regular.clear
    # idle_time_express.clear
    # Portion_regular.clear
    # Portion_express.clear



Avarage_of_avgs_regular_stt=np.mean(Avarage_of_avgs_regular_st)
Avarage_of_avgs_express_stt=np.mean(Avarage_of_avgs_express_st)

Avarage_of_avgs_regular_wtt=np.mean(Avarage_of_avgs_regular_wt)
Avarage_of_avgs_express_wtt=np.mean(Avarage_of_avgs_express_wt)

Avarage_of_max_regular_max_lengthh=np.mean(Max_of_avgs_regular_max_length)
Avarage_of_max_express_max_lengthh=np.mean(Max_of_avgs_express_max_length)

Avg_prop_express_waitingg=np.mean(Avg_prop_express_waiting)

final_portion_regular=-1*sum(Portion_regular)
final_portion_express=sum(Portion_express)


# Does the theoretical average service time of the service time distribution match
# with the experimental one for regular customer ---NO , Because the express customer some times use regular cashier
sum0=0
sum1=0
sum2=0

for i in regular_service_times:
  if i == 3:
    sum0+=1
  elif i == 5:
    sum1+=1
  elif i == 7:
    sum2+=1




avg0 = sum0 / len(regular_service_times)
avg1 = sum1 / len(regular_service_times)
avg2 = sum2 / len(regular_service_times)


avg_st_theoretical_regular = {3:avg0,5:avg1,7:avg2}



# Does the theoretical average service time of the service time distribution match
# with the experimental one for express customer ---YES
sum0=0
sum1=0
sum2=0

for i in express_service_times:
  if i == 1:
    sum0+=1
  elif i == 2:
    sum1+=1
  elif i == 3:
    sum2+=1




avg0 = sum0 / len(express_service_times)
avg1 = sum1 / len(express_service_times)
avg2 = sum2 / len(express_service_times)


avg_st_theoretical_express = {1:avg0,2:avg1,3:avg2}




# Does the theoretical average inter-arrival time of the inter-arrival time
# distribution match with the experimental one? ---YES
sum0=0
sum1=0
sum2=0
sum3=0
sum4=0

for i in inter_arrival_list:
  if i == 0:
    sum0+=1
  elif i == 1:
    sum1+=1
  elif i == 2:
    sum2+=1
  elif i == 3:
    sum3+=1
  elif i == 4:
    sum4+=1




avg0 = sum0 / len(inter_arrival_list)
avg1 = sum1 / len(inter_arrival_list)
avg2 = sum2 / len(inter_arrival_list)
avg3 = sum3 / len(inter_arrival_list)
avg4 = sum4 / len(inter_arrival_list)


avg_IAT_theoretical = {0:avg0,1:avg1,2:avg2,3:avg3,4:avg4}








df['Customer Number'] = customers
df['Customer Type'] = customer_type
df['Inter Arrival Time'] = inter_arrival_list
df['Arrival Time'] = arrival_Time_list
df['Service Start Time'] = Service_Start_Time_list
df['Waiting Time'] = waiting_times
df['Service Time'] = st_list
df['Regular'] = regular_Cashier[1:]
df['Express'] = express_Cashier[1:]



variables = {
    'Average Regular Service Time': avg_regular_st,
    'Average Express Service Time': avg_express_st,
    'Average Regular Waiting Time': avg_regular_wt,
    'Average Express Waiting Time': avg_express_wt,
    'Max Regular Queue Length': max_regular_queue_length,
    'Max Express Queue Length': max_express_queue_length,
    'Proportion of Express Waiting': prop_express_waiting,

    'Avarage_of_avgs_regular_stt':Avarage_of_avgs_regular_st,
    'Avarage_of_avgs_express_stt':Avarage_of_avgs_express_st,
    'Avarage_of_avgs_regular_wtt':Avarage_of_avgs_regular_wt,
    'Avarage_of_avgs_express_wtt':Avarage_of_avgs_express_wt,
    'Avarage_of_max_regular_max_lengthh':Avarage_of_max_regular_max_lengthh,
    'Avarage_of_max_express_max_lengthh':Avarage_of_max_express_max_lengthh,
    'Avg_prop_express_waitingg':Avg_prop_express_waiting,
    
    'Theoretical avg ST regular':avg_st_theoretical_regular,
    'Theoretical avg ST express':avg_st_theoretical_express,
    'Theoretical avg IAT':avg_IAT_theoretical,
    'Final_portion_idle_regular':final_portion_regular,
    'Final_portion_idle_express':final_portion_express,
}


# GUI
layout = [
    [sg.Button(key=variable_name, button_text=variable_name,size=(10,5),auto_size_button=True) for variable_name in variables.keys()],
    [sg.Table(values=df.values.tolist(),
              headings=df.columns.tolist(),
              auto_size_columns=True,
              justification='right',
              display_row_numbers=False,
              num_rows=min(25, len(df)),
              alternating_row_color='black',
              key='-TABLE-')],
    [sg.Button('Exit')]
]

window = sg.Window('Super Market Calender', layout, resizable=True)

# Event loop
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break


    elif event in variables:
        variable_name = event
        value = variables[variable_name]
        if variable_name in ['Avarage_of_avgs_regular_stt','Avarage_of_avgs_express_stt','Avarage_of_avgs_regular_wtt','Avarage_of_avgs_express_wtt','Avg_prop_express_waitingg']:
            # Plot histogram for specific lists
            plt.hist(value, bins=15, color='blue', edgecolor='black')
            plt.xlabel(f'{variable_name}')
            plt.ylabel('Days')
            plt.title(f'Histogram of {variable_name}')
            plt.show()
        else:
            sg.popup(f"{variable_name}: {value}")
# Close the window when the loop exits
window.close()


