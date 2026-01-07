import subprocess
import os

base_path = os.path.join(os.path.expanduser("~"), "Desktop", "amazon_scraper")

# List of scraper files
scripts = [
    "tv.py",
    "ac.py",
    "microwave.py",
    "washing_machine.py",
    "ref.py"
]


for script in scripts:
    script_path = os.path.join(base_path, script)
    print(f"\n Running {script}...\n")
    subprocess.run(["python", script_path], check=True)
    print(f" Finished {script}\n")

print(" All scraping scripts completed successfully.")