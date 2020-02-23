#------------------------------------------#
# Title: CDInventory.py
# Desc: Starter Script for Assignment 05
# Change Log: (Who, When, What)
# RevA      DBiesinger, 2030-Jan-01, Created File
# RevB      SMcElmurry, 2020Feb22,  Expand on starter code by changing the inner list to a dictionary type, and
#                                   adding failure mode checks on user input types. Also added redundancy checks
#                                   to attempt to limit duplicate entries in list.
#------------------------------------------#

# DECLARE VARIABLES
# General
strChoice = '' # User input
lstTbl = []  # list of dicts to hold data
dictRow = {}  # dictionary of data row
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object
loadData = False # tracks if data has been loaded

# Get user Input
print('The Magic CD Inventory\n')
while True:
    # 1. Display menu allowing the user to choose:
    print('[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
    print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit')
    strChoice = input('l, a, i, d, s or x: ').lower()  # convert choice to lower case at time of input
    print()

    if strChoice == 'x':
        # 5. Exit the program if the user chooses so
        break
    # LOAD DATA FROM FILE
    if strChoice == 'l':
        # Avoid clashing ID's and album/artist pairings when loading
        if len(lstTbl) != 0 or loadData:
            overLoad = input("Loading data will overwrite current inventory. Continue? (y/n) ")
            while overLoad != "y" and overLoad != "n":
                input("Please type 'y' or 'n'. Continue? (y/n) ")
            if overLoad == "y":
                loadData = True
                lstTbl = []
                objFile = open(strFileName, 'r')
                for lines in objFile:
                    preAdd = lines.strip("\n").split(",")
                    newRow = {"ID":int(preAdd[0]), "cdTitle":preAdd[1], "artistName":preAdd[2]}
                    lstTbl.append(newRow)
                objFile.close()
        # If there is no current table, load with no overwrite option
        else:
            loadData = True
            objFile = open(strFileName, 'r')
            for lines in objFile:
                preAdd = lines.strip("\n").split(",")
                newRow = {"ID":int(preAdd[0]), "cdTitle":preAdd[1], "artistName":preAdd[2]}
                lstTbl.append(newRow)
            objFile.close()
        print()
    # ADD A CD
    elif strChoice == "a":
        # Variables for redundancy check
        duplicateCheck = False
        intID = ""
        toRemove = None
        duplicateCheck = False
        overwriteOption = ""
        # Ensure an integer ID is being passed
        while type(intID) != int:
            strID = input("Enter an ID number: ")
            try:
                intID = int(strID)
            except:
                print("Please enter a valid ID number")
        strTitle = input('Enter the CD\'s Title: ')
        strArtist = input('Enter the Artist\'s Name: ')
        dictRow = {"ID":intID, "cdTitle":strTitle, "artistName":strArtist}
        # Redundancy checks against current entries
        for entryRow in lstTbl:
            # Check for ID number, code may overwrite entry (at end) if no other duplicates are found
            if entryRow["ID"] == intID:
                overwriteOption = input("ID " + strID + " exists already. Overwrite? (y/n) ")
                while overwriteOption != "y" and overwriteOption != "n":
                    overwriteOption = input("I'm sorry, please enter 'y' or 'n'. Overwrite(y/n)? ")
                if overwriteOption == "y":
                    toRemove = entryRow
            # Check if title/artist exists, break if it does and tell program not to append later
            elif entryRow["cdTitle"] == strTitle and entryRow["artistName"] == strArtist:
                print("The album " + strTitle + " by " + strArtist + " already exists under ID " + str(entryRow["ID"]) + ".")
                duplicateCheck = True
                break
        # Actions based on redundancy checks
        if duplicateCheck:
            pass
        elif overwriteOption == "":
            lstTbl.append(dictRow)
        elif toRemove != None:
            lstTbl[lstTbl.index(toRemove)] = dictRow
        print()
    # VIEW INVENTORY
    elif strChoice == 'i':
        print('ID, CD Title, Artist')
        for row in lstTbl:
            print(*row.values(), sep = ', ')
        print()
    # DELETE ENTRY
    elif strChoice == 'd':
        if len(lstTbl) > 0:
            delChoice = ""
            # Present IDs to users to choose from
            idList = []
            for row in lstTbl:
                idList.append(str(row["ID"]))
            print("Available ID's are: ")
            print(*idList, sep = ", ")
            while delChoice not in idList:
                delChoice = input("Select a valid ID to delete: ")
            for entry in lstTbl:
                if entry["ID"] == int(delChoice):
                    tableIndex = lstTbl.index(entry)
            # Display full entry to be deleted
            print("Deleting the entry: ", end = "")
            print(*lstTbl[tableIndex].values(), end = "")
            if input("Press 'y' to confirm. ") == "y":
                lstTbl.pop(tableIndex)
                print("Entry deleted. \n")
            else:
                print("Deletion not confirmed, please try again. \n")
        else:
            print("There are no entries to delete. \n")
    # SAVE THE DATA
    elif strChoice == "s":
        # Checks if user was editing a loaded file, or just adding to one
        if loadData:
            objFile = open(strFileName, "w")
        else:
            objFile = open(strFileName, "a")
        for row in lstTbl:
            strRow = ''
            for item in row.values():
                strRow += str(item) + ","
            strRow = strRow[:-1] + "\n"
            objFile.write(strRow)
        objFile.close()
    # TRY AGAIN (FOR USER INPUT)
    else:
        print('Please choose either l, a, i, d, s or x!')

