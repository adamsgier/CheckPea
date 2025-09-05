# CheckPea - AI-Powered Food Recognition and Nutrition Analysis

CheckPea API is a Flask-based web application that uses artificial intelligence to identify food items from images and provide detailed nutritional analysis and dietary recommendations.

## 🚀 Features

- **AI Food Recognition**: Uses Clarifai's computer vision API to identify food items from uploaded images
- **Food Categorization**: Automatically categorizes detected foods into groups (vegetables, fruits, grains, meat, dairy, etc.)
- **Nutritional Analysis**: Provides detailed nutritional breakdowns and recommendations
- **Personalized Dietary Advice**: Calculates personalized nutritional needs based on user metrics (height, weight, age, activity level)
- **Interactive Visualization**: Returns data in a hierarchical format suitable for bubble charts and other visualizations
- **Multi-level Food Detection**: Supports nested food categories (e.g., pizza with specific toppings)

## 🏗️ How It Works

### 1. Image Processing
- Users upload food images via base64 encoding
- Images are processed using Clarifai's food recognition model
- The AI identifies multiple food items with confidence scores

### 2. Food Categorization
The application categorizes detected foods into predefined groups:
- **DRINKS** (coffee, tea, alcoholic beverages, juices, etc.)
- **VEGETABLES** (leafy greens, root vegetables, nightshades, etc.)
- **FRUIT** (tropical, stone fruits, berries, citrus, etc.)
- **GRAIN OR CEREAL BASED** (pasta, bread, rice, breakfast cereals, etc.)
- **PLANT-BASED** (beans, tofu, nuts, seeds, aromatics, etc.)
- **MEAT AND CHICKEN** (raw meat, processed meats, grilled/roasted, etc.)
- **DAIRY OR EGG** (cheese, milk products, eggs, etc.)
- **SEAFOOD** (fish, shellfish, seafood dishes, etc.)
- **DESSERT** (cakes, pastries, candy, ice cream, etc.)
- **PREPARED DISHES OR SNACKS** (Italian, Asian, Mexican cuisines, etc.)
- **MISC** (sauces, oils, condiments, etc.)

### 3. Nutritional Calculations
The application calculates personalized nutritional recommendations based on:
- **BMI calculations** for weight management goals
- **Caloric needs** based on weight and activity level
- **Macronutrient requirements** (proteins, carbohydrates, fats)
- **Micronutrient needs** (fiber, sodium, cholesterol)
- **Special dietary considerations** (low-carb, low-sugar, etc.)

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.7+
- Clarifai API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CheckPea
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Clarifai API**
   - Get your API key from [Clarifai](https://clarifai.com/)
   - Update the API key in `main.py` (line 281):
   ```python
   metadata = (('authorization', 'Key YOUR_API_KEY_HERE'),)
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

   The application will start on `http://localhost:5000`

### Deployment (Heroku)

The project includes a `Procfile` for easy Heroku deployment:

1. **Create a Heroku app**
   ```bash
   heroku create your-app-name
   ```

2. **Set environment variables**
   ```bash
   heroku config:set CLARIFAI_API_KEY=your_api_key
   ```

3. **Deploy**
   ```bash
   git push heroku main
   ```

## 📡 API Endpoints

### `GET /`
Returns the main HTML page.

### `POST /img/`
**Purpose**: Basic food recognition
**Input**: JSON with `image_base64` field
**Output**: Dictionary of detected foods with confidence scores

```json
{
  "image_base64": "base64_encoded_image_string"
}
```

### `POST /imgfull/`
**Purpose**: Complete food analysis with categorization
**Input**: JSON with `image_base64` field
**Output**: Hierarchical JSON suitable for visualization

```json
{
  "data": [
    {
      "name": "VEGETABLES",
      "size": 0.85,
      "sub": [
        {
          "name": "tomato",
          "size": 0.92
        }
      ]
    }
  ]
}
```

### `POST /recommendation/`
**Purpose**: Get personalized nutritional recommendations
**Input**: User metrics and dietary goals
**Output**: Calculated nutritional requirements

## 🗂️ Project Structure

```
CheckPea/
├── main.py              # Main Flask application
├── requirements.txt     # Python dependencies
├── Procfile            # Heroku deployment configuration
├── testing.py          # Utility script for Google Sheets data
├── templates/
│   └── main.html       # Basic HTML template
└── README.md           # This file
```

## 🔧 Key Functions

- **`convert()`**: Processes base64 images and calls Clarifai API
- **`bubbles_backend()`**: Categorizes foods and formats output for visualization
- **`recommendation()`**: Calculates personalized nutritional needs
- **`CompareNut()`**: Compares actual vs. recommended nutrient intake

## 🎯 Use Cases

- **Dietary tracking**: Log meals by taking photos
- **Nutritional education**: Learn about food categories and nutritional content
- **Health monitoring**: Track nutrient intake against personalized recommendations
- **Food discovery**: Identify unknown foods and their nutritional properties

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is available for educational and research purposes.

## ⚠️ Important Notes

- Ensure you have a valid Clarifai API key before running the application
- The application processes images locally before sending them to Clarifai
- Nutritional calculations are based on general dietary guidelines and should not replace professional medical advice
- Some food categories in the 'HIDE' group are filtered out from results for better user experience

## 🔮 Future Enhancements

- Integration with nutrition databases for more detailed nutritional information
- User account system for tracking dietary history
- Mobile app development
- Support for multiple languages
- Integration with fitness trackers and health apps
