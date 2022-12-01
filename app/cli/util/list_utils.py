

def remove_duplicates(input_list: list) -> list:
    if input_list:
        return [item for i, item in enumerate(input_list)
                if item not in input_list[:i]]
    return []
