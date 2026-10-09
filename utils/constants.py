from pages.function1_page import function1_page
from pages.function2_page import function2_page
from pages.function3_page import function3_page
from pages.function4_page import function4_page

sidebar_dictionary = {
    "category1": ["Function1", "Function2"],
    "category2": ["Function3", "Function4"],
}

function_dictionary = {
    "Function1" : function1_page,
    "Function2" : function2_page,
    "Function3": function3_page,
    "Function4" : function4_page,
}

doc_file_dictionary = {
    "Function1" : "function1.md",
    "Function2" : "function2.md",
    "Function3": "function3.md",
    "Function4" : "function4.md",
}