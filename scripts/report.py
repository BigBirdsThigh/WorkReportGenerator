import os
import subprocess
import re

def get_panel_names():
    os.chdir('../PartLists')
    # Check for PartList File
    path = os.getcwd()
    return os.listdir(path)

def run_script(script_name, panel_name):
    # Run the specified script with the given panel name as an argument
    command = f"python {script_name} {panel_name}"
    subprocess.run(command, shell=True)

def main():
    # Find the panel name from the folder
    panel_names = get_panel_names()
    os.chdir('../PanelReports')
    for panel_name in panel_names:
        res = re.search(r"(\d)(_?\d)?", panel_name)
        panel = panel_name[:res.end()]
        try:  
                os.mkdir(panel)  
        except OSError as error:
                print(error)

    # Move back to our report.py directory
    os.chdir('..')
    os.chdir('scripts')

    
    report_script = "ReportMaker.py"
    non_completes_script = "nonCompletes.py"
    for panel_name in panel_names:
        print("processing " + panel + ": .")
        res = re.search(r"(\d)(_?\d)?", panel_name)
        panel = panel_name[:res.end()]	    
        print("processing " + panel + ": ..")
	# Run both scripts with the given panel name
        run_script(report_script, panel)
        print("Processing " + panel + ": ...")
        run_script(non_completes_script, panel)
        print("Finished Processing: " + panel)

if __name__ == "__main__":
    main()
