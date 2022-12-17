// Changes country field font color after user selection.
let countrySelected = $('#id_default_country').val();
if(!countrySelected) {
    $('#id_default_country').css('color', 'grey');
};
$('#id_default_country').change(function() {
    countrySelected = $(this).val();
    if(!countrySelected) {
        $(this).css('color', 'grey');
    } else {
        $(this).css('color', '#000');
    }
});