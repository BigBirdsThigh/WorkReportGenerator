import os
import sys

def get_panel_names():
    os.chdir('../PartLists')
    # Check for PartList File
    path = os.getcwd()
    return os.listdir(path)

def getLines(panels):
    lines = []
    for panel in panels:
        with open(panel, 'r') as file: 
            for line in file:
                if line.strip() == "":
                    continue
                if "x" in line:
                    continue
                if "n/a" in line.lower():
                    continue
                lines.append(line[:line.index("-")].strip())
    return lines

def read_existing_finishes():
    existing_parts = set()
    if os.path.exists("Finishes.txt"):
        with open("Finishes.txt", "r") as file:
            for line in file:
                part_number = line.split("-")[0].strip()
                existing_parts.add(part_number)
    return existing_parts

def createList(data, existing_parts):
    with open("Finishes.txt", "a") as file:  # Use "a" to append to the file
        for line in data:
            if line not in existing_parts:
                file.write(f"{line} - N \n")
        

panel_names = get_panel_names()

# Ensure list only contains part lists
panel_names = [x for x in panel_names if "PartList.txt" in x]
numbers = getLines(panel_names)

existing_parts = read_existing_finishes()

createList(numbers, existing_parts)
