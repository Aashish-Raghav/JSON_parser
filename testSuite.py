from jsonparser import JSON_parser, JSON_exception

print("Testing against test suite from http://www.json.org/JSON_checker/\n")
# invalid json tests
print("Tests for invalid JSON")
print("======================")
tests_passed = 0

for n in range(1,34):
    file = f"test/test/fail{n}.json"
    with open(file) as file_handle:
        file_content = file_handle.read()
        try:
            parser = JSON_parser(file_content)
            result = parser.initializeParsing()
            print(f"Test {n} FAILED: Did not recognise invalid json, parsed test file content as: {result}")

        except JSON_exception as e:
            print(f"Test {n} PASSED: Recognised invalid json, exception: {e}")
            tests_passed += 1

print(f"\nPASSED {tests_passed}/33 TESTS")

#Valid json tests
print("Tests for valid JSON")
print("======================")

tests_passed = 0

for n in range(1, 4):
    file = f"test/test/pass{n}.json"
    with open(file) as f:
        with open(file) as file_handle:
            file_content = file_handle.read()
        try:
            parser = JSON_parser(file_content)
            result = parser.initializeParsing()
            print(f"Test {n} PASSED: Parsed valid json, parsed test file content as: {result}")
            tests_passed += 1

        except JSON_exception as e:
            print(f"Test {n} FAILED: Failed to parse valid json, exception: {e}")

print(f"\nPASSED {tests_passed}/3 TESTS")