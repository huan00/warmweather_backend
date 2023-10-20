weather_condition = {
                        'temperature_high': '85 °F',
                        'temperature_low': '68 °F',
                        'wind': '10 mph',
                        'humidity': '78%',
                        'condition': 'sunny',
}

query_input = f'''You are a meteorologist. today's weather condition, generate an appropriate 
              outfit for the day. such as what tops, jacket, bottoms, footware and accessories to wear, following these constraints:

              1. I'm a male, that normally feels colder then normal people.
        

        Here are today's weather condition:
                        temperature high: {weather_condition['temperature_high']},
                        temperature low: {weather_condition['temperature_low']},
                        wind: {weather_condition['wind']},
                        humidity: {weather_condition["humidity"]},
                        condition: {weather_condition["condition"]}

                        '''



query_input_outfit = f"""
              You are a meteorologist. Given today's weather condition, generate an appropriate 
              outfit for the day. such as what tops, jacket, bottoms, footware and accessories to wear.

              Here are today's weather condition:
                        temperature high: {weather_condition['temperature_high']},
                        temperature low: {weather_condition['temperature_low']},
                        wind: {weather_condition['wind']},
                        humidity: {weather_condition["humidity"]},
                        condition: {weather_condition["condition"]}
"""

