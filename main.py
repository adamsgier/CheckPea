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

GROUP_INDEX = 0
PROBABILITY_INDEX = 1
SUB_INDEX = 2

food_dict = {
    'DRINKS':
        ['drink',
         'alcohol',
         'ale',
         'aperitif',
         'beer',
         'wine',
         'white wine',
         'whisky',
         'vodka',
         'vino',
         'champagne',
         'cocktail',
         'vermouth',
         'cobbler',
         'cognac',
         'rum',
         'tequila',
         'stout',
         'shandy',
         'liquor',
         'martini',
         'red wine',
         'gin',
         'Liqueur',
         'sake',
         'lager',
         'mead',
         'drink',
         'coke',
         'iced tea',
         'milkshake',
         'tonic',
         'soda',
         'fruit tea',
         'ginger ale',
         'drink',
         'cider',
         'water',
         'compote',
         'nectar',
         'orange juice',
         'smoothie',
         'hot chocolate',
         'juice',
         'drink',
         'black tea',
         'cappuccino',
         'espresso',
         'black coffee',
         'indian tea',
         'decaffeinated coffee',
         'herbal tea'
         ]
    ,

    'VEGETABLES':
        ['summer squash',
         'acorn squash',
         'succotash',
         'ginger',
         'orange squash',
         'galangal',
         'marinated cucumber',
         'acorn squash',
         'arracacha',
         'ahipa',
         'afalfa sprouts',
         'arugula',
         'water spinach',
         'bok choy',
         'bamboo shoots',
         'courgette',
         'beet',
         'cassava',
         'ulluco',
         'brinjal',
         'cauliflower',
         'cayenne',
         'carrot',
         'ulluco',
         'tuber',
         'taro',
         'sweet potato',
         'spuds',
         'garlic',
         'potato',
         "lamb's quarters",
         'julienne',
         "brussels sprout",
         'cabbage',
         'cauliflower',
         'chard',
         'chaya',
         'collards',
         'common purslane',
         'coriander',
         'cress',
         'dandelion greens',
         'dill',
         'tatsoi',
         'endive',
         'fat hen',
         'fennel',
         'fiddlehead',
         'swiss chard',
         'florence fennel',
         'summer purslane',
         'french beans',
         'spearmint',
         'parsley',
         'sorrel',
         'lemongrass',
         'guar',
         "lamb's lettuce",
         'romaine',
         'greater plantain',
         'komatsuna',
         "miner's lettuce",
         'lettuce',
         'asparagus',
         'cauliflower',
         'cardoon',
         'celeriac',
         'celery',
         'celtuce',
         'drumstick',
         'chinese artichoke',
         'cilantro',
         'squash',
         'edamame',
         'fava beans',
         'string bean',
         'tomatillo',
         'snow pea',
         'snap pea',
         'indian pea',
         'green pepper',
         'ivy gourd',
         'iceberg lettuce',
         'orache',
         'new zealand spinach',
         'frozen peas',
         'mizuna greens',
         'malabar',
         'spinach',
         'kohlrabi',
         'tuber',
         'truffle',
         'taro',
         'swede',
         'sprouts',
         'skirret',
         'potato',
         'rutabaga',
         'radish',
         'prairie turnip',
         'horse radish',
         'jicama',
         'jerusalem artichoke',
         'ginseng',
         'parsnip',
         'lotus root',
         'hamburg parsley',
         'chili pepper',
         'aubergine',
         'daikon',
         'tomato',
         'tomatillo',
         'tamarillo',
         'sweet pepper',
         'mushroom',
         'olive',
         'onion',
         'green onion',
         'habanero pepper',
         'red cabbage',
         'jalapeno']
    ,

    'FRUIT':
        ['breadfruit',
         'mango',
         'watercress',
         'water caltrop',
         'dried apricot',
         'damson',
         'dried fruit',
         'fig',
         'fluted pumpkin',
         'sultanas',
         'strawberry',
         'grape',
         'pineapple',
         'pumpkin',
         'pomelo',
         'pomegranate',
         'plum',
         'jabouticaba',
         'peppera',
         'pear',
         'kiwi fruit',
         'passionfruit',
         'miracle fruit',
         'lychee',
         'loquat',
         'gourd',
         'chayote',
         'coconut',
         'dragonfruit',
         'durian',
         'feijoa',
         'mango',
         'star fruit',
         'papaya',
         'honeydew melon',
         'date',
         'sweet cherry',
         'physalis',
         'jujube',
         'guava',
         'jackfruit',
         'jambul',
         'watermelon',
         'wintermelon',
         'bitter melon',
         'melon',
         'tinda',
         'guava',
         'jackfruit',
         'jambul',
         'blueberry',
         'boysenberry',
         'bilberry',
         'black currant',
         'blackberry',
         'whortleberry',
         'cloudberry',
         'cranberry',
         'cranberries',
         'elderberry',
         'mulberry',
         'strawberry',
         'marionberry',
         'gooseberry',
         'huckleberry',
         'salmonberry',
         'raspberry',
         'persimmon',
         'peppercorn',
         'juniper berry',
         'goji berry',
         "blood orange",
         'citron',
         'citrus',
         'clementine',
         'orange',
         'ugli fruit',
         'tangerine',
         'lemon',
         'grapefruit',
         'peach',
         'lime',
         'nectarine',
         'mandarin orange',
         'kumquat'
         ]
    ,

    'GRAIN OR CEREAL BASED':
        ['tamale',
         'bran',
         'barley',
         "wheat flake",
         'buckwheat',
         'corn',
         'cornflakes',
         'couscous',
         'lentil',
         'grain',
         'horse gram',
         'granola',
         'garbanzo',
         'oatmeal cookie',
         'oatmeal cereal',
         'oatmeal',
         'oat',
         'muesli bar',
         'muesli',
         'mochi',
         'malt',
         'groats',
         'angel-hair pasta',
         'vermicelli',
         'tortellini',
         'tagliatelle',
         'farfalle',
         'fettuccine',
         'spaghetti carbonara',
         'spaghetti bolognese',
         'spaghetti',
         'ravioli',
         'ramen',
         'penne',
         'macaroni',
         'linguine',
         'lasagne',
         'cereal',
         'cereal bar',
         'tortilla chips',
         'porridge',
         'popcorn',
         'nachos',
         'kettle corn',
         "brown rice",
         'rice',
         'rice flake',
         'fried rice',
         'pilaf',
         'pike',
         'paddy',
         'yeast',
         'wheat',
         'cracker',
         'dough',
         'tapioca',
         'rye',
         'garlic bread',
         'hamburger bun',
         'yeast',
         'wheat',
         'cracker',
         'dough',
         'tapioca',
         'rye',
         'garlic bread',
         'hamburger bun',
         'crispbread',
         'crouton',
         'crust',
         'toast',
         'dumpling',
         'flatbread',
         "bread rolls",
         'breadcrumb',
         'bread',
         'bread pudding',
         'brioche',
         "brown bread",
         "bun",
         'canape',
         'bread',
         'bagel',
         "wheat bread",
         'baked alaska',
         'ciabatta',
         'corn bread',
         'toast',
         'sourdough bread',
         'soda bread',
         'sliced loaf',
         'gingerbread',
         'rye bread',
         'raisin bread',
         'meatloaf'
         ]
    ,

    'PLANT-BASED':
        ["velvet bean",
         "baked beans",
         "broad beans",
         "yardlong bean",
         "winged bean",
         'common bean',
         'urad bean',
         'tofu',
         'tepary bean',
         'dolichos bean',
         'soy',
         'lima bean',
         'mung bean',
         'kidney bean',
         "wild leek",
         "welsh onion",
         'chives',
         'cloves',
         'tree onion',
         'spring onion',
         'shallot',
         'scallion',
         'potato onion',
         'peppermint',
         'pearl onion',
         'oyster',
         'garlic chives',
         'marjoram',
         'licorice',
         'leek',
         'land cress',
         'lagos bologi',
         'amaranth',
         'apricot pits',
         'sunflower seeds',
         'flax',
         'sesame seed',
         'pumpkin seeds',
         'pistachio',
         'pea',
         'okra',
         'nopal',
         'sweet corn',
         'sour cabbage',
         'relish',
         'pickled cucumber',
         'pickle',
         'napa cabbage',
         'almond',
         'walnut',
         "water chestnut",
         'beancurd',
         'cashew',
         'chickpeas',
         'tigernut',
         'tarwi',
         'tamarind',
         'split peas',
         'soy',
         'pine nut',
         'pignut',
         'pigeon pea',
         'pecan',
         'peanut',
         'pea',
         'macadamia nut'
         ]
    ,

    'MEAT AND CHICKEN':
        ['chicken',
         'meat',
         'tartare',
         'antipasto',
         'venison',
         'bruschetta',
         'carpaccio',
         'beef carpaccio',
         'beef tartare',
         'meat',
         'elephant foot yam',
         'elephant garlic',
         'escargots',
         'filet mignon',
         'octopus',
         'fowl',
         'mutton',
         'suet',
         'bratwurst',
         'wiener',
         "blood sausage",
         'chorizo',
         'corned beef',
         'spam',
         'smoked sausage',
         'sausage roll',
         'sausage',
         'salami',
         'pepperoni',
         'link sausages',
         'lamb chops',
         'steak',
         'bacon',
         'barbecue',
         'bird',
         'veal',
         'chicken',
         'chicken breast',
         'chicken leg',
         'chicken wings',
         'beef steak',
         'turkey breast',
         'tenderloin',
         'nugget',
         'steak',
         "baby back ribs",
         'brisket',
         "veal cutlet",
         'bird',
         'veal',
         'chicken',
         'chicken breast',
         'chicken leg',
         'chicken wings',
         'beef steak',
         'ham',
         'venison',
         'turkey breast',
         'tenderloin',
         'frankfurters',
         'spare ribs',
         'skewer',
         'sirloin',
         'shish kebab',
         'pork',
         'rib',
         'prime rib',
         'pot roast',
         'pork chop',
         'pancetta',
         'cutlet',
         'casserole',
         'chicken',
         'chicken breast',
         'chicken curry',
         'chicken leg',
         'chicken quesadilla',
         'chicken wings',
         'beef steak',
         'cooked meat',
         'turkey',
         'stir-fry',
         'venison',
         'turkey breast',
         'tongue',
         'duck',
         'spare ribs',
         'skewer',
         'sirloin',
         'shish kebab',
         'hamburger',
         'kebab',
         'roast beef',
         'pate',
         'paella',
         'meatball',
         'goose'
         ]
    ,

    'ANIMAL PRODUCT':
        ['whey',
         'chevre',
         'chocolate ice cream',
         'chocolate mousse',
         'milk',
         'curd',
         'custard',
         'dairy product',
         'camembert',
         'chayote',
         'brie',
         'cottage cheese',
         'cheesecake',
         'dairy product',
         'cream cheese',
         'edam cheese',
         'emmental',
         'swiss cheese',
         'mozzarella',
         'roquefort',
         'parmesan',
         'gouda cheese',
         'goats cheese',
         'Omelette',
         'yarrow',
         'yolk',
         'egg',
         'deviled eggs'
         'egg white',
         'egg yolk',
         'eggplant',
         'fried egg',
         'omelet',
         'meringue'
         ]
    ,

    'SEAFOOD':
        ['ceviche',
         'chowder',
         'clam chowder',
         'crab cakes',
         'tempura',
         'fried calamari',
         'squid',
         'lobster bisque',
         'salmon steak',
         'tuna tartare',
         'seaweed',
         'dulse',
         'sea lettuce',
         'sea grape',
         'seaweed salad',
         'sea kale',
         'sea beet',
         'laver',
         'kale',
         'caviar',
         'lobster',
         'anchovy',
         'bass',
         'carp',
         'cockle',
         'tuna',
         'sardine',
         'crab',
         'cuttlefish',
         'trout',
         'fillet',
         'fillet of sole',
         'fish steak',
         'flatfish',
         'sturgeon',
         'salted fish',
         'smoked fish',
         'smoked salmon',
         'snapper',
         'sea perch',
         'sea bass',
         'lox',
         'haddock',
         'halibut',
         'herring',
         'salmon steak',
         'salmon',
         'plaice',
         'pilchard',
         'perch',
         'mackerel',
         'kingfish',
         'kipper',
         'eel',
         'calamari',
         'clam',
         'crayfish',
         'mussel',
         'shellfish'
         ]
    ,

    'DESSERT':
        ['brownie',
         'cake',
         'cake mix',
         'carrot cake',
         'cheesecake',
         'chocolate cake',
         'chocolate chip cake',
         'cupcake',
         'tiramisu',
         'flan',
         'spongecake',
         'sponge cake',
         'souffle',
         'shortcake',
         'panna cotta',
         'fruitcake',
         'knish',
         'apple pie',
         'blueberry pie',
         "whoopie pie",
         'tartlet',
         'tart',
         'strudel',
         'porridge',
         'pie',
         'mousse',
         'meat pie',
         'chocolate cookie',
         'cinnamon roll',
         'biscuits',
         'croissant',
         'crescent roll',
         'crumble',
         'eclair',
         'english muffin',
         'muffin',
         "poppy seed roll",
         'blueberry muffin',
         'viennese',
         'Baklava',
         'roulade',
         'millefeuille',
         'blancmange',
         'cannoli',
         'chocolate cupcake',
         'cinnamon roll',
         'macaroon',
         'waffle',
         'doughnut',
         "macaron",
         'pancake',
         'toffee',
         'brittle',
         'sweetmeat',
         'sprinkles',
         'bonbon',
         'candy',
         'candy apple',
         'candy bar',
         'caramel apple',
         'chocolate candy',
         'chocolate cookie',
         'chocolate ice cream',
         'popsicle',
         'marshmallow',
         'jelly beans',
         'jordan almonds',
         'nougat',
         'apple sauce',
         'brulee',
         'parfait',
         'chocolate mousse',
         'cranberry sauce',
         'creme brulee',
         'tiramisu',
         'syrup',
         'sundae',
         'milk chocolate',
         'spread',
         'honey',
         'sorbet',
         'sherbet',
         'ice cream',
         'pudding',
         'praline',
         'frozen yogurt',
         'mole sauce',
         'marmalade',
         'maple syrup',
         'wafer',
         'candy bar',
         'chocolate bar',
         'chocolate cake',
         'chocolate candy',
         'm&m',
         'torte',
         'granola bar',
         'souffle',
         'fudge',
         'churros'
         ]
    ,

    'ETHNIC DISHES AND SNACKS':
        ['croquette',
         'tempura',
         'falafel',
         'fish and chips',
         'fish fingers',
         'french fries',
         'french toast',
         'fried calamari',
         'onion rings',
         'burrito',
         'sandwich',
         'caesar salad',
         'caprese salad',
         'corn salad',
         'salad',
         'cole slaw',
         'tzatziki',
         'slaw',
         'seaweed salad',
         'fruit salad',
         'greek salad',
         'pizza',
         'spaghetti carbonara',
         'spaghetti bolognese',
         'spaghetti',
         'ravioli',
         'gorgonzola',
         'parmesan',
         'curry',
         'chowder',
         'casserole',
         'soup',
         'french onion soup',
         'miso soup',
         'pho',
         'hummus',
         'liver pate',
         'croque madame',
         'falafel',
         'takoyaki',
         'sushi',
         'spring rolls',
         'gyoza',
         'sashimi',
         'nigiri',
         'falafel',
         'melokhia',
         "lasagna",
         'tacos',
         'chips',
         'tempura'
         ]
}


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
    probability_list = []  # probability_list = [[GROUP, PROBABILITY, [SUB]], [GROUP, PROBABILITY, [SUB]], [GROUP, PROBABILITY, [SUB]]]

    # This block of code will fill the probability list (above)
    for key in result.keys():  # Running on all the outputs of Clarifai.    key = the specific food

        group_found = False  # For each key
        for group in food_dict.keys():  # Running on all the food groups in the food dict

            if key in food_dict[group]:  # If the output from Clarifai in is this food group
                group_found = True  # Declares that a (level B) food group was found
                if add_to_probability_list(probability_list, group, key,
                                           result[key]):  # If the food group is already in the probability list
                    continue
                else:  # If the food group is not in the list
                    probability_list.append(
                        [group, result[key], [key]])  # Add new element: GROUP = group,  SUB = [key]

        if not group_found:  # If a food group wasn't found for this specific food, make new group
            if add_to_probability_list(probability_list, 'OTHER', key, result[key]):
                continue
            else:
                probability_list.append(
                    ['OTHER', result[key], [key]])  # Add new element: GROUP = group,  SUB = [key]

    # This block of code will divide the probability sum by the num of items found in this group.
    main_list = []
    for item in probability_list:  # probability_list = [[GROUP, PROBABILITY, [SUB]], [GROUP, PROBABILITY, [SUB]], [GROUP, PROBABILITY, [SUB]]]
        temp_dict = {}  # {name: <GROUP_NAME>, size: <PROBABILITY>, sub: [{name:<FOOD_NAME>, size: <PROBABILITY>}, {name:<FOOD_NAME>, size: <PROBABILITY>}, ...]}
        temp_sub_list = []  # [{name:<FOOD_NAME>, size: <PROBABILITY>}, {name:<FOOD_NAME>, size: <PROBABILITY>}, ...]
        for food in item[SUB_INDEX]:
            temp_sub_list.append({'name': food, 'size': result[food]})

        temp_dict['name'] = item[GROUP_INDEX]
        temp_dict['size'] = float(item[PROBABILITY_INDEX]) / len(item[SUB_INDEX])
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
    print(1)
    metadata = (('authorization', 'Key 6944958a2ab34ec99afb17859726e82e'),)
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
def imgFull():
    content = request.json
    img = content['image_base64']
    result = convert(img)
    return bubbles_backend(result)

if __name__ == '__main__':
    app.run(debug=True)
