import random
import argparse

def split_line_random(sentence, valid_words):
    n = len(sentence)
    
    def find_path(start_idx):
        if start_idx == n:
            return []
        
        candidates = []
        for end_idx in range(start_idx + 1, n + 1):
            frag = sentence[start_idx:end_idx]
            if frag in valid_words:
                candidates.append(frag)
        
        if not candidates:
            return None
        

        random.shuffle(candidates)
        
        for word in candidates:
            result = find_path(start_idx + len(word))
            if result is not None:
                return [word] + result
        
        return None

    res = find_path(0)
    return str(" ".join(res) if res else "")

def split_line(sentence, valid_words):
    n = len(sentence)
    squares = [0] * (n + 1)
    d = [""] * (n + 1)

    for i in range(n):
        for j in range(i + 1, n + 1):
            frag = sentence[i:j]
            if frag in valid_words:
                new_squares = squares[i] + len(frag) ** 2
                if new_squares > squares[j]:
                    squares[j] = new_squares
                    if d[i]:
                        d[j] = d[i] + " " + frag
                    else:
                        d[j] = frag

    return d[n]

def main():
    args = argparse.ArgumentParser()
    args.add_argument("--random", action = argparse.BooleanOptionalAction, default=False)
    data = open("tadeusz_input.txt", encoding='utf-8').read().split("\n")[:-1]
    valid_words = set(open("words_for_ai1.txt", encoding="utf-8").read().split("\n"))
    res = ""
    args = args.parse_args()

    if args.random == True:
        function = split_line_random
        out = "tadeusz_output_random.txt"
        print("yipiee")
    else:
        function = split_line
        out = "tadeusz_output.txt"

    for line in data:
       sentence = function(line, valid_words)
       res = res + sentence + "\n"

    with open(out, "w", encoding='utf-8') as f:
       f.write(res)
       f.close()


if __name__ == "__main__":
    main()