from django.shortcuts import render
from pyspark.sql import SparkSession
from prettytable import PrettyTable

# Default dataset filename
DEFAULT_DATASET = "data.parquet"

def index(request):
    input_string = request.GET.get('request')

    spark = SparkSession.builder.appName("wikipedia").getOrCreate()

    # Parse and execute the command
    result_table = parse_and_call_function(input_string, spark)

    # Stop the Spark session
    spark.stop()

    context = {"table": result_table}
    return render(request, 'searchTemplate/index.html', context)

def parse_and_call_function(input_string, spark):
    if not input_string:
        return PrettyTable(["Result", "Empty input string"])

    words = input_string.split()
    result_table = PrettyTable(["Result"])

    if len(words) > 0:
        if words[0].upper() == "SET":
            result = set_dataset(words[2], spark)
            result_table.add_row(result)
            if len(words) > 3:
                # If additional commands are present after SET DATASET, parse and execute them
                additional_result = parse_and_execute_additional_commands(words[3:], spark)
                result_table.add_row(additional_result)
        elif words[0].upper() == "COUNT" and len(words) == 1:
            print("COUNT")
            result = count_rows(spark)
            result_table.add_row(result)
        elif words[0].upper() == "TITLE" and len(words) > 1:
            print("TITLE")
            result = execute_search_command(search_title, words[1], spark, is_count_command(words))
            result_table.add_row(result)
        elif words[0].upper() == "CATEGORY" and len(words) > 1:
            print("CATEGORY")
            result = execute_search_command(search_category, words[1], spark, is_count_command(words))
            result_table.add_row(result)
        elif words[0].upper() == "CONTAINS" and len(words) > 1:
            print("CONTAINS")
            result = execute_search_command(contains, words[1], spark, is_count_command(words))
            result_table.add_row(result)
        else:
            result_table.add_row(["Invalid command"])
    else:
        result_table.add_row(["Empty input string"])

    return result_table

def is_count_command(words):
    return len(words) > 1 and words[-1].upper() == "COUNT"

def set_dataset(dataset_name, spark):
    # Change the Parquet file used based on the dataset_name
    parquet_file = f"{dataset_name}.parquet"
    try:
        global DEFAULT_DATASET
        DEFAULT_DATASET = parquet_file
        df = spark.read.parquet(f"wikiSearch/search/data/{DEFAULT_DATASET}")
        return [f"Changed dataset to {DEFAULT_DATASET}", f"Number of rows: {df.count()}"]
    except Exception as e:
        return [f"Error changing dataset to {DEFAULT_DATASET}", str(e)]

def parse_and_execute_additional_commands(commands, spark):
    result = PrettyTable(["Result"])
    
    for i in range(0, len(commands), 2):
        # Execute commands in pairs (e.g., "TITLE <word>")
        command = commands[i].upper()
        if command == "TITLE" and i + 1 < len(commands):
            print("TITLE")
            sub_result = execute_search_command(search_title, commands[i + 1], spark, is_count_command(commands[i + 1:]))
            result.add_row(sub_result)
        elif command == "CATEGORY" and i + 1 < len(commands):
            print("CATEGORY")
            sub_result = execute_search_command(search_category, commands[i + 1], spark, is_count_command(commands[i + 1:]))
            result.add_row(sub_result)
        elif command == "CONTAINS" and i + 1 < len(commands):
            print("CONTAINS")
            sub_result = execute_search_command(contains, commands[i + 1], spark, is_count_command(commands[i + 1:]))
            result.add_row(sub_result)
        else:
            result.add_row(["Invalid command"])
    
    return result

def execute_search_command(search_function, argument, spark, count_command=False):
    df = spark.read.parquet(f"wikiSearch/search/data/{DEFAULT_DATASET}")
    
    if count_command:
        count_result = search_function(df, argument, count_command=True)
        return [f"Number of rows: {count_result}"]
    else:
        return search_function(df, argument).collect()

def count_rows(spark):
    df = spark.read.parquet(f"wikiSearch/search/data/{DEFAULT_DATASET}")
    count_result = df.count()
    return [f"Number of rows: {count_result}"]

def search_title(df, title, count_command=False):
    result = df.filter(df["title"].contains(title))
    return result.count() if count_command else result

def search_category(df, category, count_command=False):
    result = df.filter(df["revision"]["text"]["_VALUE"].contains("[[Categories: " + category + "]]")).count()
    return result.count() if count_command else result

def contains(df, keyword, count_command=False):
    result = df.filter(df["revision"]["text"]["_VALUE"].contains(keyword))
    return result.count() if count_command else result
