import re
import file_utils as fu
import erc.erc_db_utils as erc_db
from global_data import erc_data


def insert_erc(model_id, fn):
    data = fu.load_file(fn, 'utf-8')
    erc_code_id = 0
    for d in data:
        if d[0] == 'Code':
            erc_code_id = get_erc_id(d[0], d[1])
            if erc_code_id < 1:
                erc_code_id = erc_db.insert_error_code(d[1])
                erc_data.append({
                    'id': erc_code_id,
                    'Code': d[1]
                })

        elif d[0] == 'Display':
            erc_code_display_id = get_erc_id(d[0], d[1])

            if erc_code_display_id < 1:
                erc_code_display_id = erc_db.update_code_display(erc_code_id, re.sub('\'', '`', d[1]))
                erc_data.append({
                    'id': erc_code_display_id,
                    'Code': d[1]
                })

        elif d[0] == 'Image':
            spr_image_id = get_erc_id(d[0], d[1])
            if spr_image_id < 1:
                spr_image_id = add_spr_data(d[0], 'spr_error_code_image', 'image', d[1])
            erc_db.update_code(erc_code_id, 'image_id', spr_image_id)

        elif d[0] == 'Description':
            spr_erc_code_id = get_erc_id(d[0], d[1])
            if spr_erc_code_id < 1:
                spr_erc_code_id = add_spr_data(d[0], 'spr_error_code', 'text', d[1])
            erc_db.update_code(erc_code_id, 'description_id', spr_erc_code_id)

        elif d[0] == 'Causes':
            spr_erc_code_id = get_erc_id(d[0], d[1])
            if spr_erc_code_id < 1:
                spr_erc_code_id = add_spr_data(d[0], 'spr_error_code', 'text', d[1])
            erc_db.update_code(erc_code_id, 'causes_id', spr_erc_code_id)

        elif d[0] == 'Remedy':
            spr_erc_code_id = get_erc_id(d[0], d[1])
            if spr_erc_code_id < 1:
                spr_erc_code_id = add_spr_data(d[0], 'spr_error_code', 'text', d[1])
            erc_db.update_code(erc_code_id, 'remedy_id', spr_erc_code_id)

        if erc_code_id > 0:
            erc_db.insert_link_model_error_code(model_id, erc_code_id)


def get_erc_id(name, value):
    result = 0
    for d in erc_data:
        try:
            if d[name] == value:
                result = d['id']
                break
        except:
            pass
    return result


def add_spr_data(caption, table, name, param):
    spr_erc_code_id = erc_db.insert_spr_error_code(table, name, re.sub('\'', '`', param))
    erc_data.append({
        'id': spr_erc_code_id,
        caption: param
    })
    return spr_erc_code_id
