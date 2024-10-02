from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Guest
from .forms import EventForm, GuestForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count




# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
   # Get the events for the current user
    events = Event.objects.filter(user=request.user)

    # Get counts of guests by related_to
    related_to_data = Guest.objects.values('related_to__related_name').annotate(count=Count('id')).order_by('related_to__related_name')

    # Get counts of guests by category
    category_data = Guest.objects.values('category__category_name').annotate(count=Count('id')).order_by('category__category_name')

    # Extract labels and data for the chart
    related_to_labels = [related['related_to__related_name'] for related in related_to_data]
    related_to_counts = [related['count'] for related in related_to_data]

    category_labels = [category['category__category_name'] for category in category_data]
    category_counts = [category['count'] for category in category_data]

    context = {
        'events': events,
        'related_to_labels': related_to_labels,
        'related_to_counts': related_to_counts,
        'category_labels': category_labels,
        'category_counts': category_counts,
        'events_qty': events.count()
    }

    return render(request, 'index.html', context)

def invite_view(request):
    return render(request, 'invite.html')

# List views
@login_required(login_url='/accounts/login/')
def event_list(request):
    events = Event.objects.filter(user=request.user)  # Filter events by logged-in user
    return render(request, 'eventos/grid_eventos.html', {'events': events})

#Post views
@login_required(login_url='/accounts/login/')
def create_event(request):
    print("ENTRO AL CREATE_EVENT")
    print(request.session.items())
    if request.method == 'POST':
        print("ES POST")
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)  # Don't save to the database yet
            event.user = request.user  # Assign the logged-in user
            event.save()  # Now save the event
            print("MANDO A GUARDAR")
            form.save()
            return redirect('event_list')  # Redirect to the event list after saving
    else:
        form = EventForm()

    return redirect('event_list')

@login_required(login_url='/accounts/login/')
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    guests = event.guests.all()
    event_form = EventForm(instance=event)
    guest_form = GuestForm()

    if request.method == 'POST':
        event_form = EventForm(request.POST, instance=event)
        if event_form.is_valid():
            event_form.save()
            return redirect('event_list')

    return render(request, 'eventos/form_eventos.html', {
        'event_form': event_form,
        'guest_form': guest_form,
        'event': event,
        'guests': guests
    })

# Delete views
def event_delete(request):
    print("entro a elminiar")

    event_id = request.POST.get('event_id')
    event = get_object_or_404(Event, pk=event_id)

    print("event: ", event)
    if request.method == 'POST' and event:
        event.delete()
        return redirect('event_list')
    else:
        print("No se encontro un evento con ese ID")
        return redirect('event_list')

# Views del invitado:
@login_required(login_url='/accounts/login/')
def create_guest(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event_form = EventForm(instance=event)
    guest_form = GuestForm()

    if request.method == 'POST':
        print("Mando a crear un invitado")
        form = GuestForm(request.POST)

        if form.is_valid():
            guest = form.save(commit=False)
            guest.event = event
            guest.invitation_link = request.build_absolute_uri(f'/invitacion/{event.id}/{guest.id}')
            guest.save()
            return redirect('event_detail', event.id)
        else:
            print(form.errors)


        guests = event.guests.all()
        event_form = EventForm(request.POST, instance=event)
        if event_form.is_valid():
            event_form.save()
            return redirect('event_list')

    return render(request, 'eventos/form_eventos.html', {
        'event_form': event_form,
        'guest_form': guest_form,
        'event': event,
        'guests': guests
    })
