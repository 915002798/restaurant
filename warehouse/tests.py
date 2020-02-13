import datetime

from django.test import TestCase


# Create your tests here.

# mdate = datetime.datetime.now()
# y, m, d = str(mdate).split('-')
# # d, t = d.split(' ')
# # print(d)
# # print(t)

def shelf_life(mdate, gdate):
    y, m, d = str(mdate).split('-')
    d, t = d.split(' ')

    # if int(m) == 2:
    #     if int(y) // 4:
    #         d = (int(d) + gdate) % 28  # 天
    #         x_m = (int(d) + gdate) // 28
    #         m = (int(m) + x_m) % 12  # 月
    #         x_y = (int(m) + x_m) // 12
    #         y = int(y) + x_y  # 年
    #         if d == 0:
    #             d = 28
    #     else:
    #         d = (int(d) + gdate) % 29  # 天
    #         x_m = (int(d) + gdate) // 29
    #         m = (int(m) + x_m) % 12  # 月
    #         x_y = (int(m) + x_m) // 12
    #         y = int(y) + x_y  # 年
    #         if d == 0:
    #             d = 29
    # elif int(m) == 4 or int(m) == 6 or int(m) == 9 or int(m) == 11:
    #     d = (int(d) + gdate) % 30  # 天
    #     x_m = (int(d) + gdate) // 30
    #     m = (int(m) + x_m) % 12  # 月
    #     x_y = (int(m) + x_m) // 12
    #     y = int(y) + x_y  # 年
    #     if d == 0:
    #         d = 30
    # else:
    #     d = (int(d) + gdate) % 31  # 天
    #     x_m = (int(d) + gdate) // 31
    #     m = (int(m) + x_m) % 12  # 月
    #     x_y = (int(m) + x_m) // 12
    #     y = int(y) + x_y  # 年
    #     if d == 0:
    #         d = 31
    #
    # if m == 0:
    #     m = 12
    #
    # return f'{y}-{m}-{d} {t}'


print(shelf_life('2019-12-22 20:00:00', 366))
