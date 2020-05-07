INTRODUCTION:
Hello! Welcome to CS50 Skincare, our interactive online skincare community. Our goal with creating this was to provide a means for people to log on,
browse 1735 of the world's most popular skincare products, save these products to their favorites, and share these favorites with friends.

MATERIALS:
- application.py: contains the Python program that runs the website
- helpers.py: contains the Python program that contains helper functions
- "static" folder: contains various impages and styling documents
    - animate.css
    - styles.css
- "templates" folder: contains the templates for the website
    - apology.html
    - browse.html
    - browsed.html
    - friends.html
    - index.html
    - layout.html
    - login.html
    - register.html
    - review.html
    - saved.html
    - share.html
- skincare.db: database of all tables needed for website to run
    - favorites (user_id, name, ingredient, brand, id, friend, friend_id): keeps track of products saved to favorites
    - friends (friend1id, friend2id): keeps track of friend pairings
    - ingredients (id, ingredient): keeps track of ingredients in each product using product id
    - products (id, brand, name, ingredient_list): information on all products, downloaded from an online API (https://github.com/LauraRobertson/skincareAPI)
    - reviews (testimonial, productid, review_id): keeps track of reviews written for each product
    - users (id, username, hash, first_name, last_name): login information for each user
- "misc" folder: miscellaneous files, no need to look at them

HOW TO OPEN THE PROGRAM:
To get started, enter the directory ~/project/code through the command line.
1) Execute "cd" to ensure that you’re in ~/ (i.e., your home directory).
2) Execute "cd project" to change into that directory.
3) Execute "cd code" to change into the directory that stores the code for the project.
4) Execute "flask run" and click the link to open the website.

HOW TO USE THE WEBSITE:
We wanted to make the website as user-friendly as possible.
1) To start off, you can make an account my clicking register and entering you information. This includes your first and last name, username, and password. After registering, you will be redirected to
to the login page. Log in.
2) From there, you will see an empty current favorites table. This is because you have not yet browsed or saved any products.
3) Click "Browse" to browse through 1735 of the world's most popular skincare products, via a dropdown menu of product names.
4) Click on a product to learn more. You will be taken to a product page.
5) The product page will contain information on the name, brand, ingredients, and product reviews left by our users for that specific product.
6) If you like the product, go ahead and click save to save it to your favorites!
7) After clicking save, you will be taken to your favorites table again. The column "Shared From Friend" tells you if the product was shared to you by
a friend.
8) If you want to add friends, click the "Friends" tab. You will see a list of all the users who have accounts and if you want, you can add them as
friends so that you can share products with them!
9) To share your favorite products with your friends, click the "Share" tab. You will see two dropdowns, one of your current favorite products and the
other of your current friends. Choose items/people for both to share your product into their favorites! They will see "Yes" in the "Shared from Friend" column in their favorites table.
10) Lastly, you can leave reviews of products you saved in your favorites by clicking the "Review" tab and typing in your review!