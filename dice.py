
@app.route('/dice')
def dice_home():
    return render_template('dice.html')

@app.route('/roll-dice', methods=['POST'])
def roll_dice():
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

@app.route('/reset-dice', methods=['POST'])
def reset_dice():
    return redirect(url_for('dice_home'))