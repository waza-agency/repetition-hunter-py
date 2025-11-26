"""Sample file with intentional repetitions for testing repetition-hunter."""


def process_data_v1(data):
    if data is None:
        return None
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result


def process_data_v2(items):
    if items is None:
        return None
    output = []
    for element in items:
        if element > 0:
            output.append(element * 2)
    return output


def validate_user_v1(user):
    if not user:
        return False
    if not user.get("name"):
        return False
    if not user.get("email"):
        return False
    return True


def validate_user_v2(person):
    if not person:
        return False
    if not person.get("name"):
        return False
    if not person.get("email"):
        return False
    return True


def calculate_sum_v1(numbers):
    total = 0
    for num in numbers:
        total = total + num
    return total


def calculate_sum_v2(values):
    total = 0
    for val in values:
        total = total + val
    return total
