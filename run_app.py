import os
import sys
import subprocess

def main():
    venv_python = sys.executable
    streamlit_script = "main.py"

    if not os.path.exists(streamlit_script):
        print(f"Streamlit entrypoint not found: {streamlit_script}")
        print("Make sure your app structure matches: root/main.py")
        sys.exit(1)

    print("Starting Streamlit interface...")
    print(f"Using Python: {venv_python}")
    print(f"Launching script: {streamlit_script}\n")

    try:
        subprocess.run(
            [venv_python, "-m", "streamlit", "run", streamlit_script],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Streamlit failed to start. Exit code: {e.returncode}")
    except KeyboardInterrupt:
        print("\nStreamlit server stopped by user.")

if __name__ == "__main__":
    main()


# Change ui to have tabs MICAP, each stage, and overview analysis