from flask import Blueprint, render_template, request, redirect, url_for, session

soil = Blueprint('soil', __name__)

@soil.route('/soil', methods=['GET', 'POST'])
def analyze_soil():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    result = None

    if request.method == 'POST':
        location = request.form.get('location')
        soil_type = request.form.get('soil_type')

        # Simulate analysis result
        result = {
            "ph": 6.2,
            "moisture": "Moderate",
            "fertility": "High",
            "recommendation": f"The soil in {location} is suitable for beans and maize. Add compost to enhance fertility."
        }

    return render_template('soil.html', result=result)
