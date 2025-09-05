from flask import Flask, request, jsonify, render_template
from flask.globals import request
from flask.json import jsonify
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc
import fs
stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())

from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2


import base64
from flask_cors import CORS
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GROUP_INDEX = 0
PROBABILITY_INDEX = 1
SUB_INDEX = 2

food_dict = {
 'DRINKS': ['DRINKS', 'coffee', 'tea', 'milkshake', 'iced tea', 'ALCOHOLIC BEVARAGES', 'liqueur', 'aliment', 'drink',
            'alcohol', 'ale', 'aperitif', 'beer', 'wine', 'white wine', 'whisky', 'vodka', 'vino', 'champagne',
            'cocktail', 'vermouth', 'cobbler', 'cognac', 'rum', 'tequila', 'stout', 'shandy', 'liquor', 'martini',
            'red wine', 'gin', 'Liqueur', 'sake', 'lager', 'mead', 'booze', 'brandy', 'DRINKS', 'SOFT DRINKS',
            'beverage', 'drink', 'coke', 'iced tea' 'milkshake', 'tonic', 'soda', 'fruit tea', 'ginger ale', 'DRINKS',
            'WATER OR JUICE', 'beverage', 'drink', 'cider', 'water', 'compote', 'nectar', 'orange juice', 'smoothie',
            'lemonade', 'juice', 'lime cordial', 'ice', 'DRINKS', 'HOT DRINKS', 'beverage', 'drink', 'black tea',
            'cappuccino', 'espresso', 'black coffee', 'indian tea', 'decaffeinated coffee', 'herbal tea',
            'hot chocolate', 'green tea', ' coffee', 'black coffee', 'mocha'],
 'VEGETABLES': ['VEGETABLES', 'komatsuna', "miner's lettuce", 'lettuce', 'cucumber', 'bitter gourd', 'VEG DISH',
                'polenta', 'summer squash', 'acorn squash', 'succotash', 'ginger', 'orange squash', 'galangal',
                'marinated cucumber', 'puree', 'pattypan squash', 'yellow summer squash', 'VEGETABLES', 'STARCHY VEG',
                'zucchin', 'acorn squash', 'arracacha', 'ahipa', 'yam', 'carrot', 'ulluco', 'tuber', 'taro',
                'sweet potato', 'spuds', 'garlic', 'potato', "lamb's quarters", 'julienne', 'maize', 'mashed potatoes',
                'mashua', 'puree', 'GREEN VEG', 'LEAFY GREEN', 'afalfa sprouts', 'arugula', 'water spinach', 'bay leaf',
                'brussels sprout', 'cabbage', 'cauliflower', 'chard', 'chaya', 'collards', 'common purslane',
                'coriander', 'cress', 'dandelion greens', 'dill', 'tatsoi', 'endive', 'fat hen', 'fennel', 'fiddlehead',
                'swiss chard', 'florence fennel', 'summer purslane', 'french beans', 'spearmint', 'parsley', 'sorrel',
                'lemongrass', 'guar', "lamb's lettuce", 'romaine', 'greater plantain', 'komatsuna/luffa',
                "lettuce/miner's lettuce", 'luffa', 'malabar spinach', 'pak choy', 'radicchio', 'salal', 'spinach',
                'yao choy', 'alfalfa sprouts', 'NON LEAFY GREEN', 'bok choy', 'bamboo shoots', 'courgette',
                'broccolini', 'asparagus', 'cauliflower', 'cardoon', 'celeriac', 'celery', 'celtuce', 'drumstick',
                'chinese artichoke', 'cilantro', 'squash', 'edamame', 'fava beans', 'string bean', 'tomatillo',
                'snow pea', 'snap pea', 'indian pea', 'green pepper', 'ivy gourd', 'iceberg lettuce', 'orache',
                'new zealand spinach', 'mizuna greens', 'malabar', 'spinach', 'kohlrabi', 'artichoke', 'broccoli',
                'hot pepper', 'prussian asparagus', 'samphire', 'ROOT', 'beet', 'cassava', 'ulluco', 'turnip', 'tuber',
                'truffle', 'taro', 'swede', 'sprouts', 'skirret', 'potato', 'rutabaga', 'radish', 'prairie turnip',
                'horse radish', 'jicama', 'jerusalem artichoke', 'ginseng', 'parsnip', 'lotus root', 'hamburg parsley',
                'beet root', 'burdock', 'salsify', 'NIGHTSHADE VEG OR OTHER', 'brinjal', 'cauliflower', 'cayenne',
                'cherry tomato', 'chili pepper', 'aubergine', 'daikon', 'tomato', 'tomatillo', 'tamarillo',
                'sweet pepper', 'mushroom', 'olive', 'onion', 'green onion', 'habanero pepper', 'cayenne pepper',
                'red cabbage', 'jalapeno', 'rhubarb', 'pepper', 'radicchio', 'red pepper', 'vegetable'],
 'FRUIT': ['breadfruit', 'rambutan', 'berry', 'mango', 'watercress', 'water caltrop', 'dried apricot', 'damson',
           'dried fruit', 'fig', 'fluted pumpkin', 'sultanas', 'strawberry', 'grape', 'pineapple', 'pumpkin', 'pomelo',
           'pomegranate', 'plum', 'jabouticaba', 'peppera', 'pear', 'kiwi fruit', 'passionfruit', 'miracle fruit',
           'lychee', 'loquat', 'gourd', 'apple', 'prune', 'redcurrant', 'quince', 'raisin', 'TROPICAL', 'chayote',
           'coconut', 'dragonfruit', 'durian', 'feijoa', 'mango', 'star fruit', 'papaya', 'honeydew melon', 'guava',
           'jackfruit', 'jambul', 'banana', 'cherimoya', 'ensete', 'purple mangosteen', 'rapini', ' bitter gourd',
           'STONE FRUIT (PIT)', 'date', 'sweet cherry', 'physalis', 'jujube', 'cherry', 'MELON', 'watermelon',
           'wintermelon', 'bitter melon', 'cantaloupe', 'melon', 'tinda', 'winter melon', 'BERRIES', 'blueberry',
           'boysenberry', 'bilberry', 'black currant', 'blackberry', 'whortleberry', 'cloudberry', 'cranberry',
           'cranberries', 'currant', 'elderberry', 'mulberry', 'strawberry', 'marionberry', 'gooseberry', 'huckleberry',
           'salmonberry', 'raspberry', 'persimmon', 'peppercorn', 'juniper berry', 'goji berry', 'avocado',
           'CITRIC FRUIT', 'blood orange', 'citron', 'citrus', 'clementine', 'orange', 'ugli fruit', 'tangerine',
           'lemon', 'grapefruit', 'grilled salmon', 'peach', 'lime', 'nectarine', 'mandarin orange', 'kumquat',
           'satsuma'],
 'GRAIN OR CEREAL BASED': ['GRAIN OR CEREAL', 'noodle', 'bran', 'barley', 'wheat flake', 'buckwheat', 'corn',
                           'cornflakes', 'couscous', 'lentil', 'grain', 'horse gram', 'granola', 'garbanzo',
                           'oatmeal cereal', 'oatmeal', 'frozen peas', 'oat', 'muesli bar', 'muesli', 'mochi', 'malt',
                           'groats', 'straw', 'PASTA AND NOODLES', 'angel-hair pasta', 'vermicelli', 'tortellini',
                           'tagliatelle', 'farfalle', 'fettuccine', 'spaghetti carbonara', 'spaghetti bolognese',
                           'spaghetti', 'ravioli', 'ramen', 'penne', 'macaroni', 'linguine', 'lasagne', 'pad thai',
                           'pasta', 'fusilli', 'BREAKFAST OR SNACK', 'cereal', 'cereal bar', 'tortilla chips',
                           'porridge', 'popcorn', 'nachos', 'kettle corn', 'crunch', 'supper', 'goody',
                           'oatmeal cookie', 'pumpernickel', 'RICE', 'brown rice', 'rice', 'rice flake', 'fried rice',
                           'pilaf', 'pike', 'paddy', 'BREAD', 'BREAD PRODUCTS', 'yeast', 'wheat', 'cracker', 'dough',
                           'tapioca', 'rye', 'garlic bread', 'hamburger bun', 'BREAD',
                           'CRACKER OR ALTERNATIVE BREAD BASE', 'crispbread', 'crouton', 'crust', 'toast', 'dumpling',
                           'flatbread', 'cracker', 'BREAD', 'BREAD PREPARED', 'bread rolls', 'breadcrumb', 'bread',
                           'bread pudding', 'brioche', 'brown bread', 'bun', 'canape', 'bread', 'bagel', 'wheat bread',
                           ' baked alaska', 'ciabatta', 'corn bread', 'toast', 'french bread', 'sourdough bread',
                           'soda bread', 'sliced loaf', 'gingerbread', 'rye bread', 'raisin bread', 'meatloaf',
                           'baguette', 'breadstick', 'hot dog bun', 'pita bread'],
 'PLANT-BASED': ['BEANS AND TOFU', 'pumpkin seeds', 'beans', 'velvet bean', 'baked beans', 'broad beans',
                 'yardlong bean', 'winged bean', 'common bean', 'urad bean', 'tofu', 'tepary bean', 'dolichos bean',
                 'soy', 'lima bean', 'mung bean', 'kidney bean', 'azuki bean', 'black beans', 'runner bean',
                 'moth bean', 'ricebean', 'quinoa', 'AROMATICS', 'wild leek', 'welsh onion', 'chives', 'cloves',
                 'tree onion', 'spring onion', 'shallot', 'scallion', 'potato onion', 'peppermint', 'pearl onion',
                 'oyster', 'garlic chives', 'marjoram', 'licorice', 'leek', 'land cress', 'lagos bologi', 'onion',
                 'SEEDS', 'amaranth', 'apricot pits', 'sunflower seeds', 'flax', 'sesame seed', 'pumpkin seeds  ',
                 'pistachio', 'pea', 'okra', 'nopal', 'anise', 'millet', 'PICKLED OR PACKAGED', 'sweet corn',
                 'sour cabbage', 'relish', 'pickled cucumber', 'pickle', 'napa cabbage', 'gherkin', 'sauerkraut',
                 'LEGUMES OR NUTS', 'almond', 'walnut', 'water chestnut', 'beancurd', 'cashew', 'hazelnut', 'chickpeas',
                 'tigernut', 'tarwi', 'tamarind', 'split peas', 'soy', 'pine nut', 'pignut', 'pigeon pea', 'pecan',
                 'peanut', 'pea', 'macadamia nut', 'ground beef', 'chestnut', 'legume', 'nut'],
 'MEAT AND CHICKEN': ['RAW MEAT', 'prime rib', 'loin', 'beef', 'chicken', 'meat', 'tartare', 'antipasto', 'venison',
                      'bruschetta', 'carpaccio', 'beef carpaccio', 'beef tartare', 'meat', 'elephant foot yam',
                      'elephant garlic', 'escargots', 'filet mignon', 'octopus', 'fowl', 'mutton', 'mince',
                      'prosciutto', 'SAUSAGE OR PROCESSED', 'pastrami', 'suet', 'bratwurst', 'wiener', 'blood sausage',
                      'chorizo', 'corned beef', 'spam', 'smoked sausage', 'sausage roll', 'sausage', 'salami',
                      'pepperoni', 'link sausages', 'FRIED MEAT', 'fritter', 'chicken', 'meat', 'steak', 'bacon',
                      'barbecue', 'bird', 'veal', 'chicken', 'chicken breast', 'chicken leg', 'chicken wings',
                      'beef steak', 'turkey breast', 'tenderloin', 'nugget', 'GRILLED/ROASTED', 'chicken', 'meat',
                      'steak', 'baby back ribs', 'brisket', 'veal cutlet', 'bird', 'veal', 'chicken', 'chicken breast',
                      'chicken leg', 'chicken wings', 'beef steak', 'ham', 'venison', 'turkey breast', 'tenderloin',
                      'frankfurters', 'spare ribs', 'skewer', 'sirloin', 'shish kebab', 'pork', 'rib', 'prime rib  ',
                      'pot roast', 'pork chop', 'pancetta', 'lamb chops', 'lamb', 'MEAT DISH', 'marrow', 'chicken',
                      'meat', 'cutlet', 'casserole', 'chicken', 'chicken breast', 'chicken curry', 'chicken leg',
                      'chicken quesadilla', 'chicken wings', 'beef steak', 'cooked meat', 'turkey', 'stir-fry',
                      'venison', 'turkey breast', 'tongue', 'duck', 'spare ribs', 'skewer', 'sirloin', 'shish kebab',
                      'hamburger', 'kebab', 'roast beef', 'pate', 'paella', 'meatball', 'lunchmeat', 'goose',
                      'foie gras', 'hash'],
 'DAIRY OR EGG': ['DAIRY', 'yogurt', 'scrambled', 'omelette', 'NON CHEESE', 'whey', 'chevre', 'chocolate ice cream',
                  'chocolate mousse', 'milk', 'curd', 'custard', 'dairy product', 'dairy', 'DAIRY', 'CHEESE',
                  'camembert', 'chayote', 'brie', 'cottage cheese', 'cheesecake', 'dairy product', 'cream cheese',
                  'edam cheese', 'emmental', 'swiss cheese', 'mozzarella', 'roquefort', 'parmesan', 'gouda cheese',
                  'goats cheese', 'blue cheese', 'cheddar', 'fondue', 'cheese', 'dairy', 'gouda', 'EGG', 'Omelette',
                  'yarrow', 'yolk', 'egg', 'deviled eggs', 'egg white', 'egg yolk', 'eggplant', 'fried egg', 'omelet',
                  'meringue', 'frittata', 'scrambled egg', 'dairy'],
 'SEAFOOD': ['SEAFOOD DISH', 'ceviche', 'chowder', 'clam chowder', 'crab cakes', 'tempura', 'fried calamari', 'squid',
             'lobster bisque', 'salmon steak', 'bream', 'seafood', 'RAW SEAFOOD', 'tuna tartare', 'PLANT', 'seaweed',
             'dulse', 'sea lettuce', 'sea grape', 'seaweed salad', 'sea kale', 'sea beet', 'laver', 'kale',
             'good king henry', 'hijiki', 'kombu', 'wakame', 'DELICACY', 'caviar', 'lobster', 'roe', 'FISH', 'anchovy',
             'bass', 'carp', 'cockle', 'tuna', 'sardine', 'crab', 'cuttlefish', 'trout', 'fillet', 'fillet of sole',
             'fish steak', 'flatfish', 'sturgeon', 'salted fish', 'smoked fish', 'smoked salmon', 'snapper',
             'sea perch', 'sea bass', 'lox', 'haddock', 'halibut', 'herring', 'salmon steak', 'salmon', 'plaice',
             'pilchard', 'perch', 'mackerel', 'kingfish', 'kipper', 'fish fillet', 'prawn', 'scampi', 'fish', 'marron',
             'SHELLFISH', 'calamari', 'clam', 'crayfish', 'eel', 'mussel', 'shellfish', 'scallop', 'shrimp'],
 'DESSERT': ['CAKE', 'red velvet cake', 'cookie', 'baked alaska', 'brownie', 'cake', 'cake mix', 'cake pop',
             'carrot cake', 'cheesecake', 'chocolate cake', 'chocolate chip cake', 'cupcake', 'tiramisu', 'flan',
             'spongecake', 'sponge cake', 'souffle', 'shortcake', 'panna cotta', 'fruitcake', 'knish', 'birthday cake',
             'red velvet cake' 'PIE OR TART', 'apple pie', 'blueberry pie', 'whoopie pie', 'crumble', 'tartlet', 'tart',
             'strudel', 'porridge', 'pie', 'mousse', 'meat pie', 'pork pie', 'quiche', 'BAKED GOODS',
             'chocolate cookie', 'cinnamon roll', 'biscuits', 'viennese', 'croissant', 'crescent roll', 'crumble',
             'eclair', 'english muffin', 'muffin', 'sesame roll', 'poppy seed roll', 'scone', 'raisin muffin', 'PASTRY',
             'blueberry muffin', 'viennese', 'Baklava', 'beignets', 'roulade', 'millefeuille', 'blancmange', 'cannoli',
             'chocolate cupcake', 'cinnamon roll', 'macaroon', 'baklava', 'danish pastry', 'galette', 'pastry',
             'BATTER BASED', 'waffle', 'doughnut', 'macaron', 'pavlova', 'pancake', 'crepe', 'pavlova', 'popovers',
             'CONFECTION', 'brittle', 'sweetmeat', 'sprinkles', 'sweet', 'CANDY', 'bonbon', 'candy', 'candy apple',
             'candy bar', 'caramel apple', 'chocolate candy', 'chocolate cookie', 'chocolate ice cream', 'toffee',
             'popsicle', 'marshmallow', 'jelly beans', 'jordan almonds', 'nougat', 'caramel', 'marzipan', 'bonbons',
             'lollipop', 'GEL/LIQUID OR ICECREAM', 'apple sauce', 'brulee', 'parfait', 'chocolate mousse',
             'cranberry sauce', 'creme brulee', 'tiramisu', 'syrup', 'sundae', 'chocolate ice cream', 'milk chocolate',
             'spread', 'honey', 'sorbet', 'sherbet', 'ice cream', 'pudding', 'praline', 'frozen yogurt', 'mole sauce',
             'marmalade', 'maple syrup', 'grape jelly', 'gelatin', 'jam', 'jelly', 'CHOCOLATE', 'wafer', 'candy bar',
             'chocolate bar', 'chocolate cake', 'chocolate candy', 'm&m', 'torte', 'granola bar', 'souffle',
             'granola bar', 'fudge', 'chocolate', 'FRIED', 'churros'],
 'PREPARED DISHES OR SNACKS': ['ITALIAN', 'gyoza', 'pizza', 'spaghetti carbonara', 'spaghetti bolognese', 'spaghetti',
                               'ravioli', 'gorgonzola', 'parmesan', 'frozen pizza', 'risotto', 'DEEP FRIED',
                               'croquette', 'tempura', 'falafel', 'fish and chips', 'fish fingers', 'french fries',
                               'french toast', 'fried calamari', 'onion rings', 'samposa', 'SOUP OR STEW', 'chowder',
                               'casserole', 'soup', 'french onion soup', 'miso soup', 'pho', 'gazpacho',
                               'SALTY SPREADS', 'hummus', 'liver pate', 'BREAKFAST DISH', 'croque madame', 'falafel',
                               'huevos rancheros', 'ASIAN', 'takoyaki', 'sushi', 'spring rolls', 'bibimbap', 'sashimi',
                               'nigiri', 'mozuku', 'ogonori', 'hijiki', 'kombu', 'pad thai', 'nori', 'curry',
                               'MIDDLE-EASTERN', 'falafel', 'melokhia', 'tajine', 'tabouli', 'samosa', 'pita bread',
                               'ITALIAN', 'lasagna', 'focaccia', 'gnocchi', 'MEXICAN', 'tacos', 'huevos rancheros',
                               'SAVORY SNACK', 'chips', 'tempura', 'grissini', 'kombu', 'pretzel',
                               'SANDWICHES AND WRAPS', 'burrito', 'sandwich', 'gyro', 'shawarma',
                               'grilled cheese sandwich', 'hot dog', 'SALADS', 'caesar salad', 'caprese salad',
                               'corn salad', 'salad', 'cole slaw', 'tzatziki', 'slaw', 'seaweed salad', 'fruit salad',
                               'greek salad', 'coleslaw', 'hijiki', 'tamale', 'collation', 'marinated herring',
                               'ricotta', 'poutine', 'tabouli', 'beet salad'],
 'MISC': ['VINEGAR', 'gravy', 'balsamic', 'vinaigrette', 'vinegar', 'SAUCE OR CONDIMENT', 'barbecue sauce', 'bechamel',
          'white sauce', 'chili sauce', 'chutney', 'condiment', 'coulis', 'tomato sauce', 'teriyaki',
          'sweet-and-sour sauce', 'steak sauce', 'french dressing', 'mustard', 'spaghetti sauce', 'soy sauce',
          'sour cream', 'italian dressing', 'salsa', 'salad dressing', 'pesto', 'pasta sauce', 'garlic sauce',
          'meat sauce', 'mayonnaise', 'wasabi', 'hot sauce', 'ketchup', 'guacamole', 'russian dressing', 'sauce',
          'SAVORY LIQUID', 'broth', 'aspic', 'soup', 'goulash', 'OIL OR CREAM', 'butter', 'buttercream',
          'whipped cream', 'cream', 'peanut butter', 'olive oil', 'margarine', 'butter', 'lard', 'oil'],
 'HIDE': ['BAKING INGREDIENTS', 'ladle', 'mate', 'batter', 'cocoa', 'flour', 'plain flour', 'molasses', 'SPICES',
          'allspice', 'caraway', 'cardamom', 'cayenne', 'chicory', 'chili', 'chili powder', 'anice', 'cinnamon',
          'cumin', 'turmeric', 'thyme', 'salt', 'paprika', 'pepper', 'oregano', 'marzipan', 'garam masala',
          'lemon peel', 'saffron', 'matcha', 'nutmeg', 'spices', 'HERBS', 'basil', 'chickweed', 'chicory', 'tarragon',
          'thyme', 'sunflower', 'squash blossoms', 'sorghum', 'scorzonera', 'rosemary', 'rose', 'paracress', 'oregano',
          'borage', 'sierra leone bologi', 'lavender', 'herb', 'mint', 'Brassicaceae', 'NONFOOD', 'aliment', 'aonori',
          'broil', 'carbohydrate', 'comestible', 'dessert', 'dollop', 'feast', 'fodder', 'gastronomy', 'gem', 'grass',
          'grub', 'hay', 'jug', 'kettle', 'micronutrient', 'nibble', 'papillote', 'pasture', 'peapod', 'platter',
          'puff', 'ratatouille', 'ration', 'sage', 'saute', 'spatula', 'spork', 'supper', 'unleavened', 'cucurbitaceae']
}

