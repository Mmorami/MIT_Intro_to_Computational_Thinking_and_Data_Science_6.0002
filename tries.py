dic = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
l = ['a', 'b', 'c', 'd']
# l = [1,2,3,4]
print(sum(dic[lambda i: l[i]]))
