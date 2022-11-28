# Imports
import argparse
from dataclasses import field
from datetime import date, datetime, timedelta
import csv
from itertools import product
from operator import add
import os
import pandas as pd
import date_and_time
from datumchecker import check_expired_products, check_closest_expiration
from rich.table import Table
from rich.console import Console

# start commandline tool
parser = argparse.ArgumentParser(
    prog="SuperPy", description="Inventory System")
subparser = parser.add_subparsers(dest="command")

parser.add_argument('-advance_time', type=int,
                    help='advance time by typing int')
parser.add_argument('-today',
                    help='set time')

# command to add bought products
buy = subparser.add_parser('buy')
buy.add_argument('-product_name', type=str, help='product name')
buy.add_argument('-price', type=int,
                 help='price must by interger or float')
buy.add_argument('-quantity', type=int, help='amound of the bougt product')
buy.add_argument('-expiration', type=str,
                 help='date in yyyy-mm-dd, when product is expired')

# command to sell products
sell = subparser.add_parser('sell')
sell.add_argument('-product_name', type=str, help='product name')
sell.add_argument('-price', type=int,
                  help='price must by interger or float')
sell.add_argument('-quantity', type=int,
                  help='quantity must by interger')

# command to get reports
report_bought = subparser.add_parser('report_bought')
report_sold = subparser.add_parser('report_sold')

report_inventory = subparser.add_parser('report_inventory')
report_revenue = subparser.add_parser('report_revenue')
report_revenue.add_argument('-start_date', type=str,
                            help='date in yyyy-mm-dd', required=True)
report_revenue.add_argument('-end_date', type=str, help='date in yyyy-mm-dd')

report_profit = subparser.add_parser('report_profit')
report_profit.add_argument('-start_date', type=str,
                           help='date in yyyy-mm-dd', required=True)
report_profit.add_argument('-end_date', type=str, help='date in yyyy-mm-dd')

args = parser.parse_args()
# print(args)

####################################################
# algemene code/gegevens
CSV_PATH = os.path.join(os.getcwd(), os.path.basename('inventory.csv'))
inventory_file_exists = os.path.isfile(CSV_PATH)

CSV_PATH = os.path.join(os.getcwd(), os.path.basename('bought.csv'))
bought_file_exists = os.path.isfile(CSV_PATH)

CSV_SELL_PATH = os.path.join(os.getcwd(), os.path.basename("sold.csv"))
sell_file_exists = os.path.isfile(CSV_SELL_PATH)

CSV_UNIQUE_ID_PATH = os.path.join(
    os.getcwd(), os.path.basename("unique_id.csv"))
unique_id_file_exists = os.path.isfile(CSV_UNIQUE_ID_PATH)

CSV_BOUGHT_TOTAL_PATH = os.path.join(
    os.getcwd(), os.path.basename("bought_total.csv"))
bought_total_exists = os.path.isfile(CSV_BOUGHT_TOTAL_PATH)


sold_field_names = ["ID", "Product", "Quantity", "Sold_price", "Sold_date",
                    "Expiration"]
bought_field_names = ["ID", "Product", "Quantity", "Bought_price", "Bought_date",
                      "Expiration", "InStock"]
unique_id_fieldnames = ['ID', "Product"]
bought_total_fieldnames = ['ID', 'Product',
                           'Quantity', 'InStock']

today = date_and_time.get_current_time()

# algemene code/formules


def open_read_bought():
    with open('bought.csv', 'r', newline="") as output:
        csv_reader = csv.DictReader(output)
        copy_bought_reader = [line for line in csv_reader]
        return copy_bought_reader


def open_read_sold():
    with open('sold.csv', 'r', newline="") as output:
        csv_reader = csv.DictReader(output)
        copy_sold_reader = [line for line in csv_reader]
        return copy_sold_reader


def bought_writer(x):
    writer = csv.DictWriter(
        open('bought.csv', 'w', newline=''), fieldnames=bought_field_names)  # update bought file
    writer.writeheader()
    for line in x:
        writer.writerow(line)


