my_lst = [1,3,5,7]
payoff_1 = sum(val if val%2==0 else 0 for val in my_lst)

print(payoff_1)