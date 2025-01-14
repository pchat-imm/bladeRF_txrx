prime = [2,3,5,7]
byte_array = bytearray(prime)
print("byte_array: ", byte_array)
# return bytearray(b'\x02\x03\x05\x07')

bytes_per_sample = 4
buf = bytearray(1024 * bytes_per_sample)
print("buf: ", buf)
