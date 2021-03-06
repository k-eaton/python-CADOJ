from easygui import *
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class Graph():

    def __init__(self, column_1, column_1_variable, column_2, graph_title):
        self.column_1 = column_1
        self.column_1_variable = column_1_variable
        self.column_2 = column_2
        self.graph_title = graph_title

    def create_graph(self):

        #Acquire the data. This takes a minute to download.
        death_data = pd.read_csv("death.csv")

        #Finding the data from column 1
        column_1_deaths = death_data[self.column_1] == self.column_1_variable

        #Aggregating the data
        total_column_1_deaths = death_data[column_1_deaths]

        #Comparing the number of hits from each variable in column 2 to column 1
        #and plotting them in a bar graph
        column_2_counts = total_column_1_deaths[self.column_2].value_counts().plot(kind="bar")

        #Tarting up the graph for legibility
        plt.gcf().subplots_adjust(bottom=0.6)
        plt.ylabel(self.column_1 + ': ' + self.column_1_variable)
        plt.xlabel(self.graph_title)

title = "California DoJ Death Data 1980 - 2014"

#make a graph
def graph_variables():

    #Acquire the data. This takes a minute to download.
    death_data = pd.read_csv("death.csv")

    #choosing the first column for comparison.
    column_1_choices = ["manner_of_death", "race", "age", "gender", "county", "cancel"]
    column_1_choice = buttonbox("What column would you like to explore? (Column 1)", title, column_1_choices)
    if column_1_choice == "cancel":
        msgbox("Graph aborted. \nThank you for your interest.", title)
    else:

        #choosing the variable out of the first column to look at.
        column_1_variable_choices = pd.unique(death_data[column_1_choice]).tolist()
        column_1_variable = choicebox("Pick a variable", title, column_1_variable_choices)
        if column_1_variable == None:
            msgbox("Graph aborted. \nThank you for your interest.", title)
            #graph_variables()
        else:

            #choose the second column for comparison.
            column_1_choices.remove(column_1_choice)
            column_1_choices.remove("cancel")

            column_1_choices.append("date_of_death_yyyy")
            column_1_choices.append("cancel")

            column_2 = buttonbox("What would you like to compare it to? (Column 2)", title, column_1_choices)
            if column_2 == "cancel":
                msgbox("Graph aborted. \nThank you for your interest.", title)
                #graph_variables()
            else:

                #graph_title.
                graph_title = enterbox("What would you like to call your graph?", title)
                if graph_title == None:
                    msgbox("Graph aborted. \nThank you for your interest.", title)
                else:

                    #graph.
                    graph = Graph(column_1_choice,
                                  column_1_variable,
                                  column_2,
                                  graph_title)
                    return graph

#how many graphs would you like to make?
def repeat_making_a_graph(pdf_file):
    make_another = ynbox()
    if make_another == True:

        #Create and save another graph
        graph_variables().create_graph()
        plt.savefig(pdf_file, format='pdf')
        return True
    else:
        #Save and close the PDF
        pdf_file.close()
        msgbox("Your PDF has been saved.", title)
        return False


#Make the PDF.
def make_a_pdf(pdf_title):

    #Create your PDF
    pp = PdfPages(pdf_title + '.pdf')
    
    #Make a graph
    graph_variables().create_graph()
    
    #Save that graph to the PDF
    plt.savefig(pp, format='pdf')

    #Repeat ad nauseum
    while repeat_making_a_graph(pp) != False:
        if repeat_making_a_graph(pp) == False:
            break    

def start_the_process():

    #name your PDF
    pdf_title = enterbox("What would you like to name your pdf save file? \n (The file extension will be added for you.)",
                         title)
    
    #trying to fail gracefully
    if pdf_title == None:
        msgbox("Thank you for your interest.", title)
        
    #still trying to fail gracefully
    elif pdf_title == "":
        pdf_title = enterbox("You must enter a file name. \nWhat would you like to name your pdf save file? \n(The file extension will be added for you.)",
                             title)
        make_a_pdf(pdf_title)
        
    #let's run with this puppy!
    else:
        make_a_pdf(pdf_title)

start_the_process()
