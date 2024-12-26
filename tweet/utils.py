from .models import tweet
def clone_tweet_with_changes(tweet_obj, field_name, new_value):
    # Create a dictionary of all fields except the ID
    fields = {
        field.name: getattr(tweet_obj, field.name)
        for field in tweet_obj._meta.get_fields()
        if not field.auto_created and field.concrete and field.name != 'id'
    }
    
    # Modify the specific field you want to change
    fields[field_name] = new_value

    # Create a new instance with the modified fields
    cloned_tweet = tweet(**fields)
    
    # Save the new instance to the database
    cloned_tweet.save()
    
    return cloned_tweet