pizzaSub = [
    {"name": "Margarita Pizza", 'size': 0.6},
    {"name": "Olive Pizza", 'size': 0.6},
    {"name": "Mushroom Pizza", 'size': 0.6},
    {"name": "Corn Pizza", 'size': 0.6}
]

def add_to_probability_list(probability_list, food_group, food_to_append, food_probability):
 '''
 This functino will try to add a specific food to the proability list if the food_group of it is already in the list
 If the food_group is already it will add it there (add up the probbility and add the food to the SUB list) and return True!
 Else, it won't add it and return False!

 #probability_list = [[GROUP, PROBABILITY, [SUB]], [GROUP, PROBABILITY, [SUB]], [GROUP, PROBABILITY, [SUB]]]
 '''
 found = False  # Making sure found is False for the sake of the for loop, otherwise the loop will endlessly find the sub_list, remove and append it.
 for sub_list in probability_list:  # Loop to find the item's group
  if food_group == sub_list[GROUP_INDEX]:
   sub = sub_list
   probability_list.remove(sub_list)
   sub[PROBABILITY_INDEX] += food_probability  # Adding up the probability
   sub[SUB_INDEX].append(food_to_append)  # Appending the key to the SUB list
   probability_list.append(sub)
   found = True  # Doing this because otherwise the loop will endlessly find the sub_list, remove and append it.
   break  # Stop the loop, we found what we need

 return found


