import csv
import shutil
from tempfile import NamedTemporaryFile
import datetime


filename = 'data.csv'


def read_data(user_id=None, email=None):
    with open(filename, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        unknown_user_id = None
        unknown_email = None
        for row in reader:
            if user_id is not None:
                if int(user_id) == int(row.get('id')):
                    return row
                else:
                    unknown_user_id = user_id
            if email is not None:
                if email == row.get('email'):
                    return row
                else:
                    unknown_email = email
        if unknown_user_id is not None:
            return 'User id {user_id} not found'.format(user_id=user_id)
        if unknown_email is not None:
            return 'Email {email} not found'.format(email=email)


def get_length(file_path):
    with open(file_path) as csv_file:
        reader = csv.reader(csv_file)
        reader_list = list(reader)
        return len(reader_list)


def append_data(file_path, name, email, amount):
    field_names = ['id', 'name', 'email', 'amount', 'sent', 'date']
    next_id = get_length(file_path)
    with open(file_path, 'a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        if next_id == 0:
            writer.writeheader()
            next_id += 1
        writer.writerow({
            'id': next_id,
            'name': name,
            'email': email,
            'amount': amount,
            'sent': False,
            'date': datetime.datetime.now()
        })


def edit_data(edit_id=None, email=None, amount=None, sent=None):
    temp_file = NamedTemporaryFile(mode='w', delete=False)

    with open(filename, newline='') as csv_file, temp_file:
        reader = csv.DictReader(csv_file)
        field_names = ['id', 'name', 'email', 'amount', 'sent', 'date']
        writer = csv.DictWriter(temp_file, fieldnames=field_names)
        writer.writeheader()
        for row in reader:
            if edit_id is not None:
                if int(row['id']) == int(edit_id):
                    row['amount'] = amount
                    row['sent'] = sent
            elif email is not None and edit_id is None:
                if row['email'] == str(email):
                    row['amount'] = amount
                    row['sent'] = sent
            else:
                pass
            writer.writerow(row)
    shutil.move(temp_file.name, filename)


def delete_data(edit_id=None, email=None):
    temp_file = NamedTemporaryFile(mode='w', delete=False)

    with open(filename) as csv_file, temp_file:
        reader = csv.DictReader(csv_file)
        field_names = ['id', 'name', 'email', 'amount', 'sent']
        writer = csv.DictWriter(temp_file, fieldnames=field_names)
        writer.writeheader()
        for row in reader:
            if edit_id is not None:
                if int(row['id']) != int(edit_id):
                    writer.writerow(row)
            elif email is not None and edit_id is None:
                if row['email'] != str(email):
                    writer.writerow(row)
            else:
                pass
    shutil.move(temp_file.name, filename)


if __name__ == '__main__':
    filename = 'D:\pyCharm Projects\Python Email\data.csv'
    append_data(filename, 'alice', 'otherGmail@gmail.com', 1)
    append_data(filename, 'bob', 'otherGmail@gmail.com', 5)
    append_data(filename, 'cat', 'otherGmail@gmail.com', 1)
    append_data(filename, 'dog', 'otherGmail@gmail.com', 2)
