def model_to_html(instance, max_length=50):
    """
    a function for converting a django Model to HTML tags.
    """

    elements = []
    
    # open container tags
    elements.append(f"""
        <center>
            <div class="light-border">
    """)
    
    for field in instance.__class__._meta.get_fields():
        name = str(field.name)
        type = str(field.__class__.__name__)

        # if it's not a ManyToManyField, it can be directly convert to str
        if type not in ['ManyToManyField']:
            value = str(getattr(instance, name))
            value = f'{value[:max_length]}...' if len(value)>max_length else value

            elements.append(f"""
                {name}:
                <p>{value}</p>
                <br>
            """)
        else: # 'ManyToManyField'
            # open ManyToManyField p tag
            elements.append(f"""
                {name}:
                <p style="border: 1px solid gray; border-radius: 5px;">
            """)
            # loop the ManyToManyField's objects
            for inner in getattr(instance, name).all():
                value = str(inner)
                value = f'{value[:max_length]}...' if len(value)>max_length else value
                elements.append(f"""
                    <p>{value}</p>
                """)
            # close ManyToManyField p tag
            elements.append(f"""
                </p>
                <br>
            """)
    
    # close container tags
    elements.append(f"""
            </div>
        </center>
    """)

    return ''.join(elements)