def unique_id():
    if unique_id_file_exists:
        with open('unique_id.csv', 'a+') as write_object:
            df = pd.read_csv('unique_id.csv')
           # print(df)
            name_list = list(df["Product"])
            print(name_list)
            writer = csv.DictWriter(
                write_object, fieldnames=unique_id_fieldnames)
            if args.product_name in name_list:
                product_id = df.loc[df['Product'] ==
                                    args.product_name, "ID"].iloc[0]
                print(f'{product_id} belongs to {args.product_name}')
                return product_id
            else:
                # Zoekt de laatste waarde van de unique ID's
                product_id = df['ID'].iat[-1]
                new_id = product_id + 1
                writer.writerow({"ID": new_id, 'Product': args.product_name})
                print(f'new id for {args.product_name} is {new_id}')
                return new_id
    else:
        with open('unique_id.csv', 'a+', newline="") as write_object:
            df = csv.DictWriter(write_object, fieldnames=unique_id_fieldnames)
            df.writeheader()
            df.writerow({"ID": 1, 'Product': args.product_name})
            new_id = 1
            print(new_id)
        return new_id

# Functies voor het bij houden van in en verkopen


def new_bought_product():
    product_id = unique_id()

    with open('inventory.csv', 'a+', newline="") as write_object:
        csv_writer = csv.DictWriter(
            write_object, fieldnames=bought_field_names)

        if not inventory_file_exists:
            csv_writer.writeheader()
            csv_writer.writerow(
                {"ID": product_id, 'Product': args.product_name, 'Quantity': args.quantity, 'Bought_price': args.price, "Bought_date": today, 'Expiration': args.expiration, 'InStock': True})
            print("inventory.csv file is created")
            print(f"{args.product_name} is added to inventory.csv")
        elif inventory_file_exists:
            csv_writer.writerow(
                {"ID": product_id, 'Product': args.product_name, 'Quantity': args.quantity, 'Bought_price': args.price, "Bought_date": today, 'Expiration': args.expiration, 'InStock': True})
            print(f"{args.product_name} is added to the inventory.csv")

    with open('bought.csv', 'a+', newline="") as write_object:
        csv_writer = csv.DictWriter(
            write_object, fieldnames=bought_field_names)

        if not bought_file_exists:
            csv_writer.writeheader()
            csv_writer.writerow(
                {"ID": product_id, 'Product': args.product_name, 'Quantity': args.quantity, 'Bought_price': args.price, "Bought_date": today, 'Expiration': args.expiration, 'InStock': True})
            print("bought.csv file is created")
            print(f"{args.product_name} is added to bought.csv")
        elif bought_file_exists:
            csv_writer.writerow(
                {"ID": product_id, 'Product': args.product_name, 'Quantity': args.quantity, 'Bought_price': args.price, "Bought_date": today, 'Expiration': args.expiration, 'InStock': True})
            print(f"{args.product_name} is added to the bought.csv")

    # ['ID', 'Product', 'Quantity', 'InStock']
    with open('bought_total.csv', 'a+', newline="") as write_object:

        csv_writer = csv.DictWriter(
            write_object, fieldnames=bought_total_fieldnames)
        if not bought_total_exists:
            csv_writer.writeheader()
            csv_writer.writerow({"ID": product_id, "Product": args.product_name,
                                "Quantity": args.quantity, "InStock": True})
            print("bought_total.csv is created")
            return
        elif bought_total_exists:
            df = pd.read_csv("bought_total.csv")
            # check if product ID already exists, when it exists, update quantity
            if product_id in df['ID'].values:
                old_quantity = df.loc[df.ID ==
                                      product_id, 'Quantity'].values[0]
                new_quantity = old_quantity + args.quantity
                df.loc[df.ID == product_id, 'Quantity'] = new_quantity
                df.to_csv('bought_total.csv', index=False)
                print(
                    f'quantity of {args.product_name} updated from {old_quantity} to {new_quantity}')
                return
            else:
                csv_writer.writerow({"ID": product_id, "Product": args.product_name,
                                     "Quantity": args.quantity, "InStock": True})
                print(f"{args.product_name} is added to the total_bought.csv")
                return


