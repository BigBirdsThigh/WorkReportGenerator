import os
import sys
from colorama import Fore, Back, Style, init
import re

# Initialize colorama
init(autoreset=True)

def get_panel_names():
    os.chdir('../PartLists')
    # Check for PartList File
    path = os.getcwd()
    return os.listdir(path)

panel_names = get_panel_names()

def splitData():
    output = []
    with open("Finishes.txt", 'r') as file:
        for line in file:
            if "N" in line:             
                cutOff = line.index("N") - 2
                output.append([[line[:cutOff].strip()], ["N"]])
            else:
                cutOff = line.index("Y") - 2
                output.append([[line[:cutOff].strip()], ["Y"]])
    return output

def calculate_percentages(num1, num2):
    total = num1 + num2
    
    if total == 0:
        # Handle the edge case where both numbers are 0
        return 50, 50
    
    percentage1 = (num1 / total) * 100
    percentage2 = (num2 / total) * 100
    
    return percentage1, percentage2

def buildBar(counts):
    fin = round(counts[0])  # Percentage of first part
    un = round(counts[1])   # Percentage of second part
    
    # Use a better ASCII symbol for the bar
    symbol1 = '█'  # Green part
    symbol2 = '█'  # Red part

    bar1 = symbol1 * fin
    bar2 = symbol2 * un
    
    return Fore.GREEN + f"[{bar1}" + Fore.RED + f"{bar2}]" + Style.RESET_ALL

def extract_number_and_status(item):
    # Extract the number from the part name
    match = re.search(r'\d+', item[0][0])
    number = int(match.group()) if match else float('inf')
    
    # Convert "N" to 0 and "Y" to 1 to prioritize "N" elements
    status = 0 if item[1][0] == "N" else 1
    
    # Return a tuple that sorts by status first, then by number
    return (status, number)

def printProgress(data):
    n_count = 0
    y_count = 0
    for line in data:
        number = "".join(line[0])
        if "".join(line[1]) == "N":
            n_count += 1
            print(Fore.RED + f"{number}-------------NOT FINISHED" + Style.RESET_ALL)
        else:
            y_count += 1
            print(Fore.GREEN + f"{number}-------------FINISHED" + Style.RESET_ALL)

    # Print totals
    total = y_count + n_count
    print(Style.RESET_ALL + f"\nTotal number of entires: {total}")
    print(Fore.RED + f"Total 'N' elements: {n_count}" + Fore.GREEN + f"\nTotal 'Y' elements: {y_count}")
    print(Fore.GREEN+f"Percentage of parts finished: {round((y_count/total)*100,2)}%")
    print(Fore.RED +f"Percentage of parts unfinished: {round((n_count/total)*100, 2)}%")
    counts = [y_count, n_count]
    print(buildBar(counts))

def update_file(part_number):
    updated = False
    with open("Finishes.txt", 'r') as file:
        lines = file.readlines()

    with open("Finishes.txt", 'w') as file:
        for line in lines:
            if line.startswith(part_number) and "N" in line:
                line = line.replace("N", "Y")
                updated = True
            file.write(line)
    
    return updated

# Ensure list only contains part lists
panel_names = [x for x in panel_names if "PartList.txt" in x]
data = splitData()
# Sort by status (N/Y) first, then by the extracted number
data = sorted(data, key=extract_number_and_status)
printProgress(data)

# Prompt user to mark parts as finished
while True:
    print("Enter Part Number When Finished (or type 'exit' to quit): ")
    part_number = input().strip()
    
    if part_number.lower() == "exit":
        break
    
    if update_file(part_number):
        print(f"{part_number} has been marked as FINISHED.")
    else:
        print(f"{part_number} not found or already marked as FINISHED.")
    
    # Refresh and display the updated progress
    data = splitData()
    data = sorted(data, key=extract_number_and_status)
    printProgress(data)
