from datetime import datetime
import file_utils as fu
import parser_utils as pu
from spec import spec_parser
from erc import erc_parser


def main():
    data = fu.load_file('res/db_file_list.csv', 'utf-8')

    pu.insert_brands(data)
    pu.insert_models(data)
    pu.data_analysis(data)


def get_erc_id(data, name, value):
    for d in data:
        try:
            if d[name] == value:
                print(d['id'])
                break
        except:
            pass


if __name__ == '__main__':
    start_time = datetime.now()
    print(start_time)
    main()
    print(datetime.now() - start_time)
