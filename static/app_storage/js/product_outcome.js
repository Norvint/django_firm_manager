$(document).ready(function() {

    // Watch for the 'add another booking' click
    $('#add_product_outcome').click(function(e) {
        e.preventDefault();

        // create a clone of the existing form elements, but with blank fields.
        $('tr.product-outcome-form-container:last').clone().each(function(i) {
            $(this).find('input,select').each(function(i) {
                parts = $(this).attr('id').split('-', 3);
                if (parts[2] !== 'store') {
                $(this).val('');
                }

                // update the id attributes, incrementing the form number, e.g.: "id_form-1-field_name"
                parts = $(this).attr('id').split('-', 3);
                num = parseInt(parts[1]);
                num += 1;
                $(this).attr('id', parts[0] + '-' + num + '-' +parts[2]);

                // Update the name attribute, e.g.: form-1-field_name
                parts = $(this).attr('name').split('-', 3);
                num = parseInt(parts[1]);
                num += 1;
                $(this).attr('name', parts[0] + '-' + num + '-' +parts[2]);

            });

        }).appendTo('table#product-outcome-form-wrapper');
        //         Increment the TOTAL_FORMS
        $('#id_form-TOTAL_FORMS').val(parseInt($('#id_form-TOTAL_FORMS').val()) + 1);
        throw "";
    });
});