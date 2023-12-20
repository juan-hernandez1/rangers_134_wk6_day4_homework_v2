from flask import Blueprint, flash, redirect, render_template, request

# internal import
from car_inventory.models import Product, Customer, Order, db 
from car_inventory.forms import ProductForm

#need to instantiate our Blueprint class
site = Blueprint('site', __name__, template_folder='site_templates' )


#use site object to create our routes
@site.route('/')
def shop():
   

    return render_template('car_inventory.html')


@site.route('/garage')
def garage():

     #we need to query our database to grab all of our products to display
    allprods = Product.query.all() #the same as SELECT * FROM products, list of objects 
    allcustomers = Customer.query.all()
    allorders = Order.query.all()

# making our dictionary for our shop stats/info
    garage_stats = {
        'vehicles' : len(allprods), # this is how many total products we have
        'sales' : sum([order.order_total for order in allorders]),  # [ 27.99, 83.25, 50.99 ] sum them bad boys up
        'customers' : len(allcustomers)
    }    
                            #whats on left side is html, right side is whats in our route
    return render_template('garage.html', shop=allprods, stats=garage_stats ) #looking inside our template_folder (site_templates) to find our shop.html file


@site.route('/car_inventory/create', methods=['GET', 'POST'])
def create():

    # instantiate our productform

    createform = ProductForm()

    if request.method == 'POST' and createform.validate_on_submit():
        # grab our data from our form
        year = createform.year.data
        image = createform.image.data
        make = createform.make.data
        model = createform.model.data
        description = createform.description.data
        price = createform.price.data
        quantity = createform.quantity.data
       

     # instantiate that class as an object passing in our arguments to replace our parameters

        vehicle = Product(year, price, quantity, make, model, image, description)  

        db.session.add(vehicle) # adding our new instantiating object to our database
        db.session.commit()

        flash(f"You have successfully created vehicle: {year} {make} {model}", category='success')
        return redirect('/garage')
    
    elif request.method == 'POST':
        flash("We were unable to process your request", category='warning')
        return redirect('/car_inventory/create')
    

    return render_template('create.html', form=createform )


@site.route('/shop/update/<id>', methods=['GET', 'POST']) # <parameter> this is how we pass parameters to our routes
def update(id):

    # lets grab our specific product we want to update
    vehicle = Product.query.get(id) # this should only ever bring back 1 item/object
    updateform = ProductForm()

    if request.method == 'POST' and updateform.validate_on_submit():

        vehicle.year = updateform.year.data
        vehicle.image = updateform.image.data
        vehicle.make = updateform.make.data
        vehicle.model = updateform.model.data
        vehicle.description = updateform.description.data
        vehicle.price = updateform.price.data
        vehicle.quantity = updateform.quantity.data
        

        # commit our changes
        db.session.commit()

        flash(f"You have successfully updated vehicle: {vehicle.year} {vehicle.make} {vehicle.model}", category='success')
        return redirect('/garage')
    
    elif request.method == 'POST':
        flash("We were unable to process your request", category='warning')
        return redirect('/')
    
    return render_template('update.html', form=updateform, vehicle=vehicle )


@site.route('/car_inventory/delete/<id>')
def delete(id):

    #query our database to find that object we want to delete
    vehicle = Product.query.get(id)

    db.session.delete(vehicle)
    db.session.commit()

    flash(f"You have successfully deleted vehicle: {vehicle.year} {vehicle.make} {vehicle.model}", category='success')
    return redirect('/garage')