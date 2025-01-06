import sys

def main():
    # Check if an argument is provided
    if len(sys.argv) < 2:
        print("Usage: python src.main <arg>")
        sys.exit(1)

    # Access the argument
    argument = sys.argv[1]
    
    # Process the argument (convert to integer, for example)
    try:
        number = int(argument)
        print(f"Received number: {number}")
        print(f"Square of the number: {number ** 2}")
    except ValueError:
        print("Error: Argument must be a valid integer.")

if __name__ == "__main__":
    main()
