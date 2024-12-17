CREATE_AUTHOR_VALUES = [
    ('Aleksandr', 'Pushkin', '1799-06-06', 201),  # Correct data
    ('George', 'Orwell', '1903-06-25', 201),  # Correct data
    ('Mark', 'Twain', None, 400),  # Duplicate data
    ('Harper', 'Lee', None, 201),  # Correct data
    ('Ha', 'L' * 50, None, 201),  # Correct data
    ('F' * 15, 'Le', None, 201),  # Correct data
    (None, 'Rowling', None, 422),  # Missing first name
    ('J.K.', None, None, 422),  # Missing last name
    ('', 'Test', None, 422),  # Empty first name
    ('Test', '', None, 422),  # Empty last name
    ('F', 'Last_Name', None, 422),  # Short first name
    ('First_Name', 'L', None, 422),  # Short last name
    ('F' * 16, 'Le', None, 422),  # Long first name
    ('Ha', 'L' * 51, None, 422),  # Long first name
]
