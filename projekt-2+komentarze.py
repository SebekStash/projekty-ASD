# Węzły(nody) kopca na który składają się litera/znak oraz ilość ile razy występuje
class HeapNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq

        # Służy do porównań wartości nodów
        self.left = None
        self.right = None

# Umożliwia porównanie w lini 47 Nodów, który z nich ma większą wartość.
    def __lt__(self, other):
        return self.freq < other.freq


class MinHeap:
    def __init__(self):

        # Deklaracja tablicy danych z których buowany jest kopiec
        self.heap = []

        # Rozmiar kopca
        self.size = 0

    # Zdefiniuj rodzica danego noda
    def parent(self, pos):
        return (pos - 1) // 2
    # Definicja rodzica: (i - 1) / 2

    # Zdefiniuj lewe dziecko danego noda
    def left_child(self, pos):
        return 2 * pos + 1
    # Definicja dziecka lewego: (2 * i) + 1

    # Zdefiniuj prawe dziecko danego noda
    def right_child(self, pos):
        return 2 * pos + 2
    # Definicja dziecka prawego: (2 * i) - 1

    # Zmiana elementów miejscami
    def swap(self, a, b):
        self.heap[a], self.heap[b] = self.heap[b], self.heap[a]

    # Przywróc wartość kopca po dodaniu elementu 
    # Dzieje się po zsumowaniu dwóch wcześniej usuniętych nodów
    def heapify_after_add(self, pos):
        # dopóki nie jest na pozycji korzenia i jest mniejszy od swojego rodzica
        while pos > 0 and self.heap[pos] < self.heap[self.parent(pos)]:
            # Zamieniaj miejscami z rodzicem
            self.swap(pos, self.parent(pos))
            # Dajemy znać w kodzie że node przeszedł na pozycję rodzica
            pos = self.parent(pos)

    # Przywróc wartość kopca po usunięciu noda
    # Dzieje się po usunięciu korzenia z kopca, a pierwszy pos to korzeń
    def heapify_after_remove(self, pos):
        smallest = pos
        left = self.left_child(pos)
        right = self.right_child(pos)

        # Sprawdź czy i gdzie zrobić zmianę rodzica. Z prawym dzieckiem czy lewym.
        
        # Jeśli lewe dziecko jest mniejesze niż rodzic oznacz do zamiany
        if left < self.size and self.heap[left] < self.heap[smallest]:
            smallest = left

        # Jeśli prawe dziecko jest jeszcze mniejsze niż lewe dziecko oznacz że tu trzeba dokonać zamianę z rodzicem
        # Jeśli lewe dziecko i prawe dziecko są sobie równe to zmiana nastąpi dla lewego dziecka
        if right < self.size and self.heap[right] < self.heap[smallest]:
            smallest = right

        # Jeśli najmniejszym nodem nie jest rodzic dokonaj wcześniej określonej zamiany.
        if smallest != pos:
            self.swap(pos, smallest)
            # Powtórz sprawdzanie czy kopiec jest ok tym razem dla noda który powędrował na dół.
            self.heapify_after_remove(smallest)

    # Dodaj node do kopca
    def insert(self, node):
        self.heap.append(node)
        self.size += 1
        # Przywróć kopiec
        self.heapify_after_add(self.size - 1)

    # Wydostań korzeń
    def extract_min(self):
        # Jeśli kopiec pusty zwóć nic
        if self.size == 0:
            return None
        else:
            # Zapisz korzeń
            root = self.heap[0]
            # Wstaw ostatni node w miejsce korzenia
            self.heap[0] = self.heap[self.size - 1]
            self.size -= 1
            self.heap.pop()
            
            # Przywróc kopiec dla korzenia po usunięciu elementu.
            self.heapify_after_remove(0)
            return root

# Zbuduj drzewo Huffmana
def build_huffman_tree(data):

    # Zlicz jak często występują poszczególne znaki
    frequency = {}
    for char in data:
        frequency[char] = frequency.get(char, 0) + 1

    # Utwórz kopiec MIN
    heap = MinHeap()
    for char, freq in frequency.items():
        heap.insert(HeapNode(char, freq))

    # Dopóki kopiec nie jest pusty Wyciągaj najmniejsze wartości (korzeń)
    while heap.size > 1:
        left_node = heap.extract_min()
        right_node = heap.extract_min()

        # Utwórz nowy node z dwóch usuniętych z kopca i dodaj go na kopiec
        merged = HeapNode(None, left_node.freq + right_node.freq)
        merged.left = left_node
        merged.right = right_node
        heap.insert(merged)

    # Zwróć drzewo
    return heap.extract_min()

# Kodowanie znaków na podstawie otrzymanego drzewa
# Funkcja przechodzi po drzewie i tworzy kody znaków
# Kody są przechowywane w tablicy asocjacyjnej
def generate_codes(root, current_code, codes):
    if root.char is not None:
        codes[root.char] = current_code
        return
    
    else:
        generate_codes(root.left, current_code + "0", codes)
        generate_codes(root.right, current_code + "1", codes)

# Funkcja kodująca dane wejściowe
# Dla każdego znaku w danych podstaw odpowiedni kod znaku; Zwróc zakodowane dane
def encode_string(data, codes):
    encoded_data = ""
    for char in data:
        encoded_data += codes[char]
    return encoded_data


def huffman_encoding(data):
    # Jeśli nie ma co zakodować zwróć nic.
    if len(data) == 0:
        return "", None, {}

    else:
        # Zbuduj drzewo huffmana
        root = build_huffman_tree(data)
        
        # Odczytaj kody znaków
        codes = {}
        generate_codes(root, "", codes)
        
        # Zakoduj dane wejściowe
        encoded_data = encode_string(data, codes)
        return encoded_data, root, codes


# Zapis do pliku słownika
def write_to_file_txt(codes, output_file_txt):
    with open(output_file_txt, 'w') as file:
        for char, code in codes.items():
            file.write(f"{char}:{code}\n")

# Zapis do pliku kodu binarnego
def write_to_file_binary(encoded_data, output_file_txt):
    binary_data = bytes([int(encoded_data[i:i+8], 2) for i in range(0, len(encoded_data), 8)])
    with open(output_file_txt, 'ab') as file:
        file.write(binary_data)


# Odczyt z pliku
def read_file(input_file):
    with open(input_file, 'r') as file:
        data = file.read().replace('\n', '')
    return data

input_file = "input.txt"
output_file_txt = "output.txt"

data = read_file(input_file)
encoded_data, tree_root, codes = huffman_encoding(data)
write_to_file_txt(codes, output_file_txt)
write_to_file_binary(encoded_data, output_file_txt)

# Jakbym nie próbował to nie umiem tego binarnie zapisać by zajmowało mniej miejsca, a czas goni, może to kwestia języka :(

# data = "Banany w rabarbarze"
# encoded_data, tree_root, codes = huffman_encoding(data)

# print("Dane wejściowe:", data)
# print("Zakodowane:", encoded_data)
# print("Kody:", codes)
# # for char, code in codes.items():
# #     print(char, ":", code)
