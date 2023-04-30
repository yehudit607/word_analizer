file_size_gb = 1
file_name = "test_file_1gb.txt"
test_sentence = "This is a test sentence to generate a large file for testing. "

with open(file_name, "w", encoding="utf-8") as test_file:
    bytes_written = 0
    target_bytes = file_size_gb * (1024 ** 3)
    sentence_bytes = len(test_sentence.encode("utf-8"))

    while bytes_written < target_bytes:
        test_file.write(test_sentence)
        bytes_written += sentence_bytes

print(f"Generated {file_size_gb} GB test file: {file_name}")
