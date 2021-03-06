"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""


from flask import Flask, render_template, redirect, flash, session, request
import jinja2

import model


app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""
    print session
    melons = model.Melon.get_all()
    return render_template("all_melons.html",
                           melon_list=melons)


@app.route("/melon/<int:id>")
def show_melon(id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = model.Melon.get_by_id(id)
    print melon
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""

    display_info = []
    total = 0
    
    list_melon_objects = []
    for i in session["cart"]:
        list_melon_objects.append(model.Melon.get_by_id(int(i)))

    for obj in list_melon_objects: 
        quant = session["cart"][str(obj.id)]
        price = obj.price
        subtotal_int = quant * price
        subtotal_str = "$%.2f" % (subtotal_int)
        total += subtotal_int

        display_info.append([obj.common_name, quant, obj.price_str(), subtotal_str])
    print display_info

    return render_template("cart.html", shopping_cart_list = display_info, final_total = total)


@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """

    melon = model.Melon.get_by_id(id)
    melon_id_str = str(melon.id)
    if "cart" not in session:
        session["cart"] = {}

    # checks if the melon.id is a key in session. If it is not there, get returns
    # the value 0. We then add one to increment the value. This value is then 
    # bound to the key, which is a nested dictionary in session "cart". This nested 
    # dictionary holds the key melon.id 
    session["cart"][melon_id_str] = session["cart"].get(melon_id_str, 0) +1

    flash("Succesfully added to cart.")
    return redirect("/cart")

@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """
    login_email = request.form['email']
    login_password = request.form['password']

    # returns None is the the customer's email isn't in the database
    user_logging_in = model.Customer.get_by_email(login_email)

    
    if user_logging_in:
        # user submits inccorect password
        if user_logging_in.password != login_password:
            flash("Invalid Password")
            return redirect("/login")
        else:
            session["logged_in_customer_email"] = user_logging_in.email
            print session
            return redirect('/melons')
    else:
        # user sumbits wrong email
        flash("Invalid Email")
        return redirect("/login")

@app.route("/signout")
def process_logout():
    """Allows the user to sign out of the website.

    Removes the user's id from the session.
    """
    session.pop("logged_in_customer_email", None)

    flash("You are now logged out. Thank you for visiting Ubermelon!")
    return redirect('/melons')

@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)