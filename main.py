import subprocess
import sys

def run_rq_generator(rq_number):
    """
    Runs the respective readme_rqX.py script for the selected RQ.
    """
    script_name = f"readme_rq{rq_number}.py"
    try:
        print(f"Running process for RQ{rq_number}")
        subprocess.run([sys.executable, script_name], check=True)
        print(f"Successfully generated results for RQ{rq_number}.")
    except FileNotFoundError:
        print(f"Error: {script_name} not found. Ensure it exists in the same directory as main.py.")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")

def main():
    while True:
        print("\n=== Main Menu ===")
        print("1. Generate results for RQ1")
        print("2. Generate results for RQ2")
        print("3. Generate results for RQ3")
        print("4. Generate results for RQ4")
        print("5. Generate results for RQ5")
        print("exit. Quit")
        
        choice = input("Choose an option (1-5/exit): ").strip().lower()
        
        if choice == "exit":
            print("Exiting...")
            break
        if choice not in ["1", "2", "3", "4", "5"]:
            print("Invalid choice. Try again.")
            continue
        
        run_rq_generator(choice)

if __name__ == "__main__":
    main()