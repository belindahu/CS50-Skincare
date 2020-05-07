OUR INITIAL IDEAS:
Our idea came when we found an API for skincare products online: https://github.com/LauraRobertson/skincareAPI. We wanted to make a spinoff of the Finance
problem set, calling the API constantly to access the data and run the website. In terms of functionality, our goals at the beginning of the project
were as follows:
1) GOOD outcome:
- Gather data about products
- Ability to save a product
- Ability to share a product
2) GREAT outcome:
- Gather data about products
- Ability to save a product
- Ability to share a product
- Ability to like a product
- Ability to leave comments
3) BEST outcome:
- Gather data about products
- Ability to save a product
- Ability to share a product
- Ability to like a product
- Ability to leave comments
- Create recommendations for products based off of inputted information

Given these goals, we hit everything in our BEST outcome except for creating product recommendations, which would have been our next step if we had
more time and resources.

THE PROCESS:
1) application.py
To start out, we based the structure off of the Finance problem set, keeping the login and register functions the same. From there, we worked to adapt
the existing functions to our project, for example, adapting the quote function from Finance to a browse function. In application.py, we have ten functions,
as follows:
- def register(): same as finance

- def login(): same as finance

- def index(): this renders the favorites template (saved.html). Originally, we wanted to make the index page a Welcome page. However, we ran into issues
routing. This was because when we tried to change the routing, the saved page would be routed to the index pagee. As such, we just left the homepage as the
favorites page. So when a user logs on, they will see their current favorites, and if they are new, they will see a new table.

- def browse(): this function allows the user to browse products via a dropdown bar of all 1735 products. Initially, we wanted to allow users to browse by
ingredient, hoping to create a dynamic search bar that would autocomplete. After attempting to implement that, we realized that it would make more sense
for the user to browse by product name rather than by ingredient. As such, we implemented a dropdown menu similar to the sell function in Finance. To
do this, we used a form on our browse.html page, which led to our browsed.html page. Furthemore, as we began to implement features like reviews and ingredients
to display on the browsed.html page, we added these features into the browse function. To keep track of products as the user navgiated through the website, we
stored the product ID in the buttons; for example, we stored the product IDin the "Save Product" button on the browsed.html page.

- def save(): Storing product IDs in the save button allows us to access it in our saved function and we use this ID to pull product information from the products
table to save the product to our favorites table. Within the save function, we also check to see if the product the user wants to save is already saved, and
only if not, inserting it into the favorites table. This is achieved by pulling all current favorites with the same product ID; if the length of these favorites is 0,
then we know the product is not already saved into favorites. Thus, we insert this product into the favorites table using a SQL command. From there, we pass the data
from the updated favorites table to saved.html to display the updated saved products.

- def friends(): this function allows the user to friend other users of the website. We accomplished this by pulling the relevant information about each user in our
database and displayed their information in table. Within this table, there is a column for the "Friend" button. This friend button is active only when
the other person is not already your friend. How did we accomplish this? Note that the friends datatable consists of two columns: friend1id and friend2id.
The order of friend1id and friend2id shouldn't matter in theory; however, to accomodate the fact that there are two distinct columns, we replicate the following logic
twice: if the user's session id is in one of the columns of a single row in the data, this means that the user is friends with the other friendid in the adjacent column.
Let's assign that other person id into a list. Now in the HTML of friends, we disable the friends button if the user_id of an individual exists in this previously discussed
list. If we have passed the previous check, then we insert the new friendship into the "friends" table. We made the key assumption that you are immediately friends after
clicking the button.

- def share(): the share function allows the user to share their favorite products with their friends. By utilizing multiple tables and building out various lists,
we are able to insert a product saved to the favorites of one user into the favorites table of their friend. We begin by calling all data needed - current favorites
of the user and all of their friends. Because friendships are two way relationships, we query the friends table twice, one in which the user is the first friend and the
second query in which the user is the second friend. Then, we initialize three lists: product name, friend name, and friend ID. We build out these lists by iterating through the
data and appending ID and name, then passing these lists into the share.html page. The share.html page requests the user to choose a product to share and a friend
to share it to. After these are chosen, we use the values stored in these forms to query the database and insert the product into the friend's favorites table via a SQL command,
redirecting back to the index page afterwards.

- def review(): the review function allows users to leave reviews for products they have shared in their favorites. We first call all the information necessary (as data) to build out
another list of product names (symbol_list) that are already saved in favorites. We build this list by iterating through data and appending product names derived from each row in the
data. This list is then passed through the review.html template, allowing users to select for which product they want to write a review. The product id, and the review they write,
are then inserted into the reviews table using a SQL query. The review.html template is renderred afterwards so the user can continue writing reviews.

