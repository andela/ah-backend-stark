def clean_byte_str(byte_str):
    """
    Removes b'' from bytes converted to strings
    """
    return byte_str[2:-1]
