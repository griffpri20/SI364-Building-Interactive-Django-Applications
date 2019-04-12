import csv

# python3 manage.py shell < many/load.py

from unesco.models import site, category, iso, region, states

fhand = open('unesco/load.csv')
reader = csv.reader(fhand)

site.objects.all().delete()
category.objects.all().delete()
iso.objects.all().delete()
region.objects.all().delete()
states.objects.all().delete()

i = 0
for row in reader:
    if i > 0:
        try:
            name = site.objects.get(name=row[0])
        except:
            print("Inserting name",row[0])
            # name = site(name=row[0])
            # name.save()

        try:
            desc = site.objects.get(description=row[1])
        except:
            print("Inserting description",row[1])
            # desc = site(description=row[1])
            # desc.save()

        try:
            just = site.objects.get(justification=row[2])
        except:
            print("Inserting justification",row[2])
            # just = site(justification=row[2])
            # just.save()

        try:
            year = site.objects.get(year=row[3])
        except:
            print("Inserting year",row[3])
            # year = site(year=row[3])
            # year.save()

        try:
            long = site.objects.get(longitude=row[4])
        except:
            print("Inserting longitude",row[4])
            # long = site(longitude=row[4])
            # long.save()

        try:
            lat = site.objects.get(latitude=row[5])
        except:
            print("Inserting latitude",row[5])
            # lat = site(latitude=row[5])
            # lat.save()

        try:
            area = site.objects.get(area_hectares=row[6])
        except:
            print("Inserting area_hectares",row[6])
            # area = site(area_hectares=row[6])
            # area.save()

        try:
            y = int(row[3])
        except:
            y = None
        try:
            lo = float(row[4])
        except:
            lo = None
        try:
            lat = float(row[5])
        except:
            lat = None
        try:
            ah = float(row[6])
        except:
            ah = None

        # save1 = site(name=row[0], description=row[1], justification=row[2],
        #                     year=y, longitude=lo, latitude=lat, area_hectares=ah)
        # save1.save()

        try:
            cat = category.objects.get(name=row[7])
        except:
            #print("Inserting category",row[7])
            cat = category(name=row[7])
            cat.save()

        try:
            state = states.objects.get(name=row[8])
        except:
            #print("Inserting states",row[8])
            state = states(name=row[8])
            state.save()

        try:
            r = region.objects.get(name=row[9])
        except:
            #print("Inserting region",row[9])
            r = region(name=row[9])
            r.save()

        try:
            q = iso.objects.get(name=row[10])
        except:
            #print("Inserting iso",row[10])
            q = iso(name=row[10])
            q.save()

        s = site(name=row[0], description=row[1], justification=row[2],
                 year=y, longitude=lo, latitude=lat, area_hectares=ah,
                 category=cat, state=state, region=r, iso=q)
        s.save()
    i += 1
