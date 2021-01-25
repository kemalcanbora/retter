from chalice import Chalice
import textwrap

app = Chalice(app_name='retter')


@app.route('/')
def index():
    return {"status": True}


@app.route('/wraptext', methods=["POST"])
def wrapText():
    inputText = app.current_request.query_params.get('inputText')
    maxLength = app.current_request.query_params.get('maxLength')
    try:
        lines = textwrap.wrap(inputText, int(maxLength), break_long_words=False)
    except ValueError:
        return {"result": "Maybe you can check your inputText or maxLength",
                "status": False}

    return {"result": lines,
            "status": True}


@app.route('/wraptextbody', methods=["POST"])
def wrapTextWithBodyAnotherWay():
    params = app.current_request.json_body
    if ("inputText" or "maxlength") in list(params.keys()):
        if len(params["inputText"]) > 0:
            words = iter(params["inputText"].split())
            lines, current = [], next(words)
            for word in words:
                if len(current) + 1 + len(word) > int(params["maxlength"]):
                    lines.append(current)
                    current = word
                else:
                    current += " " + word
            lines.append(current)
            return {"result": lines,
                    "status": True}
        else:
            return {"result": "You have to write something in inputText param but it's empty!",
                    "status": False}
    else:
        return {"result": "You have to use inputText and maxlength params",
                "status": False}
