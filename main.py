import datetime
import json


def showMenu(): # функция для вывода на экран меню
    print('''Press 
        1 - to create a note
        2 - to save the note
        3 - to delete the note
        4 - to edit the note
        5 - to show the list of the notes
        6 - to show the note
        any other button - to exit''')

def choiceInput(notes): # функция для навигации по меню
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

def readNoteFile(): # функция для чтения Json File, хранящего заметки
    with open('noteFile.json', 'r') as file:
        content = file.read()
        notes = json.loads(content)
    return notes


def createNote(): # функция для создания заметки
    notes = readNoteFile() #считываем из json filе, текс уже имеющихся заметок
    noteHeader = input('Enter the header of your note: ') # ввод заголовка заметки
    noteText = input('Enter the text of your note: ') # ввод текста заметки
    noteCreationDate = datetime.datetime.now().strftime("%Y.%m.%d %H:%M") #определение времени создания заметки
    notes[len(notes)+1] = [noteCreationDate, noteHeader, noteText] # вносим заметку в словарь, ключом выступает порядковый номер заметки
    saveRequest = input("Do you want to save the note? (press \"y\" to save, press any other button to show menu): ") # спрашиваем у пользователя необходиомсть сохранения созданной заметки
    if saveRequest == "y":
        saveNote(notes) # вызываем функцию, которая запишет заметку в json file
        showMenu() # показываем меню
        choiceInput(notes) # пользователь осуществляет выбор
    else: # если пользователь не хочет сохранять заметку, то перенаправляем его в меню
        showMenu()
        choiceInput(notes)


def saveNote(notes): # функция для сохранения созданной заметки в json file
    with open('noteFile.json', 'w') as file:
        content = json.dumps(notes)
        file.write(content)
        print("Your note file has been saved successfully")


def createNewFile(notes): # функция для создания пустого json file
    with open('noteFile.json', 'w') as file:
        content = json.dumps(notes)
        file.write(content)



def showOneNote(): # функция для вывода одной заметки по ID заметки
    notes = readNoteFile() # считываем json file, хранящий заметки
    noteID = input("Enter the note ID of the note you want to show ") #запрашиваем у пользователя ID интересующей заметки
    if noteID in notes.keys(): #если такой ID существует, то выводим заметку
        print(f"Note ID: {noteID}. \n   Note date: {notes[noteID][0]} \n   Note header: {notes[noteID][1].upper()} \n   Note text: {notes[noteID][2]}")
    else:#если не существует, уведомляем пользователя
        print("There is no note with such note ID in notes")
    showMenu()# показываем меню
    choiceInput(notes)# пользователь осуществляет выбор

def showNotesFromMenu(): #функция для вывода заметок с опцией применения фильтра по дате
    notes = readNoteFile()# считываем json file, хранящий заметки
    filterRequest = input("Would you like to filter notes by date?  (press \"y\" to filter, press any other button to show menu) ") #спрашиваем пользователя о необходимости применения фильтра по дате
    if filterRequest == "y": dateFilter() # если пользователь хочет применить фильтр, то вызываем соответствующую функцию
    elif filterRequest == "n": #если нет, то выводим список всех заметок, при условии, что они существуют
        if len(notes) != 0:
            for k,v in notes.items():
                print(f"Note ID: {k}. \n   Note date: {v[0]} \n   Note header: {v[1].upper()} \n   Note text: {v[2]}")
        else:
            print("There is no any note")
        showMenu()# показываем меню
        choiceInput(notes)# пользователь осуществляет выбор

def showNotes(): #функция, выводящая все заметки без опции вывода с применением фильтра по дате
    notes = readNoteFile()# считываем json file, хранящий заметки
    for k, v in notes.items(): #выводим заметки
        print(f"Note ID: {k}. \n   Note date: {v[0]} \n   Note header: {v[1].upper()} \n   Note text: {v[2]}")
    return notes

def deleteNote(): #функция, позволяющая удалить заметку
    print("What note do you want to delete?")
    notes = showNotes() #выодим заметки для выбора удаляемой заметки
    noteID = input("Enter note number ") # запришваем ID заметки для удаления
    notes.pop(noteID) #удаляем выбранную заметку
    saveNote(notes) #сохраняем полученный словарь в json file
    print("The note deleted successfully")
    showMenu() # показываем меню
    choiceInput(notes)# пользователь осуществляет выбор

def editNote():#функция для редактирования заметки
    notes = readNoteFile()# считываем json file, хранящий заметки
    print("What note do you want to edit?")
    showNotes()#выодим заметки для выбора удаляемой заметки
    noteID = input("Enter note number ")# запришваем ID заметки для удаления
    notes[int(noteID)][0] = datetime.datetime.now().strftime("%Y.%m.%d %H:%M")# через ключ словаря обращаемся к дате
    notes[int(noteID)][1] = input("Enter new header of the note: ")# через ключ словаря обращаемся к заголовку
    notes[int(noteID)][2] = input("Enter new text of the note: ")# через ключ словаря обращаемся к тексту
    saveRequest = input("Do you want to save the note? (press \"y\" to save): ")
    if saveRequest == "y": saveNote(notes)
    else:
        showMenu() # показываем меню
        choiceInput(notes)# пользователь осуществляет выбор


def dateFilter(): #функция, позволяющая осуществить фильтрацию по дате
    a = True
    """ запускаем беконечный цикл для определения начальной даты фильтрации, 
    условие выхода из которого: ввод даты пользователем в требуемом формате """
    while a:
        try:
            date_1 = input("Enter the left border of the date interval in format YYYY.MM.DD HH:MM ---> ") # пользователь вводить дату и время в указанном формате
            day_x = datetime.datetime.strptime(date_1, '%Y.%m.%d %H:%M') # переводим в машиночитаемый формат даты
            a = False # если пользователь ввел дату в необходимом формате, возвращаем False и выходим из цикла
        except:
            print("Wrong date input. Try it again ") #если дата введена некорректно, возвращаемся к блоку try снова
    a = True
    """ запускаем беконечный цикл для определения конечной даты фильтрации, 
    условие выхода из которого: ввод даты пользователем в требуемом формате """
    while a:
        try:
            date_2 = input("Enter the right border of the date interval in format YYYY.MM.DD HH:MM ---> ")
            day_y = datetime.datetime.strptime(date_2, '%Y.%m.%d %H:%M')
            a = False
        except:
            print("Wrong date input. Try it again ")
    notes = readNoteFile() # считываем json file, хранящий заметки
    counter = 0 # счетчик, позволяющий впоследствии определить, количество заметок в требуемом интервале
    for k, v in notes.items():
        day_i = datetime.datetime.strptime(v[0], '%Y.%m.%d %H:%M') # считываем дату заметки

        if day_i > day_x and day_i < day_y: #порверяем входит ли дата заметки в интересующий нас интервал
            print(f"Note ID: {k}. \n   Note date: {v[0]} \n   Note header: {v[1].upper()} \n   Note text: {v[2]}")
            counter += 1
    if counter == 0: print("There is no any note in chosen interval") #если заметок в интервале нет, уведомляем
    showMenu()# показываем меню
    choiceInput(notes)# пользователь осуществляет выбор

def main(choice):
    try:
        notes = readNoteFile() # пытаемся считать json file
    #если json file отсутствует, то создаем пустой словарь, на основе которого создаем первичный json file
    except:
        notes = {}
        createNewFile(notes)
    while choice: #запускаем бесконечный цикл, условие выхода из которого choice == False
        showMenu()
        choice = choiceInput(notes)

main(True)
