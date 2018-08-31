import time

from moba_tasks import get_user_info

profile_id = 'g1NlbysGi4KDI5aTA0V-65f9QlaA'
r = get_user_info.delay(profile_id)
while not r.ready():
    time.sleep(1)
print(type(r.get()))