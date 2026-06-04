from flask import Flask, redirect, render_template, request, session, url_for

import utils


app = Flask(__name__)
APP_NAME = "coock.in"
app.secret_key = "coock-in-sispak-secret"


def _init_answers_state():
	session["answers"] = [None] * len(utils.SKILL_METRICS)


def _get_answers_state():
	answers = session.get("answers")
	if not isinstance(answers, list) or len(answers) != len(utils.SKILL_METRICS):
		_init_answers_state()
		answers = session["answers"]
	return answers


def _first_unanswered_step(answers):
	for idx, value in enumerate(answers, start=1):
		if value is None:
			return idx
	return None


def _parse_selected_value(raw_value):
	if raw_value is None or raw_value.strip() == "":
		return None, "Silakan pilih nilai terlebih dahulu."

	try:
		number = float(raw_value)
	except ValueError:
		return None, "Nilai tidak valid."

	if number < 1 or number > 5:
		return None, "Nilai harus di rentang 1 sampai 5."

	return number, None


@app.route("/", methods=["GET", "POST"])
def onboarding():
	if request.method == "POST":
		_init_answers_state()
		return redirect(url_for("quiz", step=1))

	return render_template(
		"index.html",
		app_name=APP_NAME,
		total_questions=len(utils.SKILL_METRICS),
	)


@app.route("/quiz/<int:step>", methods=["GET", "POST"])
def quiz(step):
	total = len(utils.SKILL_METRICS)
	if step < 1 or step > total:
		return redirect(url_for("quiz", step=1))

	answers = _get_answers_state()
	error = None

	if request.method == "POST":
		action = request.form.get("action", "next")
		selected_value, error = _parse_selected_value(request.form.get("selected"))

		if error is None:
			answers[step - 1] = selected_value
			session["answers"] = answers

			if action == "back":
				previous_step = max(1, step - 1)
				return redirect(url_for("quiz", step=previous_step))

			next_step = step + 1
			if next_step > total:
				return redirect(url_for("curhat"))
			return redirect(url_for("quiz", step=next_step))

	question = utils.SKILL_METRICS[step - 1]
	current_value = answers[step - 1]

	return render_template(
		"quiz.html",
		app_name=APP_NAME,
		question=question,
		step=step,
		total=total,
		current_value=current_value,
		choices=utils.SCORE_OPTIONS,
		error=error,
	)


@app.route("/curhat", methods=["GET", "POST"])
def curhat():
	answers = _get_answers_state()
	first_missing = _first_unanswered_step(answers)
	if first_missing is not None:
		return redirect(url_for("quiz", step=first_missing))

	if request.method == "POST":
		curhat_text = request.form.get("curhat_text", "").strip()
		analysis = utils.analyze_curhat(curhat_text)
		session["curhat_text"] = curhat_text
		session["curhat_analysis"] = analysis
		return redirect(url_for("result"))

	return render_template(
		"curhat.html",
		app_name=APP_NAME,
		total_questions=len(utils.SKILL_METRICS),
	)


@app.route("/result", methods=["GET", "POST"])
def result():
	if request.method == "POST":
		_init_answers_state()
		session.pop("curhat_text", None)
		session.pop("curhat_analysis", None)
		return redirect(url_for("quiz", step=1))

	answers = _get_answers_state()
	first_missing = _first_unanswered_step(answers)
	if first_missing is not None:
		return redirect(url_for("quiz", step=first_missing))

	analysis = session.get("curhat_analysis")
	strong_skills = analysis.get("strong_ids", []) if analysis else []
	
	ranking = utils.evaluate_all_roles(answers, strong_skills=strong_skills)
	top_role = ranking[0]["role"] if ranking else "-"

	detected_strong = analysis.get("strong_skills", []) if analysis else []
	detected_weak = analysis.get("weak_skills", []) if analysis else []

	return render_template(
		"result.html",
		app_name=APP_NAME,
		ranking=ranking,
		top_role=top_role,
		detected_strong=detected_strong,
		detected_weak=detected_weak,
		curhat_text=session.get("curhat_text", "")
	)


if __name__ == "__main__":
	app.run(debug=True)
