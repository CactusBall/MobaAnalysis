import config
import configs


def _user_id(openid):
    return 'bl_%s' % openid


def _battle_detail(game_id):
    return 'bz_%s' % game_id


_gameseq_key = 'chiji_game_seq'
_user_key = 'chiji_user'


def is_battle_has(game_id):
    return config.redis.hexists(_gameseq_key, _battle_detail(game_id))


def is_user_has(openid):
    return config.redis.hexists(_user_key, _user_id(openid))


def record_game(game_id):
    config.redis.hset(_gameseq_key, _battle_detail(game_id), game_id)


def record_user(openid):
    config.redis.hset(_user_key, _user_id(openid), openid)
