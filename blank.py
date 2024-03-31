from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os, json
def load_or_create_key(filename="config.dat"):
    try:
        with open(filename, "rb") as key_file:
            key = key_file.read()
        print("Masterkey detected and loaded.")
    except FileNotFoundError:
        key = AESGCM.generate_key(bit_length=256)
        with open(filename, "wb") as key_file:
            key_file.write(key)
        print("No masterkey detected. Generating a new one.")
        print(f"New masterkey (hex): {key.hex()}")
    return key
def transform(data, key, nonce=None, mode="encrypt"):
    handler = AESGCM(key)
    if mode == "encrypt":
        nonce = nonce or os.urandom(12)
        encrypted_data = handler.encrypt(nonce, data.encode(), None)
        return nonce, encrypted_data
    elif mode == "decrypt":
        decrypted_data = handler.decrypt(nonce, data, None)
        return decrypted_data.decode()
def save_data(encrypted_data_list, filename="encrypted_data.json"):
    with open(filename, "w") as file:
        json.dump(encrypted_data_list, file)
def load_data(filename="encrypted_data.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
def main():
    key_material = load_or_create_key()
    encrypted_data_list = load_data()
    while True:
        print("\n[1] Add and encrypt a password")
        print("[2] Show all services and their encrypted passwords")
        print("[3] Decrypt a password for a service")
        print("[4] Exit")
        choice = input("Your choice: ")
        if choice == "1":
            service = input("Service name: ")
            password = input("Password: ")
            nonce, encrypted_data = transform(password, key_material)
            encrypted_data_list.append((service, nonce.hex(), encrypted_data.hex()))
            save_data(encrypted_data_list)
            print(f"Password for '{service}' encrypted and stored.")
        elif choice == "2":
            if not encrypted_data_list:
                print("No passwords stored.")
            else:
                print("Services and their encrypted passwords:")
                for service, _, encrypted in encrypted_data_list:
                    print(f"'{service}': Encrypted password (hex) - {encrypted}")
        elif choice == "3":
            service_to_find = input("Service to decrypt password for: ")
            for service, nonce, encrypted in encrypted_data_list:
                if service == service_to_find:
                    nonce_bytes = bytes.fromhex(nonce)
                    encrypted_bytes = bytes.fromhex(encrypted)
                    decrypted_password = transform(encrypted_bytes, key_material, nonce=nonce_bytes, mode="decrypt")
                    print(f"Decrypted password for '{service}': {decrypted_password}")
                    break
            else:
                print("Service not found.")
        elif choice == "4":
            print("Exiting.")
            break
        else:
            print("Invalid option. Please try again.")
if __name__ == "__main__":
    main()