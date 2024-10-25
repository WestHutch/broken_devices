This is only to be used by THS/TMS techs to automate the process when receiving a broken MacBook.

Upon first running the program, you will be prompted to enter your credentials for each step. After that, the program will never ask you again. If you entered these incorrectly, you can simply edit them in the userinfo.txt file that was created.

To run this program...
  1. Ensure python is installed on your machine
  2. Ensure your label printer is set as your default printer
  3. Download this repo and save it to your desktop
  4. In the command prompt, naviate to where you have this repo saved
       cd Desktop\broken_devices
  5. Run the following commands sequentially. This will ensure you have all necessary packages installed
       python -m venv venv
       venv\Scripts\activate.bat
       pip install -r requirements.txt
  6. Run the main script
       python broken_device_script.py
