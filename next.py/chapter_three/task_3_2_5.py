
def read_file(file_name):
    content = "__CONTENT_START__\n"
    file = None
    try:
        file = open(file_name, "r")

    except FileNotFoundError:
        content += "__NO_SUCH_FILE__"

    else:
        content += file.read()

    finally:
        content += "\n__CONTENT_END__"

        if file:
            file.close()

    return content


print(read_file("one_lined_file.txt"))
