import mysql.connector
import tabulate
import getpass

def login():
    # This function is for establishing connection
    # between python and mysql database by taking
    # input of user id and password and host name
    # then it take the input of database from the
    # user and if the database exits it will select
    # it for further queries else it will create one
    # and use it.
    try:
        global app_cursor
        global connection

        connection = mysql.connector.connect(user=input('Username: '),
                                             password=str(getpass.getpass("Password: ")), 
                                             host=input('Host: '))
        app_cursor = connection.cursor(buffered=True)
        app_cursor.execute("show databases")
        app_database = input('Database: ')
        database_selected = False

        for i in app_cursor.fetchall():

            for j in i:

                if app_database == j:
                    app_cursor.execute("use %s" % app_database)
                    print('\n', app_database, " is now the selected database.", '\n')
                    database_selected = True
                    break

        if database_selected is False:
            app_cursor.execute("create database %s" % app_database)
            app_cursor.execute("use %s" % app_database)
            print('\n', app_database, " is now the selected database.", '\n')
            # FROM HERE DATABASE FORMATION STARTS ------------------------------------------------------------------
            connection.commit()
            app_cursor.execute("create table customer(cust_id int, f_name varchar(255), s_name varchar(255), address varchar(255), city varchar(255), contact_no bigint, constraint customer_pk primary key (cust_id))")
            insertdata1 = "insert into customer(cust_id, f_name, s_name, address, city, contact_no) values(%s,%s,%s,%s,%s,%s)"

            records1 = [
                (1000,"Akshit","Bhandari","Pushp Vihar","New Delhi",8384521234),
                (1001,"Aditya","Talwar","Thapaar","Ludhiana",8384456712),
                (1002,"Sam","Marcy","Khanpur","New Delhi",7592810283),
                (1003,"Tripti","Kriti","SNU","Greater Noida",9482719203),
                (1004,"Onkar","Jha","Deoli","New Delhi",6281938264),
                (1005,"Soubhagya","Kukreja","Lajpat Nagar","New Delhi",8231801927),
                (1006,"Siddhant","Yadav","Saket","New Delhi",8383816844),
                (1007,"Manav","Mittal","South Ex","New Delhi",7482981723),
                (1008,"Ram Kumar","Goyal","Sungroor","Patiala",8391027321)
            ]
            app_cursor.executemany(insertdata1, records1)

            app_cursor.execute("create table items(item_id int, name varchar(255),quantity int, price int, supplier_id int, supplier_name varchar(255), constraint items_pk primary key (item_id))")
            insertdata2 = "insert into items(item_id, name, quantity, price, supplier_id, supplier_name) values(%s,%s,%s,%s,%s,%s)"
            records2 = [
                (23469,"Combiflam",35,30,3000,"DR Distributers Pvt Ltd"),
                (23470,"Pantosec DSR",40,100,3000,"DR Distributers Pvt Ltd"),
                (23471,"iJal",12,18,3003,"Anand Pharmaceuticals"),
                (23472,"Dairy Milk Silk",7,180,3004,"Cadbury India Ltd"),
                (23473,"Maybelline Eyeliner",4,200,3001,"Lucky Pharma"),
                (23474,"Vaseline Jelly",12,5,3001,"Lucky Pharma"),
                (23475,"Asthakind DS",25,80,3000,"DR Distributers Pvt Ltd"),
                (23476,"Azax", 500,40,124,3003,"Anand Pharmaceuticals"),
                (23477,"Vicks",20,94,3001,"Lucky Pharma"),
                (23478,"Kinder Joy",3,55,3002,"Nestle India Pvt Ltd"),
                (23479,"Meftal Spas",30,60,3000,"DR Distributers Pvt Ltd")
            ]

            app_cursor.executemany(insertdata2,records2)

            app_cursor.execute("create table ledger(invoice_no int, amount int, cust_id int, cust_fname varchar(255), pending_remarks varchar(255), constraint ledger_pk primary key (invoice_no))")
            insertdata3 = "insert into items(invoice_no, amount, cust_id, cust_fname, pending_remarks) values(%s,%s,%s,%s,%s)"
            records3 = [
                (13400,341,1002,"Sam","NULL"),
                (13401,12,1004,"Onkar","NULL"),
                (13402,721,1005,"Soubhagya","Online payment declined. Try again."),
                (13403,1032,1001,"Aditya","NULL"),
                (13404,523,1004,"Onkar","Not Delivered Yet."),
                (13405,4182,1007,"Manav","NULL"),
                (13406,132,1003,"Tripti","NULL"),
                (13407,13982,1006,"Siddhant","50% Amount paid in advance.")
            ]

            app_cursor.executemany(insertdata3,records3)

            app_cursor.execute("create table supplier(supplier_id int, name varchar(255), contact_no bigint, address varchar(255), city varchar(255), balance int, constraint supplier_pk primary key (supplier_id))")
            insertdata4 = "insert into items(supplier_id, name, contact_no, address, city, balance) values(%s,%s,%s,%s,%s,%s)"
            records4 = [
                (3000,"DR Distributers Pvt Ltd",8492018372,"Okhla Industrial Area","New Delhi",-18913),
                (3001,"Lucky Pharma",9102872312,"Jamia Milia Area","New Delhi",-912),
                (3002,"Nestle India Pvt Ltd",7282193021,"Hisar","Hisar",1213),
                (3003,"Anand Pharmaceuticals",9128391238,"Anupam Apartments","New Delhi","NULL"),
                (3004,"Cadbury India Ltd",8729102837,"Navi Mumbai","Mumbai",7812)
            ]

            app_cursor.executemany(insertdata4,records4)
            connection.commit()
            # TILL HERE DATABASE FORMATION ---------------------------------------------------------
        table_menu()

    except mysql.connector.errors.ProgrammingError:

        print("\nEnter valid Username and Password!!\n")
        login()

    except mysql.connector.errors.InterfaceError:
        print("\nEnter valid Host name.\n")
        login()

    except mysql.connector.errors.DatabaseError:
        print("\nSomething went wrong try again.\n")
        login()