2) helpers.py: This file was slightly modified from the finance PSET. In short, we only kept the apology and login_required functions. We did not need the other functions like
usd and lookup. We did not need usd because our website does not incorporate money. We did not need lookup because we decided to download all the information from the API.
After downloading the data, we inputted the data into our SQL database. The logic for the data input is included below.

2a) data.py: This python script was created to download all the product data from the API. The data was downloaded as a PANDA dataframe for easy data manipulation. Then we exported
the dataframe as a CSV to easily load the data into the SQL database.

2b) loaddata.py: This python script opens the csv file containing data about all the products in the database and inserts the data into our products table in our database.

3) skincare.db: As mentioned in the README.md, the skincare database contains various tables. The design of the database was changed and developed as the project progressed,
and we had to make multiple revisions. As mentioned in the section above, we wanted to continuously call the API to gather the information we needed. However, after
developing the project further, we realized it would be a better idea to download all for the product information into a products table in skincare.db, as well as an ingredients
table. This made it easier to access data and call it in specific ways that the online API did not support, like calling by product name. The other tables were created to
support other functions, and were adapted as needed as the code was written.

4) Styling

- browse.html: Summary: the browse page allows the user to go through the entire database of 1735 skin care products and pull up more information. In terms of style, the html file
also includes a Bootstrap carousel that cycles through some aesthetic, skincare-related images. These style features were mostly pulled from bootstrap. We decided to nest most of
of the features of the website in a container. We decided to do this to easily manipulate the color background of the elements. Previously, there was an issue that the table and
space between the carousel and the page header showed the background image. This issue was reconciled by styling the main container as a white background. In order to cycle through
all the products, we use a similar feature from the finance problem set, the sell function. In other words, this creates a dropdown select. Additionally, in order to allow each page
to have a unique background image, we create another jinja block that allows us to easily overwrite the style.css. We create a new css file for each page.

- browsed.html: the browsed page features product information, like product name, brand, and ingredients. We styled it in a way so that the ingredients, which were originally
inputted into the database as simple text, was converted into a list so we could iterate through it and format it as a list on the template page. Using the information from the
SQL queries in the browse function, we create a dynamic header using jinja as we did in the finance problem set. For aethestic purposes, we split the page into two columns.
The left column houses the Ingredients; the right column houses the Product Reviews. Using a component from Bootstrap, we fixed the height of the information stored in the column
and made it scrollable for better readability. Each element in the scrollable portion was created through a  for loop. We also include a counter for the number of times a particular
product was "favorited." Finally, there's a button, "submit form," at the bottom that allows us to pull the name of the product and input the relevant product information into our
database.

- friends.html: the friends page features all of the existing users and displays a button for the user to friend other users. When clicked for a certain user, the button will
disappear and the word "Friended!" will appear. This table features every user besides the user him/herself.The page uses jinja if statements to activate/deactivate the friend button.
While we could have used javascript to make the button dynamic, we were more familiar with jinja than javascript.

- saved.html: the saved page features the current favorites a user has saved in a table, with name, brand, and whether or not the product was shared from a friend. We iterate through
a dictionary of information pulled from the favorites table to display this information. As aforementioned, we placed the page elements in another main container to make it easier to
manipulate the element's background color.

- share.html: the share page features two dropdown menus of 1. products saved by the user and 2. the user's friends, so that the user can choose what to share and who to share it to.
- We decided to use a dropdown menu for the following reason. IF we allowed users to input text, it is difficult to ensure that the user types everything out corretly. Thus, a dropodwn
- menu solves this problem.

- review.html: the review page features two forms, a dropdown menu of products saved by the user and a text box for the user to write a review, as well as a button to submit the
review. While we originally invisioned allowing users to write comments about each product like commenting on a Facebook post, it became unclear what that might look like. Thus we
modeled this functionality off of product review features that exist on eCommerce websites.

FUTURE DIRECTIONS:
While we are very satisfied with the way this project turned out given the limited time, there are a few directions we could take this in if given more time and resources.
They are as below:
- expand the browse function to allow users to search up products by ingredient or brand
- clean the data to make it more pretty (capitalization, grammer)
- inputting product images and links to buy the products
- show who shared products in the favorites table
- implement riend requests and confirmation, instead of automatically becoming friends with someone
- show who reviewed product on browsed.html page
- allow users to click intto ingredients to search them up
- share product confirmation
- set a limit for the number of reviews a user can write per product
- link browsed.html templates for products from favorites table