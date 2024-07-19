from django.shortcuts import render, redirect  
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotFound
from django.views import View
from .models import *
import json
# Create your views here.
class Index(View):
 def get(self, request):
  return render(request,'index.html')
 
 
class CountryView(View):
 def get(self, request):
  countryobj = CountryModel.objects.all()
  return render(request,'country.html', {'country':countryobj})
 
 def post(self, request, id=None):
  if id:
   countryobj = CountryModel.objects.get(id=id)
   countryobj.delete()
   return redirect('/country/')
  else: 
      c_name = request.POST.get('country_name')
      code = request.POST.get('code')
      slug = request.POST.get('slug')
      flag = request.FILES.get('flag')
      state_available = request.POST.get('state_available')

      if state_available:
        is_state_available = True
      else:
        is_state_available = False

      countryobj = CountryModel.objects.create( name = c_name,
                                              slug = slug,
                                                code = code,
                                                flag = flag,
                                              is_state_available = is_state_available)
      return redirect('/country/')

class UpdateCountry(View):
 def get(self, request, id = None):
  countryobj = CountryModel.objects.get(id=id)
  return render(request,'countryupdate.html', {'country':countryobj})
 
 def post(self, request, id=None):
  c_name = request.POST.get('country_name')
  code = request.POST.get('code')
  slug = request.POST.get('slug')
  flag = request.FILES.get('flag')
  state_available = request.POST.get('state_available')

  
  countryobj = CountryModel.objects.get(id=id)
  if c_name:
    countryobj.name = c_name
  if code: 
    countryobj.code = code
  if slug: 
    countryobj.slug = slug
  if flag:
    countryobj.flag = flag
  
  if state_available:
    countryobj.is_state_available = True
  else:
   countryobj.is_state_available = False

  countryobj.save()
  return redirect('country')
 
 
class StateView(View):
 def get(self, request):
  countryobj = CountryModel.objects.filter(is_state_available=True)
  stateobj = StateModel.objects.all()
  return render(request,'state.html', {'countryobj':countryobj,'state':stateobj})
 
 def post(self, request):
  country_id = request.POST.get('country_id') 
  s_name = request.POST.get('statename')
  stateslug = request.POST.get('stateslug')
  language = request.POST.get('language')
  population = request.POST.get('population')

  countryobj = CountryModel.objects.get(id=country_id)
  stateobj = StateModel.objects.create(country = countryobj,
                                           statename = s_name,
                                           stateslug = stateslug,
                                            language = language,
                                            population = population,
  
  )
  return redirect('/state/')
 
class UpdateState(View):
  def get(self, request, id=None):
    stateobj = StateModel.objects.get(id=id)
    countryobj = stateobj.country
    return render(request,'stateupdate.html',{'state':stateobj, 'country':countryobj})
 
  def post(self, request, id=None):
    statename = request.POST.get('statename')
    stateslug = request.POST.get('stateslug')
    language = request.POST.get('language')
    population = request.POST.get('population')
    
    stateobj = StateModel.objects.get(id = id)  
    if statename:
      stateobj.statename =  statename                      
    if stateslug:
      stateobj.stateslug = stateslug
    if language:
      stateobj.language = language
    if population:
      stateobj.population = population
    stateobj.save()
 
    return redirect('state')
  
class DeleteState(View):
  def get(self, request, id=None):
    stateobj = StateModel.objects.get(id=id)
    return render(request,'deletestate.html',{'state':stateobj})
  
  def post(self, request, id=None):
    stateobj = StateModel.objects.get(id=id)
    stateobj.delete()
    return redirect('state')

class CityView(View):
    def get(self, request):
        countryobj = CountryModel.objects.all()
        cities = CityModel.objects.select_related('state', 'country').all()
        return render(request, 'city.html', {'country': countryobj, 'cities': cities})

    def post(self, request):
        state_id = request.POST.get('state_id')
        city_name = request.POST.get('city_name')
        slug = request.POST.get('slug')

        # Fetch the state instance using the state_id
        state = StateModel.objects.get(id=state_id)

        # Create the CityModel instance
        CityModel.objects.create(
            state=state,
            country=state.country,
            name=city_name,
            slug=slug
        )

        return redirect('city')
class CityUpdateView(View):
    def get(self, request, city_id):
        try:
            city = CityModel.objects.get(id=city_id)
        except CityModel.DoesNotExist:
            return HttpResponseNotFound("City not found")

        countries = CountryModel.objects.all()
        states = StateModel.objects.filter(country=city.country)
        return render(request, 'updatecity.html', {'city': city, 'countries': countries, 'states': states})

    def post(self, request, city_id):
        try:
            city = CityModel.objects.get(id=city_id)
        except CityModel.DoesNotExist:
            return HttpResponseNotFound("City not found")

        city_name = request.POST.get('city_name')
        slug = request.POST.get('slug')

        city.name = city_name
        city.slug = slug
        city.save()

        return redirect('city')
class CityDeleteView(View):
   def get(self, request, city_id=None):
     cityobj = CityModel.objects.get(id=city_id)
     return render(request, 'deletecity.html',{'city': cityobj})
   
   def post(self, request, city_id=None):
     cityobj = CityModel.objects.get(id=city_id)
     cityobj.delete() 
     return redirect('city')

@csrf_exempt
def get_state(request):
    data = json.loads(request.body)
    country_id = data.get('country_id')
    stateobj = StateModel.objects.filter(country=country_id)
    li = [{'id': state.id, 'state_name': state.statename} for state in stateobj]
    return JsonResponse({'message': 'Success', 'country_id': country_id, 'state': li})