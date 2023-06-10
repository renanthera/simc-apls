import base64

sample = "BwQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAkAAAAApQrkkEIJp1IAAAApkEJRiEUkkIJpkA0iEplWJE"



print(sample)

bytes = sample.encode('ascii')
print(bytes)

bytes = base64.b64decode(bytes)
print(bytes)

# decode = bytes.decode('ascii')
# print(decode)

binary = bin(int.from_bytes(bytes))
print(binary)
binary = binary[2:]
offset = 0
print('serialization version')
print(binary[offset:offset+7])
t = binary[offset:offset+7]
print(int(t[::-1],2))
offset += 8
print('specialization id')
print(binary[offset:offset+15])
offset += 16
print('tree hash')
print(binary[offset:offset+127])
offset += 128
print('file')
print(binary[offset:])

def extract_value(width):
    bitsPerChar = 6
    value = 0
    bitsNeeded = width
    extractedBits = 0
    while bitsNeeded > 0:
        remainingBits = bitsPerChar - totalExtractedBits
        bitsToExtract = min(remainingBits, bitsNeeded)
        totalExtractedBits += bitsToExtract
        maxStorable = 1 << bitsToExtract
        remainder = currentRemainingValue % maxStorable
        currentRemainingValue = remainder << extractedBits
        value += remainder << bitsToExtract
        bitsNeeded -= bitsToExtract
        if bitsToExtract < remainingBits:
            break
        else if bitsToExtract >= remainingBits:
            currentIndex += 1
            currentExtractedBits = 0
            currentRemainingValue = dataValues
