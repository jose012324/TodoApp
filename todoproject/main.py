import subprocess

def run_django_server():
    try:
        print("🚀 Running: python manage.py runserver")
        subprocess.run(["python", "manage.py", "runserver"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running server: {e}")

if __name__ == "__main__":
    run_django_server()
