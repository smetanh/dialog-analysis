# from collections import Counter
#
#
# items = ["60", "10", '20', '30', "40", '50', "10", "10", "10", "20", "20", "30"]
#
# counter = {}
# for item in items:
#     if item not in counter:
#         counter[item] = 0
#     counter[item] += 1
#
# sorted_counter = dict(sorted(counter.items(), key=lambda x: x[1], reverse=True))
#
# top_k = 3
# top_items = []
# top_percents = 0
#
# for k, v in sorted_counter.items():
#     if top_k > 0:
#         top_items.append(f"{int(100 * v / len(items))}% {k}")
#         top_percents += int(100 * v / len(items))
#         top_k -= 1
#
# top_items.append(f"{100 - top_percents}% другие")
#
# print(top_items)
d1 = [[] for x in range(6)]


d1[1] = 2

print(d1)