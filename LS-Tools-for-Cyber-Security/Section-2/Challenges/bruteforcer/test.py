import subprocess

# Path to the bruteforcer program and the wordlist file
bruteforcer_path = './bruteforcer'
wordlist_path = 'wordlist.txt'

def run_bruteforce():
    # Read the wordlist file and extract passwords
    with open(wordlist_path, 'r') as file:
        passwords = [line.strip() for line in file]

    for password in passwords:
        # Execute the bruteforcer program with the current password as input
        process = subprocess.Popen([bruteforcer_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        output, _ = process.communicate(input=password)
        print('\r',password,output, end='')
        # Check if the program output contains the flag
        if 'flag' in output.lower():
            print(f"Correct password found: {password}")
            print("Flag:", output)
            break

if __name__ == "__main__":
    run_bruteforce()

