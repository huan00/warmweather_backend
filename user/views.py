import json
from django.shortcuts import render
from .models import User
from prompt.models import Prompt
from prompt.serializers import PromptSerializer
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, permissions, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserUpdateSerializer
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
import openai
# from pydantic import BaseModel, Field, validator, conlist
from typing import List, Dict
from .prompts import query_input, query_input_outfit

import os
import environ

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())



# Create your views here.


class RegisterUser(CreateAPIView):
    permissions_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer
    
    # register view logic
    def post(self, request):
        # create a serializer of the input data
        serializer = self.serializer_class(data=request.data['userData'])
        # if data are valid create user, else raise error
        if serializer.is_valid():

            # call create function to create user
            created_user = self.create(serializer)   
            #  
            # create prompts
            # get user instance from database for token creations
            user = User.objects.get(username=serializer.data['username'].lower())

            user_serializer = self.serializer_class(user)
  
            promptData = {
                'gender': 'male',
                'sensitivity_to_cold': request.data['promptData']['sensitivityToCold'],
                'User': user_serializer.data['id']
            }

            prompt_serializer = PromptSerializer(data=promptData)
            prompt_serializer.is_valid()
            prompt_serializer.save()
            
            token = Token.objects.create(user=user)

            # return reponse
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(ObtainAuthToken):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # authenticate user with username and password
        password = request.data['password']
        username = request.data['username']
        user = authenticate(username=username, password=password)

        
        # if no user found return with error
        if not user:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

        print(user)
        user_instance = User.objects.get(username=user)
        # pull user data for requested user
        userData = self.serializer_class(User.objects.get(username=user))
    
        # create token for user
        token = Token.objects.get_or_create(user=user)

        # create reponse data with user and token
        response_data = {'token': token[0].key, 'data': userData.data}

        if token and userData:
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'unable to retrive user'}, status=status.HTTP_404_NOT_FOUND)

class UpdateView(ObtainAuthToken):
    # permissions_classes = [permissions.AllowAny]
    authentication_classes = [TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]


    def put(self, request, pk=None):
        token = request.auth
        user_id = Token.objects.get(key=token).user_id

        # check if token user match pk user
        #return error if don't match
        if pk != user_id:
           return Response({'error': 'user input conflict'}, status=status.HTTP_409_CONFLICT)

        # get user from database
        user = User.objects.get(pk=pk)
        # get data info from database
        user_serializer = UserUpdateSerializer(user).data

        # update user data from request data
        for data in request.data:
            if data == 'zip_code':
                if not isinstance(int(request.data[data]), int):
                    raise ValueError('zip code unacceptable, please check!')
            user_serializer[data] = request.data[data]
        
        # serializer updated data
        user_serializer = UserUpdateSerializer(user, data=user_serializer)
        # if data doesn't pass serializer raise error, else Save it.
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        # return updated user to client.
        return Response(user_serializer.data, status=status.HTTP_202_ACCEPTED)

class DeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def delete(self, request, pk=None):
        user_id = Token.objects.get(key=request.auth).user_id

        # make sure user_id and pk are the same before delete
        if pk != user_id:
            return Response({'error': 'user input conflict'}, status=status.HTTP_409_CONFLICT)
        
        user = User.objects.get(pk=pk)
        user.delete()

        return Response({"message": "user deleted"}, status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
def get_outfit(request):
    parser = PydanticOutputParser(pydantic_object=ClothingFeedBack)

    prompt = PromptTemplate(
        template='Anwser the user query.\n{format_instructions}\n{query}\n',
        input_variables=['query'],
        partial_variables={'format_instructions': parser.get_format_instructions()}
    )

    _input = prompt.format_prompt(query=query_input_outfit)
    output = model(_input.to_string())
    _output = parser.parse(output)

    return Response(_output, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_my_outfit(request):
    try:
        # env = environ.Env()
        # environ.Env.read_env()
        openai.api_key = os.environ['OPENAI_API_KEY']
        # print(os.getenv('OPENAI_API_KEY'))
        # env_var = os.environ.get('OPENAI_API_KEY').split(' ')
        model='text-davinci-003'
        weather = request.data
        # return Response(os.environ.get('OPENAI_API_KEY'))
        gender = weather['gender']
        sensitivity = weather['sensitivity']


        prompt =f"""
                You are a meteorologist and a fashion dresser. Given today's weather condition delimiter by ```. \
                Generate an appropriate {gender} outfit for today's weather condition. following these rules. \
                
                1. Outfit should consider what tops, jacket, pants, footware and accessories to wear. \
                2. Make sure the outfit is specific for a {gender}. \
                3. {sensitivity} compare to others. Make sure to consider this in the outfit recommendation. \
                4. recommend an appropriate jacket, base on the weather temperature. \   
                5. only return one item for pants. \
                6. only return one item for shoe. \
                7. only return one item for head. \
                8. return response in json format delimiter by ''' \
                

                tops should only consist of inner layer and mid layer.
                jacket should be consist of tops outer layer and jacket, mark as not required if not appropriate for weather.

                ```
                    Here are today's weather condition: \
                        temperature high: {weather['temperature_high']},
                        temperature low: {weather['temperature_low']},
                        wind: {weather['wind']},
                        humidity: {weather["humidity"]},
                        condition: {weather["condition"]}
                ```

                '''
                    "head": list,
                    "tops": list,
                    "jacket": list,
                    "pants": list,
                    "shoe": list,
                    "accessory": list of items such as sunglasses, gloves,
                    "suggestion": summary of outfit and weather in 20 words.
                    "extras": list of items such as sunblock, umbrella
                '''
                
                """
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "you are a meteorologist, that have good fashion sense."},
                {"role": "user", "content": prompt}
            ]
            )

        json_response = json.loads(completion.choices[0].message['content'])

        return Response(json_response, status=status.HTTP_200_OK)
    except os.getenv('OPENAI_API_KEY'):
        return ('bad')
    # return Response(json_response)


@api_view(['POST'])
def test_prompt(request):
    print(request.data)

    return Response('hello')