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

def find_2nd(string, substring):
   return string.find(substring, string.find(substring) + 1)

def createReport(filename, content):
    # Create a report file and write content to it
    os.chdir('../PanelReports')
    with open(os.path.join(filename, filename + "Incomplete.txt"), "w") as report_file:
        current_header = None
        for i in range(0, len(content)):
            curr = content[i]
            if("Note" in curr):
           	 comp = curr.index("Note")-2        
            else:
                comp = len(curr)
            # Extract the first tag for comparison
            start = curr.index("-") + 2
            if "," in curr and curr.index(",") < comp: # To ensure the comma is not in the Note
                end = curr.index(",")
            elif "Note" in curr:
                end = comp
            else:
                end = find_2nd(curr, "-")
            tag = curr[start:end].strip()  # Extract the first tag

            # If the tag changes, write a new header
            if tag != current_header:
                if current_header is not None:
                    report_file.write("\n")
                report_file.write("-----" + tag + "-----\n")
                current_header = tag

            # Write the current line
            report_file.write(curr)
    os.chdir('..')

def takeInput():
    # Use the first command-line argument as the panel name
    panel = sys.argv[1] if len(sys.argv) > 1 else input("Enter Part List e.g. Panel1: ").strip()
    os.chdir('../PartLists')
    panel_names = panel + "PartList.txt"
    readLines(panel_names, panel)

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
                content.append(f"MG{partNumberL} - {issues} - Note: {note}\n")  # Line with "R" replaced by "L"
            else:
                content.append(f"MG{partNumber} {issues} - Note: {note}\n")  # Line with note
        else:
            if "R" in partNumber:
                rIndex = partNumber.index("R")
                content.append(f"MG{partNumber} {issues}\n")  # Line with original part number
                partNumberL = partNumber[:rIndex] + "L"
                content.append(f"MG{partNumberL} - {issues}\n")  # Line with "R" replaced by "L"
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
