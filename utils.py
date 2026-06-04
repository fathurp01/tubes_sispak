import os
import re
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


SKILL_METRICS = [
	{
		"category": "Programming Logic",
		"skill": "Kemampuan problem solving, clean code, dan logika pemrograman",
		"question": "Seberapa percaya diri Anda dalam memecahkan masalah dengan logika pemrograman dan menulis clean code?",
	},
	{
		"category": "Web Logic & JS",
		"skill": "Kemahiran JavaScript/NodeJS & asynchronous programming",
		"question": "Seberapa mahir Anda menggunakan JavaScript/NodeJS, termasuk konsep asynchronous programming?",
	},
	{
		"category": "Frontend UI",
		"skill": "HTML, CSS, Tailwind, responsive & cross-browser design",
		"question": "Seberapa baik Anda mengimplementasikan desain UI yang responsif menggunakan HTML, CSS, atau Tailwind?",
	},
	{
		"category": "JS Framework",
		"skill": "React, Vue, Next.js, state management",
		"question": "Seberapa sering Anda mengembangkan aplikasi dengan framework seperti React/Vue/Next.js dan mengelola state-nya?",
	},
	{
		"category": "Mobile Development",
		"skill": "Flutter, Kotlin, Swift, Android/iOS development",
		"question": "Seberapa dalam pemahaman Anda dalam membuat aplikasi mobile (Android/iOS) menggunakan Flutter, Kotlin, atau Swift?",
	},
	{
		"category": "Server Side",
		"skill": "Backend programming (Go, Node.js, Python, Java)",
		"question": "Seberapa sering Anda menulis kode backend menggunakan Go, Node.js, Python, atau Java di proyek nyata?",
	},
	{
		"category": "Backend Framework",
		"skill": "Express.js, Gin, Fiber, Flask",
		"question": "Seberapa siap Anda membangun sistem backend menggunakan framework seperti Express.js, Gin, atau Flask?",
	},
	{
		"category": "Database SQL",
		"skill": "MySQL, PostgreSQL, query optimization",
		"question": "Seberapa kompeten Anda merancang skema relasional, menulis query kompleks, dan melakukan optimasi SQL?",
	},
	{
		"category": "NoSQL/Vector DB",
		"skill": "MongoDB, Redis, Firebase, Vector DB",
		"question": "Seberapa familiar Anda dengan database non-relasional seperti MongoDB, Redis, atau Vector DB?",
	},
	{
		"category": "API Development",
		"skill": "RESTful API, request/response, WebSocket",
		"question": "Seberapa mahir Anda mendesain dan mengimplementasikan RESTful API atau teknologi real-time (WebSocket)?",
	},
	{
		"category": "Authentication",
		"skill": "JWT, OAuth, security best practice",
		"question": "Seberapa dalam pengetahuan Anda tentang sistem autentikasi (JWT/OAuth) dan best practice keamanan aplikasi?",
	},
	{
		"category": "Version Control",
		"skill": "Git (commit, branching, collaboration workflow)",
		"question": "Seberapa disiplin Anda menerapkan branching strategy dan kolaborasi menggunakan Git?",
	},
	{
		"category": "Cloud & DevOps",
		"skill": "Docker, Kubernetes, CI/CD, cloud (AWS/GCP/Azure)",
		"question": "Seberapa siap Anda menyusun pipeline CI/CD dan men-deploy aplikasi dengan Docker/Kubernetes di layanan cloud?",
	},
	{
		"category": "System Integration",
		"skill": "Microservices, message queue (Kafka, RabbitMQ), third-party integration",
		"question": "Seberapa berpengalaman Anda mengintegrasikan berbagai layanan internal (Microservices/Message Queue) atau API pihak ketiga?",
	},
	{
		"category": "Monitoring & Logging",
		"skill": "Logging, debugging, observability (Grafana, ELK, Sentry)",
		"question": "Seberapa proaktif Anda mengatur sistem logging, monitoring, dan debugging (seperti Grafana/Sentry) di tahap produksi?",
	},
	{
		"category": "Performance",
		"skill": "Optimasi sistem (scalability, speed, lazy loading, efficiency)",
		"question": "Seberapa sering Anda melakukan optimasi performa, seperti scalability, lazy loading, dan efisiensi query/kode?",
	},
	{
		"category": "AI & ML Core",
		"skill": "Machine learning, model training, evaluation",
		"question": "Seberapa jauh Anda pernah membangun, melatih, dan mengevaluasi model machine learning mandiri?",
	},
	{
		"category": "Generative AI",
		"skill": "LLM, RAG, prompt engineering, AI agent",
		"question": "Seberapa mendalam pengalaman Anda dengan model AI generatif (LLM), RAG, atau prompt engineering?",
	},
	{
		"category": "AI Framework",
		"skill": "LangChain, LlamaIndex, AI orchestration",
		"question": "Seberapa sering Anda memakai framework AI seperti LangChain atau LlamaIndex untuk orkestrasi AI?",
	},
	{
		"category": "Data Processing",
		"skill": "Pandas, NumPy, data cleaning",
		"question": "Seberapa terampil Anda menggunakan library (seperti Pandas/NumPy) untuk memproses dan membersihkan data mentah?",
	},
	{
		"category": "Data Analysis",
		"skill": "Statistik, regression, clustering",
		"question": "Seberapa paham Anda dalam menerapkan teknik analisis klasikal, seperti regresi dan clustering, untuk menemukan pola data?",
	},
	{
		"category": "Data Visualization",
		"skill": "Tableau, Power BI, Matplotlib",
		"question": "Seberapa efektif Anda membuat dashboard atau visualisasi interaktif dari data menggunakan tool maupun kode?",
	},
	{
		"category": "Feature Engineering",
		"skill": "Data preparation dan feature extraction",
		"question": "Seberapa matang keahlian Anda dalam merancang dan mengekstrak fitur dataset yang berpengaruh bagi pemodelan?",
	},
	{
		"category": "Design Tools",
		"skill": "Figma, UI/UX design, design-to-code",
		"question": "Seberapa baik Anda berkolaborasi menggunakan Figma, memahami UX, dan mengubah desain menjadi kode?",
	},
]


