(function() {
    $("#id_category").change(function() {
        var index = $(this).find(':selected')[0].index
        var value = JSON.parse(document.getElementById('category_data').textContent);
        var columnJSON = {};
        var columns = value[index-1]['columns'].split(',')
        columns.forEach(function(val) {
          columnJSON[val.trim()] = 'null'
        })
        document.getElementById("id_data").value = JSON.stringify(columnJSON, null, 4);
    });
}).call(this);
