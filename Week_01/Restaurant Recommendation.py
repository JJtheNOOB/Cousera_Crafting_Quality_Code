#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
A restaurant recommendation system.

Here are some example dictionaries.  These correspond to the information in
restaurants_small.txt.

Restaurant name to rating:
# dict of {str: int}
{'Georgie Porgie': 87,
 'Queen St. Cafe': 82,
 'Dumplings R Us': 71,
 'Mexican Grill': 85,
 'Deep Fried Everything': 52}

Price to list of restaurant names:
# dict of {str, list of str}
{'$': ['Queen St. Cafe', 'Dumplings R Us', 'Deep Fried Everything'],
 '$$': ['Mexican Grill'],
 '$$$': ['Georgie Porgie'],
 '$$$$': []}

Cuisine to list of restaurant names:
# dict of {str, list of str}
{'Canadian': ['Georgie Porgie'],
 'Pub Food': ['Georgie Porgie', 'Deep Fried Everything'],
 'Malaysian': ['Queen St. Cafe'],
 'Thai': ['Queen St. Cafe'],
 'Chinese': ['Dumplings R Us'],
 'Mexican': ['Mexican Grill']}

With this data, for a price of '$' and cuisines of ['Chinese', 'Thai'], we
would produce this list:

    [[82, 'Queen St. Cafe'], [71, 'Dumplings R Us']]
"""

# The file containing the restaurant data.
FILENAME = 'restaurant_small.txt'


# In[38]:


def read_restaurants(file):
    """ (file) -> (dict, dict, dict)

    Return a tuple of three dictionaries based on the information in the file:

    - a dict of {restaurant name: rating%}
    - a dict of {price: list of restaurant names}
    - a dict of {cusine: list of restaurant names}
    """

    name_to_rating = {}
    price_to_names = {'$': [], '$$': [], '$$$': [], '$$$$': []}
    cuisine_to_names = {}
    
    #Read in the file, split by lines and save them into a list
    lines = open(file).read().splitlines()
    
    #Grabbing the name, rating, price, categories from the list and save them in separate lists
    names_of_res = lines[::5]
    ratings_of_res = lines[1::5]
    price_of_res = lines[2::5]
    cate_of_res = lines[3::5]
    
    #Appending info to name of restauraunts
    for i in range(len(names_of_res)):
        name_to_rating.update({names_of_res[i]: int(ratings_of_res[i][:2])})
    
    #Appending info to price of restaurants
    for i, item in enumerate(price_of_res):
        price_to_names.setdefault(item, []).append(names_of_res[i])
    
    #Appending info to cuisine categories
    for i, item in enumerate(cate_of_res):
        temp_list = item.split(',')
        for j, categories in enumerate(temp_list):
            cuisine_to_names.setdefault(categories, []).append(names_of_res[i])
    
    return (name_to_rating, price_to_names, cuisine_to_names)


# In[15]:


def filter_by_cuisine(names_matching_price, cuisine_to_names, cuisines_list):
    """ (list of str, dict of {str: list of str}, list of str) -> list of str

    >>> names = ['Queen St. Cafe', 'Dumplings R Us', 'Deep Fried Everything']
    >>> cuis = 'Canadian': ['Georgie Porgie'],
     'Pub Food': ['Georgie Porgie', 'Deep Fried Everything'],
     'Malaysian': ['Queen St. Cafe'],
     'Thai': ['Queen St. Cafe'],
     'Chinese': ['Dumplings R Us'],
     'Mexican': ['Mexican Grill']}
    >>> cuisines = ['Chinese', 'Thai']
    >>> filter_by_cuisine(names, cuis, cuisines)
    ['Queen St. Cafe', 'Dumplings R Us']
    """
    #Set up a list to hold the restaurants that is in the cuisine list
    temp_cui_list = []
    
    #Looping through the cuisines list and append the associated restaurants
    for cui in cuisines_list:
            temp_cui_list.append(cuisine_to_names[cui])
    
    return list(item[0] for item in temp_cui_list if item[0] in names_matching_price)   


# In[28]:


def build_rating_list(name_to_rating, names_final):
    """ (dict of {str: int}, list of str) -> list of list of [int, str]

    Return a list of [rating%, restaurant name], sorted by rating%

    >>> name_to_rating = {'Georgie Porgie': 87,
     'Queen St. Cafe': 82,
     'Dumplings R Us': 71,
     'Mexican Grill': 85,
     'Deep Fried Everything': 52}
    >>> names = ['Queen St. Cafe', 'Dumplings R Us']
    [[82, 'Queen St. Cafe'], [71, 'Dumplings R Us']]
    """
    rating_list = []
    final_list = []
    
    for item in names_final:
        rating_list.append(name_to_rating[item])
        
    for i in range(len(rating_list)):
        final_list.append([rating_list[i], names_final[i]])
    
    return sorted(final_list)


# In[30]:


#Main function part

def recommend(file, price, cuisines_list):
    """(file open for reading, str, list of str) -> list of [int, str] list

    Find restaurants in file that are priced according to price and that are
    tagged with any of the items in cuisines_list.  Return a list of lists of
    the form [rating%, restaurant name], sorted by rating%.
    """

    # Read the file and build the data structures.
    # - a dict of {restaurant name: rating%}
    # - a dict of {price: list of restaurant names}
    # - a dict of {cusine: list of restaurant names}
    name_to_rating, price_to_names, cuisine_to_names = read_restaurants(file)


    # Look for price or cuisines first?
    # Price: look up the list of restaurant names for the requested price.
    names_matching_price = price_to_names[price]

    # Now we have a list of restaurants in the right price range.
    # Need a new list of restaurants that serve one of the cuisines.
    names_final = filter_by_cuisine(names_matching_price, cuisine_to_names, cuisines_list)

    # Now we have a list of restaurants that are in the right price range and serve the requested cuisine.
    # Need to look at ratings and sort this list.
    result = build_rating_list(name_to_rating, names_final)

    # We're done!  Return that sorted list.
    return result


# In[39]:


recommend(FILENAME, '$', ['Chinese', 'Thai'])


# In[40]:


recommend('restaurants.txt', '$', ['Chinese', 'Thai'])


# In[ ]:




