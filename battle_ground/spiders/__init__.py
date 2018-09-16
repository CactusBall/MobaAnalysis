from spiders.BattleDetailSpider import BattleDetailSpider
from spiders.BattleListSpider import BattleListSpider

_battle_list_url = 'https://game.weixin.qq.com/cgi-bin/gamewap/getjdqssybattlelist'
_battle_detail_url = 'https://game.weixin.qq.com/cgi-bin/gamewap/getjdqssybattledetail'

battle_list_holder = BattleListSpider('GET', _battle_list_url)
battle_detail_holder = BattleDetailSpider('GET', _battle_detail_url)
