import random
from sympy import randprime
import tkinter as tk
from tkinter import scrolledtext

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []
    
    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)
    


#%%
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def extended_euclid(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_euclid(b % a, a)
        return (g, x - (b // a) * y, y)

def modular_inverse(a, n): # find multiplicative inverse of a, mod n
    g, x, _ = extended_euclid(a, n)
    return x % n if g == 1 else None

def generate_keypair(p, q): #Generates The three numbers necessary to encrypt (e and n) and decrypt (d and n)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randint(1, phi)
    while gcd(e, phi) != 1:
        e = random.randint(1, phi)
    d = modular_inverse(e, phi)
    while d is None:
        e = random.randint(1, phi)
        d = modular_inverse(e, phi)
    return ((e, n), (d, n))

def encrypt(public_key, plaintext):
    e, n = public_key
    return [pow(ord(char), e, n) for char in plaintext] #ord(char) turns each character into a corresponding number

def decrypt(private_key, ciphertext):
    d, n = private_key
    plain = ([chr(pow(char, d, n)) for char in ciphertext])#chr() turns each number back into a character
    return ''.join(plain) #Puts back into plain language

#%%
class SecureMessaging:
    def __init__(self, root, user_name, encrypt, decrypt, public, private):
        self.root = root
        self.root.title(f"{user_name} - Secure Chat")
        self.encrypt = encrypt
        self.decrypt = decrypt
        self.user_name = user_name
        self.public_key = public
        self.private_key = private
        
        
        self.message_history = Stack()
        self.message_queue = Queue()
        self.urgent_messages = Queue()

        # Chat display
        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, width=50)
        self.chat_area.pack(padx=10, pady=10)
        self.chat_area.config(state='disabled')

        # Message input
        self.entry = tk.Entry(root, width=40)
        self.entry.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))

        #Buttons on Windows
        self.send_button = tk.Button(root, text="Send", command=self.send_message) #Calls on function to send_message
        self.send_button.pack(side=tk.LEFT, padx=10, pady=(0, 10))
        
        self.urgent_button = tk.Button(root, text='URGENT SEND', command=self.send_urgent)
        self.urgent_button.pack(side=tk.LEFT, padx=10, pady=(0, 10))

        self.history_button = tk.Button(root, text="View Last Sent", command=self.view_last_sent) #Calls on function to peek() and pop() last message in stack
        self.history_button.pack(side=tk.LEFT, padx=5, pady=(0, 10))

        self.decrypt_button = tk.Button(root, text="Decrypt Next", command=self.decrypt_next) #Decrypts the first message waiting in the queue to be decrypted
        self.decrypt_button.pack(side=tk.LEFT, padx=5, pady=(0, 10))
        
        self.keys_button = tk.Button(root, text='View Keys', command=self.display_keys)
        self.keys_button.pack(side=tk.LEFT, padx=5, pady=(0,10))

    def send_message(self):
        message = self.entry.get() #tkinter method that takes text from message box that user typed in
        if message.strip():  #Checks to make sure there is actually something to send, not whitespace or empty
            self.message_history.push(message) #Pushes onto Stack
            self.encrypt(message)
            self.entry.delete(0, tk.END) # Resets message after sending
            
    def send_urgent(self):
        urgent = True
        message = self.entry.get() #tkinter method that takes text from message box that user typed in
        if message.strip():  #Checks to make sure there is actually something to send, not whitespace or empty
            self.message_history.push(message) #Pushes onto Stack
            self.encrypt(message, urgent) #Ensures the message is put into Deque, since it's now urgent
            self.entry.delete(0, tk.END) # Resets message after sending

    def display_message(self, sender, message): #Function that is used everytime something needs to be displayed in chat window
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: {message}\n")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

    def display_keys(self):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"Public key: {self.public_key}\nPrivate Key: {self.private_key}")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)
    

    def receive_encrypted(self, encrypted_msg, urgent=False):
        if urgent:
            self.urgent_messages.enqueue(encrypted_msg)
        else:  
            self.message_queue.enqueue(encrypted_msg) #Adds encrypted message to queue, ready to be decrypted once button is pressed.
        self.display_message("New Encrypted Msg", str(encrypted_msg))

    def view_last_sent(self):
        if not self.message_history.isEmpty(): #Checks to see if Stack is empty
            last = self.message_history.pop() #Takes the top of stack to be displayed  (LIFO)
            self.display_message("History", last)

    def decrypt_next(self):
        message = "Nothing left to decrypt"
        if not self.urgent_messages.isEmpty():
            encrypted_msg = self.urgent_messages.dequeue()
            decrypted_msg = self.decrypt(encrypted_msg)
            self.display_message("Decrypted", decrypted_msg)
        elif not self.message_queue.isEmpty(): #Checks to see if Queue is empty
            encrypted_msg = self.message_queue.dequeue() #Takes the front of the queue (FIFO)
            decrypted_msg = self.decrypt(encrypted_msg)
            self.display_message("Decrypted", decrypted_msg)
        else:
            self.display_message("Error", message)

#Generates keys to be used by functions below
p1, q1 = randprime(100, 1000), randprime(100, 1000)
Person1_public, Person1_private = generate_keypair(p1, q1)

p2, q2 = randprime(100, 1000), randprime(100, 1000)
Person2_public, Person2_private = generate_keypair(p2, q2)



#These functions are used as arguments in each object from SecureMessaging Class to encrypt/decrypt with their respective keys
def encrypt_with_person2_key(msg, urgent=False):
    encrypted = encrypt(Person2_public, msg)
    Person1_window.display_message("You", msg)
    Person2_window.receive_encrypted(encrypted, urgent)

def encrypt_with_person1_key(msg, urgent=False):
    encrypted = encrypt(Person1_public, msg)
    Person2_window.display_message("You", msg)
    Person1_window.receive_encrypted(encrypted, urgent)

def decrypt_with_person1_key(encrypted):
    return decrypt(Person1_private, encrypted)

def decrypt_with_person2_key(encrypted):
    return decrypt(Person2_private, encrypted)

#Tkinter methods that create the main and secondary windows
root1 = tk.Tk()
root2 = tk.Toplevel()

Person1 = input("Enter Your Name: ")
Person2 = input("Enter Name of Person you are talking to: ")

Person1_window = SecureMessaging(root1, Person1, encrypt_with_person2_key, decrypt_with_person1_key, Person1_public, Person1_private)
Person2_window = SecureMessaging(root2, Person2, encrypt_with_person1_key, decrypt_with_person2_key, Person2_public, Person2_private)

root1.mainloop()
