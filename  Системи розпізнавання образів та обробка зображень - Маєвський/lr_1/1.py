p_yes = 9/14
p_no = 5/14

p_overcast_yes, p_overcast_no = 4/9, 0/5
p_high_yes, p_high_no = 3/9, 4/5
p_strong_yes, p_strong_no = 3/9, 3/5

likelihood_yes = p_overcast_yes * p_high_yes * p_strong_yes * p_yes
likelihood_no = p_overcast_no * p_high_no * p_strong_no * p_no

total = likelihood_yes + likelihood_no
prob_yes = (likelihood_yes / total) * 100 if total > 0 else 100
prob_no = (likelihood_no / total) * 100 if total > 0 else 0

print(f"Ймовірність 'Yes': {prob_yes:.2f}%")
print(f"Ймовірність 'No': {prob_no:.2f}%")