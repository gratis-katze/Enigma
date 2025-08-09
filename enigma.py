
rotor_dict = {"I": ["EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"],
              "II": ["AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"],
              "III": ["BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"],
              "ref": "ABCDEFGDIJKGMKMIEBFTCVVJAT",
              "ABC": ["ABCDEFGHIJKLMNOPQRSTUVWXYZ"] }


def rotate(rotor_position: str):
    index = (rotor_dict["ABC"][0].index(rotor_position) + 1) % len(rotor_dict["ABC"][0])
    rotor_position = rotor_dict["ABC"][0][index]
    return rotor_position

def next_letter(letter_current: str, rotor_position_current: int, rotor_position_next: int, rotor_current: str, rotor_next: str):
    index = (rotor_dict[rotor_current][0].index(letter_current) - rotor_dict["ABC"][0].index(rotor_position_current)) % len(rotor_dict["ABC"][0])
    letter_next = rotor_dict[rotor_next][0][(index + rotor_dict["ABC"][0].index(rotor_position_next)) % len(rotor_dict["ABC"][0])]
    return letter_next

def reflect(letter, rotor_position):
    index = (rotor_dict["ABC"][0].index(letter) - rotor_dict["ABC"][0].index(rotor_position)) % len(rotor_dict["ABC"][0])
    reflector_letter = rotor_dict["ref"][index]
    if index == rotor_dict["ref"].index(reflector_letter):
        backward_index = rotor_dict["ref"].rindex(reflector_letter)
    else:
        backward_index = rotor_dict["ref"].index(reflector_letter)
    letter = rotor_dict["ABC"][0][(backward_index + rotor_dict["ABC"][0].index(rotor_position)) % len(rotor_dict["ABC"][0])]
    return letter

def Enigma(rotors, positions, message):
    
    message_out = ""
    
    rotor_right_position = positions[2]
    rotor_center_position = positions[1]
    rotor_left_position = positions[0]

    letter_counter = 0
    counters = [0, 0, 0, 0]
    
    for letter in message:
        if letter.isalpha():
            print("----------------------------------------------------------------------------------")
            letter_counter += 1
            capital_letter = True
            if letter.islower():
                capital_letter = False
                letter = letter.upper()
            
            letter_history = [letter]

            # always rotate right rotor
            rotor_right_position = rotate(rotor_right_position)

            print("Rotor positions:", rotor_left_position, rotor_center_position, rotor_right_position)

            # right rotor
            letter = next_letter(letter, "A", rotor_right_position, "ABC", rotors[2])
            letter_history.append(letter)

            # center rotor
            if rotor_center_position == rotor_dict[rotors[1]][1]:
                counters[2] += 1                
                rotor_center_position = rotate(rotor_center_position)
                rotor_left_position = rotate(rotor_left_position)

            letter = next_letter(letter, rotor_right_position, rotor_center_position, "ABC", rotors[1])
            letter_history.append(letter)

            # left rotor
            if rotor_left_position == rotor_dict[rotors[0]][1]:
                counters[3] += 1
                rotor_left_position = rotate(rotor_left_position)

            letter = next_letter(letter, rotor_center_position, rotor_left_position, "ABC", rotors[0])
            letter_history.append(letter)

            # reflector
            letter = reflect(letter, rotor_left_position)
            letter_history.append(letter)

            # left rotor backwards
            letter = next_letter(letter, rotor_left_position, rotor_center_position, rotors[0], "ABC")
            letter_history.append(letter)

            # center rotor backwards
            letter = next_letter(letter, rotor_center_position, rotor_right_position, rotors[1], "ABC")
            letter_history.append(letter)

            # right rotor backwards
            letter = next_letter(letter, rotor_right_position, "A", rotors[2], "ABC")
            letter_history.append(letter)

            if rotor_right_position == rotor_dict[rotors[2]][1]:
                counters[1] += 1
                rotor_center_position = rotate(rotor_center_position)

            print("Start: {} -> III: {} -> II: {} -> I: {} -> Reflector: {} -> I: {} -> II: {} -> III: {}".format(*letter_history))
            
            if not capital_letter:
                letter = letter.lower()
            message_out += letter

        else: 
            message_out += letter

    return message_out, letter_counter, counters

print("Please enter input message:")
message_in = input()

rotors = ["I", "II", "III"]
positions = "MCK"

message_out, letter_counter, counters = Enigma(rotors, positions, message_in)

print("")
print("Notches appeared (left center right): {} {} {}".format(counters[3], counters[2], counters[1]))
print("")
print("Output message ({} letters, {} total characters): ".format(letter_counter, len(message_in)))
print("")
print("##################################################################################")
print(message_out)
print("##################################################################################")