def bubbles_backend(result):
    """
    This function will get the food suggestions from Clarifai ("result") and return a json in the form:
    {data: [
        {name: <GROUP_NAME>, size: <PROBABILITY>, sub: [{name:<FOOD_NAME>, size: <PROBABILITY>}, {name:<FOOD_NAME>, size: <PROBABILITY>}, ...]},
        {name: <GROUP_NAME>, size: <PROBABILITY>, sub: [{name:<FOOD_NAME>, size: <PROBABILITY>}, {name:<FOOD_NAME>, size: <PROBABILITY>}, ...]},
        {name: <GROUP_NAME>, size: <PROBABILITY>, sub: [{name:<FOOD_NAME>, size: <PROBABILITY>}, {name:<FOOD_NAME>, size: <PROBABILITY>}, ...]},
        ...
    ]}
    """
    group_found = False
    # probability_list = [[GROUP, PROBABILITY, [SUB]], [GROUP, PROBABILITY, [SUB]], [GROUP, PROBABILITY, [SUB]]]
    probability_list = []

    # This block of code will fill the probability list (above)
    for key in result.keys():  # Running on all the outputs of Clarifai.    key = the specific food
        group_found = False  # For each key
        for group in food_dict.keys():  # Running on all the food groups in the food dict
            # If the output from Clarifai in is this food group
            if key in food_dict[group]:
                # Declares that a (level B) food group was found
                group_found = True
                if add_to_probability_list(probability_list, group, key,
                                           result[key]):  # If the food group is already in the probability list
                    continue
                else:  # If the food group is not in the list
                    # Add new element: GROUP = group,  SUB = [key]
                    probability_list.append([group, result[key], [key]])

        if not group_found:  # If a food group wasn't found for this specific food, make new group
            if add_to_probability_list(probability_list, 'OTHER', key, result[key]):
                continue
            else:
                # Add new element: GROUP = group,  SUB = [key]
                probability_list.append(['OTHER', result[key], [key]])

    # This block of code will divide the probability sum by the num of items found in this group.
    main_list = []
    # probability_list = [[GROUP, PROBABILITY, [SUB]], [GROUP, PROBABILITY, [SUB]], [GROUP, PROBABILITY, [SUB]]]
    for item in probability_list:
        if item[GROUP_INDEX] == 'HIDE':
            # This is a special case, if the answer from Clarifai contains something from the group 'HIDE' (See food_dict to understand) then it shouldn't show (for now at least))
            continue
        # {name: <GROUP_NAME>, size: <PROBABILITY>, sub: [{name:<FOOD_NAME>, size: <PROBABILITY>}, {name:<FOOD_NAME>, size: <PROBABILITY>}, ...]}
        temp_dict = {}
        # [{name:<FOOD_NAME>, size: <PROBABILITY>}, {name:<FOOD_NAME>, size: <PROBABILITY>}, ...]
        temp_sub_list = []
        for food in item[SUB_INDEX]:
            if (food.lower() == "pizza"):
                temp_sub_list.append(
                    {'name': food, 'size': result[food], "sub": pizzaSub})
            else:
                temp_sub_list.append(
                    {'name': food, 'size': result[food]})

        temp_dict['name'] = item[GROUP_INDEX]
        temp_dict['size'] = float(
            item[PROBABILITY_INDEX]) / len(item[SUB_INDEX])
        temp_dict['sub'] = temp_sub_list

        main_list.append(temp_dict)

    main_dict = {'data': main_list}
    return json.dumps(main_dict)


