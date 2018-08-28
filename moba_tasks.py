from config import duplicate
from net import handlers
from celery import Celery
from kombu import Queue, Exchange

app = Celery('moba_tasks', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')

task_queues = (
    Queue('queue_get_battle_info', exchange=Exchange('priority', type='direct'), routing_key='gbi'),
    Queue('queue_get_battle_list', exchange=Exchange('priority', type='direct'), routing_key='gbl'),
    Queue('queue_get_user_info', exchange=Exchange('priority', type='direct'), routing_key='gui'),
)

task_routes = ([
                   ('get_battle_info', {'queue': 'queue_get_battle_info'}),
                   ('get_battle_list', {'queue': 'queue_get_battle_list'}),
                   ('get_user_info', {'queue': 'queue_get_user_info'}),
               ],)
app.conf.update(CELERY_QUEUES=task_queues, CELERY_ROUTES=task_routes)


@app.task(name='get_battle_list')
def get_battle_list(profile_id):
    if duplicate.is_user_profile_has(profile_id):
        return True

    openid = handlers.load_user_info(profile_id)

    # todo load game list do not run, why?
    battle_list = handlers.load_user_game_list(openid)
    for battle in battle_list:
        game_seq = battle['game_seq']
        game_svr_entity = battle['game_svr_entity']
        relay_svr_entity = battle['relay_svr_entity']
        get_battle_info.delay(game_seq, game_svr_entity, relay_svr_entity, openid)
    return True


@app.task(name='get_battle_info')
def get_battle_info(game_seq, game_svr_entity, relay_svr_entity, openid):
    handlers.load_game_detail(game_seq, game_svr_entity, relay_svr_entity, openid)
