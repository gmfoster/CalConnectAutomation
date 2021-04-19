
### CalConnect Bulk Record Update Script 


#### Instructions
1. Create a new Pycharm project using a new or existing virtual environment.
2. Move CalConnect_Bulk_Updater.py into your main project directory (the top folder on the left side of your pycharm window)
3. Install requirements:
   
   In your pycharm terminal on the bottom of your window, making sure your prompt reads (venv) your-project-path>
    
        pip install -r requirements.txt

   
Note. if installing the requirements isn't working, try manually installing by navigating to File->Settings->Project: Project Name->Python Interpreter-> Click the (+) to install -> search: webdriver-manager -> install the package that matches the name exactly. Do the same thing with the other packages in requirements.txt.

4. Create a new python file in the same directory as the CalConnect_Bulk_Updater Script.
   It will ask if you want to add this file to git. Click Cancel (don't add to git, this is your credentials file you don't want to push this to github)   
   In Credentials.py paste and replace the username, password, and url with corresponding values:

         login = {
          'username': 'YOUR_USERNAME',
          'password': 'YOUR_PASSWORD',
          'list_url': 'URL_OF_LIST'
         }


Currently the script works by identifying the 3rd column of the list editing and selecting the 8th option down. This can be applied to other variables but is designed to work with Process Status + as the 3rd column being edited.

5. Right click the python file in your project tab on the left and click "Run"
6. Once you are satisfied the script is working correctly, uncomment lines 198 and 199 which will save the changes made and run again.