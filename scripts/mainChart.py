import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import json

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
    content = []
    sort = []
    occurences = []
    count = 0    
    try:
        for panel in data:
            with open (panel, "r") as parts:
                print("Reading file: " + str(panel))
                for line in parts:
                    if (line == "\n"):
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
            
                    # if "c" in codes:  # Skip if the part is completed
                    #     continue
            
                    issue = [convert.get(code, "") for code in codes]               
                    
                    issues = ", ".join(issue)
                    sort.append([note, partNumber, issues, order.get(codes[0])])
        
                occurences += collectOccurences(sort, count)
                count += 1
    except OSError as e:
        print("Error: " + panel + " is not a valid panel file, maybe you mistyped the name(panel name should be exact to part lists file name)")
        takeInput()
        
    return occurences
        
def collectOccurences(content, x):
    occurences = []
    for i in range(len(content)):
        occurences.append(["Panel" + str(x) ,content[i][2].split(",")[0]])
        
    return occurences
        
def createGraph(data):
    data = pd.DataFrame(data, columns=['Tag' , 'Count'])
    data.dropna(inplace=True)
 

    cross_tab_prop = pd.crosstab(index = data['Tag'], columns = data['Count'], normalize = "index")
    print(cross_tab_prop)

    cross_tab_prop.plot(kind='bar', 
                        stacked=True, 
                        colormap='tab10', 
                        figsize=(8, 6))
    plt.legend(loc="upper left", ncol=2)
    plt.xlabel("Panel")
    plt.ylabel("Proportion")
    plt.show()

takeInput()