def us_state_abbrev(txt, direction='name_to_abbrev', uppercase=False):
    """
    Quick convenience function.
    Converts US state names to abbreviations, or vice-versa. 
    
    Parameters:
    ------------
    txt: str, name to convert.
    direction: str, (default: 'name_to_abbrev').
            If 'name_to_abbrev': convert name to abbreviation.
            If 'abbrev_to_name' (or other): convert abbreviation to name.
    uppercase: boolean (default: False), needs to be True if the input is uppercase.
    
    Returns:
    ------------
    result: Converted result. 
    """

    us_state_to_abbrev = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'American Samoa': 'AS',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Guam': 'GU',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Northern Mariana Islands': 'MP',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Puerto Rico': 'PR',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virgin Islands': 'VI',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'
    }

    abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))

    input_dict = us_state_to_abbrev if direction == 'name_to_abbrev' else abbrev_to_us_state
    if uppercase:
        input_dict = {str.upper(k): v for k, v in input_dict.items()}

    return input_dict[txt]
