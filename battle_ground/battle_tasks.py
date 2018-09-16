from celery import Celery
from kombu import Queue, Exchange

import spiders
from configs import duplicate

app = Celery('battle_tasks', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')


@app.task
def get_battle_list(openid, after_time):
    try:
        holder = spiders.battle_list_holder
        from spiders.BattleListSpider import get_params, get_headers, get_cookies
        params = get_params(openid, after_time)
        heaeders = get_headers()
        cookies = get_cookies()
        error_code, has_next, next_after_time, battle_list = holder.request(
            params, heaeders, cookies)
    except Exception as e:
        return duplicate.is_user_has(openid)
    if error_code != 0:
        return 2
    if has_next:
        get_battle_list.delay(openid, next_after_time)
    for battle in battle_list:
        team_id = battle['team_id']
        battle_id = battle['battle_id']
        mode = battle['mode']
        dt_event_time = battle['dt_event_time']
        get_battle_info.delay(openid, team_id, battle_id, mode, dt_event_time)
    return 0


@app.task
def get_battle_info(openid, team_id, battle_id, mode, dt_event_time):
    try:
        holder = spiders.battle_detail_holder
        from spiders.BattleDetailSpider import get_params, get_headers, get_cookies
        params = get_params(openid, team_id, battle_id, mode, dt_event_time)
        heaeders = get_headers()
        cookies = get_cookies()
        error_code, prey_list = holder.request(params, heaeders, cookies)
    except Exception as e:
        return duplicate.is_battle_has(battle_id)
    if error_code != 0:
        return 2
    for user in prey_list:
        get_battle_list.delay(openid, user)
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