ROLE_CONFIG = {
	"Backend Developer": {
		"core": [1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
		"bonus": [3, 4],
	},
	"Frontend Developer": {
		"core": [1, 2, 3, 4, 10, 12, 14, 16, 24],
		"bonus": [5, 6, 8, 11, 13, 15],
	},
	"Mobile Developer": {
		"core": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 24],
		"bonus": [13, 15],
	},
	"AI Engineer": {
		"core": [1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
		"bonus": [],
	},
	"Data Scientist": {
		"core": [1, 6, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
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
	
	# Mengambil semua skill dengan nilai di bawah 4 (belum mahir/mandiri) sebagai gap
	all_gaps = sorted(ranked, key=lambda x: x[1])
	gaps = [item for item in all_gaps if item[1] < 4.0]
	
	# Jika tidak ada yang di bawah 4, tetap ambil 2 terendah sebagai area pengembangan
	if not gaps:
		gaps = all_gaps[:2]

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


def evaluate_all_roles(answers, strong_skills=None):
	results = []
	for role_name, cfg in ROLE_CONFIG.items():
		role_key = role_name.lower().replace(" ", "_")
		role_res = _evaluate_role(role_name, role_key, answers, cfg)
		
		role_res["original_score"] = role_res["score"]
		role_res["nlp_bonus"] = 0.0
		
		if strong_skills:
			bonus = 0.0
			for skill_idx in strong_skills:
				if skill_idx in cfg.get("core", []):
					bonus += 1.5
				elif skill_idx in cfg.get("bonus", []):
					bonus += 0.75
			bonus = min(5.0, bonus)
			
			role_res["score"] = min(100.0, role_res["score"] + bonus)
			role_res["nlp_bonus"] = bonus
			role_res["label"] = label_from_score(role_res["score"])
			
		results.append(role_res)
	return sorted(results, key=lambda item: item["score"], reverse=True)


def load_stopwords(path):
	if os.path.exists(path):
		with open(path, 'r', encoding='utf-8') as f:
			return set(word.strip().lower() for word in f.read().splitlines() if word.strip())
	return set()


class INIdrisStemmer:
	def __init__(self):
		self.dictionary = set()
		self.load_dictionary("kata-dasar.txt")
		self.suffixes_list = sorted([
			"an","at","i", "iah", "ilah", "in","is","isme","kan","lah","nya","wan","wi", "tah", "ku", "mu"
		], key=len, reverse=True)
		self.prefixes_list = sorted([
			"be","bel","ber","di","dwi","ke","me","mem","men","meng","meny","mono","pe","pel","pem","pen","peng","peny","per","pra","pro","se","sub","ter"
		], key=len, reverse=True)

	def load_dictionary(self, path):
		if os.path.exists(path):
			with open(path, 'r', encoding='utf-8') as f:
				words = f.read().splitlines()
				self.dictionary = set(word.strip().lower() for word in words if word.strip())

	def is_vowel(self, char):
		return char.lower() in 'aiueo'

	def remove_suffix(self, word):
		for suffix in self.suffixes_list:
			if word.endswith(suffix):
				if len(word) > len(suffix):
					return word[:-len(suffix)]
		return word

	def remove_prefix(self, word):
		for prefix in self.prefixes_list:
			if word.startswith(prefix):
				if len(word) > len(prefix):
					return word[len(prefix):]
		return word

	def apply_rule2(self, word):
		if (word.startswith("men") or word.startswith("pen")) and len(word) > 3 and self.is_vowel(word[3]):
			return "t" + word[3:]
		if (word.startswith("meng") or word.startswith("peng")) and len(word) > 4 and self.is_vowel(word[4]):
			return "k" + word[4:]
		if (word.startswith("meny") or word.startswith("peny")) and len(word) > 4 and self.is_vowel(word[4]):
			return "s" + word[4:]
		if (word.startswith("mem") or word.startswith("pem")) and len(word) > 3 and self.is_vowel(word[3]):
			return "p" + word[3:]
		return word

	def stem(self, word):
		current_word = word
		if current_word in self.dictionary:
			return current_word
		for prefix in self.prefixes_list:
			if current_word.startswith(prefix):
				if len(current_word) > len(prefix):
					candidate = current_word[len(prefix):]
					if candidate in self.dictionary:
						return candidate
		processed_rule2 = self.apply_rule2(current_word)
		if processed_rule2 != current_word:
			if processed_rule2 in self.dictionary:
				return processed_rule2
			prefix_rule2 = self.remove_prefix(processed_rule2)
			if prefix_rule2 in self.dictionary:
				return prefix_rule2
		processed_suffix = self.remove_suffix(current_word)
		if processed_suffix != current_word:
			if len(processed_suffix) > 1:
				return self.stem(processed_suffix)
		return word


KEYWORD_TO_METRIC = {
	# Programming Logic (1)
	"problem solving": 1, "clean code": 1, "logika": 1, "algoritma": 1,
	# Web Logic & JS (2)
	"javascript": 2, "js": 2, "nodejs": 2, "node.js": 2, "node": 2, "asynchronous": 2, "async": 2,
	# Frontend UI (3)
	"html": 3, "css": 3, "tailwind": 3, "responsive": 3, "ui": 3, "ux": 3, "bootstrap": 3,
	# JS Framework (4)
	"react": 4, "reactjs": 4, "vue": 4, "vuejs": 4, "nextjs": 4, "next.js": 4, "nuxt": 4, "state management": 4, "redux": 4,
	# Mobile Development (5)
	"flutter": 5, "kotlin": 5, "swift": 5, "android": 5, "ios": 5, "mobile": 5,
	# Server Side (6)
	"backend": 6, "go": 6, "golang": 6, "python": 6, "java": 6, "server": 6,
	# Backend Framework (7)
	"express": 7, "expressjs": 7, "gin": 7, "fiber": 7, "flask": 7, "django": 7, "laravel": 7,
	# Database SQL (8)
	"sql": 8, "mysql": 8, "postgresql": 8, "postgres": 8, "sqlite": 8, "oracle": 8,
	# NoSQL/Vector DB (9)
	"nosql": 9, "mongodb": 9, "mongo": 9, "redis": 9, "firebase": 9, "firestore": 9, "vector db": 9,
	# API Development (10)
	"api": 10, "restful": 10, "rest api": 10, "websocket": 10, "graphql": 10,
	# Authentication (11)
	"jwt": 11, "oauth": 11, "auth": 11, "autentikasi": 11, "security": 11, "keamanan": 11,
	# Version Control (12)
	"git": 12, "github": 12, "gitlab": 12,
	# Cloud & DevOps (13)
	"docker": 13, "kubernetes": 13, "k8s": 13, "ci/cd": 13, "cicd": 13, "aws": 13, "gcp": 13, "azure": 13, "cloud": 13, "devops": 13,
	# System Integration (14)
	"microservices": 14, "microservice": 14, "kafka": 14, "rabbitmq": 14,
	# Monitoring & Logging (15)
	"logging": 15, "log": 15, "debugging": 15, "grafana": 15, "elk": 15, "sentry": 15, "monitoring": 15,
	# Performance (16)
	"optimasi": 16, "scalability": 16, "speed": 16, "lazy loading": 16, "performa": 16,
	# AI & ML Core (17)
	"machine learning": 17, "ml": 17, "deep learning": 17, "model": 17, "training": 17,
	# Generative AI (18)
	"llm": 18, "rag": 18, "prompt": 18, "openai": 18, "chatgpt": 18, "ai agent": 18,
	# AI Framework (19)
	"langchain": 19, "llamaindex": 19,
	# Data Processing (20)
	"pandas": 20, "numpy": 20, "scipy": 20, "cleaning": 20,
	# Data Analysis (21)
	"statistik": 21, "statistika": 21, "regression": 21, "regresi": 21, "clustering": 21,
	# Data Visualization (22)
	"tableau": 22, "powerbi": 22, "power bi": 22, "matplotlib": 22, "seaborn": 22,
	# Feature Engineering (23)
	"feature engineering": 23, "extraction": 23,
	# Design Tools (24)
	"figma": 24, "sketch": 24, "adobe xd": 24
}


def format_keyword(kw):
	upper_keywords = {
		"js", "html", "css", "sql", "nosql", "api", "jwt", "oauth", "cicd", "ci/cd", 
		"aws", "gcp", "azure", "db", "ai", "ml", "llm", "rag", "elk", "ux", "ui", "k8s"
	}
	if kw.lower() in upper_keywords:
		return kw.upper()
	if kw.lower() in ["nodejs", "node.js", "nextjs", "next.js", "vuejs", "reactjs", "expressjs"]:
		return {
			"nodejs": "Node.js",
			"node.js": "Node.js",
			"nextjs": "Next.js",
			"next.js": "Next.js",
			"vuejs": "Vue.js",
			"reactjs": "React.js",
			"expressjs": "Express.js"
		}.get(kw.lower(), kw.title())
	return kw.title()


def analyze_curhat(text):
	if not text:
		return {
			"strong_ids": [],
			"weak_ids": [],
			"strong_skills": [],
			"weak_skills": []
		}
	
	stemmer = INIdrisStemmer()
	stopwords = load_stopwords("stopwords.txt")
	
	clauses = re.split(r'[,.;!?\n]|\b(?:tapi|tetapi|namun|sedangkan|melainkan)\b', text.lower())
	
	detected_skills = {}
	
	negation_words = {
		'belum', 'kurang', 'lemah', 'bingung', 'sulit', 'susah', 'kesulitan',
		'tidak', 'tak', 'belajar', 'pemula', 'basic', 'sedikit', 'lupa', 'ragu',
		'gap', 'lemah', 'lemahnya'
	}
	
	for clause in clauses:
		clause = clause.strip()
		if not clause:
			continue
		
		clean_clause = re.sub(r"[^a-zA-Z0-9\s]", " ", clause)
		tokens = clean_clause.split()
		
		stemmed_tokens = []
		for token in tokens:
			if token not in stopwords:
				stemmed_tokens.append(stemmer.stem(token))
			else:
				stemmed_tokens.append(token)
		
		has_negation = False
		for token in tokens + stemmed_tokens:
			if token in negation_words:
				has_negation = True
				break
		
		clause_strength = 0.0 if has_negation else 1.0
		
		for kw, skill_idx in KEYWORD_TO_METRIC.items():
			pattern = r'\b' + re.escape(kw) + r'\b'
			if re.search(pattern, clause):
				if skill_idx not in detected_skills:
					detected_skills[skill_idx] = {"strengths": [], "keywords": set()}
				detected_skills[skill_idx]["strengths"].append(clause_strength)
				detected_skills[skill_idx]["keywords"].add(kw)
				
	strong_ids = []
	weak_ids = []
	strong_skills = []
	weak_skills = []
	
	for skill_idx, info in detected_skills.items():
		strengths = info["strengths"]
		avg_strength = sum(strengths) / len(strengths)
		category = SKILL_METRICS[skill_idx - 1]["category"]
		
		formatted_kws = [format_keyword(kw) for kw in info["keywords"]]
		kws_str = ", ".join(sorted(formatted_kws))
		display_name = f"{category} ({kws_str})"
		
		if avg_strength >= 0.5:
			strong_ids.append(skill_idx)
			strong_skills.append(display_name)
		else:
			weak_ids.append(skill_idx)
			weak_skills.append(display_name)
			
	return {
		"strong_ids": strong_ids,
		"weak_ids": weak_ids,
		"strong_skills": strong_skills,
		"weak_skills": weak_skills
	}
