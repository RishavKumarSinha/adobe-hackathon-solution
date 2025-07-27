import os
import sys

sys.path.append(os.path.abspath('challenge_1a'))
sys.path.append(os.path.abspath('challenge_1b'))

def main():
    challenge_to_run = os.getenv("CHALLENGE", "1a")

    if challenge_to_run == "1a":
        from challenge_1a import process_1a
        process_1a.main()
    elif challenge_to_run == "1b":
        from challenge_1b import process_1b
        process_1b.main()
    else:
        print(f"Invalid challenge specified: {challenge_to_run}. Use '1a' or '1b'.")
        sys.exit(1)

if __name__ == "__main__":
    main()