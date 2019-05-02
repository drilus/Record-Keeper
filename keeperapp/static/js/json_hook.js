// We need to hook the event for choosing a category
(function() {
    $("#id_category").change(function() {
        // Grab the index of the dropdown item
        var index = $(this).find(':selected')[0].index
        // Grab the sanitized data passed from the view
        var value = JSON.parse(document.getElementById('category_data').textContent);
        var columnJSON = {};
        // Django includes a blank dropdown item. We must subtract 1 from our index
        var columns = value[index-1]['columns'].split(',')
        columns.forEach(function(val) {
          columnJSON[val.trim()] = 'null'
        })
        // Overwrite the contents of the 'data' JSONField with our newly generated JSON column names
        // TODO: This field should be hidden. Column names / data should be their own CharField's
        document.getElementById("id_data").value = JSON.stringify(columnJSON, null, 4);
    });
}).call(this);
