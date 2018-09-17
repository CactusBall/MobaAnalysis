import logging

from celery import Celery
from kombu import Queue, Exchange

import spiders
from configs import duplicate

app = Celery('battle_tasks', backend='redis://localhost:6379/1', broker='redis://localhost:6379/1')


@app.task
def get_battle_list(openid, plat_id, after_time):
    try:
        holder = spiders.battle_list_holder
        from spiders.BattleListSpider import get_params, get_headers, get_cookies
        params = get_params(openid, plat_id, after_time)
        heaeders = get_headers()
        cookies = get_cookies()
        error_code, plat_id, has_next, next_after_time, battle_list = holder.request(
            params, heaeders, cookies)
    except Exception as e:
        return duplicate.is_user_has(openid, after_time, plat_id)
    if error_code != 0:
        return 2
    if len(battle_list) == 0:
        if plat_id == 0:
            get_battle_list.delay(openid, 1, next_after_time)
        if plat_id == 1:
            get_battle_list.delay(openid, 0, next_after_time)
    if has_next:
        get_battle_list.delay(openid, plat_id, next_after_time)
    for battle in battle_list:
        team_id = battle['team_id']
        battle_id = battle['battle_id']
        if duplicate.is_battle_has(battle_id):
            continue
        logging.warn('Found a new battle %s' % battle_id)
        mode = battle['mode']
        dt_event_time = battle['dt_event_time']
        get_battle_info.delay(openid, plat_id, team_id, battle_id, mode, dt_event_time)
    return 0


@app.task
def get_battle_info(openid, plat_id, team_id, battle_id, mode, dt_event_time):
    try:
        holder = spiders.battle_detail_holder
        from spiders.BattleDetailSpider import get_params, get_headers, get_cookies
        params = get_params(openid, team_id, plat_id, battle_id, mode, dt_event_time)
        heaeders = get_headers()
        cookies = get_cookies()
        error_code, plat_id_, prey_list = holder.request(params, heaeders, cookies)
    except Exception as e:
        logging.warn(e)
        return duplicate.is_battle_has(battle_id)
    logging.warn('pre %s' % prey_list)
    if error_code != 0:
        return 2
    for user in prey_list:
        get_battle_list.delay(openid, 0, user)
    return 0


task_queues = (
    Queue('queue_get_battle_info', exchange=Exchange('ex_gbi', type='direct'), routing_key='gbi'),
    Queue('queue_get_battle_list', exchange=Exchange('ex_gbl', type='direct'), routing_key='gbl')
)

task_routes = {
    'battle_tasks.get_battle_info': {'queue': 'queue_get_battle_info', 'routing_key': 'gbi'},
    'battle_tasks.get_battle_list': {'queue': 'queue_get_battle_list', 'routing_key': 'gbl'},
}
app.conf.update(CELERY_QUEUES=task_queues, CELERY_ROUTES=task_routes)
