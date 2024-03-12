def check_error(data):
    if 'error' in data and data['error'] != None:
        error_code = data['error']['code']
        error_message = data['error']['message']
        if error_code == 401:
            print("Token Authentication failed: " + error_message)
            exit(1)
        else:
            print(f"Error {error_code}: {error_message}")
            exit(1)