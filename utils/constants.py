from views.function1_page import function1_page
from views.function2_page import function2_page
from views.function3_page import function3_page
from views.function4_page import function4_page
from views.home_page import home_page

sidebar_dictionary = {
    "category1": ["Function1", "Function2"],
    "category2": ["Function3", "Function4"],
}

function_dictionary = {
    "Home": home_page,
    "Function1" : function1_page,
    "Function2" : function2_page,
    "Function3": function3_page,
    "Function4" : function4_page,
}

doc_file_dictionary = {
    "Home" : "home.md",
    "Function1" : "function1.md",
    "Function2" : "function2.md",
    "Function3": "function3.md",
    "Function4" : "function4.md",
}