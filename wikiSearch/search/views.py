from django.shortcuts import render
from prettytable import PrettyTable
from django.conf import settings
import time
import json
import os
import re

DEFAULT_DATASET = "x0.1r.parquet"
DATAFRAME = settings.SPARK.read.parquet(f"wikiSearch/search/data/{DEFAULT_DATASET}")
DATASETS = ["x0.01r", "x0.05r", "x0.1r", "x0.2r", "x0.3r"]
def index(request):
    global DEFAULT_DATASET
    print(DEFAULT_DATASET)
    input_string = request.GET.get('request')
    result_table = PrettyTable(["Result"])

    start_time = time.time()
    if input_string:
        parse_and_execute_commands(input_string, settings.SPARK, result_table)

    if input_string:
        if 'COUNT' in input_string:
            result_table.add_row([f"Number of rows: {DATAFRAME.count()}"])
        elif 'SENTIMENT' in input_string:
            rows = DATAFRAME.collect()
            for row in rows:
                result_table.add_row([f"Title: {row['title']} Sentiment: {sentiment_analysis(row)}"])
        elif 'DATASET' in input_string and not ('TITLE' in input_string or 'CONTAINS' in input_string or 'CATEGORY' in input_string):
            pass
        else:
            DATAFRAME.collect()
            save_result_to_file(result)


    context = {"table": result_table}

    end_time = time.time()

    time_difference = end_time - start_time
    data = {"time": time_difference, "query": input_string}

    if os.path.exists('result.json'):
        with open('result.json', 'r') as f:
            existing_data = json.load(f)
            existing_data.append(data)
        with open('result.json', 'w') as f:
            json.dump(existing_data, f)
    else:   
        with open('result.json', 'w') as f:
            json.dump([data], f)

    print(f"Time taken: {time_difference} seconds")

    return render(request, 'searchTemplate/index.html', context)

def parse_and_execute_commands(input_string, spark, result_table):
    global DATAFRAME
    DATAFRAME = spark.read.parquet(f"wikiSearch/search/data/{DEFAULT_DATASET}")
    reset_dataframe = True 
    words = re.findall(r'(?:\w+|"[^"]*")', input_string)
    print(words)
    if len(words) > 0:
        i = 0
        while i < len(words):
            command = words[i].upper()
            print(command)
            if command == "SET":
                result = set_dataset(words[i + 2])
                if len(words) > i + 3 and words[i + 3].upper() in ["TITLE", "CATEGORY", "CONTAINS"]:
                    i += 3
                    continue
                elif len(words) == i + 3:
                    i += 2
                    result_table.add_row(result)
            elif command == "TITLE" and i + 1 < len(words):
                print("TITLE")
                if words[i + 1].startswith('"') and words[i + 1].endswith('"'):
                    phrase = words[i + 1][1:-1]
                    execute_search_command(search_title, phrase, spark, reset_dataframe)
                    reset_dataframe = False
                else:
                    result_table.add_row(["Invalid TITLE command: Phrase should be enclosed in double quotes"])
            elif command == "CATEGORY" and i + 1 < len(words):
                print("CATEGORY")
                if words[i + 1].startswith('"') and words[i + 1].endswith('"'):
                    category = words[i + 1][1:-1]
                    execute_search_command(search_category, category, spark, reset_dataframe)
                    reset_dataframe = False
                else:
                    result_table.add_row(["Invalid CATEGORY command: Phrase should be enclosed in double quotes"])
            elif command == "CONTAINS" and i + 1 < len(words):
                print("CONTAINS")
                if words[i + 1].startswith('"') and words[i + 1].endswith('"'):
                    phrase = words[i + 1][1:-1]
                    execute_search_command(contains, phrase, spark, reset_dataframe)
                    reset_dataframe = False
                else:
                    result_table.add_row(["Invalid CONTAINS command: Phrase should be enclosed in double quotes"])
            elif command == "COUNT" or command == "DATASET" or command in DATASETS or command == "AND":
                pass
            else:
                result_table.add_row(["Invalid command"])
            i += 1
    return spark.read.parquet(f"wikiSearch/search/data/{DEFAULT_DATASET}")

def extract_quoted_phrase(input_string):
    match = re.search(r'"([^"]*)"', input_string)
    return match.group(1) if match else ""

def set_dataset(dataset_name):
    print(dataset_name)
    parquet_file = f"{dataset_name}.parquet"
    global DEFAULT_DATASET
    print('default dataset' + DEFAULT_DATASET)
    DEFAULT_DATASET = parquet_file
    print('default dataset' + DEFAULT_DATASET)
    return [f"Changed dataset to {DEFAULT_DATASET}"]

def execute_search_command(search_function, argument, spark, reset_dataframe):
    if reset_dataframe:
        global DATAFRAME
        DATAFRAME = spark.read.parquet(f"wikiSearch/search/data/{DEFAULT_DATASET}")
    search_function(argument)

def search_title(title):
    global DATAFRAME
    DATAFRAME = DATAFRAME.filter(DATAFRAME["title"].contains(title))

def search_category(category):
    global DATAFRAME
    DATAFRAME = DATAFRAME.filter(DATAFRAME["revision"]["text"]["_VALUE"].contains("[[Categories: " + category + "]]"))

def contains(keyword):
    global DATAFRAME
    DATAFRAME = DATAFRAME.filter(DATAFRAME["revision"]["text"]["_VALUE"].contains(keyword))

def sentiment_analysis(data):
    text = data["revision"]["text"]["_VALUE"][:511]
    return settings.SENTIMENT_PIPELINE(text)

def save_result_to_file(result):
    with open('output_result.txt', 'w') as f:
        for row in result:
            f.write(str(row) + '\n')