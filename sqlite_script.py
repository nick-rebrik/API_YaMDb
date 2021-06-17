import argparse
import csv
import sqlite3
import traceback
import sys
import re
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', help='Path to database')
    parser.add_argument('--csv', help='Path to csv file')
    parser.add_argument('--table', help='SQL Table name')
    args = parser.parse_args()    
    connection = sqlite3.connect(args.db)
    cursor = connection.cursor()    
    with open(args.csv, encoding='utf-8') as file:
        line = 0
        for row in csv.reader(file, quotechar='"', delimiter=',',
                    skipinitialspace=True):
            line += 1
            if line == 1:
                values = '?'
                headers = (', '.join(row))
                for value in range(1, len(row)):
                    values += ', ?'
            insert_records = (
                'INSERT INTO {table} ({headers}) VALUES ({values})'
            ).format(table=args.table, headers=headers, values=values)
            if line != 1:
                try:
                    if '"' in row[0]:
                        new = re.split(r",(?!\s)", row[0])
                        print(new)
                        cursor.execute(insert_records, new)
                except sqlite3.IntegrityError as err1:
                    raise 
                    FORMAT = (
                        '\033[1;31m' + 'Похоже на то, что в строках с этим pk '
                        'какие-то данные уже есть.' + '\033[0m' + '\nОшибка:'
                    )
                    print(FORMAT, err1)
                    
                except sqlite3.OperationalError as err2:
                    raise err2
                    FORMAT = (
                        '\033[1;31m' + 'Похоже на то, что что-то '
                        'не так с названиями или количеством столбцов '
                        'в CSV или DB.' + '\033[0m' + '\nОшибка:'
                    )
                    print(FORMAT, err2)
                 
    connection.commit()    
    print(
        'В таблицу {table} базы данных {db} записаны следующие строки:'.format(
            table=args.table,
            db=args.db
        )
    )
    select_all = 'SELECT * FROM {table}'.format(table=args.table)
    for line in cursor.execute(select_all).fetchall():
        print('\033[32m' + 'Записана строка: ' + '\033[0m', line)    
    connection.close()