import sqlalchemy_access.pyodbc
from sqlalchemy import create_engine


def convert_file_to_base64():
    with open('file.png', 'rb') as binary_file:
        import base64
        binary_file_data = binary_file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        base64_message = base64_encoded_data.decode('utf-8')
        print(base64_message)


def is_db_connected(db_uri: str) -> bool:
    """
    :param db_uri:
    :return:
    """
    try:
        eng = create_engine(db_uri)
        eng.execute("SELECT 1")
    except:
        return False
    else:
        eng.dispose()
        return True