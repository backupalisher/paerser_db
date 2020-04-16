from db import db
import re
import file_utils as fu
from spec import spec_db_utils as sdbu
from global_data import spr_details_options_data, detail_options_data


def insert_options(model_id, detail_id, fn):
    caption_parent_id = 0
    sub_caption_parent_id = 0
    spr_option_name_id = 0
    spr_option_value_id = 0
    detail_option_id = 0

    data = fu.load_file(fn, 'Windows-1251')
    for d in data:
        if d:
            name = d[0]
            value = re.sub(r'(\smm+$)|(\sмм+$)|(\sстр+$)|(\sстр/мин$)|(\sкг$)|'
                           r'(\sВт$)|(\sлистов$)|(\sгг$)|(\sс$)|(\sсек$)|(\')', '', d[1])
            if name == 'main_image' or name == 'image':
                if name == 'main_image':
                    db.i_request(f'UPDATE models SET main_image = \'{value}\' WHERE id = {model_id}')
                else:
                    db.i_request(f'UPDATE models SET image = concat( s.image || \'{value}\'  || \';\') '
                                 f'FROM (SELECT image FROM models WHERE id = {model_id}) s WHERE models.id = {model_id}')
            else:
                if name != 'Model':
                    spr_option_name_id = set_convert({k for k, v in spr_details_options_data if v == name})
                    if spr_option_name_id < 1:
                        spr_option_name_id = sdbu.insert_spr_detail_options(name)
                        spr_details_options_data.append((spr_option_name_id, name))

                    spr_option_value_id = set_convert({k for k, v in spr_details_options_data if v == value})
                    if spr_option_value_id < 1:
                        spr_option_value_id = sdbu.insert_spr_detail_options(value)
                        spr_details_options_data.append((spr_option_value_id, value))

            if (name == 'Caption') | (name == 'Status'):
                caption_parent_id = search_detail_options_data(spr_option_name_id, spr_option_value_id)
                if caption_parent_id < 1:
                    caption_parent_id = sdbu.insert_detail_options(spr_option_name_id, spr_option_value_id, 'Null')
                    detail_options_data.append([caption_parent_id, spr_option_name_id, spr_option_value_id])
                sdbu.link_detail_options(detail_id, caption_parent_id)

            elif name == 'SubCaption':
                sub_caption_parent_id = search_detail_options_data(spr_option_name_id, spr_option_value_id)
                if sub_caption_parent_id < 1:
                    sub_caption_parent_id = sdbu.insert_detail_options(spr_option_name_id, spr_option_value_id, caption_parent_id)
                    detail_options_data.append([sub_caption_parent_id, spr_option_name_id, spr_option_value_id])
                sdbu.link_detail_options(detail_id, sub_caption_parent_id)

            elif name == 'EndSubCaption':
                sub_caption_parent_id = 0
            else:
                if sub_caption_parent_id > 0:
                    detail_option_id = sdbu.insert_detail_options(spr_option_name_id, spr_option_value_id, sub_caption_parent_id)
                else:
                    detail_option_id = sdbu.insert_detail_options(spr_option_name_id, spr_option_value_id, caption_parent_id)

            if detail_option_id > 0 and detail_id > 0:
                sdbu.link_detail_options(detail_id, detail_option_id)


def set_convert(s):
    if len(s) < 1:
        v = 0
    else:
        v = list(s)[0]
    return v


def search_detail_options_data(spr_option_name_id, spr_option_value_id):
    result = 0
    for item in detail_options_data:
        if item[1] == spr_option_name_id:
            if item[2] == spr_option_value_id:
                result = item[0]
                break

    return result
