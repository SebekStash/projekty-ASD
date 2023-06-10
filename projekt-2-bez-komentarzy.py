class HeapNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

class MinHeap:
    def __init__(self):
        self.heap = []
        self.size = 0

    def parent(self, pos):
        return (pos - 1) // 2

    def left_child(self, pos):
        return 2 * pos + 1

    def right_child(self, pos):
        return 2 * pos + 2

    def swap(self, a, b):
        self.heap[a], self.heap[b] = self.heap[b], self.heap[a]

    def heapify_after_add(self, pos):
        while pos > 0 and self.heap[pos] < self.heap[self.parent(pos)]:
            self.swap(pos, self.parent(pos))
            pos = self.parent(pos)

    def heapify_after_remove(self, pos):
        smallest = pos
        left = self.left_child(pos)
        right = self.right_child(pos)
        
        if left < self.size and self.heap[left] < self.heap[smallest]:
            smallest = left

        if right < self.size and self.heap[right] < self.heap[smallest]:
            smallest = right

        if smallest != pos:
            self.swap(pos, smallest)
            self.heapify_after_remove(smallest)

    def insert(self, node):
        self.heap.append(node)
        self.size += 1
        self.heapify_after_add(self.size - 1)

    def extract_min(self):
        if self.size == 0:
            return None
        else:
            root = self.heap[0]
            self.heap[0] = self.heap[self.size - 1]
            self.size -= 1
            self.heap.pop()
            
            self.heapify_after_remove(0)
            return root

def build_huffman_tree(data):

    frequency = {}
    for char in data:
        frequency[char] = frequency.get(char, 0) + 1

    heap = MinHeap()
    for char, freq in frequency.items():
        heap.insert(HeapNode(char, freq))

    while heap.size > 1:
        left_node = heap.extract_min()
        right_node = heap.extract_min()

        merged = HeapNode(None, left_node.freq + right_node.freq)
        merged.left = left_node
        merged.right = right_node
        heap.insert(merged)

    return heap.extract_min()

def generate_codes(root, current_code, codes):
    if root.char is not None:
        codes[root.char] = current_code
        return
    
    else:
        generate_codes(root.left, current_code + "0", codes)
        generate_codes(root.right, current_code + "1", codes)

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
