# Record Keeper

If you would like to try out a live demo (feel free to create an account) you can log in with an account that has dummy data populated:

<http://record-keeper-webapp.herokuapp.com>  
username=test_user  
password=8charpas

I'm Kent Jones and I started writing this web application in my free time as a demonstration. In addition I wanted to try something I've not done before. That ended up being **dynamic** tables / forms.

Normally you would query data and present it to the user in a predefined manner.

Example:  
A book / movie site may allow the user to track which books he/she might have read. In addition the user could add a rating for the book along with a brief description.

This is all predefined on the backend. There are book fields within the object that are queried and displayed to the user.

Name | Author | Rating | Thoughts
---------|----------|---------|---------
 Harry Potter - The Philosopher's Stone | J. K. Rowling | 5 | Such a great book!
 The Name of the Wind | Patrick Rothfuss | 5 | Such a fantastic story!
 The Doors of Stone | Patrick Rothfuss | ? | When will it be done!?

Name, Author, Rating, and Thoughts will never change. They are "**static**".

This application has "**dynamic**" headers / columns. The user is able to define the type of data to be tracked. This is done by the user entering a comma separated list of columns. The data for the columns is stored in JSON on the backend. The user doesn't need to know JSON. They simply enter their information on a dynamic form that builds JSON in javascript.

Example:  
The user creates a category and names it Restaurants. For each record they want to record:

* Name
* Cost
* Date
* Enjoyment

The data for this would be stored in the database as JSON:

```json
{
    "Name": "Whataburger",
    "Cost": "9.50",
    "Date": "2019/04/24",
    "Enjoyment": "It was a lifeless meat patty with no taste"
}
```

This allows the user to define their own tables and columns giving them the choice to determine the type of data to be stored.

## Problems faced during development

Some of the issues I encountered:

* JSON stored in different databases
  * Locally I use sqlite3 while heroku uses Postgres
* Rendering temporary dynamic fields within a form
  * These fields are what is used to generate the JSON data
* Integrating S3 with Heroku
  * This was, by far, the largest issue I had faced.
  * S3 was lacking up-to-date documentation with django-storages

### JSON stored in different databases

As I didn't want to install Postgres on my development machine I needed the json field to behave the same. I solved this by using the **jsonfield**  package which basically converts a TextField into a JSONField albeit with some limitations.

### Rendering temporary dynamic fields within a form

Dynamic forms was a bit of a pain at first. I had attempted a coupe different solutions that were overly complex. There had to be a less complex method. I needed to give the user a choice of which category to use and display a form field for each of the column names that were defined. I used the following to solve this issue:

```python
class RecordColumnForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super(RecordColumnForm, self).__init__(*args, **kwargs)
        names = Category.objects.filter(user=user)
        for name in names:
            columns = name.columns.split(',')
            for column in columns:
                self.fields['column_{}_{}'.format(name.id, column.strip())] = \
                    forms.CharField(label=column.strip(), required=False)
```

This creates a standard form (not a ModelForm) and doesn't actually save the resulting data. It creates a CharField for each column specified across all categories. If the user had 3 categories with each category having 4 columns this form would be rendered with 12 fields.

I then combined the RecordColumnForm with the AddRecordForm.

```python
class AddRecordForm(forms.ModelForm):
    file = forms.FileField(required=False)
    data = JSONField()

    class Meta:
        model = Record
        widgets = {'data': forms.HiddenInput()}
        fields = (
            'category',
            'data',
            'file'
        )

    # Only pull category objects that are created by the user
    # Default uses Category.objects.all()
    def __init__(self, user, *args, **kwargs):
        super(AddRecordForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)
```

When the form is rendered it will have:

1. category
2. data
3. file
4. n number of columns

Example:  
User creates two categories. One is **restaurants** and the other is **travel**. Restaurants has 3 columns (name, cost, date) while Travel has 4 columns (airline, cost, date, miles). Resulting in a form with 9 total fields (**data** is already hidden). Each of the dynamic fields has an id associating it with the correct category.

1. category
2. file
3. name (id_column_1_name)
4. cost (id_column_1_cost)
5. date (id_column_1_date)
6. airline (id_column_2_airline)
7. cost (id_column_2_cost)
8. date (id_column_2_date)
9. miles (id_column_2_miles)

We can now hide all the temporary fields on document load and remove the styling (display=none) for the fields we want to display.

```javascript
// Hide all fields
function hideElements() {
  $('*[id*=id_column_]').each(function() {
    id = this.id
    document.getElementById(id).parentNode.style.display = "none";
  });
}
```

```javascript
// Display the fields associated with the chosen category
var columns = value[index-1]['columns'].split(',')
columns.forEach(function(val) {
    $(document.getElementById('id_column_'+ choice_id + '_' + val.trim()).parentNode.removeAttribute('style'))
})
```

If the user chose the category **Travel** the fields presented would be:

1. category
2. file
3. airline
4. cost
5. date
6. miles

In order to build the JSON data we need to hook the submit event in order to fill the hidden **data** column before POST.

```javascript
// Build our JSON data and overwrite 'id_data' contents before submitting
$("#id_form").submit(function( event ) {
    var columnJSON = {};
    $('*[id*=id_column_]:visible').each(function() {
    columnJSON[$('label[for=' + this.id).text()] = this.value
    document.getElementById("id_data").value = JSON.stringify(columnJSON, null, 4);
    });
});
```

### Integrating S3 with Heroku

Integrating Heroku with Django is pretty seamless. However, Heroku uses an ephemeral file system. This, essentially, removes all files uploaded that aren't static resources. This is a severe limitation for a demonstration web application. Up until this point I've always deployed code within an EC2 instance. I wanted to keep costs down as much as possible. I ended up using **Heroku** for the platform and **S3** for the media.

There is plenty of documentation for integrating Heroku within Django. However, the documentation for integrating S3 was outdated.

What made this particularly troublesome is that each change had to be committed and pushed to Heroku. There is no way to make a change without committing first. So I ended up with a lot commits that consisted of a 1 line code change in a short period of time. In hindsight, I should have created an S3 git branch to perform my work and merge once it was done.