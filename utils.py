import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


SKILL_METRICS = [
	{
		"category": "Web Logic & JS",
		"skill": "JavaScript/NodeJS & Logic",
		"question": "Seberapa sering Anda menggunakan JavaScript atau NodeJS untuk menyelesaikan logika bisnis di proyek nyata?",
	},
	{
		"category": "Frontend UI",
		"skill": "HTML, CSS, Tailwind, Responsive Design",
		"question": "Seberapa percaya diri Anda membangun antarmuka responsif yang konsisten di berbagai ukuran layar?",
	},
	{
		"category": "JS Framework",
		"skill": "React, Vue, Angular",
		"question": "Sejauh mana Anda dapat mengembangkan fitur secara mandiri menggunakan React, Vue, atau Angular?",
	},
	{
		"category": "Mobile Development",
		"skill": "Flutter, React Native, Kotlin, Swift",
		"question": "Seberapa siap Anda membangun dan merilis aplikasi mobile dari tahap development sampai build release?",
	},
	{
		"category": "Server Side",
		"skill": "Python, Java, PHP, Ruby",
		"question": "Seberapa kuat pengalaman Anda membangun fitur backend dari desain endpoint sampai implementasi?",
	},
	{
		"category": "Database SQL",
		"skill": "MySQL, PostgreSQL, BigQuery",
		"question": "Seberapa nyaman Anda menulis query SQL untuk kebutuhan aplikasi atau analisis data?",
	},
	{
		"category": "NoSQL/Vector DB",
		"skill": "MongoDB, Firebase, Vector DB",
		"question": "Seberapa sering Anda menggunakan NoSQL atau vector database sesuai kebutuhan arsitektur sistem?",
	},
	{
		"category": "API & Integration",
		"skill": "REST API, Postman, Microservices",
		"question": "Seberapa kuat pengalaman Anda mengintegrasikan API dan melakukan debugging integrasi antar layanan?",
	},
	{
		"category": "Version Control",
		"skill": "Git (Commit, Branch, Merge)",
		"question": "Seberapa disiplin Anda menerapkan workflow Git, termasuk branching strategy dan conflict resolution?",
	},
	{
		"category": "Cloud & DevOps",
		"skill": "Docker, Kubernetes, CI/CD, AWS",
		"question": "Seberapa siap Anda melakukan deployment dan automasi release menggunakan Docker, CI/CD, atau layanan cloud?",
	},
	{
		"category": "AI & ML Core",
		"skill": "Training Model, Evaluation, PyTorch/TensorFlow",
		"question": "Seberapa jauh Anda pernah melatih, mengevaluasi, dan memperbaiki performa model machine learning?",
	},
	{
		"category": "Generative AI",
		"skill": "LLM, RAG, AI Agent",
		"question": "Seberapa siap Anda membangun solusi GenAI seperti RAG atau AI agent untuk kebutuhan produk?",
	},
	{
		"category": "Data Processing",
		"skill": "Pandas, NumPy, Data Cleaning",
		"question": "Seberapa rutin Anda melakukan data cleaning, transformasi, dan eksplorasi data sebelum analisis lanjutan?",
	},
	{
		"category": "Data Visualization",
		"skill": "Matplotlib, Seaborn, BI Tools",
		"question": "Seberapa efektif Anda menyajikan insight lewat visualisasi data untuk stakeholder non-teknis?",
	},
	{
		"category": "Design Tools",
		"skill": "Figma, UI/UX Design",
		"question": "Seberapa baik Anda berkolaborasi menggunakan Figma dan menerapkan prinsip UI/UX dalam implementasi produk?",
	},
]


