#include <iostream>
#include <conio.h>
#include <windows.h>
#include <mysql.h>
#include <sstream>
#include <string>

using namespace std;

int main()
{
    MYSQL *con;

    // for connecting to the database
    string host, username, password, database;
    cout << "Username: ";
    cin >> username;
    cout << "Password: ";
    cin >> password;
    cout << "Host: ";
    cin >> host;
    cout << "Database: ";
    cin >> database;

    con = mysql_init(0);
    con = mysql_real_connect(con, host, username, password, database, 0, NULL, 0);

    if (con)
    {
        cout << " " << database << " is now the selected database.\n";
        //        FOR CREATING THE DATABASE ------------------------------------------------------------------------------------------
        //        mysql_query(con,"create table customer(cust_id int, f_name varchar(255), s_name varchar(255), address varchar(255), city varchar(255), contact_no bigint)");

        //        mysql_query(con,"insert into customer(cust_id, f_name, s_name, address, city, contact_no) values (1000,"Akshit","Bhandari","Pushp Vihar","New Delhi",8384521234), (1001,"Aditya","Talwar","Thapaar","Ludhiana",8384456712), (1002,"Sam","Marcy","Khanpur","New Delhi",7592810283),(1003,"Tripti","Kriti","SNU","Greater Noida",9482719203),(1004,"Onkar","Jha","Deoli","New Delhi",6281938264),(1005,"Soubhagya","Kukreja","Lajpat Nagar","New Delhi",8231801927),(1006,"Siddhant","Yadav","Saket","New Delhi",8383816844),(1007,"Manav","Mittal","South Ex","New Delhi",7482981723),(1008,"Ram Kumar","Goyal","Sungroor","Patiala",8391027321)");
        //

        //        mysql_query(con,"create table items(item_id int, name varchar(255),quantity int, price int, supplier_id int, supplier_name varchar(255), constraint items_pk primary key (item_id))");

        //        mysql_query(con,"insert into items(item_id, name, quantity, price, supplier_id, supplier_name) values (23469,"Combiflam",35,30,3000,"DR Distributers Pvt Ltd"),(23470,"Pantosec DSR",40,100,3000,"DR Distributers Pvt Ltd"),(23471,"iJal",12,18,3003,"Anand Pharmaceuticals"),(23472,"Dairy Milk Silk",7,180,3004,"Cadbury India Ltd"),(23473,"Maybelline Eyeliner",4,200,3001,"Lucky Pharma"),(23474,"Vaseline Jelly",12,5,3001,"Lucky Pharma"),(23475,"Asthakind DS",25,80,3000,"DR Distributers Pvt Ltd"),(23476,"Azax", 500,40,124,3003,"Anand Pharmaceuticals"),(23477,"Vicks",20,94,3001,"Lucky Pharma"),(23478,"Kinder Joy",3,55,3002,"Nestle India Pvt Ltd"),(23479,"Meftal Spas",30,60,3000,"DR Distributers Pvt Ltd")");

        //        mysql_query(con,"create table ledger(invoice_no int, amount int, cust_id int, cust_fname varchar(255), pending_remarks varchar(255), constraint ledger_pk primary key (invoice_no))");

        //        mysql_query(con,"insert into items(invoice_no, amount, cust_id, cust_fname, pending_remarks) values (13400,341,1002,"Sam","NULL"),(13401,12,1004,"Onkar","NULL"),(13402,721,1005,"Soubhagya","Online payment declined. Try again."),(13403,1032,1001,"Aditya","NULL"),(13404,523,1004,"Onkar","Not Delivered Yet."),(13405,4182,1007,"Manav","NULL"),(13406,132,1003,"Tripti","NULL"),(13407,13982,1006,"Siddhant","50% Amount paid in advance.")");

        //        mysql_query(con,"create table supplier(supplier_id int, name varchar(255), contact_no bigint, address varchar(255), city varchar(255), balance int, constraint supplier_pk primary key (supplier_id))");

        //        mysql_query(con,"insert into items(supplier_id, name, contact_no, address, city, balance) values (3000,"DR Distributers Pvt Ltd",8492018372,"Okhla Industrial Area","New Delhi",-18913),(3001,"Lucky Pharma",9102872312,"Jamia Milia Area","New Delhi",-912),(3002,"Nestle India Pvt Ltd",7282193021,"Hisar","Hisar",1213),(3003,"Anand Pharmaceuticals",9128391238,"Anupam Apartments","New Delhi","NULL"),(3004,"Cadbury India Ltd",8729102837,"Navi Mumbai","Mumbai",7812)");

        // CREATING DATABASE FINISHED ---------------------------------------------------------------

        int choice = 0;
        std::cout << "\n\n---------------------------------------------------------------------\nTo perform given queries enter the numerical value\nassigned to them:-\n\n1 => Get details of payments that are pending.\n2 => Get details of items that are about to exhaust.\n3 => Check which supplier has credit pending.\n4 => Find customer.\n5 => Get list of items supplied by a particular supplier.\n6 => Logging out of database.\n\nNote:- To terminate any operation you selected by mistake (queries 4 & 5 only) enter '?' symbol, it'll take you back to this menu.\n\n";

        // Taking input and prompting the user repeatedly until the user selects a
        // no from the given choice.
        while (choice < 1 || choice > 6)
        {
            std::cout << "Your Choice: ";
            std::cin >> choice;
        }

        while (choice != 6)
        {
            switch (choice)
            {
            // This set of code will be executed when user wants to
            // know about pending_remarks in ledger table that are NOT NULL
            case 1:
            {
                mysql_query(con, "SELECT * FROM ledger WHERE pending_remarks IS NOT NULL");
                MYSQL_RES *res = mysql_use_result(con);
                MYSQL_FIELD *fields = mysql_fetch_fields(res);

                cout << endl;

                MYSQL_ROW row;
                while ((row = mysql_fetch_row(res)) != NULL)
                {

                    for (int i = 0; i < 5; i++)
                    {
                        cout << row[i] << "\t\t";
                    }
                    cout << endl;
                }
                mysql_free_result(res);
                break;
            }

                // choice 2 is to select items which are extinguishing fast.
                // ie, items with quantity <= 5

            case 2:
            {
                mysql_query(con, "SELECT * FROM items WHERE quantity <= 5");
                MYSQL_RES *res = mysql_use_result(con);
                MYSQL_FIELD *fields = mysql_fetch_fields(res);

                cout << endl;

                MYSQL_ROW row;
                while ((row = mysql_fetch_row(res)) != NULL)
                {

                    for (int i = 0; i < 6; i++)
                    {
                        cout << row[i] << "\t\t";
                    }
                    cout << endl;
                }
                mysql_free_result(res);
                break;
            }

                // This is for choice 3 viz. to find suppliers which are to be
                // paid. ie, the business is in debt of these suppliers.
                // we can find this by checking for balance < 0

            case 3:
            {
                mysql_query(con, "SELECT * FROM supplier WHERE balance < 0");
                MYSQL_RES *res = mysql_use_result(con);
                MYSQL_FIELD *fields = mysql_fetch_fields(res);

                cout << endl;

                MYSQL_ROW row;
                while ((row = mysql_fetch_row(res)) != NULL)
                {

                    for (int i = 0; i < 6; i++)
                    {
                        cout << row[i] << "\t\t";
                    }
                    cout << endl;
                }
                mysql_free_result(res);
                break;
            }

                // This set of code is run to get all the info about a particular
                // customer.

            case 4:
            {
                string cust_id;
                std::cout << "Enter Customer ID of desired customer: ";
                std::cin >> cust_id;
                mysql_query(con, "SELECT * FROM customer WHERE cust_id = %s", (cust_id));
                MYSQL_RES *res = mysql_use_result(con);
                MYSQL_FIELD *fields = mysql_fetch_fields(res);

                cout << endl;

                MYSQL_ROW row;
                while ((row = mysql_fetch_row(res)) != NULL)
                {

                    for (int i = 0; i < 6; i++)
                    {
                        cout << row[i] << "\t\t";
                    }
                    cout << endl;
                }
                mysql_free_result(res);
                break;
            }

                // This set of code is run to get a list of items supplied
                // by a particular supplier. All the items are arranged in
                // increasing order of their quantities.

            case 5:
            {
                string supp_id;
                std::cout << "Enter Supplier ID of desired supplier: ";
                std::cin >> supp_id;
                mysql_query(con, "SELECT * FROM customer WHERE cust_id = %s", (supp_id));
                MYSQL_RES *res = mysql_use_result(con);
                MYSQL_FIELD *fields = mysql_fetch_fields(res);

                cout << endl;

                MYSQL_ROW row;
                while ((row = mysql_fetch_row(res)) != NULL)
                {

                    for (int i = 0; i < 6; i++)
                    {
                        cout << row[i] << "\t\t";
                    }
                    cout << endl;
                }
                mysql_free_result(res);
                break;
            }

            // This set of code is choice 6 that is Save and exit application.
            // Its saves all the query processed and closes the connection and cursor.
            // After that it leave a vague input statement to prevent to sudden close of console window.
            case 6:
            {
                cout << "Press any key to exit...\n";
                getchar();
                return 0;
            }
            }
        }
    }
    else
        cout << "connection failed" << endl;

    return 0;
}