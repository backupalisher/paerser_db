from db import db


def insert_spr_detail_options(data):
    q = db.i_request(f'WITH s as (SELECT id FROM spr_detail_options '
                     f'WHERE LOWER(name) = LOWER(\'{data}\')), i as '
                     f'(INSERT INTO spr_detail_options (name) SELECT \'{data}\' '
                     f'WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s')

    return q[0][0]


def insert_detail_options(caption_spr_id, detail_option_spr_id, parent_id):
    q = db.i_request(f'WITH s as (SELECT id FROM detail_options WHERE '
                     f'caption_spr_id = \'{caption_spr_id}\' AND detail_option_spr_id = \'{detail_option_spr_id}\'), '
                     f'i as (INSERT INTO detail_options (caption_spr_id, detail_option_spr_id, parent_id) '
                     f'SELECT \'{caption_spr_id}\', \'{detail_option_spr_id}\', \'{parent_id}\' '
                     f'WHERE NOT EXISTS (SELECT 1 FROM s) returning id) SELECT id FROM i UNION ALL SELECT id FROM s')

    return q[0][0]


def link_models_spr_details(model_id, spr_detail_id):
    q = db.i_request(f'WITH s as (SELECT id FROM details '
                     f'WHERE model_id = {model_id} AND spr_detail_id = {spr_detail_id}), i as '
                     f'(INSERT INTO details (model_id, spr_detail_id) SELECT {model_id}, {spr_detail_id} '
                     f'WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s')

    return q[0][0]


def link_detail_options(detail_id, detail_option_id):
    db.i_request(f'WITH s as (SELECT 1 FROM link_details_options '
                 f'WHERE detail_id = {detail_id} AND detail_option_id = {detail_option_id}), i as '
                 f'(INSERT INTO link_details_options (detail_id, detail_option_id) '
                 f'SELECT {detail_id}, {detail_option_id} '
                 f'WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING 0) select * from i union all select * from s')


def get_id(table_name, where_name, param):
    return db.i_request(f'SELECT id FROM {table_name} WHERE "{where_name}" = \'{param}\'')