def sell_product():
    product_id = unique_id()
    copy_bought_reader = open_read_bought()
    # Checks all the expiration dates and updates the inventory
    check_expired_products(copy_bought_reader)
    # Gets the expiration date thats closest to today
    closest_expiration_date = check_closest_expiration(
        args.product_name, copy_bought_reader)
    with open('sold.csv', 'a+', newline="") as write_object:
        csv_writer = csv.DictWriter(
            write_object, fieldnames=sold_field_names)
        if bought_file_exists:
            for line in copy_bought_reader:
                if args.product_name == line["Product"] and line["InStock"] == "True" and line["Expiration"] == str(closest_expiration_date):
                    quant = int(line['Quantity'])
                    print(f"quantity of {args.product_name} is {quant}")
                    if quant == args.quantity:
                        new_quantity = 0
                    # Update quantity.
                        line['Quantity'] = new_quantity
                        line['InStock'] = False
                        bought_writer(copy_bought_reader)
                        print(
                            f'quantity of {args.product_name} updated from {quant} to {new_quantity}')
                        if sell_file_exists:
                            csv_writer.writerow({"ID": product_id, "Product": args.product_name,
                                                 "Quantity": args.quantity, "Sold_price": args.price, "Sold_date": today, "Expiration": closest_expiration_date})
                            print(
                                f"{args.product_name} is added to the sold.csv")
                            return
                        elif not sell_file_exists:
                            csv_writer.writeheader()
                            csv_writer.writerow({"ID": product_id, "Product": args.product_name,
                                                 "Quantity": args.quantity, "Sold_price": args.price, "Sold_date": today, "Expiration": closest_expiration_date})
                            print("sold.csv is created")
                            print(
                                f"{args.product_name} is added to the sold.csv")
                            return
                        break
                    elif quant > args.quantity:
                        new_quantity = quant - args.quantity
                    # Update quantity
                        line['Quantity'] = new_quantity
                        bought_writer(copy_bought_reader)

                        print(
                            f'quantity of {args.product_name} updated from {quant} to {new_quantity}')
                        if sell_file_exists:
                            csv_writer.writerow({"ID": product_id, "Product": args.product_name,
                                                "Quantity": args.quantity, "Sold_price": args.price, "Sold_date": today, "Expiration": closest_expiration_date})
                            print(
                                f"{args.product_name} is added to the sold.csv")

                        elif not sell_file_exists:
                            csv_writer.writeheader()
                            csv_writer.writerow({"ID": product_id, "Product": args.product_name,
                                                "Quantity": args.quantity, "Sold_price": args.price, "Sold_date": today, "Expiration": closest_expiration_date})
                            print("sold.csv is created")
                            print(
                                f"{args.product_name} is added to the sold.csv")
                        break
                    else:
                        print(
                            f"There are only {quant} {args.product_name}s in stock..")
                        return

        else:
            print(f"Something went wrong")
            return


# get reports functions


