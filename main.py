import datetime
import json


def showMenu():
    print('''Press 
        1 - to create a note
        2 - to save the note
        3 - to delete the note
        4 - to edit the note
        5 - to show the list of the notes
        6 - to show the note
        any other button - to exit''')

def choiceInput(notes):
    yourChoice = input('Your choice is ')
    if yourChoice == "1":
        print("to create a note")
        createNote()
    elif yourChoice == "2":
        print("to save a note")
        saveNote(notes)
    elif yourChoice == "3":
        print("to delete a note")
        deleteNote()
    elif yourChoice == "4":
        print("to edit a note")
        editNote()
    elif yourChoice == "5":
        print("to show the list of the notes")
        showNotesFromMenu()
    elif yourChoice == "6":
        print("to show the note")
        showOneNote()
    else:
        print("to exit")
        return False

def readNoteFile():
    with open('noteFile.json', 'r') as file:
        content = file.read()
        notes = json.loads(content)
    return notes


def createNote():
    notes = readNoteFile()
    noteHeader = input('Enter the header of your note: ')
    noteText = input('Enter the text of your note: ')
    noteCreationDate = datetime.datetime.now().strftime("%Y.%m.%d %H:%M");
    notes[len(notes)+1] = [noteCreationDate, noteHeader, noteText]
    saveRequest = input("Do you want to save the note? (press \"y\" to save, press any other button to show menu): ")
    if saveRequest == "y":
        saveNote(notes)
        showMenu()
        choiceInput(notes)
    else:
        showMenu()
        choiceInput(notes)


def saveNote(notes):
    with open('noteFile.json', 'w') as file:
        content = json.dumps(notes)
        file.write(content)
        print("Your note file has been saved successfully")


def createNewFile(notes):
    with open('noteFile.json', 'w') as file:
        content = json.dumps(notes)
        file.write(content)



def showOneNote():
    notes = readNoteFile()
    noteID = input("Enter the note ID of the note you want to show ")
    if noteID in notes.keys():
        print(f"Note ID: {noteID}. \n   Note date: {notes[noteID][0]} \n   Note header: {notes[noteID][1].upper()} \n   Note text: {notes[noteID][2]}")
    else:
        print("There is no note with such note ID in notes")
    showMenu()
    choiceInput(notes)

def showNotesFromMenu():
    notes = readNoteFile()
    filterRequest = input("Would you like to filter notes by date?  (press \"y\" to filter, press any other button to show menu) ")
    if filterRequest == "y": dateFilter()
    elif filterRequest == "n":
        if len(notes) != 0:
            for k,v in notes.items():
                print(f"Note ID: {k}. \n   Note date: {v[0]} \n   Note header: {v[1].upper()} \n   Note text: {v[2]}")
        else:
            print("There is no any note")
        showMenu()
        choiceInput(notes)

def showNotes():
    notes = readNoteFile()
    for k,v in notes.items():
        print(f"Note ID: {k}. \n   Note date: {v[0]} \n   Note header: {v[1].upper()} \n   Note text: {v[2]}")
    return notes

def deleteNote():
    print("What note do you want to delete?")
    notes = showNotes()
    noteID = input("Enter note number ")
    notes.pop(noteID)
    saveNote(notes)
    print("The note deleted successfully")
    showMenu()
    choiceInput(notes)

def editNote():
    notes = readNoteFile()
    print("What note do you want to edit?")
    showNotes()
    noteID = input("Enter note number ")
    notes[int(noteID)][0] = datetime.datetime.now().strftime("%Y.%m.%d %H:%M");
    notes[int(noteID)][1] = input("Enter new header of the note: ")
    notes[int(noteID)][2] = input("Enter new text of the note: ")
    saveRequest = input("Do you want to save the note? (press \"y\" to save): ")
    if saveRequest == "y": saveNote(notes)
    else:
        showMenu()
        choiceInput(notes)


def dateFilter():
    a = True
    while a:
        try:
            date_1 = input("Enter the left border of the date interval in format YYYY.MM.DD HH:MM ---> ")
            day_x = datetime.datetime.strptime(date_1, '%Y.%m.%d %H:%M')
            a = False
        except:
            print("Wrong date input. Try it again ")
    a = True
    while a:
        try:
            date_2 = input("Enter the right border of the date interval in format YYYY.MM.DD HH:MM ---> ")
            day_y = datetime.datetime.strptime(date_2, '%Y.%m.%d %H:%M')
            a = False
        except:
            print("Wrong date input. Try it again ")
    notes = readNoteFile()
    counter = 0
    for k, v in notes.items():
        day_i = datetime.datetime.strptime(v[0], '%Y.%m.%d %H:%M')

        if day_i > day_x and day_i < day_y:
            print(f"Note ID: {k}. \n   Note date: {v[0]} \n   Note header: {v[1].upper()} \n   Note text: {v[2]}")
            counter += 1
    if counter == 0: print("There is no any note in chosen interval")
    showMenu()
    choiceInput(notes)

def main(choice):
    try:
        notes = readNoteFile()
    except:
        notes = {}
        createNewFile(notes)
    while choice:
        showMenu()
        choice = choiceInput(notes)

main(True)
