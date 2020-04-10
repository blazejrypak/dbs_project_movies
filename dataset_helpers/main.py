import csv
import json
import ast
from datetime import datetime


# class DatasetParser:
#     def __init__(self):
#         self.location = '/home/bubo/Desktop/DBMS_PROJECT/the-movies-dataset/'
#         self.movies_keywords = []
#         self.keywords = []
#
#     def parse(self, relative_path):
#         csv_file = self.location+relative_path
#         with open(csv_file, newline='') as file:
#             reader = csv.DictReader(file)
#             count = 0
#             for elem in reader:
#                 self.keywords.extend(ast.literal_eval(elem['keywords']))
#                 for e in ast.literal_eval(elem['keywords']):
#                     self.movies_keywords.append({'movie_id': elem['id'], 'keyword_id': e['id']})
#                 # count += 1
#                 # if count == 5:
#                 #     break
#         print(len(self.keywords))
#         print(len(self.movies_keywords))
#
#     def save(self):
#         with open(self.location+'movie_keywords.csv', 'w') as file:
#             writer = csv.writer(file)
#             writer.writerow(['movie_id', 'keyword_id'])
#             for item in self.movies_keywords:
#                 writer.writerow([item['movie_id'], item['keyword_id']])
#         with open(self.location+'keywords_parsed.csv', 'w') as file:
#             writer = csv.writer(file)
#             writer.writerow(['id', 'name'])
#             for item in self.keywords:
#                 writer.writerow([item['id'], item['name']])
        # print(self.keywords)


# datasetParser = DatasetParser()
# datasetParser.parse('keywords.csv')
# datasetParser.save()


def general_parser(relative_file_path, output_file_name, column_to_parse, *args):
    """ :arg relative_file_path - absolute path to file to be parsed
        :arg output_file_name   - output file name
        :arg column_to_parse    - name of column to be parsed
        :arg *args              - others column to add to output file
    """
    with open(output_file_name, 'w') as write_file:
        writer = csv.writer(write_file)

        columns2parse = [column_to_parse]
        for arg in args:
            columns2parse.append(arg)

        output_columns = []
        got_header = False
        dict_keys = []
        with open(relative_file_path, newline='') as read_file:
            reader = csv.DictReader(read_file)
            try:
                for row in reader:
                    for name in columns2parse:
                        try:
                            cell_obj = ast.literal_eval(row[name])
                        except Exception:
                            continue
                        if isinstance(cell_obj, list) or isinstance(cell_obj, dict):
                            if got_header:
                                if isinstance(cell_obj, list):
                                    for elem in cell_obj:
                                        row_values = []
                                        for key in dict_keys:
                                            row_values.append(elem[key])
                                        for arg in args:
                                            row_values.append(row[arg])
                                        writer.writerow(row_values)
                                elif isinstance(cell_obj, dict):
                                    row_values = []
                                    for key in dict_keys:
                                        row_values.append(cell_obj[key])
                                    for arg in args:
                                        row_values.append(row[arg])
                                    writer.writerow(row_values)
                            else:
                                if isinstance(cell_obj, list) and len(cell_obj) > 0 and not got_header:
                                    dict_keys = cell_obj[0].keys()
                                elif isinstance(cell_obj, dict) and not got_header:
                                    dict_keys = cell_obj.keys()
                                if not got_header:
                                    for k in dict_keys:
                                        output_columns.append(str(column_to_parse+'_'+k))
                                    output_columns.extend(columns2parse[1:])
                                    writer.writerow(output_columns)
                                    got_header = True
            except Exception:
                pass



timestampStr = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")

# general_parser('/home/bubo/Desktop/DBMS_PROJECT/the-movies-dataset/movies_metadata.csv', f'parse_{timestampStr}',
#                'genres')
# general_parser('/home/bubo/Desktop/DBMS_PROJECT/the-movies-dataset/movies_metadata.csv', f'parse_{timestampStr}',
#                'belongs_to_collection', 'movieid')



# /////////////////////////////////////////////////////////////////////////////////////////

# Always add created_at, update_at as now()


# 1. fill moviesTB, movies_metadata.csv

# general_parser('/home/bubo/Desktop/DBMS_PROJECT/the-movies-dataset/movies_metadata.csv', 'genres',
#                'genres', 'movieid')

# general_parser('/home/bubo/Desktop/DBMS_PROJECT/the-movies-dataset/movies_metadata.csv', 'Languages',
#                'spoken_languages', 'movieid')

# general_parser('/home/bubo/Desktop/DBMS_PROJECT/the-movies-dataset/movies_metadata.csv', 'ProductionCompanies',
#                'production_companies', 'movieid')

# general_parser('/home/bubo/Desktop/DBMS_PROJECT/the-movies-dataset/movies_metadata.csv', 'ProductionCountries',
#                'production_countries', 'movieid')

# general_parser('/home/bubo/Desktop/DBMS_PROJECT/the-movies-dataset/credits.csv', 'Casts',
#                'cast', 'id')

