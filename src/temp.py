import os

newpath = r"./run_logs/"
if not os.path.exists(newpath):
    os.makedirs(newpath)
    print(f"Directory '{newpath}' created successfully.")
else:
    print(f"Directory '{newpath}' already exists.")
