def get_user_symptoms():
    print("Welcome to the Health Therapist!")
    print("Please answer with 'yes' or 'no'. Let's begin...\n")

    symptoms_list = [
        "fever", "cough", "fatigue", "headache", "sore throat",
        "runny nose", "shortness of breath", "nausea", "vomiting", "diarrhea",
        "muscle pain", "joint pain", "rash", "chest pain", "dizziness",
        "sensitivity to light", "abdominal pain", "loss of smell", "loss of taste", "chills"
    ]

    user_symptoms = []

    for i, symptom in enumerate(symptoms_list):
        if i >= 50:
            break  # Max of 50 questions
        answer = input(f"Do you have {symptom}? ").strip().lower()
        if answer == "yes":
            user_symptoms.append(symptom)
    
    return user_symptoms

def diagnose(symptoms):
    # Dictionary of illnesses and their common symptoms
    illnesses = {
        "Common Cold": {"cough", "runny nose", "sore throat", "fatigue"},
        "Flu": {"fever", "chills", "muscle pain", "fatigue", "cough"},
        "COVID-19": {"fever", "cough", "loss of taste", "loss of smell", "fatigue"},
        "Migraine": {"headache", "sensitivity to light", "nausea", "vomiting"},
        "Food Poisoning": {"nausea", "vomiting", "diarrhea", "abdominal pain"},
        "Allergy": {"runny nose", "rash", "sore throat"},
        "Pneumonia": {"fever", "cough", "chest pain", "shortness of breath"}
    }

    match_scores = {}
    for illness, illness_symptoms in illnesses.items():
        matches = illness_symptoms.intersection(symptoms)
        score = len(matches) / len(illness_symptoms)
        match_scores[illness] = score

    # Get illness with highest score
    best_match = max(match_scores, key=match_scores.get)
    best_score = match_scores[best_match]

    if best_score > 0.4:
        return f"\n⚠️ Possible diagnosis: {best_match} (match: {best_score:.0%})"
    else:
        return "\n❓ Symptoms are unclear. Please consult a doctor for an accurate diagnosis."

def main():
    user_symptoms = get_user_symptoms()
    if not user_symptoms:
        print("\n✅ You reported no symptoms. Stay healthy!")
    else:
        result = diagnose(set(user_symptoms))
        print(result)

if __name__ == "__main__":
    main()
#work
