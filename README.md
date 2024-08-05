"# WorkReportGenerator" 

Explanation
------
Make sure to delete contents of *PanelReports* but do *NOT* delete the PanelReports folder
1. Each part at work has it's unique *Part Number* 
2. While going through and detailing each part a number of issues may arise e.g. drawing unreadable, incorrect measurements etc.
3. In order to make the tasks of recording and addressing these issues simpler and more streamlined I developed this simple script
4. In the folder PartLists we create a text file corresponding to the panel e.g. Panel1PartList.txt
5. In that file we enter data in the form {PartNumber} - {IssueCode(s)} - N: {Note(optional)}
6. I have created a dictionary that maps codes like "di" to errors like DRAWING INCOMPREHENSIBLE
7. The hope is that using this means a user can quickly jot down parts and the issues they faced, if any, and add a note if they feel additional info is required

Output
------
The script creats subfolders inside of the *PanelReports* folder for each part list that exists, it then creates two reports. 
1. The full onordered and unfiltered list of every part
2. A list only containing any part not tagged as completed, this list is sorted to have parts labelled IMPOSSIBLE first, then the NOT ATTEMPTED parts and lastly the ATTEMPTING parts
This system is designed to make the task of the detailer who reviews the work easier as they get a list of where to focus their attention when reviewing work

Issue Codes
------
    "c": "COMPLETED",
    "a": "ATTEMPTING",
    "wf": "WELDED FABRICATION",
    "x": "IMPOSSIBLE",
    "di": "DRAWING ISSUE",
    "cc": "CHECK CLIP",
    "bs": "BOLT SPACING",
    "n/a": "NOT ATTEMPTED",
    "i": "DRAWING INCOMPREHENSIBLE"