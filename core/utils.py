def remove_non_alphanumeric(value: str):
    return "".join([e for e in value if e.isalnum()])

def first_occurrence(lines, value):
    low = 0
    high = len(lines) - 1
    mid = 0

    while low <= high:

        mid = (high + low) // 2
        uf = lines[mid].split("@")[1]

        if uf < value:
            low = mid + 1

        elif uf > value:
            high = mid - 1

        elif uf == value:
            if len(lines) == 1: return mid
            elif mid == 0: return mid
            elif lines[mid - 1].split("@")[1] != value: return mid
            else: high = mid - 1
                
 
    # If we reach here, then the element was not present
    return -1

def last_occurrence(lines, value):
    low = 0
    high = len(lines) - 1
    mid = 0

    while low <= high:

        mid = (high + low) // 2
        uf = lines[mid].split("@")[1]

        if uf < value:
            low = mid + 1

        elif uf > value:
            high = mid - 1

        elif uf == value:
            if len(lines) == 1: return mid
            elif mid == 0: return mid
            elif len(lines) - 1 == mid: return mid
            elif lines[mid + 1].split("@")[1] != value: return mid
            else: low = mid + 1
                
 
    # If we reach here, then the element was not present
    return -1