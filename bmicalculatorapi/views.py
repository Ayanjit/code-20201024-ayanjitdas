from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework import status
from urllib.request import urlopen
import ijson

@api_view(['GET'])
def CalculateBMI(request):

    personDataJSONName = request.GET.get('personJSON', 'persondata.json')
    personDataJSONLink = 'https://b2u2.s3.ap-south-1.amazonaws.com/' + personDataJSONName
    
    fetchedJson = None
    
    try:
        fetchedJson = urlopen(personDataJSONLink)
    except Exception as e:
        return JsonResponse({'error' : 'File ' + personDataJSONName + ' not found'}, status=status.HTTP_404_NOT_FOUND)


    updatedPersonCollection = []
    overWeightPersonCount = 0
    personDataCollection = ijson.items(fetchedJson, 'item')
    for person in personDataCollection:
        gender = person['Gender']
        height = float(person['HeightCm'])
        weight = float(person['WeightKg'])
        
        bmiCatagory = ''
        healthRisk = ''

        if height > 0 and weight > 0:
            #calculation
            bmi = weight / pow(height / 100.0 , 2)
            bmiCatagory, healthRisk = GetBMIRelatedData(bmi)

            if bmiCatagory == 'Overweight':
                overWeightPersonCount += 1

        updatedPerson = person
        updatedPerson['BMI'] = bmi
        updatedPerson['BMICategory'] = bmiCatagory
        updatedPerson['HealthRisk'] = healthRisk
        updatedPersonCollection.append(updatedPerson)

    return JsonResponse({'OverWeightPersonCount' : overWeightPersonCount,
                         'data': updatedPersonCollection}, status=status.HTTP_200_OK)


def GetBMIRelatedData(bmi):
    bmiCatagory = None
    healthRisk = None

    if bmi <= 18.4:
        bmiCatagory = 'Underweight'
        healthRisk = 'Malnutrition risk'
    elif bmi >= 18.5 and bmi <= 24.9:
        bmiCatagory = 'Normal weight'
        healthRisk = 'Low risk'
    elif bmi >= 25 and bmi <= 29.9:
        bmiCatagory = 'Overweight'
        healthRisk = 'Enhanced risk'
    elif bmi >= 30 and bmi <= 34.9:
        bmiCatagory = 'Moderately obese'
        healthRisk = 'Medium risk'
    elif bmi >= 35 and bmi <= 39.9:
        bmiCatagory = 'Severely obese'
        healthRisk = 'High risk'
    elif bmi >= 40:
        bmiCatagory = 'Very severely obese'
        healthRisk = 'Very high risk'
    
    return bmiCatagory,healthRisk