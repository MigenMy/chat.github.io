from flask import Flask, render_template_string, request, jsonify
import g4f

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat with Graphics</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        .message {
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 5px;
        }

        .user-message {
            background-color: #007bff;
            color: #fff;
        }

        .bot-message {
            background-color: #28a745;
            color: #fff;
        }
    </style>
</head>
<body>
    <div class="container">
        <div id="chat-box"></div>
        <form id="chat-form">
            <div class="form-group">
                <input type="text" class="form-control" id="user-input" placeholder="Enter your message...">
            </div>
            <button type="submit" class="btn btn-primary">Send</button>
        </form>
    </div>

    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script>
        $(document).ready(function () {
            $('#chat-form').submit(function (e) {
                e.preventDefault();
                var userInput = $('#user-input').val().trim();
                if (userInput === '') return;

                $('#chat-box').append('<div class="message user-message">' + userInput + '</div>');
                $('#user-input').val('');

                $.ajax({
                    url: '/chat',
                    type: 'POST',
                    data: {user_input: userInput},
                    success: function (data) {
                        var botResponse = data.conversation[data.conversation.length - 1].content;
                        $('#chat-box').append('<div class="message bot-message">' + botResponse + '</div>');
                    }
                });
            });
        });
    </script>
</body>
</html>
""")

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    conversation = [{'role': 'user', 'content': user_input}]

    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        stream=True,
    )

    bot_response = ''.join(response)

    conversation.append({'role': 'bot', 'content': bot_response})

    return jsonify({'conversation': conversation})

if __name__ == '__main__':
    app.run(debug=True)
