1. The function check_closest_expiration

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

This function checks if the product is in the inventory and then which products are the closest to the expiration date. So when this product is bought, it sells the one closest to the expiration date. Therefore there are less wasted products!



2. The function unique_id

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

This function makes sure every product has an unique ID, so it is easier to grap an item based on the id. If we enter a product is searches for the ID it belongs to and if it is a new product it will make a new unique ID.

3. General check if the csv files exists

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

These lines of code make it easy the refere back to, so it is easy to check if the files already exists or that the should be made.
When the file has to be made, it is important to make a header row. When the files exists it is only necessary to add a new row.


4. Gereral expirience
This excersise in general was a difficult but challenging excersise. It was fun to do, but it took me a while. Lot of hours at work en lots to do at home, made that I had little time to work on this excersise. With as result, that is was difficult to get in the flow (forgetting where you were, what you did, how the lines you wrote worked). 

I most likely am missing something to make a passing grade, but I think I made it work and i love to hear about what is should change or add to my files!

PS

Should I be writing these reports in English or is Dutcch fine aswell?