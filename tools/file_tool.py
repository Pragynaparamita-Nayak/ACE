from datetime import datetime

virtual_files = {}

def write_file(filename, content):

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    virtual_files[filename] = {
        "content": content,
        "created_at": now,
        "updated_at": now
    }

    return f"{filename} written successfully"


def read_file(filename):

    file_data = virtual_files.get(filename)

    if file_data is None:
        return "File not found"

    return file_data["content"]


def ls():
    return list(virtual_files.keys())


def edit_file(filename, new_content):

    if filename in virtual_files:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        virtual_files[filename]["content"] = new_content
        virtual_files[filename]["updated_at"] = now

        return f"{filename} updated successfully"

    return "File not found"


def get_file_metadata(filename):

    if filename in virtual_files:
        return {
            "created_at": virtual_files[filename]["created_at"],
            "updated_at": virtual_files[filename]["updated_at"]
        }

    return "File not found"