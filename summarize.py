import os
# Import the EvaDB package
import evadb
from groq import Groq
import warnings
warnings.filterwarnings("ignore")

# Connect to EvaDB and get a database cursor for running queries
cursor = evadb.connect().cursor()

cursor.query("DROP DATABASE IF EXISTS MLNotes;").df()

#creating SQLite database to hold contents of PDF
"""
# Create the SQLite database
cursor.query("""
#CREATE DATABASE MLNotes
#WITH ENGINE = 'sqlite',
#PARAMETERS = {
    #"database": "evadb_ml_notes.db"
#};
""").df()

#defining the AI function with EvaDB
cursor.query("""
    #CREATE FUNCTION IF NOT EXISTS TextSummarizer
    #TYPE HuggingFace
    #TASK 'summarization'
    #MODEL 'facebook/bart-large-cnn'
""").df()
"""

#summarizing a PDF
def summarize_pdf(pdf_path):
    cursor = evadb.connect().cursor()

    #drop table if it already exists
    cursor.query("DROP TABLE IF EXISTS MLNotes").df()

    #loading pdf into table
    cursor.query(f"""
    LOAD PDF '{pdf_path}' INTO MLNotes;
    """).df()

    #drop table
    cursor.query("DROP TABLE IF EXISTS CombinedMLText;").df()

    # Create the CombinedMLText table
    cursor.query("CREATE TABLE CombinedMLText (full_text TEXT);").df()

    #the AI text summarizer applies the function on rows of data
    #but when we first enter pdf into table there isnt enough data per row, so its problematic
    #i created a new temporary table that stores all of the content from the pdf in one row
    #we can now apply the summarizer on the whole pdf

    #getting all text rows corresponding to the specific PDF
    text_rows = cursor.query("""
        SELECT data
        FROM MLNotes
    """).df()

    #combing text into one string
    full_text = ' '.join(text_rows['data'].tolist())

    #inserting combined text into temporary table
    cursor.query(f"""
    INSERT INTO CombinedMLText (full_text) VALUES ('{full_text}');
    """).df()

    #applying function
    summary = cursor.query("""
    SELECT full_text, TextSummarizer(full_text)
    FROM CombinedMLText
""").df()

    return summary

#used Groq, had issue with OpenAI
def answer_question(question):
    client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        model="llama3-8b-8192",
    )

    answer_text = chat_completion.choices[0].message.content

    return answer_text

#main program
def main():
    print("============================================")
    print(" Hello 👋 Welcome to SummarAI!")
    print(" This app allows you to summarize notes 📝 and ask any questions 🙋‍♂️ you have!")
    print("============================================\n")

    pdf_path = input("\n Please enter the path to the PDF file that you would like to summarize: ")
    print(f" The path you entered is {pdf_path}")
    confirmation = input(" Is this the correct path? (type yes/no): ").strip().lower()

    if confirmation == "no":
        print("Ending the program. Please rerun the program and enter the correct path.")

    print(f"\nSummarAI is summarizing the PDF! This might take a second...⏳")
    summary_df = summarize_pdf(pdf_path)

    summary_text = summary_df['summary_text'].iloc[0]

    print(f"\nYour notes summarized: ")
    print(summary_text)

    save_summary = input("\nWould you like to save your summary to a file? (type yes/no): ")
    if save_summary == "yes":
        output_path = input("What is the path you would like to save your file to? (e.g. notes.txt)")
        with open(output_path, "w") as file:
            file.write(summary_text)
        print(f"Your summary has succesfully been saved to {output_path}! ✅")

    print("============================================")
    print("Now you have the opportunity to ask questions about the notes! Enter 'exit' to leave.")
    while True:
        question = input("\n Enter your question: ")
        if question.lower() == "exit":
            print("Thank you for using SummarAI! You are now exiting the program.")
            break
        answer = answer_question(question)
        print(f"Answer: {answer}")

if __name__ == "__main__":
    main()








