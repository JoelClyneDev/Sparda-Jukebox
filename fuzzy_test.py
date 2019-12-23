from fuzzywuzzy import fuzz
from fuzzywuzzy import process

values = ["ultra violet", "super ultra violet", "max violet"]

print(process.extract("violet", values))