# with open("C:/Users/adams/Downloads/Eq_it-na_pizza-margherita_sep2005_sml.jpg", "rb") as img_file:
#     my_string = base64.b64encode(img_file.read())

filename = 'pizza.jpg'  # I assume you have a way of picking unique filenames



def convert(my_string):
    imgdata = base64.b64decode(my_string)
    # print(imgdata)
    with open(filename, 'wb') as f:
        f.write(imgdata)
    with open(filename, "rb") as f:
        file_bytes = f.read()

    # print(file_bytes)
    api_key = os.getenv('CLARIFAI_API_KEY', 'YOUR_API_KEY_HERE')
    metadata = (('authorization', f'Key {api_key}'),)
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            model_id="bd367be194cf45149e75f01d59f77ba7",
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            base64=file_bytes
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )

    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

    # Since we have one input, one output will exist here.
    output = post_model_outputs_response.outputs[0]
    print(output.data.concepts[0])
    y = []
    z ={}
    for x in output.data.concepts:
        z[x.name] = x.value

    return z


def bmi(weight, height):
 return weight / (height ** 2)


def pounds(weight_in_kg):
 return weight_in_kg * 2.205


def cal(weight, activity):
 return pounds(weight) * 15 - (activity * 100)


def protein(weight, recommendation_dict):
 if recommendation_dict['weight_gain'] is False and recommendation_dict['muscle_gain'] is False:
  return weight * 0.7

 if recommendation_dict['weight_gain'] is True and recommendation_dict['muscle_gain'] is False:
  return weight * 1.5

 if recommendation_dict['muscle'] is True:
  return weight * 2


