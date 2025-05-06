import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext, END
import signal

def list_drives():
    result = subprocess.run(
        ["lsblk", "-dn", "-o", "NAME,SIZE,MODEL"],
        stdout=subprocess.PIPE, text=True
    )
    drives = []
    for line in result.stdout.strip().split('\n'):
        if not line:
            continue
        parts = line.split(None, 2)
        if len(parts) < 2:
            continue
        name, size = parts[0], parts[1]
        model = parts[2] if len(parts) > 2 else ""
        if name.startswith("loop") or name.startswith("ram"):
            continue
        drives.append((f"/dev/{name}", f"{size} {model}".strip()))
    return drives

def run_ventoyplugson(selected_drive, output_widget, exit_btn):
    # Ask for sudo password
    password = simpledialog.askstring("Sudo Password", "Enter your sudo password:", show='*')
    if password is None:
        output_widget.insert(END, "Cancelled by user.\n")
        return

    # Prepare the command
    cmd = ["sudo", "-S", "./VentoyPlugson.sh", selected_drive]
    try:
        os.chdir("/opt/ventoy/")
    except Exception as e:
        output_widget.insert(END, f"Failed to change directory: {e}\n")
        return

    # Start the process
    try:
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        # Store the process object on the exit button for later access
        exit_btn.proc = proc

        # Send the password and read output
        try:
            proc.stdin.write(password + "\n")
            proc.stdin.flush()
        except Exception as e:
            output_widget.insert(END, f"Failed to send password: {e}\n")
            return

        for line in proc.stdout:
            output_widget.insert(END, line)
            output_widget.see(END)
        proc.wait()
        if proc.returncode == 0:
            output_widget.insert(END, "\nProcess completed successfully.\n")
        else:
            output_widget.insert(END, f"\nProcess exited with code {proc.returncode}.\n")
    except Exception as e:
        output_widget.insert(END, f"Failed to run VentoyPlugson.sh: {e}\n")

def on_exit_process(exit_btn, output_widget):
    proc = getattr(exit_btn, 'proc', None)
    if proc and proc.poll() is None:
        proc.send_signal(signal.SIGINT)
        output_widget.insert(END, "\nSent Ctrl+C (SIGINT) to the process.\n")
    else:
        output_widget.insert(END, "\nNo running process to terminate.\n")

def on_run():
    selected = drive_var.get()
    if not selected:
        messagebox.showwarning("No drive selected", "Please select a drive.")
        return
    # Open a new window for output
    output_win = tk.Toplevel(root)
    output_win.title("Ventoy Plugson Output")
    output_text = scrolledtext.ScrolledText(output_win, width=100, height=30)
    output_text.pack(fill="both", expand=True)
    output_text.insert(END, f"Running VentoyPlugson.sh for {selected}...\n\n")
    exit_btn = tk.Button(output_win, text="Exit", command=lambda: on_exit_process(exit_btn, output_text))
    exit_btn.pack(pady=5)
    root.after(100, lambda: run_ventoyplugson(selected, output_text, exit_btn))

# Tkinter GUI
root = tk.Tk()
root.title("Ventoy Plugson Launcher")

tk.Label(root, text="Select Drive:").pack(pady=5)

drives = list_drives()
drive_var = tk.StringVar()
drive_combo = ttk.Combobox(root, textvariable=drive_var, state="readonly")
drive_combo['values'] = [f"{d[0]} ({d[1]})" for d in drives]
drive_combo.pack(pady=5, padx=10)

def update_drive_var(event):
    idx = drive_combo.current()
    if idx >= 0:
        drive_var.set(drives[idx][0])

drive_combo.bind("<<ComboboxSelected>>", update_drive_var)

run_btn = tk.Button(root, text="Run Ventoy Plugson", command=on_run)
run_btn.pack(pady=10)

exit_btn_main = tk.Button(root, text="Exit", command=root.destroy)
exit_btn_main.pack(pady=5)

root.mainloop()