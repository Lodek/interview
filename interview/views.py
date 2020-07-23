from django.shortcuts import render

from .forms import SetupForm

def setup(request):
    form = SetupForm()
    return render(request, 'interview/setup.html', {'form': form})
