def simple_hash(input_string):
    hash_value = 0

    for char in input_string:
        char_value = ord(char)

        hash_value = (hash_value * 31 + char_value) % 1000000007

    return hash_value


input_data = "HelloWorld"
print(f"Input String: {input_data}")
print(f"Hash Value: {simple_hash(input_data)}")