def fiber(sex, age, calorie_intake):
 modifier = (calorie_intake - 2000) / 1000 * 14 if calorie_intake >= 2000 else 0

 if sex == 'Male' and age < 50:
  return 35 + modifier

 if sex == 'Female' and age < 50:
  return 25 + modifier

 if sex == 'Male' and age > 50:
  return 30 + modifier

 if sex == 'Female' and age > 50:
  return 20 + modifier


def carbs(calories, recommendation_dict):
 return calories / 8 if recommendation_dict['reduce_carbs'] is False else calories / 10


def sugar(calories, age, recommendation_dict):
 if age > 18 and recommendation_dict['reduce_sugar'] is False:
  return calories / 53
 if age < 18 and recommendation_dict['reduce_sugar'] is False:
  return calories / 53 - 5

 if age > 18 and recommendation_dict['reduce_sugar'] is True:
  return calories / 53 - 10
 if age < 18 and recommendation_dict['reduce_sugar'] is True:
  return calories / 53 - 15


def total_lipid(calories, recommendation_dict):
 if recommendation_dict['reduce_fats'] is False:
  return calories / 25
 else:
  return calories / 30


def saturated(calories, recommendation_dict):
 tot_lip = total_lipid(calories, recommendation_dict)

 if recommendation_dict['reduce_fats'] is False:
  return tot_lip / 3
 else:
  return tot_lip / 3 - 5


