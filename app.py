import os
import json
import subprocess
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

DATA_DIR = "/data"  # Ensure all tasks operate within this directory

# Ensure /data exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

@app.route('/run', methods=['POST'])
def run_task():
    task_description = request.args.get('task', '')

    if not task_description:
        return jsonify({"error": "Task description is required"}), 400

    try:
        # Process the task (You'll implement actual handlers here)
        result = process_task(task_description)

        return jsonify({"message": "Task executed successfully", "result": result}), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/read', methods=['GET'])
def read_file():
    file_path = request.args.get('path', '')

    # Security check: Prevent accessing files outside /data
    if not file_path.startswith(DATA_DIR):
        return jsonify({"error": "Access to this file is not allowed"}), 403

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    return send_file(file_path, as_attachment=False), 200

def process_task(task):
    """
    Parses the task description and executes the corresponding operation.
    """
    if "format" in task.lower() and "prettier" in task.lower():
        return run_prettier()
    elif "count" in task.lower() and "wednesdays" in task.lower():
        return count_wednesdays()
    elif "sort" in task.lower() and "contacts" in task.lower():
        return sort_contacts()
    else:
        raise ValueError("Unknown task description")

def run_prettier():
    """
    Formats the /data/format.md file using Prettier.
    """
    file_path = os.path.join(DATA_DIR, "format.md")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")
    
    subprocess.run(["npx", "prettier@3.4.2", "--write", file_path], check=True)
    return f"Formatted {file_path}"

def count_wednesdays():
    """
    Counts the number of Wednesdays in /data/dates.txt.
    """
    file_path = os.path.join(DATA_DIR, "dates.txt")
    output_file = os.path.join(DATA_DIR, "dates-wednesdays.txt")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")

    with open(file_path, 'r') as f:
        dates = f.readlines()

    from datetime import datetime

    wednesdays = sum(1 for date in dates if datetime.strptime(date.strip(), "%Y-%m-%d").weekday() == 2)

    with open(output_file, 'w') as f:
        f.write(str(wednesdays))

    return f"Wednesdays counted and written to {output_file}"

def sort_contacts():
    """
    Sorts /data/contacts.json by last_name, then first_name.
    """
    file_path = os.path.join(DATA_DIR, "contacts.json")
    output_file = os.path.join(DATA_DIR, "contacts-sorted.json")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")

    with open(file_path, 'r') as f:
        contacts = json.load(f)

    contacts.sort(key=lambda x: (x.get("last_name", ""), x.get("first_name", "")))

    with open(output_file, 'w') as f:
        json.dump(contacts, f, indent=2)

    return f"Contacts sorted and saved to {output_file}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
