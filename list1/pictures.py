'''
Zadanie 4
Używamy algo sliding window żeby policzyć liczbe zmian wymaganych dla kazdego dist elementowego podłańcucha(substring'a)
Po policzeniu pierwszego okienka nastepne okna liczymy patrzac na poprzednie na
pierwszy element poprzedniego okna i ostatni element bieżącego zeby obliczyc liczbe 0 (wymaganych zmian).
Trzymamy przy tym licznik jedynek ktory mowi nam ile ruchow musimy wykonac by usunac reszte jedynek z ciagu.
'''
def opt_changes(sequence: str, dist):
    current = sequence[0:dist].count('1')
    counter = current
    opt = current
    for i in range(1,len(sequence) - dist+1):
        current = current - int(sequence[i-1]) + int(sequence[i+dist-1])
        counter += int(sequence[i+dist-1])
        if current > opt:
            opt = current
    return dist - opt + counter - opt


def main():
    input = open("zad4_input.txt").read().split("\n")[:-1]
    res = ""
    for block in input:
        sequence,dist = block.split(" ")
        n_changes = opt_changes(sequence,int(dist))
        res = res + str(n_changes) + "\n"
    with open("zad4_output.txt", "w") as f:
        f.write(res)
        f.close()

if __name__ == "__main__":
    main()