def table_menu():
    # This function gives the user the menu for running
    # desired queries by entering the corresponding number

    print('''\n\n-----------------------------------------------------------------------------------
    To perform given queries enter the numerical value\nassigned to them:-\n
    1 => Get details of payments that are pending.
    2 => Get details of items that are about to exhaust.
    3 => Check which supplier has credit pending.
    4 => Find customer.
    5 => Get list of items supplied by a particular supplier.
    6 => Logging out of database.
    
Note:- To terminate any operation you selected by 
       mistake (queries 4 & 5 only) enter '?' symbol it will take you back
       to the menu.

    ''')

    try:

        def table_menu_functions(a):
            if a == 1:
                # This set of code will be executed when user wants to 
                # know about pending_remarks in ledger table that are NOT NULL
                try:
                    app_cursor.execute('''SELECT *
                        FROM ledger
                        WHERE pending_remarks IS NOT NULL''')
                    
                    b = app_cursor.fetchall()
                    for row in b:
                        print(row)
                    connection.commit()
                    table_menu()
                except mysql.connector.errors.ProgrammingError:
                    print("Error in database.")
                    table_menu()

            elif a == 2:
                # choice 2 is to select items which are extinguishing fast.
                # ie, items with quantity <= 5
                
                try:
                    app_cursor.execute('''SELECT *
                        FROM items
                        WHERE quantity <= 5''')

                    b = app_cursor.fetchall()
                    for row in b:
                        print(row)

                    connection.commit()
                    table_menu()
                except mysql.connector.errors.ProgrammingError:
                    print("Error in database\n.")
                    table_menu()
            elif a == 3:
                # This is for choice 3 viz. to find suppliers which are to be
                # paid. ie, the business is in debt of these suppliers.
                # we can find this by checking for balance < 0
                try:
                    app_cursor.execute('''SELECT *
                        FROM supplier
                        WHERE balance < 0''')

                    b = app_cursor.fetchall()
                    for row in b:
                        print(row)

                    connection.commit()
                    table_menu()
                except mysql.connector.errors.ProgrammingError:
                    print("Error in database\n.")
                    table_menu()
            elif a == 4:
                # This set of code is run to get all the info about a particular
                # customer.
                cust_id = str(input("Enter Customer ID of desired customer: "))
                try:
                    app_cursor.execute('''SELECT *
                        FROM customer
                        WHERE cust_id = %s''' % cust_id)
                    
                    b = app_cursor.fetchone()
                    for row in b:
                        print(row)

                    connection.commit()
                    table_menu()
                except mysql.connector.errors.ProgrammingError:
                    print("Error in database\n.")
                    table_menu()
            elif a == 5:
                # This set of code is run to get a list of items supplied
                # by a particular supplier. All the items are arranged in
                # increasing order of their quantities.
                supp_id = str(input("Enter Supplier ID of desired Supplier: "))
                try:
                    app_cursor.execute('''SELECT *
                        FROM items
                        WHERE supplier_id = %s
                        ORDER BY quantity''' % supp_id)
                    
                    b = app_cursor.fetchall()
                    for row in b:
                        print(row)

                    connection.commit()
                    table_menu()
                except mysql.connector.errors.ProgrammingError:
                    print("Error in database\n.")
                    table_menu()
            elif a == 6:
                # This set of code is choice 6 that is Save and exit application.
                # Its saves all the query processed and closes the connection and cursor.
                # After that it leave a vague input statement to prevent to sudden close of console window.
                import sys
                connection.commit()
                app_cursor.close()
                connection.close()
                input("Press any key to exit..")
                sys.exit()
            else:
                # If users enter anything other than listed in menu then this code will be executed.
                # It again asks for the input from the user.
                print("Enter Number from The menu only.")
                choice = int(input("Your Choice: "))
                table_menu_functions(choice)
        table_menu_choice = int(input("Your Choice: "))
        table_menu_functions(table_menu_choice)

    except ValueError:
        # If user enter anything other than integer.
        print("Enter valid input.")
        table_menu()


login()
