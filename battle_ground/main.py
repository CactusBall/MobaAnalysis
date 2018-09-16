import spiders
from battle_tasks import get_battle_list
openid = 'osewR0szPXJyn9Gg2Xhvjb-_X71s'
after_time = 0
get_battle_list.delay(openid, after_time)
# holder = spiders.battle_list_holder
# from spiders.BattleListSpider import get_params, get_headers, get_cookies
#
# params = get_params(openid, after_time)
# heaeders = get_headers()
# cookies = get_cookies()
# error_code, has_next, next_after_time, battle_list = holder.request(
#     params, heaeders, cookies)
#
# print(error_code)
# print(has_next)
# print(next_after_time)
# print(battle_list)
#
# battle = battle_list[0]
# team_id = battle['team_id']
# battle_id = battle['battle_id']
# mode = battle['mode']
# dt_event_time = ['dt_event_time']
#
#
#
# holder = spiders.battle_detail_holder
# from spiders.BattleDetailSpider import get_params, get_headers, get_cookies
#
# params = get_params(openid, team_id, battle_id, mode, dt_event_time)
# heaeders = get_headers()
# cookies = get_cookies()
# error_code, prey_list = holder.request(params, heaeders, cookies)
# print('----------------')
# print(prey_list)