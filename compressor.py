# Code from: https://github.com/Rijkaron/huffman/blob/master/main.py
# Accesed date: 27th April 2022
# By: Aron Rijken
# Changes: Added file to be compressed after saving from Turtle.

class Node:
    """A class used to represent a Node in the huffman binary tree"""
    def __init__(self, byte, frequency):
        # Constructor for the Node class
        self.byte = byte
        self.frequency = frequency
        self.leftChild = None
        self.rightChild = None

def build_tree(input_bytes: bytearray) -> Node:
    #Function to generate the huffman tree
    # Get the frequency per byte
    frequencies = {}
    for byte in input_bytes:
        frequencies[byte] = frequencies.get(byte, 0) + 1

    nodes = [Node(byte, frequencies[byte]) for byte in frequencies]

    while len(nodes) > 1:
        # Sort the nodes from low -> high by frequency
        nodes = sorted(nodes, key=lambda node: node.frequency)

        # Combine the 2 least common nodes to 1 new node
        new_node = Node(None, nodes[0].frequency + nodes[1].frequency)
        new_node.leftChild = nodes[0]
        new_node.rightChild = nodes[1]
        nodes.remove(nodes[0])
        nodes.remove(nodes[0])
        nodes.append(new_node)

    # Return the parent tree node
    return nodes[0]

def get_codes(node: Node) -> dict:
    # Get the codes corresponding to the bytes from the tree
    codes = {}

    def get_next_code(node: Node, prefix: str = ''):
        # Recursive function to loop through every node in the tree and add it to the 'codes' dictionary
        if node.byte is not None:
            codes[node.byte] = prefix
        else:
            get_next_code(node.leftChild, prefix + '0')
            get_next_code(node.rightChild, prefix + '1')

    get_next_code(node)
    return codes

def dec_to_bin(number: int, bits: int) -> str:
    # Converts an integer to a binary string with a certain bit length
    return ('0' * bits + bin(number)[2:])[-bits:]

def bin_string_to_bytearray(binary_string: str) -> bytearray:
    # Fill in bits if the binary string is not dividable by 8 (byte)
    binary_string += ((8 - len(binary_string)) % 8) * '0'

    # Generate the bytearray
    bytes_array = bytearray()
    for binary_byte in [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]:
        bytes_array.append(int(binary_byte, 2))

    return bytes_array

def compress_file(input_filename: str, output_filename: str):
    # Function to compress a file with the huffman algorithm Arguments
    with open(input_filename, 'rb') as input_file:
        input_bytes = bytearray(input_file.read())
        output_binary_string = ''

        # If the file is not empty
        if len(input_bytes) > 0:
            # Build the tree and get the codes from the tree
            tree = build_tree(input_bytes)
            codes = get_codes(tree)

            # Transform the bytes to their corresponding codes
            output = "".join([codes[byte] for byte in input_bytes])

            # Get the length of the code lengths.
            max_code_length_length = len(bin(max(map(lambda code: len(code), codes.values())))) - 2

            # Write the amount of codes
            output_binary_string += dec_to_bin(len(codes), 8)
            # Length cannot be 0, so there's the possibility to save 1 byte)
            output_binary_string += dec_to_bin(max_code_length_length - 1, 8)

            # Write all the codes to the output
            for i, (byte, code) in enumerate(codes.items()):
                output_binary_string += dec_to_bin(byte, 8)
                output_binary_string += dec_to_bin(len(code), max_code_length_length)
                output_binary_string += code

            # Write the length of the filler byte
            output_binary_string += dec_to_bin((len(output_binary_string) + len(output) + 3) % 8, 3)
            # Write the actual compressed data
            output_binary_string += output

        # Save the output to the file
        with open(output_filename, 'wb+') as output_file:
            output_file.write(bin_string_to_bytearray(output_binary_string))

if __name__ == '__main__':
    compress_file('working.txt', 'circle-compressed')