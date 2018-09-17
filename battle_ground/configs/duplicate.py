import logging

import configs


def _user_id(openid, time, plat_id):
    return 'bl_%s_%s_%s' % (openid, time, plat_id)


def _battle_detail(game_id):
    return 'bz_%s' % game_id


_gameseq_key = 'chiji_game_seq'
_user_key = 'chiji_user'


def is_battle_has(game_id):
    return configs.redis.hexists(_gameseq_key, _battle_detail(game_id))


def is_user_has(openid, time, plat_id):
    return configs.redis.hexists(_user_key, _user_id(openid, time, plat_id))


def record_game(game_id):
    configs.redis.hset(_gameseq_key, _battle_detail(game_id), game_id)


def record_user(openid, time, plat_id):
    configs.redis.hset(_user_key, _user_id(openid, time, plat_id), openid)
