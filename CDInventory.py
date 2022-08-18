#------------------------------------------#
# Title: Assignment06_Starter.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# PMoy, 2022-Aug-14, Refactored into functions and added minor validations
# PMoy, 2022-Aug-17, Added error handling and converted to binary data
#------------------------------------------#

import pickle # used to save/load binary files
import os.path # used to check if file exists

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
checkID = set() # set of IDs to avoid duplicates
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object

# -- PROCESSING -- #
class DataProcessor:
    """Processing and transforming data within table operations"""
    
    @staticmethod
    def addCDToTable(newCD):
        """Function to add CD data to table
        
        Reads the ID, title, and artist from a tuple representing a CD and adds
        to the table. Checks for duplicate ID
        
        Args:
            newCD (tuple): tuple representing CD containing ID, title, artist
            
        Returns:
            None.
        """
        intID = int(newCD[0])
        if intID in checkID:
            input('canceling... Duplicate ID. CD not added. Press [ENTER] to continue to the menu.')    
        else:
            dicRow = {'ID': intID, 'Title': newCD[1], 'Artist': newCD[2]}
            lstTbl.append(dicRow)
            checkID.add(intID)
            
    @staticmethod
    def removeCDFromTable(deleteID):
        """Function to remove CD from table
        
        Searches table for a row with ID matching the parameter ID and removes
        that row if it exists.
        
        Args:
            deleteID (int): Integer denoting ID of CD to delete
            
        Returns:
            None.
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == deleteID:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                checkID.remove(int(deleteID))
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
            
    @staticmethod
    def resetTable():
        """Function to reset table
        
        Resets table, clearing table contents and contents of ID check set
        
        Args:
            None.
            
        Returns:
            None.
        """
        lstTbl.clear()
        checkID.clear()
        
    @staticmethod
    def loadTable(data):
        '''Function to load table and populate checkID set
        
        Sets lstTbl to the data loaded, checking that it loaded and populating the checkID set.
        
        Args:
            data (list of dict): List of dicts representing loaded table.
        
        Returns:
            None.
        '''
        if data != None:
            DataProcessor.resetTable()
            global lstTbl
            lstTbl = data
            for row in lstTbl:
                checkID.add(row['ID'])       

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table; one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
         
        Returns:
            List of dicts object loaded from file, or None if there is nothing to load or an error.
        """
        if not os.path.isfile(file_name): # create file if it does not exist
            open(file_name, 'a').close() 
            return None
        else: 
            with open(file_name, 'rb') as fileObj:
                fileContents = None
                try:
                    fileContents = pickle.load(fileObj)
                except Exception as e:
                    print('Error loading file!')
                    print(type(e), e, e.__doc__, sep='\n')
                    print('\nProgram started, but nothing was loaded...\n')
                return fileContents
        
    @staticmethod
    def write_file(file_name, table):
        """Function to manage data writing to file

        Writes data from list of dicts to file identified by file_name 
       
        Args:
            file_name (string): name of file to write data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        with open(file_name, 'wb') as fileObj:
            pickle.dump(table, fileObj)
            
# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[c] Clear Current Inventory\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case string of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'c', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s, c, or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    def get_new_CD():
        intID = -1
        while True:
            strID = input('Enter ID: ').strip()
            try:
                intID = int(strID)
                break;
            except ValueError as e:
                print('That is not an integer!\n')
                print(type(e), e, e.__doc__, sep='\n')
                print('Please try again.\n\n')
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        return intID, strTitle, strArtist
    # TODO add I/O functions as needed

# 1. When program starts, read in the currently saved Inventory
DataProcessor.loadTable(FileProcessor.read_file(strFileName))

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled\n')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            DataProcessor.loadTable(FileProcessor.read_file(strFileName))
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        cdToInsert = IO.get_new_CD()

        # 3.3.2 Add item to the table
        DataProcessor.addCDToTable(cdToInsert)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        intIDDel = -1
        while True:
            strIDDel = input('Which ID would you like to delete? ').strip()
            try:
                intIDDel = int(strIDDel)
                break
            except ValueError as e:
                print(type(e), e, e.__doc__, sep='\n')
        # 3.5.2 search thru table and delete CD
        
        # TODO move processing code into function
        DataProcessor.removeCDFromTable(intIDDel)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)

        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 process clear table and start from scratch 
    elif strChoice == 'c':
        # 3.7.1 Clear table and ID checker
        DataProcessor.resetTable()
        continue  # start loop back at top.
    # 3.8 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




