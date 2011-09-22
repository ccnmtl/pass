from django.core.management.base import BaseCommand, CommandError
#from data.models import Site,Location,Series,Row
from careermapblock.models import *
import csv, pdb
class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        path_to_files = 'county_stats'
        county_stat_columns =  os.listdir (path_to_files)
        (location,created) = Location.objects.get_or_create(name='H1',site=site)
        for column in columns:
            #open the file
            
            #read in the whole file into a 2D array.
            
            #make a list of counties
            
            #assert the counties exist in the DB
            
            #assert the stats exist in the DB
            
            #prompt the user if they want to replace the values in the DB with the ones in the file
            
            exit
        
            (series,created) = Series.objects.get_or_create(name=column,location=location)
            reader = csv.reader(open("columns/%s.csv" % column))
            for row in reader:
                datetime = row[0]
                datum = row[1]
                r = Row.objects.create(series=series,
                                       timestamp=datetime,
                                       value=datum)

