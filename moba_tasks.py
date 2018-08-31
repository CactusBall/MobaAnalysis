import logging
import random
import time

from celery import Celery
from kombu import Queue, Exchange

from net import handlers

app = Celery('moba_tasks', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')


@app.task
def get_user_info(profile_id):
    try:
        error_code, openid = handlers.load_user_info(profile_id)
    except Exception:
        time.sleep(random.randint(40, 60))
        raise IOError
    if error_code != 0:
        time.sleep(random.randint(1, 20))
        return False
    get_battle_list.delay(openid)
    return True


@app.task
def get_battle_list(openid):
    logging.info("get_battle_list %s " % openid)
    time.sleep(random.randint(1, 10))
    try:
        error_code, battle_list, openid = handlers.load_user_game_list(openid)
    except Exception:
        time.sleep(random.randint(10, 20))
        raise IOError
    if error_code != 0:
        time.sleep(random.randint(1, 10))
        return False
    if error_code == 45009:
        time.sleep(random.randint(10, 20))
        return False
    for battle in battle_list:
        game_seq = battle['game_seq']
        game_svr_entity = battle['game_svr_entity']
        relay_svr_entity = battle['relay_svr_entity']
        get_battle_info.delay(game_seq, game_svr_entity, relay_svr_entity, openid)
    return True


@app.task
def get_battle_info(game_seq, game_svr_entity, relay_svr_entity, openid):
    try:
        error_code, profile_ids = handlers.load_game_detail(game_seq, game_svr_entity, relay_svr_entity, openid)
    except Exception:
        time.sleep(random.randint(10, 20))
        raise IOError
    if error_code != 0:
        time.sleep(random.randint(1, 10))
        return False
    for profile_id in profile_ids:
        get_user_info.delay(profile_id)
    return True


task_queues = (
    Queue('queue_get_battle_info', exchange=Exchange('ex_gbi', type='direct'), routing_key='gbi'),
    Queue('queue_get_battle_list', exchange=Exchange('ex_gbl', type='direct'), routing_key='gbl'),
    Queue('queue_get_user_info', exchange=Exchange('ex_gui', type='direct'), routing_key='gui')
)

task_routes = {
    'moba_tasks.get_battle_info': {'queue': 'queue_get_battle_info', 'routing_key': 'gbi'},
    'moba_tasks.get_battle_list': {'queue': 'queue_get_battle_list', 'routing_key': 'gbl'},
    'moba_tasks.get_user_info': {'queue': 'queue_get_user_info', 'routing_key': 'gui'},
}
app.conf.update(CELERY_QUEUES=task_queues, CELERY_ROUTES=task_routes)
