from flask import Blueprint, render_template, request, jsonify
from markupsafe import escape
from data.various import mock_json
from icecream import ic

from ai.test_persistence import get_chain_with_message_history_2, invoke_and_save

chain_with_message_history_2 = get_chain_with_message_history_2()



routes_blueprint = Blueprint("routes", __name__)


@routes_blueprint.route('/index')
def index():
    return render_template('index.html')

# variable routes
@routes_blueprint.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(escape(username))

@routes_blueprint.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@routes_blueprint.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)


@routes_blueprint.route('/chat')
def chat():
    return render_template('/chat.html') 


@routes_blueprint.route('/chat', methods=['POST', 'GET'])
def handle_button_click():

    if request.method == 'POST':
        ic("post method in handle_button_click")
        
    # Return the template to keep the page visible
    return render_template('chat.html')


    return render_template('hello.html', name=name)




@routes_blueprint.route('/button_clicked', methods=['POST'])
def button_clicked():

    if request.method=="POST":
        print("button_clicked")
        return "This was Post"

    print("this is get")
    return 'Button clicked!'




@routes_blueprint.route('/read_input', methods=['POST', 'GET'])
def read_input():
    if request.method=="POST":
        return str(add(5,6))
    
@routes_blueprint.route('/send_text', methods=['POST'])
def send_text():
    text = request.form['text']
    # Call your Python function here

    return str(text)


@routes_blueprint.route('/mock')
def mock():
  return render_template('mock.html', data=mock_json)







@routes_blueprint.route('/api/datapoint3', methods= ['POST'])
def api_datapoint3():
    ic("api_datapoint3")
    ic(request)
    ic(request.get_json())
    user_input = request.get_json()['user_input']

    print(user_input)
    print()

    response = invoke_and_save(chain_with_message_history_2, "abc123", user_input)
    return response



@routes_blueprint.route('/ena')
def ena():
  return render_template('temp1.html')

@routes_blueprint.route('/api/datapoint')
def api_datapoint():

    ic(api_datapoint)

    random_number = random.randint(1, 100)
    double_random_number = random_number * 2
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    dictionary_to_return = {
        'random_number': random_number,
        'double_random_number': double_random_number,
        'timestamp': timestamp
    }

    return jsonify(dictionary_to_return)

def show_the_login_form(name=None):
    return render_template("/hello.html", name = name)


def do_the_login():
    return render_template("/chat.html")

    