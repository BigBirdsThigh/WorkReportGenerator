import os
import sys

convert = {
	"c":"COMPLETED",
	"a":"ATTEMPTING",
	"wf":"WELDED FABRICATION",
	"x": "IMPOSSIBLE",
	"di": "DRAWING ISSUE",
	"cc": "CHECK CLIP",
	"bs": "BOLT SPACING",
	"n/a": "NOT ATTEMPTED",
	"i": "DRAWING INCOMPREHENSIBLE"
}

def createReport(filename, content):
	# Create a report file and write content to it
	os.chdir('../PanelReports')
	with open(os.path.join(filename, filename + "Report.txt"), "w") as report_file:
		report_file.write(content)
		os.chdir('..')

def takeInput():
    # Use the first command-line argument as the panel name
    panel = sys.argv[1] if len(sys.argv) > 1 else input("Enter Part List e.g. Panel1: ").strip()
    os.chdir('../PartLists')
    panel_name = panel + "PartList.txt"
    readLines(panel_name, panel)



def createContent(note, partNumber, issues):
    content = ""

    if note.strip():  # Check if note is not just whitespace
        if "R" in partNumber:
            rIndex = partNumber.index("R")
            content += f"MG{partNumber} {issues} - Note: {note}\n"  # Line with original part number
            partNumberL = partNumber[:rIndex] + "L"
            content += f"MG{partNumberL} {issues} - Note: {note}\n"  # Line with "R" replaced by "L"
        else:
            content += f"MG{partNumber} {issues} - Note: {note}\n"  # Line with note
    else:
        if "R" in partNumber:
            rIndex = partNumber.index("R")
            content += f"MG{partNumber} {issues}\n"  # Line with original part number
            partNumberL = partNumber[:rIndex] + "L"
            content += f"MG{partNumberL} {issues}\n"  # Line with "R" replaced by "L"
        else:
            content += f"MG{partNumber} {issues}\n"  # Line without note

    return content

def readLines(filename, panel):
    # Read lines from the part list file and format the content
    content = ""
    try:
        with open(filename, "r") as data:
            lines = data.readlines()
            for line in lines:
                issueIndex = line.index('-') + 2
                partNumber = line[:issueIndex].strip()
                
                if "N:" in line:  # extract our issue codes
                    NoteIndex = line.index('N:')
                    note = line[NoteIndex+2:].strip()
                    issueCode = line[issueIndex:NoteIndex-1].strip()
                else:
                    note = ""
                    issueCode = line[issueIndex:].strip()

                # Split issue codes and convert them
                codes = issueCode.lower().split()
                issue = [convert.get(code, "UNKNOWN") for code in codes]
                issues = ", ".join(issue)

                # Append the content for each part
                content += createContent(note, partNumber, issues)
        
        # Create the report with the accumulated content
        createReport(panel, content)
    except OSError as e:
        print("Error: " + filename + " is not a valid panel file, maybe you misstyped the name(panel name should be exact to part lists file name)")
        takeInput()

takeInput()