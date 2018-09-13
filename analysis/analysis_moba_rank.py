qing_tong = '青铜'
bai_yin = '白银'
huang_jin = '黄金'
bo_jin = '铂金'
zuan_shi = '钻石'
xing_yao = '星耀'
wang_zhe = '王者'
nothing = '无段位'

ranks = {
    qing_tong: [],
    bai_yin: [],
    huang_jin: [],
    bo_jin: [],
    zuan_shi: [],
    xing_yao: [],
    wang_zhe: [],
    nothing: [],
}


def get_rank_from_code(code):
    if code in [1, 2, 3]:
        return qing_tong
    elif code in [4, 5, 6]:
        return bai_yin
    elif code in [17, 7, 8, 9]:
        return huang_jin
    elif code in [18, 19, 10, 11, 12]:
        return bo_jin
    elif code in [20, 21, 13, 14, 15]:
        return zuan_shi
    elif code in [22, 23, 24, 25, 26]:
        return xing_yao
    elif code in [16]:
        return wang_zhe
    else:
        return nothing


print(get_rank_from_code(19))
