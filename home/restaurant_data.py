
"""
Central source of restaurant information for the Kalimpong chatbot.

Menu prices and dishes are transcribed from the menu photo provided by
the user. Glass-bottle drink availability was separately confirmed by
the user.

Do not invent prices, portions, ingredients, or availability.
"""

RESTAURANT_INFO = {
    "name": "Kalimpong Restaurant",

    # Existing project details; address still needs reconfirmation.
    "address": (
        "68QF+GQP, Tipa Road, McLeod Ganj, "
        "Dharamshala, Himachal Pradesh 176215"
    ),

    # Printed on the supplied menu photo.
    "phone": "+91 98167 43703",

    "google_maps_url": (
        "https://www.google.com/maps/search/?api=1"
        "&query=Kalimpong+Restaurant%2C+68QF%2BGQP%2C+"
        "Tipa+Road%2C+McLeod+Ganj%2C+Dharamshala"
    ),

    "zomato_menu_url": (
        "https://www.zomato.com/dharamshala/"
        "kalimpong-restaurant-mcleodganj/menu"
    ),

    # Previously recorded hours; reconfirm with the restaurant.
    "opening_hours": {
        "monday": "11 AM–10 PM",
        "tuesday": "11 AM–10 PM",
        "wednesday": "Closed",
        "thursday": "11 AM–10 PM",
        "friday": "11 AM–10 PM",
        "saturday": "11 AM–10 PM",
        "sunday": "11 AM–10 PM",
    },

    # Each item has a consistent schema for future searching.
    # prices_inr uses "listed" for a single printed price and
    # "full"/"half" only when both prices are explicitly shown.
    "menu_items": [
        # momos

        {
            "name": "Non-Veg Steamed Momos",
            "category": "Momo's",
            "variants": ["Mutton", "Chicken", "Pork"],
            "diet": "non-vegetarian",
            "prices_inr": {"listed": 200},
            "portion_note": "Menu shows one price; size unspecified.",
        },
        {
            "name": "Non-Veg Fried Momos",
            "category": "Momo's",
            "variants": ["Mutton", "Chicken", "Pork"],
            "diet": "non-vegetarian",
            "prices_inr": {"listed": 220},
            "portion_note": "Menu shows one price; size unspecified.",
        },
        {
            "name": "Veg Steamed Momos",
            "category": "Momo's",
            "variants": [],
            "diet": "vegetarian",
            "prices_inr": {"listed": 180},
            "portion_note": "Menu shows one price; size unspecified.",
        },
        {
            "name": "Veg Fried Momos",
            "category": "Momo's",
            "variants": [],
            "diet": "vegetarian",
            "prices_inr": {"listed": 200},
            "portion_note": "Menu shows one price; size unspecified.",
        },

        # NOODLE SOUP

        {
            "name": "Thukpa",
            "category": "Noodle Soup",
            "variants": ["Mutton", "Chicken"],
            "diet": "non-vegetarian",
            "prices_inr": {"full": 180, "half": 160},
        },
        {
            "name": "Keema Thukpa",
            "category": "Noodle Soup",
            "variants": ["Mutton", "Chicken"],
            "diet": "non-vegetarian",
            "prices_inr": {"full": 180, "half": 160},
        },
        {
            "name": "Dry Thukpa",
            "category": "Noodle Soup",
            "variants": ["Mutton", "Chicken"],
            "diet": "non-vegetarian",
            "prices_inr": {"listed": 180},
            "portion_note": "Menu shows one price; size unspecified.",
        },
        {
            "name": "Veg Thukpa",
            "category": "Noodle Soup",
            "variants": [],
            "diet": "vegetarian",
            "prices_inr": {"full": 170, "half": 150},
        },
        {
            "name": "Thenthuk",
            "category": "Noodle Soup",
            "variants": ["Mutton", "Chicken"],
            "diet": "non-vegetarian",
            "prices_inr": {"listed": 200},
            "portion_note": "Menu shows one price; size unspecified.",
        },
        {
            "name": "Veg Thenthuk",
            "category": "Noodle Soup",
            "variants": [],
            "diet": "vegetarian",
            "prices_inr": {"listed": 180},
            "portion_note": "Menu shows one price; size unspecified.",
        },
        {
            "name": "Mokthuk",
            "category": "Noodle Soup",
            "variants": ["Mutton", "Chicken"],
            "diet": "non-vegetarian",
            "prices_inr": {"listed": 220},
            "portion_note": "Menu shows one price; size unspecified.",
        },

        # HOUSE SPECIALTIES

        {
            "name": "Chicken Chilly",
            "category": "House Specialties",
            "variants": [],
            "diet": "non-vegetarian",
            "prices_inr": {"listed": 350},
        },
        {
            "name": "Pork Chilly",
            "category": "House Specialties",
            "variants": [],
            "diet": "non-vegetarian",
            "prices_inr": {"listed": 350},
        },
        {
            "name": "Mutton Fried Shapta",
            "category": "House Specialties",
            "variants": [],
            "diet": "non-vegetarian",
            "prices_inr": {"listed": 350},
        },

        # NOODLES & RICE

        {
            "name": "Chowmein",
            "category": "Noodles & Rice",
            "variants": ["Mutton", "Chicken"],
            "diet": "non-vegetarian",
            "prices_inr": {"listed": 200},
        },
        {
            "name": "Veg Chowmein",
            "category": "Noodles & Rice",
            "variants": [],
            "diet": "vegetarian",
            "prices_inr": {"listed": 180},
        },
        {
            "name": "Fried Rice",
            "category": "Noodles & Rice",
            "variants": ["Mutton", "Chicken"],
            "diet": "non-vegetarian",
            "prices_inr": {"listed": 200},
        },
        {
            "name": "Veg Fried Rice",
            "category": "Noodles & Rice",
            "variants": [],
            "diet": "vegetarian",
            "prices_inr": {"listed": 180},
        },
        {
            "name": "Bakchoy with Tofu",
            "category": "Noodles & Rice",
            "variants": [],
            "diet": "unspecified",
            "prices_inr": {"listed": 250},
        },
        {
            "name": "Plain Rice",
            "category": "Noodles & Rice",
            "variants": [],
            "diet": "unspecified",
            "prices_inr": {"listed": 90},
        },
        {
            "name": "Tingmo",
            "category": "Noodles & Rice",
            "variants": [],
            "diet": "unspecified",
            "prices_inr": {"listed": 40},
        },

        # DRINKS

        {
            "name": "Ginger Lemon with Honey",
            "category": "Drinks",
            "variants": [],
            "diet": "unspecified",
            "prices_inr": {"listed": 70},
        },
        {
            "name": "Ginger Lemon Tea",
            "category": "Drinks",
            "variants": [],
            "diet": "unspecified",
            "prices_inr": {"listed": 60},
        },
        {
            "name": "Lemon Tea",
            "category": "Drinks",
            "variants": [],
            "diet": "unspecified",
            "prices_inr": {"listed": 50},
        },
        {
            "name": "Lemon Pepsi",
            "category": "Drinks",
            "variants": [],
            "diet": "unspecified",
            "prices_inr": {"listed": 50},
        },
        {
            "name": "Lemon Soda",
            "category": "Drinks",
            "variants": [],
            "diet": "unspecified",
            "prices_inr": {"listed": 50},
        },
        {
            "name": "Softdrinks",
            "category": "Drinks",
            "variants": [],
            "diet": "unspecified",
            "prices_inr": {"listed": 30},
        },
        {
            "name": "Mineral Water",
            "category": "Drinks",
            "variants": [],
            "diet": "unspecified",
            "prices_inr": {"listed": 30},
        },
    ],

    # Confirmed by the user separately from the printed menu.
    
    "glass_bottle_drinks": {
        "availability": True,
        "container": "glass bottle",
        "available_options": [
            "Pepsi",
            "Slice",
            "Mountain Dew",
            "Soda",
        ],
        "prices_inr": {
            "per_bottle": 30,
        },
        "price_note": "All listed glass-bottle drinks cost ₹30 per bottle.",
        "confirmed_by_user": True,
    },

    "dietary_information": {
        "ingredient_lists": "not_provided",
        "verified_gluten_free_items": None,
        "verified_vegan_items": None,
        "allergen_information": "not_provided",
        "cross_contamination_information": "not_provided",
        "important_note": (
            "The restaurant has not provided verified ingredient, "
            "gluten-free, vegan, allergen, or cross-contamination data. "
            "This does not mean a dish is unsafe or safe; its status "
            "is simply unconfirmed."
        ),
    },

    
    "verification_status": {
        "menu_items_and_printed_prices": "transcribed_from_menu_photo",
        "glass_bottle_drinks": "confirmed_by_user",
        "glass_bottle_drink_prices": "confirmed_by_user",
        "phone": "printed_on_menu_photo",
        "address": "confirmed_by_user",
        "opening_hours": "confirmed_by_user",
        "zomato_menu_url": "confirmed_by_user",
    },

}
