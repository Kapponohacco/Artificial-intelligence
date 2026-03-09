'''
Algorytm dynamiczny
W jednej liscie zapisujemy sumę kwadratow dlugosci, w drugiej podział na słowa.
Wszystkie poprawne słowa trzymamy w secie, jest troche gorszym wyjsciem od drzewa trie, ale jest wystarczająco dobry.
'''

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
    data = open("zad2_input.txt", encoding='utf-8').read().split("\n")[:-1]
    valid_words = set(open("words_for_ai1.txt", encoding="utf-8").read().split("\n"))
    res = ""
    for line in data:
       sentence = split_line(line, valid_words)
       res = res + sentence + "\n"

    with open("zad2_output.txt", "w", encoding='utf-8') as f:
       f.write(res)
       f.close()


if __name__ == "__main__":
    main()