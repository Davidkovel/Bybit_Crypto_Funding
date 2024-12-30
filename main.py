# import schedule
# import time
#
# from funding import *
#
# provider = FundingProvider()
#
#
# def schedule_orders():
#     schedule.every().day.at("23:50").do(provider.check_funding)
#     schedule.every().day.at("07:50").do(provider.check_funding)
#     schedule.every().day.at("15:50").do(provider.check_funding)
#
#     # schedule.every().day.at("23:59:57").do(provider.close_orders)
#     # schedule.every().day.at("07:59:57").do(provider.close_orders)
#     # schedule.every().day.at("15:59:57").do(provider.close_orders)
#
#
# if __name__ == "__main__":
#     provider.execute()
#     # schedule_orders()
#     # while True:
#     #     schedule.run_pending()
#     #     time.sleep(1)

def min_sides(K):
    high = 3
    while (high * (high - 3)) // 2 < K:
        high *= 2

    low = 3
    while low < high:
        mid = (low + high) // 2
        D = (mid * (mid - 3)) // 2

        if D >= K:
            high = mid
        else:
            low = mid + 1

    return low

K = int(input())
print(min_sides(K))
