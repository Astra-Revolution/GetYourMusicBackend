from social_media.models import Genre, Instrument


def create_data(apps, schema_editor):
    genres = ['Latino', 'Classic', 'Pop', 'Rock', 'Alternative']
    for genre in genres:
        Genre(name=genre).save()
    instruments = ['Guitar', 'Piano', 'Violin', 'Bass', 'Drums', 'Voice']
    for instrument in instruments:
        Instrument(name=instrument).save()