from django.shortcuts import render
from prettytable import PrettyTable
from django.conf import settings

# Default dataset filename
DEFAULT_DATASET = "x0.3r.parquet"

def index(request):
    input_string = request.GET.get('request')
    result_table = PrettyTable(["Result"])
    df = parse_and_call_function(input_string, settings.SPARK, result_table)

    if input_string:
        if 'COUNT' in input_string:
            result_table.add_row([f"Number of rows: {df.count()}"])
        elif 'TITLE' not in input_string or 'SET' not in input_string or 'CATEGORY' not in input_string:
            pass
        else:
            result_table.add_row(df.collect())
        
    context = {"table": result_table}
    return render(request, 'searchTemplate/index.html', context)

def parse_and_call_function(input_string, spark, result_table):
    if not input_string:
        return spark.read.parquet(f"wikiSearch/search/data/{DEFAULT_DATASET}")

    words = input_string.split()

    if len(words) > 0:
        if words[0].upper() == "SET":
            result = set_dataset(words[2])
            if len(words) == 3:
                result_table.add_row(result)
            if len(words) > 3:
                return parse_and_execute_additional_commands(words[3:], spark)
        elif words[0].upper() == "TITLE" and len(words) > 1:
            print("TITLE")
            return execute_search_command(search_title, words[1], spark)
        elif words[0].upper() == "CATEGORY" and len(words) > 1:
            print("CATEGORY")
            return execute_search_command(search_category, words[1], spark)
        elif words[0].upper() == "CONTAINS" and len(words) > 1:
            print("CONTAINS")
            return execute_search_command(contains, words[1], spark)
        else:
            result_table.add_row(["Invalid command"])
    else:
        result_table.add_row(["Empty input string"])

    return spark.read.parquet(f"wikiSearch/search/data/{DEFAULT_DATASET}")

def set_dataset(dataset_name):
    parquet_file = f"{dataset_name}.parquet"
    try:
        global DEFAULT_DATASET
        DEFAULT_DATASET = parquet_file
        return [f"Changed dataset to {DEFAULT_DATASET}"]
    except Exception as e:
        return [f"Error changing dataset to {DEFAULT_DATASET}", str(e)]

def parse_and_execute_additional_commands(commands, spark):
    for i in range(0, len(commands), 2):
        command = commands[i].upper()
        if command == "TITLE" and i + 1 < len(commands):
            print("TITLE")
            return execute_search_command(search_title, commands[i + 1], spark)
        elif command == "CATEGORY" and i + 1 < len(commands):
            print("CATEGORY")
            return execute_search_command(search_category, commands[i + 1], spark)
        elif command == "CONTAINS" and i + 1 < len(commands):
            print("CONTAINS")
            return execute_search_command(contains, commands[i + 1], spark)
    return spark

def execute_search_command(search_function, argument, spark):
    df = spark.read.parquet(f"wikiSearch/search/data/{DEFAULT_DATASET}")
    return search_function(df, argument)

def search_title(df, title):
    return df.filter(df["title"].contains(title))

def search_category(df, category):
    return df.filter(df["revision"]["text"]["_VALUE"].contains("[[Categories: " + category + "]]"))

def contains(df, keyword):
    return df.filter(df["revision"]["text"]["_VALUE"].contains(keyword))
    