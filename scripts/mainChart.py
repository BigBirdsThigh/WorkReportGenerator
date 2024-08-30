import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import json
import seaborn as sns


def loadKeys():
    with open('Keys.txt') as f:
        data = f.read()
        js = json.loads(data)
    return js

convert = loadKeys() # Load codes from Keys.txt to maintain consistency

order = {
    "x": 0,
    "n/a": 1,
    "a": 2,
    "c": 3
}

def takeInput():
    data = []
    # Use the first command-line argument as the panel name
    panels = sys.argv[1:] if len(sys.argv) > 1 else [input("Enter Part List e.g. Panel1: ").strip()]
    os.chdir('../PartLists')
    panel_names = panels
    data = readLines(panels)
    createGraph(data)


def readLines(data):
    # Read lines from the part list file and format the content
    occurences = []
    count = 0    
    try:
        for panel in data:
            sort = []  # Clear the sort list for each panel
            with open(panel, "r") as parts:
                print(f"Processing {panel}:")
                for line in parts:
                    if line.strip() == "":
                        continue
                    issueIndex = line.index('-') + 2
                    partNumber = line[:issueIndex].strip()
                    
                    if "N:" in line:  # extract our issue codes
                        NoteIndex = line.index('N:')
                        note = line[NoteIndex + 2:].strip()
                        issueCode = line[issueIndex:NoteIndex - 1].strip()
                    else:
                        note = ""
                        issueCode = line[issueIndex:].strip()
            
                    # Split issue codes and convert them
                    codes = issueCode.lower().split()
            
                    issue = [convert.get(code, "") for code in codes]               
                    issues = ", ".join(issue)
                    sort.append([note, partNumber, issues, order.get(codes[0])])

                if sort:  # Ensure data exists for this panel
                    print(f"Data for {panel} collected successfully.")
                else:
                    print(f"No data found for {panel}.")

                occurences += collectOccurences(sort, count, panel)
                count += 1

    except OSError as e:
        print(f"Error: {panel} is not a valid panel file, maybe you mistyped the name (panel name should be exact to part lists file name)")
        takeInput()
        
    return occurences


        
def collectOccurences(content, x, name):
    occurences = []
    for i in range(len(content)):
        print(f"Collecting issue for {name}: {content[i][2].split(',')[0]}")
        occurences.append([name[:name.index("PartList")] ,content[i][2].split(",")[0]])
    return occurences

        
def createGraph(data):
    data = pd.DataFrame(data, columns=['Panel', 'Issue'])
    data.dropna(inplace=True)
    plt.style.use('fivethirtyeight')
  
    
    # Ensure the columns (categories) are ordered consistently
    issue_order = ['ATTEMPTING', 'COMPLETED', 'IMPOSSIBLE', 'NOT ATTEMPTED']
    cross_tab_prop = pd.crosstab(index=data['Panel'], columns=data['Issue'], normalize="index").round(4) * 100
    cross_tab_prop = cross_tab_prop[issue_order]  # Reorder columns

    print(cross_tab_prop)

    # Define custom colors corresponding to your categories
    colors = ['#ff7f00', '#4daf4a', '#e41a1c', '#377eb8']  # Orange, Green, Red, Blue

    ax = cross_tab_prop.plot(kind='bar', 
                        stacked=True, 
                        figsize=(11, 6),
                        legend=True,
                        color=colors,  # Use custom colors in order
                        alpha=0.85,  # Set opacity level
                        yticks=[0,10,20,30,40,50,60,70,80,90,100, 110])

    plt.legend(loc='upper left', ncol=2)

    # Adding percentage labels to the bars
    for p in ax.patches:
        width = p.get_width()  # Get the width of each bar
        height = p.get_height()  # Get the height of each bar
        x, y = p.get_xy()  # Get the x and y coordinates of the bottom left corner of the bar
        ax.text(x + width / 2, y + height / 2, f'{height:.1f}%', 
                ha='center', va='center', color='black', fontsize=10)

    plt.xlabel("Panel")
    plt.ylabel("Proportion(%)")
    plt.subplots_adjust(bottom=0.21)
    
    plt.show()



takeInput()