## AI Tool:I have used Claude for AI assistance 
## Framework:Django

## Prompt 1-First i pasted the word document to claude and asked "in here what i have to do in this assignment"
Accepted <br>
Then it properly break the assignment and explain me the assignment and i cross checked it with my own understanding


## Prompt2-Can you suggest some edge cases
Accepted <br>
So i have some edge cases of my own then i added these with given by claude

## Prompt 3-i am thinking of creating a json like structure where box its dimensions,cost,max weight carrying category all is listed and not using any db then when we use POST request the server will calculate the total volume(if multiple products) and weight . then all this volume,weight is compared with this boxes in json if products total volume and weight is lesser or equal to any of the boxes in the json file we will return that boxes info
Accepted <br>
this i thought to not include db at first so as to decrease the complexity of this project then i consult it with claude and also think if we don't have db then we can't be add more box if new box will be included in future, so added database and used postgresSQL for the same

## Prompt4-i am creating 'box' table which will have Serial No,Internal Dimension,Cost,Weight Capacity,Cost
Accepted <br>
Consult the structure of box table which will be carrying the different type of boxes.

## Prompt 5-Also i don't think other than this table any other table is needed because everyproduct is different and we have to just compare the product dimensions weight against the box's weight capacity and dimenstion
Accepted <br>
Then i again i took decision of not making any further table which means initially i thought i also will make product table but when thought and saw use case it was clear just give the product input the backend should check it return the suitable box if it exists in the table else return "No suitable box"

## Prompt6-now create sample data for this box table to inserted in atleast 10 different boxes
Accepted <br>
Now i generate dummy data for box table through this prompt 

## Prompt7-i am creating one POST API which will inside body contains the given products dimenstions,weight capacity
Accepted <br>
Consulted about the API creation in this project


## Prompt8-i want to ask if asesser clone this project pushed on github then how database he will install or what he need to do?
Accepted <br>
Asked and in what way should i maked readme.md file so that accesser can understand and run this project in his local environment

## Prompt9-To debug the code at different places