def view_bought_csvfile():
    table = Table(title='Bought total list')
    with open('bought_total.csv', 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        itercsvreader = iter(csvreader)
        for i in next(itercsvreader):
            table.add_column(i, style='cyan')
        for row in itercsvreader:
            table.add_row(row[0], row[1], row[2],
                          row[3])
        console = Console()
        console.print(table)


def view_sold_csvfile():
    table = Table(title='Sold list')
    with open('sold.csv', 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        itercsvreader = iter(csvreader)
        for i in next(itercsvreader):
            table.add_column(i, style='cyan')
        for row in itercsvreader:
            table.add_row(row[0], row[1], row[2], row[3], row[4], row[5])
        console = Console()
        console.print(table)


def view_inventory_csvfile():
    # Current inventory products table
    copy_bought_reader = open_read_bought()
    check_expired_products(copy_bought_reader)
    table = Table(title='Inventory')
    with open('inventory.csv', 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        itercsvreader = iter(csvreader)
        for i in next(itercsvreader):
            table.add_column(i, style='cyan')
        for row in itercsvreader:
            if row[6] == "True":
                table.add_row(row[0], row[1], row[2],
                              row[3], row[4], row[5], row[6])
        console = Console()
        console.print(table)
    # Expired products table
    table = Table(title='Expired products')
    with open('inventory.csv', 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        itercsvreader = iter(csvreader)
        for i in next(itercsvreader):
            table.add_column(i, style='cyan')
        for row in itercsvreader:
            if row[6] == "Expired":
                table.add_row(row[0], row[1], row[2],
                              row[3], row[4], row[5], row[6])
        console = Console()
        console.print(table)

    # Out of stock products table
    table = Table(title='Out of stock')
    with open('inventory.csv', 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        itercsvreader = iter(csvreader)
        for i in next(itercsvreader):
            table.add_column(i, style='cyan')
        for row in itercsvreader:
            if row[6] == "False":
                table.add_row(row[0], row[1], row[2],
                              row[3], row[4], row[5], row[6])
        console = Console()
        console.print(table)


def report_revenue_view():
    total_revenue_list = []
    if args.end_date is None:
        if args.start_date == 'today':
            startdate = today
        elif args.start_date == 'yesterday':
            startdate = datetime.strptime(
                today, "%Y-%m-%d").date() - timedelta(days=1)
        else:
            startdate = datetime.strptime(args.start_date, "%Y-%m-%d").date()
        with open('sold.csv', 'r') as file:
            csvreader = csv.reader(file, delimiter=',')
            itercsvreader = iter(csvreader)
            for row in itercsvreader:
                if row[4] == str(startdate):
                    revenue = int(row[3]) * int(row[2])
                    total_revenue_list.append(revenue)
            total_revenue = sum(total_revenue_list)
            console = Console()
            console.print(f"Revenue on {args.start_date} is {total_revenue} ")
            return
    else:
        if args.start_date == 'today':
            startdate = today
        elif args.start_date == 'yesterday':
            startdate = datetime.strptime(
                today, "%Y-%m-%d").date() - timedelta(days=1)
        else:
            startdate = datetime.strptime(args.start_date, "%Y-%m-%d").date()
        enddate = datetime.strptime(
            args.end_date, "%Y-%m-%d").date()
        while startdate <= enddate:
            delta = timedelta(days=1)
            with open('sold.csv', 'r') as file:
                csvreader = csv.reader(file, delimiter=',')
                itercsvreader = iter(csvreader)
                for row in itercsvreader:
                    if row[4] == str(startdate):
                        revenue = int(row[3]) * int(row[2])
                        total_revenue_list.append(revenue)
            startdate += delta
            total_revenue = sum(total_revenue_list)
        console = Console()
        console.print(
            f"Revenue between {args.start_date} and {args.end_date} is {total_revenue} ")
        return


def report_profit_view():
    total_revenue_list = []
    total_costs_list = []
    if args.end_date is None:
        if args.start_date == 'today':
            startdate = today
        elif args.start_date == 'yesterday':
            startdate = datetime.strptime(
                today, "%Y-%m-%d").date() - timedelta(days=1)
        else:
            startdate = datetime.strptime(args.start_date, "%Y-%m-%d").date()
        with open('sold.csv', 'r') as file:
            csvreader = csv.reader(file, delimiter=',')
            itercsvreader = iter(csvreader)
            for row in itercsvreader:
                if row[4] == str(startdate):
                    revenue = int(row[3]) * int(row[2])
                    total_revenue_list.append(revenue)
            total_revenue = sum(total_revenue_list)

        with open('bought.csv', 'r') as file:
            csvreaderbought = csv.reader(file, delimiter=',')
            itercsvreaderbought = iter(csvreaderbought)
            for row in itercsvreaderbought:
                if row[4] == str(startdate):
                    costs = int(row[3]) * int(row[2])
                    total_costs_list.append(costs)
            total_costs = sum(total_costs_list)
        profit = total_revenue - total_costs
        console = Console()
        console.print(f"Profit over {args.start_date} is {profit} ")
        return
    else:
        if args.start_date == 'today':
            startdate = today
        elif args.start_date == 'yesterday':
            startdate = datetime.strptime(
                today, "%Y-%m-%d").date() - timedelta(days=1)
        else:
            startdate = datetime.strptime(args.start_date, "%Y-%m-%d").date()
        enddate = datetime.strptime(
            args.end_date, "%Y-%m-%d").date()
        while startdate <= enddate:
            delta = timedelta(days=1)
            with open('sold.csv', 'r') as file:
                csvreader = csv.reader(file, delimiter=',')
                itercsvreader = iter(csvreader)
                for row in itercsvreader:
                    if row[4] == str(startdate):
                        revenue = int(row[3]) * int(row[2])
                        total_revenue_list.append(revenue)
            total_revenue = sum(total_revenue_list)

            with open('bought.csv', 'r') as file:
                csvreaderbought = csv.reader(file, delimiter=',')
                itercsvreaderbought = iter(csvreaderbought)
                for row in itercsvreaderbought:
                    if row[4] == str(startdate):
                        costs = int(row[3]) * int(row[2])
                        total_costs_list.append(costs)
                total_costs = sum(total_costs_list)
                startdate += delta
            profit = total_revenue - total_costs
        console = Console()
        console.print(
            f"Profit between {args.start_date} and {args.end_date} is {profit} ")
        return


if args.command == 'buy':
    new_bought_product()
elif args.command == 'sell':
    sell_product()
elif args.command == 'report_bought':
    view_bought_csvfile()
elif args.command == 'report_sold':
    view_sold_csvfile()
elif args.command == 'report_inventory':
    view_inventory_csvfile()
elif args.command == 'report_revenue':
    report_revenue_view()
elif args.command == 'report_profit':
    report_profit_view()
elif args.command == None:
    if args.advance_time is not None:
        date_and_time.change_time(args.advance_time)
