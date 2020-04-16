from datetime import datetime
import file_utils as fu
import parser_utils as pu


def main():
    data = fu.load_file('res/db_file_list.csv', 'utf-8')

    pu.insert_brands(data)
    pu.insert_models(data)
    pu.data_analysis(data)


if __name__ == '__main__':
    start_time = datetime.now()
    print(start_time)
    main()
    print(datetime.now() - start_time)
