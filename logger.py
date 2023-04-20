
FILE_PATH = ""


def log(prompt, response, user):
    write_on_file(str(user) + prompt + "\n" + response)


def write_on_file(file, name='log'):
    # Write a file with a standard name
    filename = name + '.md'
    try:
        with open(FILE_PATH + filename, 'a', encoding='utf-8-sig') as buffer:
            buffer.write(file)
        print("Data saved successfully!")
    except Exception as e:
        print("Couldn't save data!")
        print(e)
