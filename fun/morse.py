def morse_to_text(morse_code):
    # Create a dictionary mapping morse code to characters
    morse_code_dict = {
        '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F',
        '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
        '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R',
        '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
        '-.--': 'Y', '--..': 'Z', '.----': '1', '..---': '2', '...--': '3',
        '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
        '----.': '9', '-----': '0', '/': ' ', '//': '\n'
    }
    
    # Split the morse code string into a list of morse code words
    morse_code_words = morse_code.split('/')
    
    # Initialize an empty list to store the characters for each morse code word
    characters_list = []
    
    # Iterate through each morse code word
    for word in morse_code_words:
        # Split the word into a list of morse code characters
        morse_code_chars = word.split()
        
        # Initialize an empty list to store the characters for this word
        word_characters_list = []
        
        # Iterate through each morse code character
        for char in morse_code_chars:
            # If the character is not in the dictionary, ignore it
            if char not in morse_code_dict:
                continue
            
            # Add the character to the list
            word_characters_list.append(morse_code_dict[char])
        
        # Join the list of characters for this word into a single string and add it to the list of character strings
        characters_list.append(''.join(word_characters_list))
    
    # Join the list of character strings into a single string and return it
    return ' '.join(characters_list)


def text_to_morse(text):
    # Create a dictionary mapping characters to morse code
    morse_code_dict = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
        '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
        '9': '----.', '0': '-----', ' ': '/', '\n': '//'
    }
    
    # Initialize an empty list to store the morse code for each character
    morse_code_list = []
    
    # Iterate through each character in the text
    for char in text:
        # Convert the character to uppercase
        char = char.upper()
        
        # If the character is not in the dictionary, ignore it
        if char not in morse_code_dict:
            continue
        
        # Add the morse code for the character to the list
        morse_code_list.append(morse_code_dict[char])
    
    # Join the list of morse code strings into a single string and return it
    return ' '.join(morse_code_list)


