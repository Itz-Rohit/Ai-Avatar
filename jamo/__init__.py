# jamo/__init__.py
# Dummy jamo package to bypass the null byte error in the original jamo package.
# This dummy provides a basic placeholder for hangul_to_jamo.

def hangul_to_jamo(text):
    # Since you are not using Korean phonemization,
    # simply return the input text unchanged.
    return text
