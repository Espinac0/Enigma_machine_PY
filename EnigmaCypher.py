abcd = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
actual = 0
class Rotor:
    def __init__(self, permutacion_ini, to, ringstellung, grundstellung):
        self.permutacion_ini = ""
        self.to =  ord(to.upper()) - ord('A')
        self.position = 0
        self.ringstellung = ord(ringstellung.upper()) - ord('A')
        self.grundstellung = ord(grundstellung.upper()) - ord('A')
        self.position = self.grundstellung 
        self.to = (self.to + self.grundstellung - self.ringstellung + 26) % 26 
        aux = permutacion_ini
        for i in range(self.ringstellung):
            aux = aux[25] + aux[0:25]
        for j in range(26):
            codigo_unicode = (ord(aux[j]) + self.ringstellung - ord ('A')) % 26
            siguiente_letra = chr(ord('A') + codigo_unicode)
            self.permutacion_ini += siguiente_letra

    def rotate(self):
        self.position = (self.position + 1) % 26

    def substitute(self, letter):
        if actual == 1:
            index = (ord(letter) - ord('A')) % 26
        elif actual == 2:
            index = (ord(letter) - ord('A')) % 26
        else:
            index = (ord(letter) - ord('A') + self.position) % 26
        
        
        return self.permutacion_ini[index]
    
    def substitute2(self, letter):
        if actual == 1:
            index = self.permutacion_ini.index(chr((ord(letter) + self.position - ord('A'))%26 + ord('A')))
        elif actual == 2:
            index = self.permutacion_ini.index(letter)
        else:
            index = self.permutacion_ini.index(letter)
        return abcd[index % 26]
    
    def is_at_notch(self):
        return self.position == self.to

class Reflector:
    def __init__(self, permutacion_ini):
        self.permutacion_ini = permutacion_ini

    def reflect(self, index, valor):
        return self.permutacion_ini[(ord(index) - ord('A') - valor + 26)%26]

class Maquina:
    def __init__(self, rotor1, rotor2, rotor3, reflector):
        self.rotor1 = rotor1
        self.rotor2 = rotor2
        self.rotor3 = rotor3
        self.reflector = reflector

    def encrypt(self, plaintext):
        ciphertext = ""
        global actual
        for letter in plaintext:
            if letter.isalpha():
                
                self.rotor3.rotate()
                if self.rotor3.is_at_notch():
                    self.rotor2.rotate()
                elif self.rotor2.is_at_notch():
                    self.rotor1.rotate()
                    self.rotor2.rotate()
                actual = 3
                encrypted_letter = self.rotor3.substitute(letter)
                actual = 2


                encrypted_letter = self.rotor2.substitute(abcd[(abcd.index(encrypted_letter) - self.rotor3.position + self.rotor2.position + 26) % 26])
                actual = 1
                encrypted_letter = self.rotor1.substitute(abcd[(abcd.index(encrypted_letter) - self.rotor2.position + self.rotor1.position + 26) % 26])
                encrypted_letter = self.reflector.reflect(encrypted_letter, rotor1.position)
                
                encrypted_letter = self.rotor1.substitute2(encrypted_letter)
                actual = 2
                encrypted_letter = self.rotor2.substitute2(abcd[(abcd.index(encrypted_letter) - self.rotor1.position + self.rotor2.position + 26) % 26])
                actual = 3
                encrypted_letter = self.rotor3.substitute2(abcd[(abcd.index(encrypted_letter) - self.rotor2.position + self.rotor3.position + 26) % 26])
                
                ciphertext += abcd[(abcd.index(encrypted_letter) - self.rotor3.position + 26) % 26]
                
                
                
        return ciphertext

# ejemplo
rotor1_permutacion_ini = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
rotor1_to = 'Q'
rotor1_ringstellung = 'G'
rotor1_grundstellung = 'E'

rotor2_permutacion_ini = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
rotor2_to = 'E'
rotor2_ringstellung = 'M'
rotor2_grundstellung = 'N'

rotor3_permutacion_ini = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
rotor3_to = 'V'
rotor3_ringstellung = 'A'
rotor3_grundstellung = 'I'

reflector_permutacion_ini = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

rotor1 = Rotor(rotor1_permutacion_ini, rotor1_to, rotor1_ringstellung, rotor1_grundstellung)
rotor2 = Rotor(rotor2_permutacion_ini, rotor2_to, rotor2_ringstellung, rotor2_grundstellung)
rotor3 = Rotor(rotor3_permutacion_ini, rotor3_to, rotor3_ringstellung, rotor3_grundstellung)
reflector = Reflector(reflector_permutacion_ini)

enigma = Maquina(rotor1, rotor2, rotor3, reflector)

textonormal = "MEXENCANTAXPROGRAMARXENXPYTHON"
textocifrado = enigma.encrypt(textonormal)
print(textocifrado)
