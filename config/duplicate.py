import config


def _user_profile(profile_id):
    return 'up_%s' % profile_id


def _user_openid(openid):
    return 'uo_%s' % openid


def _user_battle(game_seq):
    return 'ub_%s' % game_seq


_profile_key = 'moba_profile_id'
_openid_key = 'moba_openid'
_gameseq_key = 'moba_game_seq'


def is_user_profile_has(profile_id):
    return config.redis.hexists(_profile_key, _user_profile(profile_id))


def is_user_openid_has(openid):
    return config.redis.hexists(_openid_key, _user_openid(openid))


def is_battle_has(game_seq):
    return config.redis.hexists(_gameseq_key, _user_battle(game_seq))


def record_profile(profile_id):
    config.redis.hset(_profile_key, _user_profile(profile_id), profile_id)


def record_openid(openid):
    config.redis.hset(_openid_key, _user_openid(openid), openid)


def record_game(game_seq):
    config.redis.hset(_gameseq_key, _user_battle(game_seq), game_seq)
