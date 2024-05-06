import random
import pandas as pd
import numpy as np
import PySimpleGUI as sg
import matplotlib.pyplot as plt

def generateRandomDemand():
    r = random.random()
    if r <= 0.2:
        demand = 0
    elif r <= 0.54:
        demand = 1
    elif r < 0.9:
        demand = 2
    else:
        demand = 3
    return demand
def generateRandomLeadTime():
    r = random.random()
    if r <= 0.4:
        LeadTime = 1
    elif r <= 0.75:
        LeadTime = 2
    else:
        LeadTime = 3
    return LeadTime


# Define the initial inventory and showroom
inventory = 3
showroom = 4

# Define the review period
review_period = 3

# Define the holding cost and selling price
holding_cost = 1000
selling_price = 10000

# Define the simulation parameters
df = pd.DataFrame()
num_days = 10
shortage_count = 0
order_day = 0
lead_time_list = []
days_list = []
demand_list = []
IS_shortage = []
starting_inventory = []
starting_showroom = []
ending_inventory = []
ending_showroom = []
shortage_inventory_list = []
shortage_showroom_list = []
order_day_list = []
order_quantity_list = []
net_profits = []

# define the average list of all average
avg_profit_runs = []
avg_inv_runs = []
avg_sh_runs = []
avg_daemand_runs=[]

# Run more than one time
for i in range(30):
    # Run the simulation
    for day in range(1, num_days + 1):
        days_list.append(day)

        ordering_cost = 0
        if day == order_day:
            showroom += (5 - showroom)
            inventory += (10 - inventory)
            ordering_cost = 20000

        starting_showroom.append(showroom)
        starting_inventory.append(inventory)
        # get demand
        demand = generateRandomDemand()
        demand_list.append(demand)

        # Sell from inventory
        if inventory >= demand:
            inventory -= demand
            IS_shortage.append("NO")
        # Sell from showroom
        elif inventory + showroom >= demand:
            # shortage_count += 1
            showroom -= (demand - inventory)
            inventory = 0
            IS_shortage.append("NO")
        # Lost opportunity
        else:
            IS_shortage.append("yes")

        Showroom_Shortage = 5 - showroom
        Inventory_Shortage = 10 - inventory
        order_quantity = (Inventory_Shortage) + (Showroom_Shortage)

        shortage_showroom_list.append(Showroom_Shortage)
        shortage_inventory_list.append(Inventory_Shortage)
        order_quantity_list.append(order_quantity)

        # Check if we need to place an order
        if day % review_period == 0:
            # Place an order
            lead_time = generateRandomLeadTime()
            order_day = day + lead_time
            order_day_list.append(order_day)
            lead_time_list.append(lead_time)
        else:
            order_day_list.append("NONE")
            lead_time_list.append("NONE")

        net_profit = selling_price * demand - holding_cost * (inventory + showroom) - ordering_cost

        # Calculate the net profit
        net_profits.append(net_profit)

        # Record the ending inventory and showroom
        ending_inventory.append(inventory)
        ending_showroom.append(showroom)

    # Calculate the average ending units in the showroom and inventory
    avg_ending_showroom = int(np.mean(ending_showroom))
    avg_sh_runs.append(avg_ending_showroom)
    avg_ending_inventory = int(np.mean(ending_inventory))
    avg_inv_runs.append(avg_ending_inventory)
    # Calculate the average net profit for the car dealer
    sum = 0
    for i in net_profits:
        if i >= 0:
            sum += i
    avg_net_profit = sum / len(net_profits)

    # Add them to list
    avg_profit_runs.append(avg_net_profit)


    #Avarage demand for days
    Avg_demands=np.mean(demand_list)
    avg_daemand_runs.append(Avg_demands)


df['Day Number'] = days_list
df['Starting showroom cars'] = starting_showroom
df['Starting inventory cars'] = starting_inventory
df['Demand'] = demand_list
df["Showroom after demand"] = ending_showroom
df["Inventory after demand"] = ending_inventory
df["Showroom shortage"] = shortage_showroom_list
df["Inventory shortage"] = shortage_inventory_list
df["Lead Time "] = lead_time_list
df["Order day"] = order_day_list
df["Order quantity"] = order_quantity_list
df["IS shortage"] = IS_shortage
df["Net profit"] = net_profits

# Calculate the number of days when a shortage condition occurs
shortage_days = 0
for i in IS_shortage:
  if i == "yes":
    shortage_days+=1

# Calculate the average for averages
final_profit_avg = np.mean(avg_profit_runs)
final_showroom_avg = np.mean(avg_sh_runs)
final_inventory_avg = np.mean(avg_inv_runs)
final_demand_avg= np.mean(avg_daemand_runs)


#Does the theoretical average demand of the demand distribution match the experimental one?
sum0=0
sum1=0
sum2=0
sum3=0
for i in demand_list:
  if i == 0:
    sum0+=1
  elif i == 1:
    sum1+=1
  elif i == 2:
    sum2+=1
  elif i == 3:
    sum3+= 1

avg0 = sum0 / len(demand_list)
avg1 = sum1 / len(demand_list)
avg2 = sum2 / len(demand_list)
avg3 = sum3 / len(demand_list)

avg_demand_theoretical = {0:avg0,1:avg1,2:avg2,3:avg3}

#Does the theoretical average lead time of the lead time distribution match the experimental one?
sum1=0
sum2=0
sum3=0
for i in lead_time_list:
  if i == 1:
    sum1+=1
  elif i == 2:
    sum2+=1
  elif i == 3:
    sum3+= 1

avg1 = sum1 / len(lead_time_list)
avg2 = sum2 / len(lead_time_list)
avg3 = sum3 / len(lead_time_list)

avg_leadtime_theoretical={1:avg1,2:avg2,3:avg3}


# GUI
variables = {
    'Average ending units in showroom': avg_ending_showroom,
    'Average ending units in inventory': avg_ending_inventory,
    'Number of days when a shortage condition occurs': shortage_days,
    'Average net profit for the car dealer': avg_net_profit,
    'Final net profit average': final_profit_avg,
    'Final showroom average': final_showroom_avg,
    'Final inventory average': final_inventory_avg,
    'Final demand average': final_demand_avg,
    'Histogram for avg profits': avg_profit_runs,
    'Histogram for Final showroom average': avg_sh_runs,
    'Histogram fot Final inventory average': avg_inv_runs,
    'Histogram fot Final demand average': avg_daemand_runs,

    'Experimental avarage of demand':avg_demand_theoretical,
    'Experimental avarage of leadtime':avg_leadtime_theoretical,

}

layout = [
    [sg.Button(key=variable_name, button_text=variable_name,visible = True, size=(10, 5), auto_size_button=True) for variable_name in variables.keys()],
    [sg.Table(values=df.values.tolist(),
              headings=df.columns.tolist(),
              auto_size_columns=True,
              justification='center',
              vertical_scroll_only=False,
              display_row_numbers=False,
              num_rows=min(25, len(df)),
              alternating_row_color='black',
              key='-TABLE-')],
    [sg.Button('Exit')]
]


window = sg.Window('Super Market Calendar', layout, resizable=True)

# Event loop
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break

    elif event in variables:
        # Display the selected variable and its value without the table
        variable_name = event
        value = variables[variable_name]

        if variable_name in ['Histogram for avg profits', 'Histogram for Final showroom average', 'Histogram fot Final inventory average','Histogram fot Final demand average']:
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







