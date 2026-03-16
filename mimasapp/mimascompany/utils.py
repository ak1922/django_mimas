import random

# Generate username
def generate_username(first_name, last_name):

    first_list = list(first_name.lower())
    last_list = list(last_name.lower())

    combo_list = first_list + last_list
    random.shuffle(combo_list)

    shuffled_string = ''.join(combo_list)
    string_count = len(shuffled_string)
    username = shuffled_string[:5] + str(string_count)

    return username
