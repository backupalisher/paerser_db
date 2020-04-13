from db import db


def insert_spr_modules(param):
    q = db.i_request(f'WITH s as (SELECT id FROM spr_modules '
                     f'WHERE LOWER(name) = LOWER(\'{param}\')), i as '
                     f'(INSERT INTO spr_modules (name) SELECT \'{param}\' '
                     f'WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s')
    return q[0][0]


def insert_partcodes(param):
    q = db.i_request(f'WITH s as (SELECT id FROM partcodes '
                     f'WHERE LOWER(code) = LOWER(\'{param}\')), i as '
                     f'(INSERT INTO partcodes (code) SELECT \'{param}\' '
                     f'WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s')
    return q[0][0]


def insert_spr_details(param):
    q = db.i_request(f'WITH s as (SELECT id FROM spr_details '
                     f'WHERE LOWER(name) = LOWER(\'{param}\')), i as '
                     f'(INSERT INTO spr_details (name) SELECT \'{param}\' '
                     f'WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s')
    return q[0][0]


def update_partcode_desc(code, param):
    db.i_request(f'UPDATE partcodes SET description = concat(s.description || \'{param}\' || \';\') '
                 f'FROM(SELECT description FROM partcodes WHERE id = {code}) s WHERE partcodes.id = {code}')


def insert_spr_module_image(param):
    q = db.i_request(f'WITH s as (SELECT id FROM spr_module_image '
                     f'WHERE image = \'{param}\'), i as '
                     f'(INSERT INTO spr_module_image (image) SELECT \'{param}\' '
                     f'WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s')
    return q[0][0]


def link_model_module_image(model_id, module_id, img_id):
    db.i_request(f'WITH s as (SELECT 1 FROM link_model_module_image '
                 f'WHERE model_id = {model_id} AND spr_module_id = {module_id} AND spr_module_image_id = {img_id}), '
                 f'i as (INSERT INTO link_model_module_image (model_id, spr_module_id, spr_module_image_id) '
                 f'SELECT {model_id}, {module_id}, {img_id} WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING 0) '
                 f'SELECT * FROM i UNION ALL SELECT * FROM s')


def link_part_model_module_spr(partcode_id, model_id, module_id, spr_detail_id):
    db.i_request(f'WITH s as (SELECT 1 FROM details '
                 f'WHERE partcode_id = {partcode_id} AND model_id = {model_id} AND module_id = {module_id} AND '
                 f'spr_detail_id = {spr_detail_id}), i as '
                 f'(INSERT INTO details (partcode_id, model_id, module_id, spr_detail_id) '
                 f'SELECT {partcode_id}, {model_id}, {module_id}, {spr_detail_id} WHERE NOT EXISTS '
                 f'(SELECT 1 FROM s) RETURNING 0) SELECT * FROM i UNION ALL SELECT * FROM s')


def link_models_spr_details(model_id, spr_detail_id):
    q = db.i_request(f'WITH s as (SELECT id FROM details '
                     f'WHERE model_id = {model_id} AND spr_detail_id = {spr_detail_id}), i as '
                     f'(INSERT INTO details (model_id, spr_detail_id) SELECT {model_id}, {spr_detail_id} '
                     f'WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s')
