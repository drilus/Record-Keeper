// Hide all our temporary elements
function hideElements() {
  $('*[id*=id_column_]').each(function() {
    id = this.id
    document.getElementById(id).parentNode.style.display = "none";
  });
}

// We need to hook the event for choosing a category
(function() {
    // Hide all temporary fields on load
    hideElements()

    // Enable our DateTimePicker
    $('.datetime-input').datetimepicker({
      format:'YYYY-MM-DD HH:mm:ss',
      icons: {
        time: "far fa-clock",
        date: "far fa-calendar-alt",
        up: "fa fa-arrow-up",
        down: "fa fa-arrow-down",
        previous: "fas fa-caret-left",
        next: "fas fa-caret-right",
        today: "fas fa-crosshairs"
      }
    });
    
    $("#id_category").change(function() {
        // Set all temp fields to hidden when choosing a new category
        hideElements()

        // Grab the index of the dropdown item
        var index = $(this).find(':selected')[0].index

        // Save the object id. We'll use this to find the temp fields
        if (index === 0) return;
        var choice_id = $(this).find(':selected').val()

        // Grab the sanitized data passed from the view
        // TODO: Remove dependency on 'category_data'
        var value = JSON.parse(document.getElementById('category_data').textContent);

        // Django includes a blank dropdown item. We must subtract 1 from our index
        var columns = value[index-1]['columns'].split(',')
        columns.forEach(function(val) {
          $(document.getElementById('id_column_'+ choice_id + '_' + val.trim()).parentNode.removeAttribute('style'))
        })
    });
    // Build our JSON data and overwrite 'id_data' contents before submitting
    $("#id_form").submit(function( event ) {
      var columnJSON = {};
      $('*[id*=id_column_]:visible').each(function() {
        columnJSON[$('label[for="' + this.id + '"').text()] = this.value;
      });
      document.getElementById("id_data").value = JSON.stringify(columnJSON, null, 4);
    });
}).call(this);