def trans(calories, recommendation_dict):
 tot_lip = total_lipid(calories, recommendation_dict)

 if recommendation_dict['reduce_fats'] is False:
  return tot_lip / 12
 else:
  return tot_lip / 15


def cholesterol(recommendation_dict):
 if recommendation_dict['reduce_cholesterol'] is False:
  return 300
 else:
  return 200


def sodium(calories, age, recommendation_dict):
 if age > 18 and recommendation_dict['reduce_sodium'] is False:
  return calories * 1.15

 elif age < 18 and recommendation_dict['reduce_sodium'] is False:
  return calories * 1.15 - 200

 else:
  return calories * 0.9


def recommendation(height, weight, activity, sex, age, recommendation_dict):
 """
 recommendation_dict = {
     'weight_loss': bool,
     'weight_gain': bool,
     'muscle_gain': bool,
     'weight_maintain': bool,
     'reduce_carbs': bool,
     'reduce_sugar': bool,
     'increase_fiber': bool,
     'reduce_fats': bool,
     'reduce_cholesterol': bool,
     'reduce_sodium': bool
 }
 ^^ RECOMMENDATION DICT PASSED IN THIS FORMAT (ALL GOALS MUST EXIST)
 :param bmi:
 :param cal:
 :param recommendation_dict:
 :return:
 """
 bmi_user = bmi(weight, height)

 if bmi_user <= 19.5:
  recommendation_dict['weight_loss'] = False
 elif bmi_user > 32:
  recommendation_dict['weight_gain'] = False

 calories = cal(weight, activity)
 nutrient_dict = {
  'proteins': protein(weight, recommendation_dict),
  'fibers': fiber(sex, age, calories),
  'carbs': carbs(calories, recommendation_dict),
  'sugars': sugar(calories, age, recommendation_dict),
  'total_lipids': total_lipid(calories, recommendation_dict),
  'saturated_fats': saturated(calories, recommendation_dict),
  'trans_fats': trans(calories, recommendation_dict),
  'cholesterol': cholesterol(recommendation_dict),
  'sodium': sodium(calories, age, recommendation_dict)
 }
 return nutrient_dict


