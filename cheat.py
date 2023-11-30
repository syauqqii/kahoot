from json import dump, load
from requests import get
from os import mkdir, path, system

def clearScreen():
    system("clear||cls")

def printAnswers():
    print(f"\n > Answer Information")
    for i, (key, value) in enumerate(answers.items()):
        separator = " :" if i < 9 else ":"
        if type(value) == list:
            print('   - ', key, separator, f"{', '.join(value)}")
        else:
            print('   - ', key, separator, f"{value}")

if __name__ == '__main__':
    try:
        clearScreen()
        API         = 'https://play.kahoot.it/rest/kahoots/{}'
        QUIZ_ID     = input("\n > Contoh Input : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx\n\n   Input Quiz ID: ")

        answers, images, questions = {}, {}, {}

        try:
            clearScreen()
            url  = get(API.format(QUIZ_ID))
            data = url.json()
            creator_username = data["creator_username"]
            description = str("-") if str(data["description"]) == "" else str(data["description"])
            title = data["title"]
            quizlength = len(data['questions'])

            print(f"\n > About Quiz")
            print(f"   - Creator     : {creator_username}")
            print(f"   - Title       : {title}")
            print(f"   - Description : {description}")

            def isQuestion(dat):
                try:
                    eval(dat)
                    return True
                except KeyError:
                    return False

            question = 0
            for x in range(quizlength):
                if isQuestion("data['questions'][question]['choices']"):
                    try:
                        if data['questions'][question]['type'] == "quiz":
                            if data['questions'][question]['choices'][0]['correct']:
                                answers[f"Question {question + 1}"] = 'Red'
                            elif data['questions'][question]['choices'][1]['correct']:
                                answers[f"Question {question + 1}"] = 'Blue'
                            elif data['questions'][question]['choices'][2]['correct']:
                                answers[f"Question {question + 1}"] = 'Yellow'
                            elif data['questions'][question]['choices'][3]['correct']:
                                answers[f"Question {question + 1}"] = 'Green'
                        elif data['questions'][question]['type'] == "jumble":
                            length = len(data['questions'][question]['choices'])
                            for y in range(length):
                                if answers.get(f"Question {question + 1}") is None:
                                    answers[f"Question {question + 1}"] = None
                                answers[f"Question {question + 1}"] += str(data['questions'][question]['choices'][y]['answer']).upper()

                        elif data['questions'][question]['type'] == "survey":
                            answers[f"Question {question + 1}"] = None

                        elif data['questions'][question]['type'] == "content":
                            answers[f"Question {question + 1}"] = None

                        elif data['questions'][question]['type'] == "multiple_select_quiz":
                            multiselect = []

                            for z in range(len(data['questions'][question]['choices'])):
                                if data['questions'][question]['choices'][0]['correct']:
                                    multiselect.append("Blue")

                                if data['questions'][question]['choices'][1]['correct']:
                                    multiselect.append("Red")

                                if data['questions'][question]['choices'][2]['correct']:
                                    multiselect.append("Yellow")

                                if data['questions'][question]['choices'][3]['correct']:
                                    multiselect.append("Green")

                            answers[f"Question {question + 1}"] = list(dict.fromkeys(multiselect))
                        else:
                            answers[f"Question {question + 1}"] = None

                        questions[f"Question {question + 1}"] = data["questions"][question]["question"]

                        if isQuestion('data["questions"][question]["image"]'):
                            images[f"Question {question + 1}"] = data["questions"][question]["image"]
                        else:
                            images[f"Question {question + 1}"] = None

                        question += 1
                    except Exception as err:
                        print(err)
                else:
                    answers[f"Question {question + 1}"]   = None
                    images[f"Question {question + 1}"]    = None
                    questions[f"Question {question + 1}"] = None
                    question += 1

        except Exception as err:
            print(" ! There was an error! It could be because the quiz id is incorrect.\n")
            print(err)

        printAnswers()

        dir_path = path.dirname(path.realpath(__file__))
        data_path = path.join(dir_path, "result", f"{QUIZ_ID}.json")

        if not path.exists(path.join(dir_path, "result")):
            mkdir(path.join(dir_path, "result"), 0o666)

        if not path.exists(data_path):
            with open(data_path, "x") as f:
                startconfig = {
                    "answers": {},
                    "questions": {},
                    "images": {}
                }
                dump(startconfig, f, indent=4)

        with open(data_path, "r") as f:
            config = load(f)

        for i, v in answers.items():
            config["answers"][i] = None if v is None else v

        for i, v in questions.items():
            config["questions"][i] = None if v is None else str(v).replace("T or F: ", '').replace("</b>", '').replace("<b>T or  F: ", '').replace('<b>', '')

        for i, v in images.items():
            config["images"][i] = None if v is None else v

        with open(data_path, "w+") as f:
            dump(config, f, indent=4)
            

        input("\n > Press [Enter] to exit.")
    except KeyboardInterrupt:
        print("\n\n > [CTRL + C] Pressed")
        exit()
