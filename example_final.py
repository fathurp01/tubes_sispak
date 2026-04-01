import numpy as np
from skfuzzy import control as ctrl

print("Skala penilaian: 1 (sangat rendah) sampai 5 (sangat tinggi)")
print("Ketik q kapan saja untuk keluar.\n")

while True:
    try:
        p1 = input("1. Kemahiran JavaScript/NodeJS dan logic: ")
        if p1.lower() == "q":
            break
        p2 = input("2. HTML, CSS, Tailwind, responsive design: ")
        if p2.lower() == "q":
            break
        p3 = input("3. React, Vue, atau Angular: ")
        if p3.lower() == "q":
            break
        p4 = input("4. Python, Java, PHP, atau Ruby: ")
        if p4.lower() == "q":
            break
        p5 = input("5. MySQL, PostgreSQL, atau BigQuery: ")
        if p5.lower() == "q":
            break
        p6 = input("6. MongoDB atau vector database: ")
        if p6.lower() == "q":
            break
        p7 = input("7. REST API, Postman, microservices: ")
        if p7.lower() == "q":
            break
        p8 = input("8. Git commit, branch, merge: ")
        if p8.lower() == "q":
            break
        p9 = input("9. Docker, Kubernetes, AWS/Azure, CI/CD: ")
        if p9.lower() == "q":
            break
        p10 = input("10. Model training, evaluation, PyTorch/TensorFlow: ")
        if p10.lower() == "q":
            break
        p11 = input("11. LLM, RAG, AI Agent, Orchestration: ")
        if p11.lower() == "q":
            break
        p12 = input("12. Figma atau tools UI/UX: ")
        if p12.lower() == "q":
            break

        p1 = float(p1); p2 = float(p2); p3 = float(p3); p4 = float(p4)
        p5 = float(p5); p6 = float(p6); p7 = float(p7); p8 = float(p8)
        p9 = float(p9); p10 = float(p10); p11 = float(p11); p12 = float(p12)

        semua_nilai = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12]
        if any((x < 1 or x > 5) for x in semua_nilai):
            print("\nInput harus di rentang 1 sampai 5.\n")
            continue

        fe_i1 = np.mean([p1, p2, p3])
        fe_i2 = np.mean([p8, p12])
        fe_i3 = np.mean([p7, p9])

        be_i1 = np.mean([p1, p4])
        be_i2 = np.mean([p5, p6])
        be_i3 = np.mean([p7, p9])

        ai_i1 = np.mean([p10, p11])
        ai_i2 = np.mean([p1, p4, p5])
        ai_i3 = np.mean([p7, p9])

        fe_in1 = ctrl.Antecedent(np.arange(1, 5.01, 0.01), "fe_in1")
        fe_in2 = ctrl.Antecedent(np.arange(1, 5.01, 0.01), "fe_in2")
        fe_in3 = ctrl.Antecedent(np.arange(1, 5.01, 0.01), "fe_in3")
        fe_out = ctrl.Consequent(np.arange(0, 101, 1), "fe_out")

        fe_in1.automf(names=["low", "medium", "high"])
        fe_in2.automf(names=["low", "medium", "high"])
        fe_in3.automf(names=["low", "medium", "high"])
        fe_out.automf(names=["low", "medium", "high"])

        fe_rule1 = ctrl.Rule(fe_in1["high"] & fe_in2["high"], fe_out["high"])
        fe_rule2 = ctrl.Rule(fe_in1["high"] & fe_in3["high"], fe_out["high"])
        fe_rule3 = ctrl.Rule(fe_in1["medium"] & fe_in2["high"], fe_out["high"])
        fe_rule4 = ctrl.Rule(fe_in1["medium"] & fe_in2["medium"], fe_out["medium"])
        fe_rule5 = ctrl.Rule(fe_in1["low"] | fe_in2["low"], fe_out["low"])
        fe_rule6 = ctrl.Rule(fe_in1["low"] & fe_in3["low"], fe_out["low"])

        fe_ctrl = ctrl.ControlSystem([fe_rule1, fe_rule2, fe_rule3, fe_rule4, fe_rule5, fe_rule6])
        fe_sim = ctrl.ControlSystemSimulation(fe_ctrl)
        fe_sim.input["fe_in1"] = fe_i1
        fe_sim.input["fe_in2"] = fe_i2
        fe_sim.input["fe_in3"] = fe_i3
        fe_sim.compute()
        fe_score = float(fe_sim.output["fe_out"])

        be_in1 = ctrl.Antecedent(np.arange(1, 5.01, 0.01), "be_in1")
        be_in2 = ctrl.Antecedent(np.arange(1, 5.01, 0.01), "be_in2")
        be_in3 = ctrl.Antecedent(np.arange(1, 5.01, 0.01), "be_in3")
        be_out = ctrl.Consequent(np.arange(0, 101, 1), "be_out")

        be_in1.automf(names=["low", "medium", "high"])
        be_in2.automf(names=["low", "medium", "high"])
        be_in3.automf(names=["low", "medium", "high"])
        be_out.automf(names=["low", "medium", "high"])

        be_rule1 = ctrl.Rule(be_in1["high"] & be_in2["high"], be_out["high"])
        be_rule2 = ctrl.Rule(be_in1["medium"] & be_in3["high"], be_out["high"])
        be_rule3 = ctrl.Rule(be_in1["high"] & be_in3["high"], be_out["high"])
        be_rule4 = ctrl.Rule(be_in1["medium"] & be_in2["medium"], be_out["medium"])
        be_rule5 = ctrl.Rule(be_in1["low"] | be_in2["low"], be_out["low"])
        be_rule6 = ctrl.Rule(be_in1["low"] & be_in2["low"], be_out["low"])

        be_ctrl = ctrl.ControlSystem([be_rule1, be_rule2, be_rule3, be_rule4, be_rule5, be_rule6])
        be_sim = ctrl.ControlSystemSimulation(be_ctrl)
        be_sim.input["be_in1"] = be_i1
        be_sim.input["be_in2"] = be_i2
        be_sim.input["be_in3"] = be_i3
        be_sim.compute()
        be_score = float(be_sim.output["be_out"])

        ai_in1 = ctrl.Antecedent(np.arange(1, 5.01, 0.01), "ai_in1")
        ai_in2 = ctrl.Antecedent(np.arange(1, 5.01, 0.01), "ai_in2")
        ai_in3 = ctrl.Antecedent(np.arange(1, 5.01, 0.01), "ai_in3")
        ai_out = ctrl.Consequent(np.arange(0, 101, 1), "ai_out")

        ai_in1.automf(names=["low", "medium", "high"])
        ai_in2.automf(names=["low", "medium", "high"])
        ai_in3.automf(names=["low", "medium", "high"])
        ai_out.automf(names=["low", "medium", "high"])

        ai_rule1 = ctrl.Rule(ai_in1["high"] & ai_in2["high"], ai_out["high"])
        ai_rule2 = ctrl.Rule(ai_in1["high"] & ai_in3["high"], ai_out["high"])
        ai_rule3 = ctrl.Rule(ai_in1["medium"] & ai_in2["high"], ai_out["high"])
        ai_rule4 = ctrl.Rule(ai_in1["medium"] & ai_in2["medium"], ai_out["medium"])
        ai_rule5 = ctrl.Rule(ai_in1["low"] | ai_in2["low"], ai_out["low"])
        ai_rule6 = ctrl.Rule(ai_in1["low"] & ai_in2["low"], ai_out["low"])

        ai_ctrl = ctrl.ControlSystem([ai_rule1, ai_rule2, ai_rule3, ai_rule4, ai_rule5, ai_rule6])
        ai_sim = ctrl.ControlSystemSimulation(ai_ctrl)
        ai_sim.input["ai_in1"] = ai_i1
        ai_sim.input["ai_in2"] = ai_i2
        ai_sim.input["ai_in3"] = ai_i3
        ai_sim.compute()
        ai_score = float(ai_sim.output["ai_out"])

        hasil = {
            "Frontend Developer": fe_score,
            "Backend Developer": be_score,
            "AI Engineer": ai_score
        }

        ranking = sorted(hasil.items(), key=lambda x: x[1], reverse=True)

        print("\nAnalisis Karier Anda:")
        for role, score in ranking:
            if score >= 85:
                label = "Sangat Cocok"
            elif score >= 70:
                label = "Cocok"
            elif score >= 55:
                label = "Cukup Cocok"
            elif score >= 40:
                label = "Kurang Cocok"
            else:
                label = "Tidak Cocok"
            print(f"- {role}: {score:.1f}% ({label})")

        print(f"\nKesimpulan: Fokus utama ke {ranking[0][0]}.")
        print("-" * 45 + "\n")

    except ValueError:
        print("\nMasukkan angka yang valid (1-5).\n")