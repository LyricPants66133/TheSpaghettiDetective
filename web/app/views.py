import os
from binascii import hexlify
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

# Create your views here.
def index(request):
    return redirect('/printers/')

@login_required
def printer_grid(request):
    printers = Printer.objects.filter(user=request.user)
    return render(request, 'printers_grid.html', {'printers': printers})

@login_required
def new_printer(request):
    form = PrinterForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            printer = form.save(commit=False)
            printer.user = request.user
            printer.auth_token = hexlify(os.urandom(10)).decode()
            printer.save()
            return redirect('/printers/{}/#step-2'.format(printer.id))

    return render(request, 'printer_wizard.html', {'form': form})

@login_required
def edit_printer(request, id):
    instance = get_object_or_404(Printer, id=id)
    return render(request, 'printer_wizard.html', {'form': PrinterForm(instance=instance)})