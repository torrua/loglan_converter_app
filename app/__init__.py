import sqlalchemy_access.pyodbc


def convert_file_to_base64():
    with open('file.png', 'rb') as binary_file:
        import base64
        binary_file_data = binary_file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        base64_message = base64_encoded_data.decode('utf-8')
        print(base64_message)