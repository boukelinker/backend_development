# Do not modify these lines
__winc_id__ = '71dd124b4a6e4d268f5973db521394ee'
__human_name__ = 'strings'

# Add your code after this line

scorer_name_0 = "Ruud Gullit"
scorer_name_1 = "Marco van Basten"
player = "Frank Rijkaard"

goal_0 = 32
goal_1 = 54

scorers = scorer_name_0 + " " + \
    str(goal_0) + ", " + scorer_name_1 + " " + str(goal_1)

report = scorer_name_0 + f' scored in the ' + str(goal_0) + f'nd minute' + \
    '\n' + scorer_name_1 + f' scored in the ' + str(goal_1) + f'th minute'

first_name = player[player.find("Frank"):len("Frank")]
last_name = player[player.find("Rijkaard"):]
last_name_len = len(player[player.find("Rijkaard"):])
name_short = first_name[0]+'. ' + last_name
chant = (first_name + "! ")*(len(first_name)-1)+first_name + "!"
good_chant = chant[-1] != " "

print(first_name)
print(last_name_len)
print(name_short)
print(chant)
print(good_chant)
