prime = [2,3,5,7]
byte_array = bytearray(prime)
# print("byte_array: ", byte_array)
# return bytearray(b'\x02\x03\x05\x07')

bytes_per_sample = 4
buf = bytearray(1024 * bytes_per_sample)
# print("buf: ", buf)


num_samples = int(1e6)
num_samples_read = 0

num = min(len(buf) // bytes_per_sample, num_samples - num_samples_read)
rest_buf= len(buf) // bytes_per_sample
rest_samplesRead = num_samples - num_samples_read
min(rest_buf, rest_samplesRead)