from django.shortcuts import render
from pyspark.sql import SparkSession
from prettytable import PrettyTable

def index(request):
    input_string = request.GET.get('request')

    spark = SparkSession.builder.appName("wikipedia").getOrCreate()
    df = spark.read.parquet("wikiSearch/search/data/data.parquet")

    result_table = parse_and_call_function(input_string, df)

    spark.stop()

    context = {"table": result_table}
    return render(request, 'searchTemplate/index.html', context)

def parse_and_call_function(input_string, df):
    if not input_string:
        return PrettyTable(["Result", "Empty input string"])

    words = input_string.split()
    result_table = PrettyTable(["Result"])

    if len(words) > 0:
        if words[0].upper() == "TITLE" and len(words) > 1:
            print("TITLE")
            result = search_title(words[1], df)
            result_table.add_row(result)
        elif words[0].upper() == "CATEGORY" and len(words) > 1:
            print("CATEGORY")
            result = search_category(words[1], df)
            result_table.add_row(result)
        elif words[0].upper() == "CONTAINS" and len(words) > 1:
            print("CONTAINS")
            result = contains(words[1], df)
            result_table.add_row(result)
        else:
            result_table.add_row(["Invalid command"])
    else:
        result_table.add_row(["Empty input string"])

    return result_table

def search_title(title, df):
    return df.filter(df["title"].contains(title)).collect()

def search_category(category, df):
    return df.filter(df("revision.text._VALUE").contains("Categories: " + category)).count()

def contains(keyword, df):
    return df.filter(df("revision.text._VALUE").contains(keyword)).collect()
