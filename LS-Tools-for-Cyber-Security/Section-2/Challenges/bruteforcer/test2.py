import subprocess

# Path to the bruteforcer program and the wordlist file
bruteforcer_path = './bruteforcer'
wordlist_path = 'wordlist.txt'

def run_bruteforce():
    # Read the wordlist file and extract passwords
    with open(wordlist_path, 'r') as file:
        passwords = [line.strip() for line in file]

    # Create the Popen object once outside the loop
    process = subprocess.Popen([bruteforcer_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    # Convert the list of passwords to a newline-separated string
    passwords_str = '\n'.join(passwords)

    # Execute the bruteforcer program and pass all passwords at once
    output, _ = process.communicate(input=passwords_str)
    print("\r", passwords_str,output, end = "")
    # Check if the program output contains the flag
    if 'flag' in output.lower():
        print("Correct password found:", output)
    else:
        print("Password not found.")

if __name__ == "__main__":
    run_bruteforce()

