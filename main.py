import tkinter as tk
from tkinter import messagebox, IntVar

reference_text = "The quick brown fox jumps over the lazy dog This sentence contains every letter of the alphabet. " \
                 "Now is the time for all good men to come to the aid of their party. The sky is blue, and the sun is " \
                 "shining brightly. Life is like a bicycle, to keep your balance, you must keep moving. In three words," \
                 " I can sum up everything I've learned about life: it goes on. Success is not final, failure is not " \
                 "fatal: It is the courage to continue that counts"
reference_words = reference_text.split()
reference_lines = reference_text.split('\n')


def timer():
    current_second = int(second.get())
    time_widget.config(text = f'Time: {current_second}s')
    correct_words = count_words()
    wpm = calculate_wpm(len(correct_words))
    wpm_widget.config(text = f"WPM: {wpm}")

    if current_second > 0:
        current_second -= 1
        second.set(current_second)
        highlight_text(count_words())
        root.after(1000, timer)
    elif current_second == 0:
        check_spelling()


def count_words():
    text_context = text_widget.get("1.0", "end-1c")
    words = text_context.split()
    correct_words = []
    for word in words:
        if word.lower() in [w.lower() for w in reference_words]:
            correct_words.append(word)
    return correct_words


def start_timer(event):
    text_widget.unbind("<KeyPress>")
    timer()


def check_spelling():
    text_widget.tag_remove("correct", "1.0", tk.END)
    text_widget.tag_remove("incorrect", "1.0", tk.END)
    correct_words = count_words()
    highlight_text(correct_words)
    second.set(0)
    messagebox.showinfo("Word count:", f"Your WPM (Words Per Minute) result is: \n{calculate_wpm(len(correct_words))}")
    text_widget.config(state = tk.DISABLED)


def calculate_wpm(correct_word_count):
    total_time = 61 - int(second.get())
    wpm = (correct_word_count / total_time) * 60
    return round(wpm, 2)


def highlight_text(correct_words):
    text_widget.tag_config("correct", foreground="green")
    text_widget.tag_config("incorrect", foreground="red")
    text_context = text_widget.get("1.0", "end-1c")
    words = text_context.split()
    start_index = "1.0"

    for word in words:
        start_index = text_widget.search(word, start_index, stopindex = tk.END, nocase = True, regexp = True)
        end_index = f"{start_index}+{len(word)}c"
        if word in correct_words:
            text_widget.tag_add("correct", start_index, end_index)
        else:
            text_widget.tag_add("incorrect", start_index, end_index)
        start_index = end_index


def update_highlighting(event):
    reference_text_widget.tag_config("current", background = "#58F5DF")
    text_context = text_widget.get("1.0", "end-1c")
    words = text_context.split()
    start_index = "1.0"
    for word in words:
        start_index = text_widget.search(word, start_index, stopindex = tk.END, nocase = True, regexp = True)
        end_index = f"{start_index}+{len(word)}c"
        if word:
            reference_text_widget.tag_add("current", start_index, end_index)
        start_index = end_index

# def update_highlighting(event):
#     reference_text_widget.tag_remove("highlight", "1.0", tk.END)
#     text_content = text_widget.get("1.0", tk.END).lower()
#     reference_words = reference_text_widget.get("1.0", tk.END).split()
#     for word in reference_words:
#         start = 0
#         while True:
#             start_index = text_content.find(word, int(start))
#             if start_index == -1:
#                 break
#             end = f"{start_index}+{len(word)}c"
#             reference_text_widget.tag_add("highlight", f"1.{start_index}", f"1.{start_index + len(word)}")
#             start = start_index + len(word) + 1
#     reference_text_widget.tag_config("highlight", background = "beige")


root = tk.Tk()
root.title("Typing Speed Test")
root.config(bg = 'skyblue')
second = IntVar()
second.set(60)

top_frame = tk.Frame(root, bg = 'skyblue')
top_frame.grid(row = 0, column = 0)

tk.Label(top_frame,
         text = "How fast are your fingers? Do the one-minute typing test to find out!",
         foreground = 'black', bg = '#58F5DF', font = ('Helvetica', 20), padx = 20, pady = 20,
         justify = "center").grid(row = 0, column = 0, pady = 10, padx = 5)

middle_frame = tk.Frame(root, height = 400, bg = '#58F5DF', pady=10)
middle_frame.grid(row = 1, column = 0)

bottom_frame = tk.Frame(root, height = 100, width = 500, bg = 'sky blue')
bottom_frame.grid(row = 4, column = 0)

label = tk.Label(middle_frame, text = 'Write below:',
                 width = 25, height = 2, font = ('Helvetica', 20),
                 background = '#58F5DF', foreground = 'black')
label.grid(row = 2, column = 0)

text_widget = tk.Text(middle_frame, width = 45, height = 7,
                      padx = 50, pady = 20, font = ('Helvetica', 20), background = '#58D8F5',
                      foreground = 'black')
text_widget.grid(row = 3, column = 0)
text_widget.bind("<KeyPress>", start_timer)

reference_text_widget = tk.Text(middle_frame, wrap = "word", width = 50, height = 7,
                                foreground = "black", bg = "#58D8F5", font = ('Helvetica', 20),
                                padx = 15, pady = 15)
reference_text_widget.grid(row = 0, column = 0, pady = (20, 0), padx = 50)
reference_text_widget.insert(tk.END, reference_text)

text_widget.bind("<KeyRelease>", update_highlighting)

time_widget = tk.Label(bottom_frame, text = 'Time: 60s', padx = 65, bg = 'sky blue', foreground = 'black')
time_widget.grid(row = 0, column = 0, padx = 40)

wpm_widget = tk.Label(bottom_frame, text = 'WPM: 0', padx=65, foreground = 'black', bg='sky blue')
wpm_widget.grid(row = 0, column = 1, padx = 40)

root.mainloop()
