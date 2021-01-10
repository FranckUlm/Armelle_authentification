from getpass import *
import psycopg2
import os

os.chdir('D:/tests python/LoginsandPasswords_list_TaF')
# créer un objet en entrant le username et checker s'il est déjà utilisé dans la base de donnée"
# demander à ce nouvel utilsateur un code et réaliser l'authentification"


class Authentification():

    """Créer un username et un password avec certaines caractéristiques"""

    def __init__(self, u = "no_name", p = "123AZe", t = "no_table"):
        self.u = u
        self.p = p
        self.t = t

    def validate_username(self, u):
        """check la liste des identifiants déjà existants"""

        with open("UsernameforLogin.txt", "r") as user_list:
            read_if_user_exists = user_list.read()

        b = 0
        while b != 1:
            if u not in read_if_user_exists:
                print("Creation of a new profil.")
                with open("UsernameforLogin.txt", "a") as user_list:
                    user_list.write("{}, ".format(u))
                b = 1
            else:
                print("This username is already used.")
                print(read_if_user_exists)
                u = input("Choose another username : ")

    def validate_password(self, p):
        """Check la validité du mot de passe"""

        get_password = False
        while get_password != True:

            lower = False
            upper = False
            digit = False
            length = False

            for k in p:
                if k.islower():
                    lower = True
                if k.isupper():
                    upper = True
                if k.isdigit():
                    digit = True
                if len(p) == 6:
                    length = True

            # mistake = [lower, upper, digit, length]
            #print(mistake)

            valide = lower and upper and digit and length

            if valide:
                #A tester
                Pass = str(Password_choice)
                p = str(p)
                print("The password is good.")
                with open("PasswordforLogin.txt", "a") as user_list:
                    user_list.write("{},\n".format(p))
                    get_password = True
            else:
                print("The password is not correct.")
                # Check s'il y a au moins un caractère minuscule
                if lower == False:
                    print("You must at least use one lowercase character.")
                # Check s'il y a au moins un caractère majuscule
                if upper == False:
                    print("You must at least use one uppercase character.")
                # Check s'il y a au moins un chiffre
                if digit == False:
                    print("You must at least use one digit character.")
                # Check la longueur du mot de passe
                if len(self.p) != 6:
                    print("Password length is wrong.")
                p = getpass("Please, follow the instructions. Use at least 1 lowercase letter, 1 uppercase letter, 1 digit and only 6 characters. Password : ")  

    def UP_dict(self, Username, Password):
        dict = {}
        dict[Username] = Password[-8:-2]
        print("Voici vos informations personnelles : {}.".format(dict))

    def usernames_insertion(self, u, t):
        """Insertion of data into a database table"""

        print("Insertion of datas into {}".format(t))
        
        #PSQL command
        psql = (
            """
            INSERT INTO (%s) (usernames) 
                VALUES (%s) RETURNING id;
            """
        )

        connection = None
        id = None

        try:
            print("Connection to the table : {}".format(self.t))
            #Connection to the db server
            connection = psycopg2.connect(
                database ="",
                user ="postgres",
                password ="",
                host ="localhost",
                port ="5432",
            )

            print("Connection to {} established.".format(self.t))
            cur = connection.cursor()

            #Execute the statement
            cur.execute(psql, (self.t, self.u))
            print("PSQL statement executed.")

            #id = cursor.fetchone()[0]

            #Save the changings
            print("Changes saved.")
            connection.commit()

            #close de cursor
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                print("Connection closed.")
                connection.close()

        return id

    def passwords_insertion(self, p, t):
        """Insertion of data into a database table"""

        print("Insertion of datas into {}.".format(t))

        #PSQL command
        psql = (
            """
            INSERT INTO (%s) (passwords) 
                VALUES (%s) RETUNRING id;
            """
        )

        connection = None
        id = None

        try:
            #Connection to the db server
            connection = psycopg2.connect(
                database ="",
                user ="postgres",
                password ="",
                host ="localhost",
                port ="5432",
            )

            cur = connection.cursor()

            #Execute the statement
            cur.execute(psql, (self.t, self.p))
            print("PSQL statement executed.")

            #id = cursor.fetchone()[0]

            #Save the changings
            print("Changes saved.")
            connection.commit()

            #close de cursor
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                print("Connection closed.")
                connection.close()

        return id

Profil_creation = True

while Profil_creation:
    new_account = Authentification()

    #creation of the username
    Username_choice = input("Username : ")
    new_account.validate_username(Username_choice)

    #creation of the password
    Password_choice = getpass("Choose a password with at least 1 lowercase letter, 1 uppercase letter, 1 digit and only 6 characters, Password : ")
    new_account.validate_password(Password_choice)

    #creation of the tuple username, password in a dict :
    # to be FINISHED
    with open("PasswordforLogin.txt", "r") as user_list:
        read_if_user_exists = user_list.read()
    new_account.UP_dict(Username_choice, read_if_user_exists[0::])
    #le dict n'indique pas la valeur de la clé 
    #en entier et réécrit par dessus en supprimant le précédent identifiant.

    table = input("Which table would you like to update ? ")
    
    #reading of the username and the associated password
    with open("UsernameforLogin.txt", "r") as users_list:
        new_user = users_list.read()
    new_account.usernames_insertion(new_user, table)

    with open("PasswordforLogin.txt", "r") as passwords_list:
        associated_password = passwords_list.read()
    #insertion of the datas into the database
    new_account.passwords_insertion(associated_password, table)
    #To be resolved
