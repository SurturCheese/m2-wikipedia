from django.shortcuts import render
from prettytable import PrettyTable
from django.conf import settings
import time
import json
import os
import re

DEFAULT_DATASET = "x0.1r.parquet"

def index(request):
    input_string = request.GET.get('request')
    result_table = PrettyTable(["Result"])

    start_time = time.time()

    df = parse_and_execute_commands(input_string, settings.SPARK, result_table)

    if input_string:
        if 'COUNT' in input_string:
            result_table.add_row([f"Number of rows: {df.count()}"])
        elif 'DATASET' in input_string and not ('TITLE' in input_string or 'CONTAINS' in input_string or 'CATEGORY' in input_string):
            pass
        else:
            df.collect()

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
    if not input_string:
        return spark.read.parquet(f"wikiSearch/search/data/{DEFAULT_DATASET}")

    words = re.findall(r'(?:[^\s"]|"(?:\\.|[^"])*")+', input_string)

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
                    result_table.add_row(result)
            elif command == "TITLE" and i + 1 < len(words):
                print("TITLE")
                # Check if the phrase is enclosed in double quotes
                if words[i + 1].startswith('"') and words[i + 1].endswith('"'):
                    phrase = words[i + 1][1:-1]
                    return execute_search_command(search_title, phrase, spark)
                else:
                    result_table.add_row(["Invalid TITLE command: Phrase should be enclosed in double quotes"])
            elif command == "CATEGORY" and i + 1 < len(words):
                print("CATEGORY")
                # Check if the phrase is enclosed in double quotes
                if words[i + 1].startswith('"') and words[i + 1].endswith('"'):
                    category = words[i + 1][1:-1]
                    return execute_search_command(search_category, category, spark)
                else:
                    result_table.add_row(["Invalid CATEGORY command: Phrase should be enclosed in double quotes"])
            elif command == "CONTAINS" and i + 1 < len(words):
                print("CONTAINS")
                # Check if the phrase is enclosed in double quotes
                if words[i + 1].startswith('"') and words[i + 1].endswith('"'):
                    phrase = words[i + 1][1:-1]
                    return execute_search_command(contains, phrase, spark)
                else:
                    result_table.add_row(["Invalid CONTAINS command: Phrase should be enclosed in double quotes"])
            else:
                result_table.add_row(["Invalid command"])
            i += 1

    return spark.read.parquet(f"wikiSearch/search/data/{DEFAULT_DATASET}")


def extract_quoted_phrase(input_string):
    match = re.search(r'"([^"]*)"', input_string)
    return match.group(1) if match else ""

def set_dataset(dataset_name):
    parquet_file = f"{dataset_name}.parquet"
    try:
        global DEFAULT_DATASET
        DEFAULT_DATASET = parquet_file
        return [f"Changed dataset to {DEFAULT_DATASET}"]
    except Exception as e:
        return [f"Error changing dataset to {DEFAULT_DATASET}", str(e)]

def execute_search_command(search_function, argument, spark):
    df = spark.read.parquet(f"wikiSearch/search/data/{DEFAULT_DATASET}")
    return search_function(df, argument)

def search_title(df, title):
    print('title : ' + title)
    return df.filter(df["title"].contains(title))

def search_category(df, category):
    return df.filter(df["revision"]["text"]["_VALUE"].contains("[[Categories: " + category + "]]"))

def contains(df, keyword):
    return df.filter(df["revision"]["text"]["_VALUE"].contains(keyword))
