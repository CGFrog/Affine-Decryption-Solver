from collections import Counter
import enchant

"""
I made this to help me solve my Number Theory homework
while still engaging with the material in a way that helped me learn.

I am certain that there are better algorithms out there but this is how we were doing it by hand.

"""

# Converts letters to their corresponding number
def text_to_numbers(text):
    return [ord(c.lower()) - ord('a') for c in text]
# Converts numbers back to text
def numbers_to_text(numbers):
    return ''.join(chr(n + ord('a')) for n in numbers)
# Finds modular inverses
def mod_inverse(a, m=26):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None
# Decrypts characters given an affine function.
def affine_decrypt(cipher, a, b):
    a_inv = mod_inverse(a)
    if a_inv is None:
        return None
    return [(a_inv * (y - b)) % 26 for y in cipher]
# This is used to filter all the gibberish out and only show us the messages that have a high-score for english.
def score_decryption(text):
    d = enchant.Dict("en_US")
    score = 0
    for size in range(3, 7):
        for i in range(len(text) - size + 1):
            word = text[i:i+size]
            if d.check(word):
                score += 1
    return score
# List is sorted from most common letters to least common.
english_freq_order = text_to_numbers("ETAOINSHRDLCUMWFGYPBVKJXQZ")
ciphertext = text_to_numbers("MJMZKCXUNMGWIRYVCPUWMPRRWGMIOPMSNYSRYRAZPXMCDWPRYEYXD")
counter = Counter(ciphertext)
# Finds the 5 most common letters in the encrypted message
cipher_freq_order = [pair[0] for pair in counter.most_common(5)]
# Score that a message needs to have before being displayed.
score_threshold = 15
best_score = 0
best_result = ""
for i in range(len(cipher_freq_order)):
    for j in range(len(cipher_freq_order)):
        if i == j:
            continue
        # sets c1 and c2 equal to the ith and jth most common letter in the message respectively.
        c1, c2 = cipher_freq_order[i], cipher_freq_order[j]
        for m in range(len(english_freq_order)):
            for n in range(len(english_freq_order)):
                if m == n:
                    continue
                # sets p1 and p2 equal to the mth and nth most common english letters respectively.
                p1, p2 = english_freq_order[m], english_freq_order[n]
                diff_p = (p1 - p2) % 26
                diff_c = (c1 - c2) % 26
                # Calculates mod inverse and skips iteration if there is none.
                inv = mod_inverse(diff_p)
                if inv is None:
                    continue      
                a = (diff_c * inv) % 26
                b = (c1 - a * p1) % 26
                decrypted_nums = affine_decrypt(ciphertext, a, b)
                if decrypted_nums:
                    # Decrypts the numbers using hypothetical a,b and scores its likelihood of being english.
                    decrypted_text = numbers_to_text(decrypted_nums)
                    score = score_decryption(decrypted_text)
                    # if the test scores high enough we will print it out, if not we continue.
                    if score >= score_threshold:
                        print(f"[score={score}] a={a}, b={b}: {decrypted_text} at {i},{j} iteration")
                    if score > best_score: # When I run the program this immediately spits out the correct cipher.
                        best_score = score
                        best_result = f"a={a}, b={b}: {decrypted_text} at {i},{j} iteration"
print(best_result) # If the program were to run until the end (which hopefully it does not that would take a long long time worst case O(n^2m^2) I think) we print best result.
