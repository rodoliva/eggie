# Product Interface

Currently in my country a concept has gained strength, the awareness of the quality life of the animals we consume.

My project is aimed at a specific group, called happy chickens, eggie is management web application that seeks to help these small producers who really take care of their chickens and want to sell what they do not consume, and in this way reduce their costs.

![Screen record Gif]()


## Database

The first step was to collect some needs, such as income and cost management, somewhere to save the data of the coop, the nest and incubator, with the registration of the number of chickens, roosters, and eggs. With this I made a class database model in Flask-SQLAchemy:

- user: name, password
- sales: description, quantity, unitary price, total income and date
- cost: description, quantity, unitary cost, total cost and date
- eggs: quantity and date
- chicken coop: description, quantity of chickens, quantity of rooster
- chicken nest: description, quantity of chickens, initial and final date
- incubator: description, quantity of eggs, initial and final date

### Web app

The second step was to create a web app with an easy to handle interface that allow to add all of the data to the database. Right now is running in a pythonanywhere web server and is currently collecting real data with a real test user.

### Improvements

The last stage, which begins when data is collected for a month, is to improve the app:

- Add graphics
- Other statistics
- Ability to download data to other platforms
- Work with data passed in the same app
