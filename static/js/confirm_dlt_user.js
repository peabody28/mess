$('#dlt').click(function confirmDelete(event) {
    event.preventDefault();
    if (confirm("Вы подтверждаете удаление?")) {
        location.href = $(this).attr('href')
    }
});