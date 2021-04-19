
### CalConnect Bulk Record Update Script 


#### Instructions
1. Create a new Pycharm project using a new or existing virtual environment.
2. Move CalConnect_Bulk_Updater.py into your main project directory (the top folder on the left side of your pycharm window)
3. Install requirements:
   
   In your pycharm terminal on the bottom of your window, making sure your prompt reads (venv) your-project-path>
    
        pip install selenium
    
        pip install webdriver-manager

        pip install dotenv
   
Note. if installing the requirements isn't working, try manually installing by navigating to File->Settings->Project: Project Name->Python Interpreter-> Click the (+) to install -> search: webdriver-manager -> install the package that matches the name exactly. Do the same thing with selenium.

4. Navigate into python code and enter your CalConnect username/password into the self.username and self.password variables on lines 30,31

5. Enter the url of the list of incident id's that are to be updated in the self.list_url variable. 


Currently the script works by identifying the 3rd column of the list editing and selecting the 8th option down. This can be applied to other variables but is designed to work with Process Status + as the 3rd column being edited.

6. Right click the python file in your project tab on the left and click "Run"
7. Once you are satisfied the script is working correctly, uncomment lines 198 and 199 which will save the changes made and run again.