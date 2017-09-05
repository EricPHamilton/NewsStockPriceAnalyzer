import pickle

def percent_change(original_num, new_num):
    return ((new_num - original_num) / original_num) * 100

with open('../data/processed_statements.txt', 'rb') as f:
    existing_statements = pickle.load(f)

    for i in range(0, len(existing_statements)):
        change = percent_change(existing_statements[i][4], existing_statements[i][5])
        existing_statements[i] = existing_statements[i] + tuple([change])

    with open('../data/percent_added_statements.txt', 'wb') as f:
        pickle.dump(existing_statements, f)


