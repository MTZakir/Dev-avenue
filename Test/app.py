from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route('/')
def chat():
    chat_info = [
        {
            'type': 'company',
            'company_pic': '/static/images/netflix.png',
            'recent_chat': 'We have sent the admin info via email to your registered email in this site please do check and let us know if you have any concerns',
            'company_name': 'Netflix',
        },]
    return render_template('/chat.html', chat_info=chat_info)

if __name__ == '__main__':
    app.run(debug=True)
