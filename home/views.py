import math
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Guest, GuestCategory, RelatedTo
from .forms import EventForm, GuestForm, ExcelUploadForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, F, Q
from django.contrib import messages
import pandas as pd
from twilio.rest import Client



# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
   # Get the events for the current user
    events = Event.objects.filter(user=request.user)

    # Annotate each event with the count of guests, guests by category, and guests by related_to
    events_with_guests = events.annotate(
        total_guests=Count('guests'),  # Count all guests related to this event
        total_confirmed=Count('guests', filter=Q(guests__will_assist=True)),  # Count all confirmed guests related to this event

    )

    # Extract data for the charts
    for event in events_with_guests:
        category_counts = event.guests.values('category__category_name').annotate(count=Count('id'))
        related_counts = event.guests.values('related_to__related_name').annotate(count=Count('id'))
        related_labels = []
        related_data = []
        category_labels = []
        category_data = []

        for related in related_counts:
            related_labels.append(related['related_to__related_name'])
            related_data.append(related['count'])

        for category in category_counts:
            category_labels.append(category['category__category_name'])
            category_data.append(category['count'])

        event.guests_by_related_to = {'related_labels': related_labels, 'related_data':related_data}
        event.guests_by_category = {'category_labels': category_labels, 'category_data':category_data}
    context = {
        'events': events_with_guests,
        'category_labels': category_labels,
        'events_qty': events.count(),
    }

    return render(request, 'index.html', context)

def invite_view(request):
    return render(request, 'invite.html')

def guest_invite_view(request, event_id, guest_id):
    event = get_object_or_404(Event, id=event_id)
    guest = get_object_or_404(Guest, id=guest_id)
    ctx = { 'event':event, 'guest':guest}
    return render(request, 'invite.html', ctx)

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
    upload_guest_form = ExcelUploadForm()

    if request.method == 'POST':
        event_form = EventForm(request.POST, instance=event)
        if event_form.is_valid():
            event_form.save()
            return redirect('event_list')

    return render(request, 'eventos/form_eventos.html', {
        'event_form': event_form,
        'guest_form': guest_form,
        'upload_guest_form': upload_guest_form,
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
            guest.save()
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

def edit_guest(request, event_id, guest_id):
    # Get the event and guest objects
    event = get_object_or_404(Event, pk=event_id)
    guest = get_object_or_404(Guest, pk=guest_id)

    guests = event.guests.all()
    event_form = EventForm(instance=event)
    guest_form = GuestForm()

    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        form = GuestForm(request.POST, instance=guest)  # Bind the form with the guest data
        if form.is_valid():
            guest = form.save(commit=False)
            guest.event = event
            guest.save()
            guest.invitation_link = request.build_absolute_uri(f'/invitacion/{event.id}/{guest.id}')
            guest.save()
            return redirect('event_detail', event_id=event.pk)  # Redirect back to event detail page
    else:
        # If not POST, render the form with the guest's current data
        form = GuestForm(instance=guest)

    return render(request, 'eventos/form_eventos.html', {
        'event_form': event_form,
        'guest_form': guest_form,
        'event': event,
        'guests': guests
    })

def delete_guest(request, event_id):
    guest_id = request.POST.get('guest_id')
    guest = get_object_or_404(Guest, pk=guest_id)

    print("guest: ", guest)
    if request.method == 'POST' and guest:
        guest.delete()
        return redirect('event_detail', event_id=event_id)
    else:
        print("No se encontro un invitado con ese ID")
        return redirect('event_detail', event_id=event_id)

def delete_all_guest(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    guests = event.guests.all()

     # Check if there are guests to delete
    if guests.exists():
        guests.delete()  # Delete all guests associated with the event
        messages.success(request, "All guests have been successfully deleted.")
    else:
        messages.info(request, "There are no guests to delete.")

    return redirect('event_detail', event_id=event_id)  # Redirect to the event detail page

def upload_guests(request, event_id,):
    event = get_object_or_404(Event, id=event_id)

    print("ENTRO AL upload_guests")
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print("ES VALIDO EL FORM")
            # Get the uploaded Excel file
            excel_file = request.FILES['excel_file']

            # Use pandas to read the Excel file
            try:
                df = pd.read_excel(excel_file)
                print("SE LEYO BIEN EL EXCEL: ", df)

                # Expected columns: N°, Nombre, Primer Nombre, Segundo Nombre, etc.
                expected_columns = [
                    "N°", "Nombre", "Primer Nombre", "Segundo Nombre", "Primer apellido",
                    "Segundo Apellido", "Numero Telefonico", "Previo", "Toma", "Alcohol",
                    "Relacion", "Vinculo", "Edad", "related_to", "category"
                ]
                # Validate that all expected columns are present
                if not all(column in df.columns for column in expected_columns):
                    messages.error(request, "The uploaded file does not have the correct columns.")
                    return redirect('upload_excel')

                required_fields = [
                    "Primer Nombre", "Primer apellido", "Numero Telefonico",
                    "related_to", "category"
                ]
                # Process each row and insert into the database
                for index, row in df.iterrows():
                    print("ENTRO AL FOR: ", row)

                    if any(is_nan(row.get(field)) for field in required_fields):
                        continue  # Skip to the next iteration if any field is NaN or missing

                    full_name = " ".join([row[col] for col in ['Primer Nombre', 'Segundo Nombre', 'Primer apellido', 'Segundo Apellido'] if not is_nan(row[col])])
                    category = get_object_or_404(GuestCategory, pk=row['category'])
                    related = get_object_or_404(RelatedTo, pk=row['related_to'])
                    guest = Guest(
                        name=full_name,
                        phone=row['Numero Telefonico'] or '00000000',
                        related_to=related,
                        category=category,
                        email= "example@example.com",
                        event= event,
                        additional_guests_amount= 1,
                    )
                    guest.save()
                    guest.invitation_link = request.build_absolute_uri(f'/invitacion/{event.id}/{guest.id}')
                    guest.save()

                messages.success(request, "Guests were successfully added from the Excel file.")
                return redirect('event_detail', event.id)

            except Exception as e:
                print("ERROR EN EL TRY: ", e)
                messages.error(request, f"Error processing the file: {e}")
                return redirect('event_detail', event.id)
        else:
            print("form error: ", form.errors)
    else:
        print("NO ES POST")
        form = ExcelUploadForm()

    return redirect('event_detail', event.id)


def invite_guest(request, guest_id):
    guest = get_object_or_404(Guest, id=guest_id)

    # Call the Twilio API to send the message
    message_sid = send_whatsapp_message(guest)
    print(f"Message sent with SID: {message_sid}")

    return redirect('event_detail', event_id=guest.event.id)


# Helper Functions
def return_event_detail(request, event, guests, event_form, guest_form, upload_guest_form):
        return render(request, 'eventos/form_eventos.html', {
        'event_form': event_form,
        'guest_form': guest_form,
        'upload_guest_form': upload_guest_form,
        'event': event,
        'guests': guests
    })

def is_nan(value):
    return isinstance(value, float) and math.isnan(value)

def send_whatsapp_message(guest):
    print("enviar wa")

