from celery import Celery
from kombu import Queue, Exchange

from config import duplicate
from net import handlers, proxies

app = Celery('moba_tasks', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')


@app.task
def get_user_info(profile_id):
    prox, ip = proxies.get_proxies()
    try:
        error_code, openid = handlers.load_user_info(profile_id, prox, ip)
    except Exception as e:
        return duplicate.is_user_profile_has(profile_id)
    if error_code != 0:
        return 2
    get_battle_list.delay(openid, prox, ip)
    return 0


@app.task
def get_battle_list(openid, prox, ip):
    try:
        error_code, zone_area_id, open_id = handlers.load_zone_area_id(openid, prox, ip)
    except Exception as e:
        return duplicate.is_zone_has(openid)
    if error_code != 0:
        return 2
    get_battle_list_p.delay(open_id, 0, zone_area_id, prox, ip)
    return 0


@app.task
def get_battle_list_p(openid, offset, zone_area_id, prox, ip):
    try:
        error_code, battle_list, open_id, has_next, next_offset = handlers.load_user_game_list(openid, offset,
                                                                                               zone_area_id, prox, ip)
    except Exception as e:
        return duplicate.is_user_openid_has(openid)
    if error_code != 0:
        return 2
    if has_next:
        get_battle_list_p.delay(openid, next_offset, zone_area_id, prox, ip)
    for battle in battle_list:
        game_seq = battle['game_seq']
        game_svr_entity = battle['game_svr_entity']
        relay_svr_entity = battle['relay_svr_entity']
        get_battle_info.delay(game_seq, game_svr_entity, relay_svr_entity, open_id, prox, ip)
    return 0


@app.task
def get_battle_info(game_seq, game_svr_entity, relay_svr_entity, openid, prox, ip):
    try:
        error_code, profile_ids = handlers.load_game_detail(game_seq, game_svr_entity, relay_svr_entity, openid, prox,
                                                            ip)
    except Exception as e:
        return duplicate.is_battle_has(game_seq)
    if error_code != 0:
        return 2
    for profile_id in profile_ids:
        get_user_info.delay(profile_id)
    return 0


task_queues = (
    Queue('queue_get_battle_info', exchange=Exchange('ex_gbi', type='direct'), routing_key='gbi'),
    Queue('queue_get_battle_list', exchange=Exchange('ex_gbl', type='direct'), routing_key='gbl'),
    Queue('queue_get_user_info', exchange=Exchange('ex_gui', type='direct'), routing_key='gui'),
    Queue('queue_get_battle_list_p', exchange=Exchange('ex_gbl_p', type='direct'), routing_key='gbl_p')
)

task_routes = {
    'moba_tasks.get_battle_info': {'queue': 'queue_get_battle_info', 'routing_key': 'gbi'},
    'moba_tasks.get_battle_list': {'queue': 'queue_get_battle_list', 'routing_key': 'gbl'},
    'moba_tasks.get_user_info': {'queue': 'queue_get_user_info', 'routing_key': 'gui'},
    'moba_tasks.get_battle_list_p': {'queue': 'queue_get_battle_list_p', 'routing_key': 'gbl_p'},
}
app.conf.update(CELERY_QUEUES=task_queues, CELERY_ROUTES=task_routes)
