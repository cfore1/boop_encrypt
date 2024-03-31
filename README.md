# boop_encrypt
Simple password manager that uses AES (Advanced Encryption Standard) encryption. In order to decrypt the passwords stored in .json file, the key, (config.dat) must be present.
One key is intended as a masterkey used for multiple passwords. These passwords are decrypted and stored in a .json file and can only be accessed with the masterkey created during the session relating to said passwords.
If no key is present, the program creates one. Keys are persistent with .json files, meaning that config.dat can be removed from the machine, stored securely and dropped into the repo to decrypt.
