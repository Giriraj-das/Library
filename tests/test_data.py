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
    ('First', 'Last', '', 422),  # Empty row in date
]

CREATE_BOOK_VALUES = [
    ('War and Peace', 'A historical novel by Leo Tolstoy.', 1, 5, 201),  # Correct data
    ('War', 'The war is', 1, 5, 201),  # Correct data
    ('The Idiot', None, 1, 1, 201),  # Correct data
    ('T' * 100, None, 1, 1, 201),  # Correct data
    ('T' * 101, None, 1, 1, 422),  # Long title
    ('Wa', None, 1, 1, 422),  # Short title
    ('War', 'The war i', 1, 1, 422),  # Short description
    ('To Kill a Mockingbird', '', 1, 1, 422),  # Empty row in description
    (None, 'A philosophical novel by Fyodor Dostoevsky.', 1, 2, 422),  # Missing title
    ('', 'Empty title.', 1, 4, 422),  # Empty title
    ('To Kill a Mockingbird', 'A novel about racial injustice.', 1, -1, 422),  # Negative available copies
]
