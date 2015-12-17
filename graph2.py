from easygui import *
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


class Graph():

    def __init__(self, title, csv_file):
        self.title = title
        self.csv_file = csv_file

        #Acquire the data. This takes a minute to download.
        self.data_file = pd.read_csv(csv_file)
        self.set_the_columns()

    def set_the_columns(self):

    	# IMPORTANT - change the choices to match your csv file.
    	# I realize this should be an option, but I couldn't figure
    	# out how to implement it. Seriously, I built a factory, and
    	# it still wouldn't revert to the original set of choices.
        self.choices = ["manner_of_death", "race", "age", "gender", "county"]

        #choosing the first column for comparison.
        self.column_1_choice = buttonbox("What column would you like to explore? (Column 1)", title, self.choices)
        column_1_variable_choices = pd.unique(self.data_file[self.column_1_choice]).tolist()
        self.column_1_variable = choicebox("Pick a variable", title, column_1_variable_choices)
        if self.column_1_variable == None:
        	self.set_the_columns()
        else:
        	#remove the first column choice from available choices.
            self.choices.remove(self.column_1_choice)
            
            #OPTIONAL - Add additional choices for column 2
            self.choices.append("date_of_death_yyyy")

            #choose the second column for comparison.
            self.column_2 = buttonbox("What would you like to compare it to? (Column 2)", title, self.choices)

			#graph_title.
            self.graph_title = enterbox("What would you like to call your graph?", title)
            if self.graph_title == None:
                msgbox("Graph aborted. \nThank you for your interest.", title)

    def create_graph(self):

        #Finding the data from column 1
        column_1_data = self.data_file[self.column_1_choice] == self.column_1_variable

        #Aggregating the data
        total_column_1_data = self.data_file[column_1_data]

        #Comparing the number of hits from each variable in column 2 to column 1
        #and plotting them in a bar graph
        column_2_counts = total_column_1_data[self.column_2].value_counts().plot(kind="bar")

        #Tarting up the graph for legibility
        plt.gcf().subplots_adjust(bottom=0.6)
        plt.ylabel(self.column_1_choice + ': ' + self.column_1_variable)
        plt.xlabel(self.graph_title)


class PDF():

	def __init__(self, title, csv_file):
		self.title = title
		self.csv_file = csv_file
		self.pdf_title = enterbox("What would you like to name your pdf save file? \n (The file extension will be added for you.)",
	                        	  title)
		#trying to fail gracefully
		if self.pdf_title == None:
			msgbox("Thank you for your interest.", title)
	        
	    #still trying to fail gracefully
		elif self.pdf_title == "":
			pdf_title = enterbox("You must enter a file name. \nWhat would you like to name your pdf save file? \n(The file extension will be added for you.)",
	                             title)
			self.make_a_pdf(self.pdf_title)
	        
	    #let's run with this puppy!
		else:
			self.make_a_pdf(self.pdf_title)



	#how many graphs would you like to make?
	def repeat_making_a_graph(self, pdf_file, title, csv_file):
		make_another = ynbox()
		if make_another == True:

	        #Create and save another graph
			Graph(title, csv_file).create_graph()
			plt.savefig(pdf_file, format='pdf')
			return True
		else:
			#Save and close the PDF
			pdf_file.close()
			msgbox("Your PDF has been saved.", title)
			return False


	#Make the PDF.
	def make_a_pdf(self, pdf_title):

		#Create your PDF
		pp = PdfPages(pdf_title + '.pdf')

		Graph(title, csv_file).create_graph()

	    #Save that graph to the PDF
		plt.savefig(pp, format='pdf')

	    #Repeat ad nauseum
		while self.repeat_making_a_graph(pp, title, csv_file) != False:
			if self.repeat_making_a_graph(pp, title, csv_file) == False:
				break    


title = "California DoJ Death Data 1980 - 2014"
csv_file = "death.csv"

new_file = PDF(title, csv_file)
