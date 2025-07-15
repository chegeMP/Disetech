from flask import Blueprint, render_template, request, redirect, session, url_for

advisor = Blueprint('advisor', __name__)

@advisor.route('/advisor', methods=['GET', 'POST'])
def crop_advice():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    result = None
    if request.method == 'POST':
        symptoms = request.form.get('symptoms', '').lower()

        if "yellow" in symptoms and "spot" in symptoms:
            result = {
                "problem": "Likely: Leaf Spot Disease",
                "advice": "Remove infected leaves and apply appropriate fungicide."
            }
        elif "wilting" in symptoms:
            result = {
                "problem": "Likely: Bacterial Wilt",
                "advice": "Ensure proper drainage and avoid overwatering."
            }
        else:
            result = {
                "problem": "Unknown",
                "advice": "Try providing more details or consult a specialist."
            }

    return render_template("advisor.html", result=result)
