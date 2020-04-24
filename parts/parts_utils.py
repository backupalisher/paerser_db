import re
import file_utils as fu
from parts import parts_db_utils
from global_data import parts_data


def insert_parts(model_id, fn):
    data = fu.load_file(fn, 'utf-8')
    for d in data:
        module_id = 0
        pc_id = 0
        pn_id = 0
        try:
            print(f'\rpart code: {d[0]} - {d[1]}', end='')
        except:
            pass
        if d[0]:
            module_id = get_id('module', d[0])
            if module_id < 1:
                module_id = parts_db_utils.insert_spr_modules(re.sub('\'', '`', d[0]))
                parts_data.append({
                    'id': module_id,
                    'module': d[0]
                })

        if d[1]:
            pc_id = get_id('pc', d[1])
            if pc_id < 1:
                pc_id = parts_db_utils.insert_partcodes(re.sub('\'', '`', d[1]))
                parts_data.append({
                    'id': pc_id,
                    'pc': d[1]
                })

        if d[2]:
            pn_id = get_id('pn', d[2])
            if pn_id < 1:
                pn_id = parts_db_utils.insert_spr_details(re.sub('\'', '`', d[2]))
                parts_data.append({
                    'id': pn_id,
                    'pn': d[2]
                })

        if d[3]:
            parts_db_utils.update_partcode_desc(pc_id, re.sub('\'', '`', d[3]))

        if d[4]:
            img_id = get_id('img', d[4])
            if img_id < 1:
                img_id = parts_db_utils.insert_spr_module_image(d[4])
                parts_data.append({
                    'id': img_id,
                    'img': d[3]
                })
            parts_db_utils.link_model_module_image(model_id, module_id, img_id)

        parts_db_utils.link_part_model_module_spr(pc_id, model_id, module_id, pn_id)
    print()


def get_id(name, value):
    result = 0
    for d in parts_data:
        try:
            if d[name] == value:
                result = d['id']
                break
        except:
            pass
    return result
