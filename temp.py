group_1 = [1,2,3,4,5,6,7,8,9]
group_2 = [1,2,3,4,5,6,7,8,9]

group_3 = [10,20,30,40,50,60,70,80,90]

tot_list = [group_1,group_2,group_3]
print(tot_list.index(group_2))


def test():
    return []

for g1,g2 in test():
    for ind in g1:
        print("choco")
        for ind in g2:
            print(ind)