from locations.models import Region, Province, District


def create_data(apps, schema_editor):
    regions = {'Lima': {'Lima': ['Lima', 'Jesus Maria', 'Pueblo Libre'],
                        'Barranca': ['Supe', 'Barranca']},
               'Arequipa': {'Arequipa': ['Yanahurara', 'Arequipa', 'Cayma'],
                            'Islay': ['Cocachacra', 'Punta de Bombon']},
               'Cuzco': {'Cuzco': ['Cuzco'],
                         'Espinar': ['Espinar']}}
    for r in regions:
        Region(name=r).save()
    db_regions = Region.objects.all()
    for db_region in db_regions:
        provinces = regions[db_region.name]
        for p in provinces:
            Province(name=p, region=db_region).save()
        db_provinces = Province.objects.filter(region_id=db_region.id)
        for db_province in db_provinces:
            print(db_province)
            districts = regions[db_region.name].get(db_province.name)
            for d in districts:
                District(name=d, province=db_province).save()
