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
    "a": 2
}


def createReport(filename, content):
    # Create a report file and write content to it
    os.chdir('../PanelReports')
    with open(os.path.join(filename, filename + "Incomplete.txt"), "w") as report_file:
        for i in range(0, len(content)):
            if i > 0:
                prev = content[i-1]
                start = prev.index("-")
                end = prev.index(",")
                prev = prev[start+2:end]
                curr = content[i]
                end = curr.index(",")
                curr = curr[start+2:end]
                if curr != prev:
                    report_file.write("\n")
                    report_file.write("-----" + curr + "-----\n")
                report_file.write(content[i])
            else:
                curr = content[i]
                start = curr.index("-")
                curr = content[i]
                end = curr.index(",")
                curr = curr[start+2:end]
                report_file.write("-----" + curr + "-----\n")
                report_file.write(content[i])
    os.chdir('..')

def takeInput():
    # Use the first command-line argument as the panel name
    panel = sys.argv[1] if len(sys.argv) > 1 else input("Enter Part List e.g. Panel1: ").strip()
    os.chdir('../PartLists')
    panel_name = panel + "PartList.txt"
    readLines(panel_name, panel)

def createContent(inputContent):
    content = []
    nIndex = 0
    pIndex = 1
    iIndex = 2
    
    for line in inputContent:
        note = line[nIndex]
        partNumber = line[pIndex]
        issues = line[iIndex]
        if note.strip():  # Check if note is not just whitespace
            if "R" in partNumber:
                rIndex = partNumber.index("R")
                content.append(f"MG{partNumber} {issues} - Note: {note}\n")  # Line with original part number
                partNumberL = partNumber[:rIndex] + "L"
                content.append(f"MG{partNumberL} {issues} - Note: {note}\n")  # Line with "R" replaced by "L"
            else:
                content.append(f"MG{partNumber} {issues} - Note: {note}\n")  # Line with note
        else:
            if "R" in partNumber:
                rIndex = partNumber.index("R")
                content.append(f"MG{partNumber} {issues}\n")  # Line with original part number
                partNumberL = partNumber[:rIndex] + "L"
                content.append(f"MG{partNumberL} {issues}\n")  # Line with "R" replaced by "L"
            else:
                content.append(f"MG{partNumber} {issues}\n")  # Line without note

    return content

def readLines(filename, panel):
    # Read lines from the part list file and format the content
    content = []
    sort = []
    try:
        with open(filename, "r") as data:
            lines = data.readlines()
            for line in lines:
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

                if "c" in codes:  # Skip if the part is completed
                    continue

                issue = [convert.get(code, "") for code in codes]               
                
                issues = ", ".join(issue)
                sort.append([note, partNumber, issues, order.get(codes[0])])

        content = sorted(sort, key=lambda x: (x[3], x[1]))
        # Append the content for each part
        content = createContent(content)
        
        # Create the report with the accumulated content
        createReport(panel, content)
    except OSError as e:
        print("Error: " + filename + " is not a valid panel file, maybe you mistyped the name(panel name should be exact to part lists file name)")
        takeInput()

takeInput()
