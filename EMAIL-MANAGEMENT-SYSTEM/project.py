#importing library needed to run program
import time
import pickle
import os
import re

#Main menu messages stored in a varaible for easy access
main_menu_message = ('\n Mailing List Manager '
                     '\n --------- '
                     '\n\t (A)dd a new account '
                     '\n\t (L)ist existing accounts '
                     '\n\t (C)hange email address '
                     '\n\t (D)elete an account '
                     '\n\t (E)xport to CSV '
                     '\n\t (Q)uit')

#Class of User
class User(object):
    def __init__(self,name,email):
        self.name = name
        self.email = email
        self.created = time.strftime("%A, %C. %B %Y %I:%M%p")
        self.updated = time.strftime("%A, %C. %B %Y %I:%M%p")

#to validte email and return valid email
def emailvalid(email):
     while not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
         email = input("Enter an email address : ")
     if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
         return 'none'
     else:
         return email
def namevalid(name):
    while not name:
        name = input("Enter a name : ")
    return name

#to load data from file & accept input from user
def load_func():
    with open('data.txt', 'rb') as f:
        user_list = pickle.load(f)

    name = namevalid(input('Enter a name : ').title())

    email = emailvalid(input("Enter an email address : ").lower())
    #creating User object instance
    people = [User(name, email)]
    #looping through object and storing data in dict
    for p in people:
        data = dict([
            ("name", p.name),
            ("email", p.email),
            ("created", p.created),
            ("updated", p.updated)
        ])
        #Appending this dict to a list
        user_list.append(data.copy())
    #Dumping the updated list to a file
    with open('data.txt', 'wb') as f:
        pickle.dump(user_list, f)
    print('{} at {} has been recorded'.format(name,email))
    main_menu()

#function add new account
def add_new_action():
    #checking weather file exit of not
    if(os.path.isfile('data.txt')):
        load_func()
    #if no file exit , we are creating a new list and opening file and dump empty list to file
    else:
        user_list = []
        with open('data.txt', 'wb') as f:
            pickle.dump(user_list, f)
        load_func()

#function displaying all accounts
def list_accounts():
    with open('data.txt', 'rb') as f:
        user_list = pickle.load(f)
    if not user_list:
        print("No records found")
        main_menu()
    for index,x in enumerate(user_list):
        print('\n{}. {}: {} \n \n Created :  {} \n \n Updated : {}'.format(index+1,
                                              x['name'],
                                              x['email'],
                                              x['created'],
                                              x['updated']))
    main_menu()

#function to changing email address
def change_email():
    with open('data.txt', 'rb') as f:
        user_list = pickle.load(f)
    if not user_list:
        print("No records found")
        main_menu()
    userInputID = input("\nEnter record ID : ")
    try:
        userInputID = int(userInputID)
    except ValueError:
        change_email()
    uID = userInputID - 1
    #checking weather record avaliable or not
    try:
        data = user_list[uID]
    except IndexError:
        print('There are no records with the ID {} '.format(userInputID))
        main_menu()
    user_list[uID]['email'] = emailvalid(input("Enter an email address : ").lower())
    user_list[uID]['updated'] = time.strftime("%A, %C. %B %Y %I:%M%p")
    with open('data.txt', 'wb') as f:
        pickle.dump(user_list, f)
    print('{} at {} has been updated'.format(user_list[uID]['name'], user_list[uID]['email']))
    main_menu()


#function deleting an account
def delete_account():
    with open('data.txt', 'rb') as f:
        user_list = pickle.load(f)
    if not user_list:
        print("No records found")
        main_menu()
    userInputID = input("\nEnter record ID to delete: ")
    try:
        userInputID = int(userInputID)
    except ValueError:
        delete_account()
    uID = userInputID - 1
    try:
        data = user_list[uID]
    except IndexError:
        print('There are no records with the ID {} '.format(userInputID))
        main_menu()
    print('You are about to delete {} : {}'.format(user_list[uID]['name'],user_list[uID]['email']))
    choice = input('Do you wish to delete record? (Y/N) :')
    if choice == 'Y' or choice == 'y':
        del user_list[uID]
    elif choice == 'N' or choice =='n':
        main_menu()
    else:
        delete_account()
    with open('data.txt', 'wb') as f:
        pickle.dump(user_list, f)
    print("Record Deleted")
    main_menu()

#fucntion exporting to csv file
def export_csv():
    with open('data.txt', 'rb') as f:
        user_list = pickle.load(f)
    if not user_list:
        print("No records found")
        main_menu()
    import csv
    csvfile = "accounts.csv"
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(('ID', 'Name', 'Email','Created','Updated'))
        for index,x in enumerate(user_list):
            writer.writerow((index+1, x['name'], x['email'], x['created'], x['updated']))
    print('Accounts saved as accounts.csv')
    main_menu()

#this runs first - The Menu
def main_menu():
    print(main_menu_message)
    first_choice = input('Your Choice : ')
    #loading the previous data from text file to a list


    # checking weather the input is string or not
    # if its string then its given to mainmenu or
    # if its number > record is printed on screen
    try:
        first_choice = int(first_choice)
        with open('data.txt', 'rb') as f:
            user_list = pickle.load(f)
        try:

            first_choice = first_choice - 1
            data = user_list[first_choice]
            print('\n{}. {}: {} \n \n Created :  {} \n \n Updated : {}'.format(first_choice + 1,
                                                                               user_list[first_choice]['name'],
                                                                               user_list[first_choice]['email'],
                                                                               user_list[first_choice]['created'],
                                                                               user_list[first_choice]['updated']))
        except IndexError:
            print('There are no records with the ID {} '.format(first_choice + 1))
            main_menu()
        main_menu()
    except ValueError:
        if first_choice == 'A' or first_choice == 'a':
            add_new_action()
        elif first_choice == 'L' or first_choice == 'l':
            list_accounts()
        elif first_choice == 'C' or first_choice == 'c':
            change_email()
        elif first_choice == 'D' or first_choice == 'd':
            delete_account()
        elif first_choice == 'E' or first_choice == 'e':
            export_csv()
        elif first_choice == 'Q' or first_choice == 'q':
            print('Thank You')
            exit()
        else:
            main_menu()

#Program Starts here by calling initial screen
main_menu()



