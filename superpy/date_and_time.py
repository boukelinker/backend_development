from datetime import datetime, timedelta


def get_current_time():
    current_datetime = datetime.now()
    #print("current date & time: ", current_datetime.strftime('%Y-%m-%d'))

    file_name = "current_datetime.txt"
    file = open(file_name, 'w')
    date_time = str(current_datetime.strftime('%Y-%m-%d'))
    file.write(date_time)
    #print("file created: ", file_name)
    file.close()
    return date_time

# get_current_time()


def change_time(timechanger):
    file_name = "current_datetime.txt"
    file = open(file_name, 'r')
    date = datetime.strptime(file.read(), '%Y-%m-%d')
    print('old date: '+str(date.strftime('%Y-%m-%d')))
    new_date = date + timedelta(days=timechanger)
    print('new date: ' + str(new_date.strftime('%Y-%m-%d')))
    file.close()
    file = open(file_name, 'w')
    file.write(str(new_date.strftime('%Y-%m-%d')))
    file.close()

# change_time(-2)
