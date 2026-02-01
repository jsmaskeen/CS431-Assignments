import sys
import subprocess
import math
from itertools import permutations


def problem1():
    """Reference:
    https://www.geeksforgeeks.org/dsa/columnar-transposition-cipher/
    3grams to score the results:
    https://calmcode.io/datasets/english_3grams
    """
    print("Problem: columns-101")
    ciphertext = "UOLTICH1EEAOREIITMFSHLEE6NRIRANPSHBRFEFCR"
    len_k = 5
    sols = []
    col_len, rem = divmod(len(ciphertext), len_k)
    trigram_counts = {}
    total_count = 0
    with open("english_3grams.csv", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 2:
                gram = parts[0].upper()
                count = int(parts[1])
                trigram_counts[gram] = count
                total_count += count

    def scorer(text):
        score = 0
        text = text.upper()
        for i in range(len(text) - 2):
            trigram = text[i : i + 3]
            if trigram in trigram_counts:
                prob = trigram_counts[trigram] / total_count
                score += math.log10(prob)
            else:
                score += math.log10(1 / (total_count * 10))

        return score

    for perm in permutations(list(range(1, 1 + len_k))):
        matrix_cols = [""] * (len_k + 1)
        idx = 0
        for k in perm:
            col_height = col_len + 1 if k <= rem else col_len
            chunk = ciphertext[idx : idx + col_height]
            matrix_cols[k] = chunk
            idx += col_height
        decoded = []
        for r in range(col_len + 1):
            for c in range(1, len_k + 1):
                if r < len(matrix_cols[c]):
                    decoded.append(matrix_cols[c][r])

        decoded_msg = "".join(decoded)
        sols.append((perm, decoded_msg, scorer(decoded_msg)))

    sols.sort(key=lambda x: x[2], reverse=True)
    print("\n".join(map(lambda x: f"{x[1]} | {x[2]:4.2f}", sols[:7])))


def problem2():
    """References:
    https://www.geeksforgeeks.org/dsa/vigenere-cipher/
    https://stackoverflow.com/questions/19880190/interactive-input-output-using-python
    https://stackoverflow.com/questions/59787040/stuck-in-infinite-loop-while-trying-to-read-all-lines-in-proc-stdout-readline
    """

    print("Problem: vigenere-101")
    key = "VICTORY"
    len_k = len(key)
    ciphertext = "Be3cmXfz!T0cEk4qb3bDb"
    alphabets = "abcdefghijklmnopqrstuvwxyz"

    def char2idx(char):
        return ord(char.lower()) - ord("a")

    def decode(c1, c2):
        rotated = alphabets[char2idx(c2) :] + alphabets[: char2idx(c2)]
        dec = alphabets[rotated.find(c1.lower())]
        return dec if not c1.isupper() else dec.upper()

    decoded = ""
    cnt = 0
    for idx in range(len(ciphertext)):
        if ciphertext[idx].isalpha():
            decoded += decode(ciphertext[idx], key[cnt % len_k])
            cnt += 1
        else:
            decoded += ciphertext[idx]

    print(f"Decoded vigenere: {decoded}")
    proc = subprocess.Popen(
        ["nc", "10.0.118.104", "5050"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    lines = []
    for _line in iter(proc.stdout.readline, b""):
        if _line == "\n":
            break
        lines.append(_line)
    proc.stdin.write(f"{decoded.strip()}\n")
    proc.stdin.flush()
    lines = []
    for _line in iter(proc.stdout.readline, b""):
        lines.append(_line)
        if _line.endswith("\n"):
            break
    print("Flag:", lines[0].split(": ")[-1])


def rail_fence_decode(rails, ciphertext):
    """Reference:
        https://www.geeksforgeeks.org/dsa/rail-fence-cipher-encryption-decryption/
    """
    cols = len(ciphertext)
    m = [[" " for _ in range(cols)] for _ in range(rails)]
    r, c = 0, 0
    for _ in range(cols):
        if r == 0:
            down = True
        elif r == rails - 1:
            down = False
        m[r][c] = "t"
        c += 1
        if down:
            r += 1
        else:
            r -= 1
    # print('\n'.join([''.join(rr) for rr in m]))
    idx = 0

    for r in range(rails):
        for c in range(cols):
            if m[r][c] == "t":
                m[r][c] = ciphertext[idx]
                idx += 1

    print('\n'.join([''.join(rr) for rr in m]))

    decoded = ""
    r, c = 0, 0
    for _ in range(cols):
        if r == 0:
            down = True
        elif r == rails - 1:
            down = False
        decoded += m[r][c]
        c += 1
        if down:
            r += 1
        else:
            r -= 1
    print(f"Flag: {decoded}")


def problem3():
    """Reference:
        https://www.geeksforgeeks.org/dsa/rail-fence-cipher-encryption-decryption/
    """
    print("Problem: Rail Force One")
    ciphertext = "MHASIDYAKHBEWDEMFXTNURRCPQYTVORSRYAILEIHZTLTGOSREE4EUJATBOFO"
    rails = 16
    rail_fence_decode(rails, ciphertext)


def problem4():
    """Reference:
        https://www.geeksforgeeks.org/dsa/rail-fence-cipher-encryption-decryption/
    """
    print("Problem: Rail Force Two")
    ciphertext = "MAYBETRYRAILS4AFTERTHISTCNMEASHIKWFUPVRLZGEUBOOJEOTEYOQRXDHD"[23:]
    rail_fence_decode(4, ciphertext)


if __name__ == "__main__":
    n = sys.argv
    if len(n) != 2:
        print(f"Usage solution.py <problem_id>")
        exit()
    prob = int(n[1])
    exec(f"problem{prob}()")
