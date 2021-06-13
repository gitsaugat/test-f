from async_function import main_function
from asgiref.wsgi import WsgiToAsgi
import asyncio
import threading
from flask import Flask, render_template
app = Flask(__name__)

##############################RSI##################################

# COPY PASTE MY ASYNC FUNCTION (some_function()) HERE

#########################Flask Render#############################

# WHEN THE / URL IS CALLED, THE ASYNC FUNCTION ABOVE IS CALLED AND MUST RETURN AN ARRAY
# FOLLOWING THIS, THE ARRAY IS SENT TO home.html through the rsiValues variable


@app.route('/', methods=['GET'])
def my_route_page_function():
    data = main_function()
    print(data)
    return render_template('home.html',  rsiValues=data)

# ernal Server Error
# DONT FORGET TO PUT HOME.HTML in a /templates folder, good luck


if __name__ == "__main__":
    app.run(port=5000,  debug=True)
