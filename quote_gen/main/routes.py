from flask import render_template, request, Blueprint
from quote_gen.main.lstm import generate_text, model_simplified
main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
def adder_page():
    errors = ""
    if request.method == "POST":
        seed = None
        temperature = None
        words = None
        seed = request.form["seed"]
        try:
            temperature = float(request.form["temperature"])
            if temperature > 1.5 or temperature < 0:
                errors += "<p>Please enter a float between 0 and 1.5 for temperature.</p>\n".format(
                request.form["temperature"])
                temperature = None
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(
                request.form["temperature"])
        try:
            words = float(request.form["words"])
            if words > 100000 or words < 0:
                errors += "<p>Please enter a float between 0 and 100000 for quote length.</p>\n".format(
                request.form["words"])
                words = None
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(
                request.form["words"])

        if seed is not None and temperature is not None and words is not None:
            #result = seed
            result = generate_text(model=model_simplified, start_string=seed,
                                   num_generate=int(words)+len(seed), temperature=temperature)
            result = result.replace("␣", "")
            return '''
                <html>
                    <body style="background-color:skyblue;">
                    <center>
                        <p><font size="5">The result is:</font></p>
                        <p><font size="5">{result}</font></p>
                        <p><font size="5"><a href="/">Click here to generate again</font></a>
                    </center>
                    </body>
                </html>
            '''.format(result=result)

    return '''
        <html>
            <body style="background-color:skyblue;">
            <center>
                {errors}
                <h1><font size="24">Quote Generator</font></h1>
                <p><font size="5">Enter your starting string:</font></p>
                <form method="post" action=".">
                    <p><input name="seed" /></p>
                <p><font size="5">Enter your temperature:</font></p>
                    <p><input name="temperature" /></p>
                <p><font size="5">Enter your quote length:</font></p>
                    <p><input name="words" /></p>
                    <p><input type="submit" value="Generate quote" /></p>
                </form>
            </center>
            </body>
        </html>
    '''.format(errors=errors)
