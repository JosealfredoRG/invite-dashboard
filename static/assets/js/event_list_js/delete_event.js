$(document).ready(function() {
    $('#deleteRowModal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var eventName = button.data('event-name'); // Extract info from data-* attributes
        var eventId = button.data('event-id');

        var modal = $(this);
        modal.find('#event-name').text(eventName); // Update the modal's content
        modal.find('#event_id').val(eventId); // Set the hidden input with the event ID
    });
});