def CompareNut(json,nutrient_dict):
    GoodDict = {}
    BadDict = {}
    if json['Carbohydrate, by difference'] >= nutrient_dict['carbs'] * 7:
        GoodDict['carbs'] = json['Carbohydrate, by difference'] - (nutrient_dict['carbs'] * 7)
    else:
        BadDict['carbs'] = (nutrient_dict['carbs'] * 7) - json['Carbohydrate, by difference']
    if json['Protein'] >= nutrient_dict['proteins'] * 7:
        GoodDict['proteins'] = json['Protein'] - (nutrient_dict['proteins'] * 7)
    else:
        BadDict['proteins'] = (nutrient_dict['proteins'] * 7) - json['Protein']
    if json['Fiber, total dietary'] <= nutrient_dict['fibers'] * 7:
        GoodDict['fibers'] = (nutrient_dict['fibers'] * 7) - json['Fiber, total dietary']
    else:
        BadDict['fibers'] = json['Fiber, total dietary'] - (nutrient_dict['fibers'] * 7)
    if json['Sugars, total including NLEA'] >= nutrient_dict['sugars'] * 7:
        GoodDict['sugars'] = json['Sugars, total including NLEA'] - (nutrient_dict['sugars'] * 7)
    else:
        BadDict['sugars'] = (nutrient_dict['sugars'] * 7) - json['Sugars, total including NLEA']
    if json['Fatty acids, total saturated'] >= nutrient_dict['saturated_fats'] * 7:
        GoodDict['saturated_fats'] = json['Fatty acids, total saturated'] - (nutrient_dict['saturated_fats'] * 7)
    else:
        BadDict['saturated_fats'] = (nutrient_dict['saturated_fats'] * 7) - json['Fatty acids, total saturated']
    if json['Total lipid (fat)'] >= nutrient_dict['total_lipids'] * 7:
        GoodDict['total_lipids'] = json['Total lipid (fat)'] - (nutrient_dict['total_lipids'] * 7)
    else:
        BadDict['total_lipids'] = (nutrient_dict['total_lipids'] * 7) - json['Total lipid (fat)']
    if json['Fatty acids, total trans'] >= nutrient_dict['trans_fats'] * 7:
        GoodDict['trans_fats'] = json['Fatty acids, total trans'] - (nutrient_dict['trans_fats'] * 7)
    else:
        BadDict['trans_fats'] = (nutrient_dict['trans_fats'] * 7) - json['Fatty acids, total trans']
    if json['Cholesterol'] >= nutrient_dict['cholesterol'] * 7:
        GoodDict['cholesterol'] = json['Cholesterol'] - (nutrient_dict['cholesterol'] * 7)
    else:
        BadDict['cholesterol'] = (nutrient_dict['cholesterol'] * 7) - json['Cholesterol']
    if json['Sodium, Na'] >= nutrient_dict['sodium'] * 7:
        GoodDict['sodium'] = json['Sodium, Na'] - (nutrient_dict['sodium'] * 7)
    else:
        BadDict['sodium'] = (nutrient_dict['sodium'] * 7) - json['Sodium, Na']
    return {GoodDict, BadDict}





app = Flask(__name__)
CORS(app)

@app.route('/')
def main():
    return render_template("main.html")


@app.route('/img/', methods=['GET', 'POST'])
def index():
    content = request.json
    img = content['image_base64']
    result = convert(img)
    return result

@app.route('/imgfull/', methods=['GET', 'POST'])
def imgfull():
    content = request.json
    img = content['image_base64']
    result = convert(img)
    result['pizza'] = 0.9896452903747559
    print(result)
    return bubbles_backend(result)

@app.route('/recommendation/', methods=['GET', 'POST'])
def recommendation():
    content = request.json
    recommendation(content.height, content.weight, content.activity, content.sex, content.age, content.recommendation_dict)



if __name__ == '__main__':
    app.run(debug=True)
