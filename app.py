from flask import Flask, render_template, request, redirect, url_for
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

# Initialize RPS game stats
rps_stats = {
    'total_games': 0,
    'user_wins': 0,
    'computer_wins': 0,
    'ties': 0
}

@app.route('/')
def home():
    return render_template('index.html', stats=rps_stats)

@app.route('/play-rps', methods=['POST'])
def play_rps():
    if 'restart' in request.form:
        reset_rps_stats()
        return redirect(url_for('home'))
    
    user_choice = request.form['choice']
    computer_choice = get_computer_choice()
    result = determine_rps_winner(user_choice, computer_choice)
    
    update_rps_stats(result)
    
    return render_template('index.html', 
                        user_choice=user_choice,
                        computer_choice=computer_choice,
                        result=result,
                        stats=rps_stats)

@app.route('/dice', methods=['GET', 'POST'])
def dice_game():
    if request.method == 'POST':
        if 'restart' in request.form:
            return redirect(url_for('dice_game'))
        
        import random
        dice_count = int(request.form.get('dice_count', 1))
        sides = int(request.form.get('sides', 6))
        
        rolls = [random.randint(1, sides) for _ in range(dice_count)]
        total = sum(rolls)
        
        return render_template('dice.html', 
                            rolls=rolls,
                            total=total,
                            dice_count=dice_count,
                            sides=sides)
    
    return render_template('dice.html')

@app.route('/qr-generator', methods=['GET', 'POST'])
def qr_generator():
    qr_code = None
    if request.method == 'POST':
        data = request.form.get('qr-data', '')
        if data:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save the image to a bytes buffer
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            qr_code = base64.b64encode(buffer.getvalue()).decode()
    
    return render_template('qr_generator.html', qr_code=qr_code)

# Helper functions for RPS
def get_computer_choice():
    import random
    return random.choice(['rock', 'paper', 'scissors'])

def determine_rps_winner(user, computer):
    if user == computer:
        return "tie"
    if (user == 'rock' and computer == 'scissors') or \
       (user == 'paper' and computer == 'rock') or \
       (user == 'scissors' and computer == 'paper'):
        return "user"
    return "computer"

def update_rps_stats(result):
    rps_stats['total_games'] += 1
    if result == "user":
        rps_stats['user_wins'] += 1
    elif result == "computer":
        rps_stats['computer_wins'] += 1
    else:
        rps_stats['ties'] += 1

def reset_rps_stats():
    global rps_stats
    rps_stats = {
        'total_games': 0,
        'user_wins': 0,
        'computer_wins': 0,
        'ties': 0
    }

if __name__ == '__main__':
    app.run(debug=True)