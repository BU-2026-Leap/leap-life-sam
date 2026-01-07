import boto3
from flask import Flask, render_template, request, jsonify
from botocore.exceptions import ClientError
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Connect to AWS DynamoDB
# (AWS credentials are automatically handled by Zappa/Lambda)
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('SpaceInvaders')


@app.route('/')
def game():
    current_high_score = 0
    champion_name = "CPU"

    try:
        # Fetch the global high score from DynamoDB
        response = table.get_item(Key={'id': 'global_high_score'})
        if 'Item' in response:
            item = response['Item']
            # DynamoDB stores numbers as Decimal, convert to int
            current_high_score = int(item.get('score', 0))
            champion_name = item.get('player_name', 'CPU')
    except Exception as e:
        print(f"Database error: {e}")

    return render_template('game.html', high_score=current_high_score, champion=champion_name)


@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.get_json()
    new_name = data.get('name', 'Anonymous')
    new_score = int(data.get('score', 0))

    try:
        # 1. Get the current high score
        response = table.get_item(Key={'id': 'global_high_score'})

        # Default values if table is empty
        current_high_score = 0

        if 'Item' in response:
            current_high_score = int(response['Item'].get('score', 0))

        # 2. Only update if the new score is higher
        if new_score > current_high_score:
            table.put_item(
                Item={
                    'id': 'global_high_score',
                    'score': new_score,
                    'player_name': new_name
                }
            )
            return jsonify({'status': 'new_record'})
        else:
            return jsonify({'status': 'not_high_score'})

    except Exception as e:
        print(f"Error saving score: {e}")
        return jsonify({'status': 'error'}), 500


if __name__ == '__main__':
    app.run(debug=True)