import argparse
from dataclasses import field
from datetime import datetime, timedelta
import csv
from itertools import product
from operator import add
import os
import pandas as pd
import date_and_time
from rich.table import Table
from rich.console import Console


today = date_and_time.get_current_time()
bought_field_names = ["ID", "Product", "Quantity", "Bought_price", "Bought_date",
                      "Expiration", "InStock"]

# ___________________________________________
# Hier onder nieuwe code


def check_expired_products(x):
    for line in x:
        expiration_date = datetime.strptime(
            line["Expiration"], "%Y-%m-%d").date()

        if expiration_date < datetime.strptime(today, "%Y-%m-%d").date():
            line["InStock"] = "Expired"

    writer = csv.DictWriter(
        open('inventory.csv', 'w', newline=''), fieldnames=bought_field_names)
    writer.writeheader()
    for line in x:
        writer.writerow(line)
    return


def check_closest_expiration(product, x):
    expiration_date_list = []
    expiration_list = [line["Expiration"]
                       for line in x if product == line["Product"] and line['InStock'] == "True"]

    if len(expiration_list) == 0:
        return print(f"There are no {product}s in stock..")

    for date in expiration_list:
        expiration_date = datetime.strptime(
            date, "%Y-%m-%d").date()
        expiration_date_list.append(expiration_date)

    closest_date = min(expiration_date_list, key=lambda x: abs(
        x - datetime.strptime(today, "%Y-%m-%d").date()))
    print(closest_date)
    return closest_date


# print(check_expired_products(copy_bought_reader))
# print(check_closest_expiration("apple", copy_bought_reader))