ROLE_CONFIG = {
	"Backend Developer": {
		"core": [1, 5, 6, 7, 8, 9, 10],
		"bonus": [2, 3],
	},
	"Frontend Developer": {
		"core": [1, 2, 3, 8, 9, 15],
		"bonus": [4, 5, 6, 10],
	},
	"Mobile Developer": {
		"core": [1, 2, 3, 4, 5, 6, 7, 8, 9, 15],
		"bonus": [10],
	},
	"AI Engineer": {
		"core": [1, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
		"bonus": [],
	},
	"Data Scientist": {
		"core": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
		"bonus": [],
	},
}


CORE_WEIGHT = 0.85
BONUS_WEIGHT = 0.15
FIT_BANDS = [
	(85, "Sangat Cocok"),
	(70, "Cocok"),
	(55, "Cukup Cocok"),
	(40, "Kurang Cocok"),
	(0, "Tidak Cocok"),
]

SCORE_OPTIONS = [
	{"value": "", "label": "Pilih nilai"},
	{"value": "1", "label": "1 - Belum pernah"},
	{"value": "2", "label": "2 - Pernah coba"},
	{"value": "3", "label": "3 - Cukup"},
	{"value": "4", "label": "4 - Mandiri"},
	{"value": "5", "label": "5 - Sangat mahir"},
]


def _mean_by_index(values, indices, default_value=3.0):
	if not indices:
		return float(default_value)
	return float(np.mean([values[i - 1] for i in indices]))


def label_from_score(score):
	for threshold, label in FIT_BANDS:
		if score >= threshold:
			return label
	return "Tidak Cocok"


def _next_target_band(score):
	thresholds = [85, 70, 55, 40]
	for threshold in sorted(thresholds):
		if score < threshold:
			return threshold, label_from_score(threshold)
	return None, None


def _build_single_metric_system(metric_key):
	in_metric = ctrl.Antecedent(np.arange(1, 5.01, 0.01), f"{metric_key}_in")
	out_metric = ctrl.Consequent(np.arange(0, 100.01, 0.01), f"{metric_key}_fit")

	in_metric.automf(names=["low", "medium", "high"])
	out_metric["low"] = fuzz.trapmf(out_metric.universe, [0, 0, 12, 35])
	out_metric["medium"] = fuzz.trimf(out_metric.universe, [30, 50, 70])
	out_metric["high"] = fuzz.trapmf(out_metric.universe, [88, 97, 100, 100])

	rules = [
		ctrl.Rule(in_metric["low"], out_metric["low"]),
		ctrl.Rule(in_metric["medium"], out_metric["medium"]),
		ctrl.Rule(in_metric["high"], out_metric["high"]),
	]

	return ctrl.ControlSystem(rules)


def _fuzzy_skill_to_fit(metric_key, value):
	metric_ctrl = _build_single_metric_system(metric_key)
	sim = ctrl.ControlSystemSimulation(metric_ctrl)
	sim.input[f"{metric_key}_in"] = value
	sim.compute()
	return float(sim.output[f"{metric_key}_fit"])


def _format_skill_line(index, score):
	item = SKILL_METRICS[index - 1]
	return f"{item['category']} - {item['skill']}: {score:.1f}/5"


def _build_role_feedback(answers, cfg):
	role_indices = sorted(set(cfg["core"] + cfg["bonus"]))
	ranked = sorted(((idx, answers[idx - 1]) for idx in role_indices), key=lambda x: x[1], reverse=True)

	if not ranked:
		return [], [], False

	max_val = ranked[0][1]
	min_val = ranked[-1][1]
	is_balanced = abs(max_val - min_val) < 0.05
	if min_val >= 4.5 or abs(max_val - min_val) < 0.3:
		return ranked[:3], [], is_balanced

	strengths = ranked[:3]
	gaps = sorted(ranked, key=lambda x: x[1])[:2]
	return strengths, gaps, is_balanced


def _build_role_recommendations(score, cfg, answers):
	target_score, target_label = _next_target_band(score)
	if target_score is None:
		return ["Pertahankan konsistensi portofolio; fokus pada proyek real agar profil tetap kompetitif."]

	core_ranked = sorted(((idx, answers[idx - 1]) for idx in cfg["core"]), key=lambda x: x[1])
	bonus_ranked = sorted(((idx, answers[idx - 1]) for idx in cfg["bonus"]), key=lambda x: x[1])

	steps = [f"Target berikutnya: naik ke minimal {target_score:.0f}% ({target_label})."]

	for idx, val in core_ranked[:2]:
		item = SKILL_METRICS[idx - 1]
		if val < 4.0:
			steps.append(
				f"Prioritaskan core {item['skill']} dari {val:.1f} ke >=4.0 (fokus proyek kecil terarah 2-3 minggu)."
			)
		else:
			steps.append(
				f"Perkuat core {item['skill']} dengan bukti portofolio/implementasi produksi agar nilai tetap stabil."
			)

	if bonus_ranked:
		idx, val = bonus_ranked[0]
		item = SKILL_METRICS[idx - 1]
		steps.append(
			f"Sebagai booster, naikkan bonus {item['skill']} dari {val:.1f} ke >=3.5 untuk dorongan skor tambahan."
		)

	return steps[:4]


def _evaluate_role(role_name, role_key, answers, cfg):
	core_val = _mean_by_index(answers, cfg["core"])
	has_bonus = len(cfg["bonus"]) > 0
	bonus_val = _mean_by_index(answers, cfg["bonus"], default_value=3.0)

	core_fit = _fuzzy_skill_to_fit(f"{role_key}_core", core_val)
	bonus_fit = _fuzzy_skill_to_fit(f"{role_key}_bonus", bonus_val) if has_bonus else None

	if has_bonus:
		weighted = (CORE_WEIGHT * core_fit) + (BONUS_WEIGHT * bonus_fit)
		final_score = weighted / (CORE_WEIGHT + BONUS_WEIGHT)
	else:
		final_score = core_fit

	strengths, gaps, is_balanced = _build_role_feedback(answers, cfg)
	recommendations = _build_role_recommendations(final_score, cfg, answers)

	return {
		"role": role_name,
		"score": float(final_score),
		"label": label_from_score(final_score),
		"core_fit": core_fit,
		"bonus_fit": bonus_fit,
		"has_bonus": has_bonus,
		"strength_lines": [_format_skill_line(idx, val) for idx, val in strengths],
		"gap_lines": [_format_skill_line(idx, val) for idx, val in gaps],
		"is_balanced": is_balanced,
		"recommendations": recommendations,
	}


def evaluate_all_roles(answers):
	results = []
	for role_name, cfg in ROLE_CONFIG.items():
		role_key = role_name.lower().replace(" ", "_")
		results.append(_evaluate_role(role_name, role_key, answers, cfg))
	return sorted(results, key=lambda item: item["score"], reverse=True)
