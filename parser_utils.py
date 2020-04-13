from db import db_utils
from global_data import g_data
from erc import erc_parser
from spec import spec_parser, spec_db_utils as sdbu
from parts import parts_utils
import file_utils as fu


def insert_brands(data):
    for d in data:
        brand = d[0]
        db_utils.insert_brand(brand)


def insert_models(data):
    old_brand = ''
    brand_id = 0
    for models in data:
        brand = models[0]
        model = models[1]
        print(model)
        if brand != old_brand:
            brand_id = sdbu.get_id('brands', 'name', brand)[0][0]
            old_brand = brand

        # добавляем model в таблицу models
        model_id = db_utils.insert_model(model, brand_id)

        # добовляем model в таблицу spr_details
        spr_details_id = db_utils.insert_spr_details(model)

        # линкуем model и spr_details в таблице link_models_spr_details
        details_id = sdbu.link_models_spr_details(model_id, spr_details_id)

        g_data.append({
            brand: brand_id,
            model: model_id,
            'partcode_id': None,
            'module': None,
            'spr_details_id': spr_details_id,
            'details_id': details_id,
        })

    fu.save_process(g_data)


def data_analysis(data):
    for d in data:
        model = d[1]
        print(model)

        model_id = 0
        details_id = 0
        for key in g_data:
            if model in key.keys():
                model_id = key[model]
                details_id = key['details_id']
                break

        if d[2]:
            spec_parser.insert_options(model_id, details_id, d[2])
        if d[3]:
            erc_parser.insert_erc(model_id, d[3])
        if d[4]:
            parts_utils.insert_parts(model_id, d[4])
