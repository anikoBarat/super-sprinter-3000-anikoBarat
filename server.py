from flask import Flask, render_template, redirect, request, session

server_object = Flask(__name__)


@server_object.route("/")
def route_list():
    with open("supersprinter.csv", "r") as f:
        content_to_read = list()
        for line in f:
            line = line.split(";")
            content_to_read.append(line)
    return render_template("list.html", content=content_to_read)


@server_object.route("/list")
def route_list2():
    return redirect("/")


@server_object.route("/story")
def route_addstory():
    story_text = ""
    if "story" in session:
        story_text = session["story"]
    return render_template(
        "form.html",
        title_of_head="Add new story",
        button_label="Create",
        business_value=1000,
        estimation=2.5,
        id='0')


@server_object.route("/story/<int:story_id>", methods=["GET"])
def route_editstory(story_id):
    cube = ""
    with open("supersprinter.csv", "r") as f:
        for line in f:
            line = line.split(";")
            if line[0] == str(story_id):
                cube = line
                break
    return render_template(
        "form.html",
        title_of_head="Edit story",
        button_label="Update",
        title=cube[1],
        story=cube[2],
        acceptance=cube[3],
        business_value=cube[4],
        estimation=cube[5],
        status=cube[6][:-1],
        id=cube[0])


@server_object.route("/save-story-<id>", methods=["POST"])
def route_savestory(id):
    print("POST request received!")
    list_of_keys = ["title", "story", "criteria", "businessvalue", "estimation", "status"]
    if id == "0":
        with open("supersprinter.csv", "r") as f:
            max_id = 0
            for line in f:
                line = line.split(";")
                if int(line[0]) > max_id:
                    max_id = int(line[0])
        with open("supersprinter.csv", "a") as f:
            content_to_save = str(max_id + 1) + ";"
            i = 0
            while i < len(list_of_keys) - 1:
                content_to_save += request.form[list_of_keys[i]] + ";"
                i += 1
            content_to_save += request.form[list_of_keys[i]] + "\n"
            f.write(content_to_save)
        return redirect("/")
    else:
        list_to_modify = list()
        with open("supersprinter.csv", "r") as f:
            for line in f:
                line = line.split(";")
                if line[0] == id:
                    i = 0
                    while i < len(list_of_keys):
                        line[i + 1] = request.form[list_of_keys[i]]
                        i += 1
                    line[i] += "\n"
                list_to_modify.append(line)
        with open("supersprinter.csv", "w") as f:
            for line in list_to_modify:
                content_to_save = ""
                for item in line:
                    content_to_save += item + ";"
                content_to_save = content_to_save[:-1]
                f.write(content_to_save)
        return redirect("/")


@server_object.route("/delete-<id>", methods=["GET"])
def route_deletestory(id):
    print("POST request received!")
    list_of_keys = ["title", "story", "criteria", "businessvalue", "estimation", "status"]
    list_to_modify = list()
    with open("supersprinter.csv", "r") as f:
        for line in f:
            line = line.split(";")
            if line[0] != id:
                list_to_modify.append(line)
    with open("supersprinter.csv", "w") as f:
        for line in list_to_modify:
            content_to_save = ""
            for item in line:
                content_to_save += item + ";"
            content_to_save = content_to_save[:-1]
            f.write(content_to_save)
    return redirect("/")


if __name__ == "__main__":
    server_object.secret_key = "server_object_magic"  # Change the content of this string
    server_object.run(
        debug=True,
        port=5000
    )
